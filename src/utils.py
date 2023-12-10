import os
from uuid import uuid4
from typing import Type

import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile
from sqlalchemy import func, select
from cloudinary import uploader

from src.administrations.utils import create_administrations
from src.auth.models import User
from src.auth.utils import create_user
from src.contacts.utils import create_contacts
from src.database.database import Base, get_async_session
from src.departments.utils import create_main_departments, create_sub_departments
from src.exceptions import INVALID_PHOTO, OVERSIZE_FILE
from src.slider_main.utils import create_slides
from src.config import PHOTO_FORMATS, settings, IS_PROD, MAX_FILE_SIZE
from src.database.fake_data import (
    CONTACTS,
    DEPARTMENTS,
    SUB_DEPARTMENTS,
    SLIDES,
    ADMINISTRATIONS,
)

if IS_PROD:
    from src.database.redis import init_redis, redis

    lock = redis.lock("my_lock")


async def lifespan(app: FastAPI):
    if IS_PROD:
        await init_redis()
        await lock.acquire(blocking=True)
    async for s in get_async_session():
        async with s.begin():
            user_count = await s.execute(select(func.count()).select_from(User))
            if user_count.scalar() == 0:
                await create_user(
                    email=settings.ADMIN_USERNAME, password=settings.ADMIN_PASSWORD
                )
                await create_main_departments(DEPARTMENTS)
                await create_sub_departments(SUB_DEPARTMENTS)
                await create_contacts(**CONTACTS)
                await create_slides(SLIDES)
                await create_administrations(ADMINISTRATIONS)
    if IS_PROD:
        await lock.release()
    yield


async def save_photo(file: UploadFile, model: Type[Base]) -> str:
    if not file.content_type in PHOTO_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_PHOTO % (file.content_type, PHOTO_FORMATS)
        )
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=OVERSIZE_FILE)

    folder_path = os.path.join("static", model.__name__)
    if IS_PROD:
        os.makedirs(folder_path, exist_ok=True)

        file_name = f'{uuid4().hex[:16]}.{file.filename.split(".")[-1]}'
        file_path = os.path.join(folder_path, file_name)
        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(await file.read())
        return file_path
    else:
        upload_result = uploader.upload(file.file, folder=folder_path)
        return upload_result["url"]
