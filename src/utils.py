from typing import Type

from fastapi import FastAPI, UploadFile
from sqlalchemy import func, select
from cloudinary import uploader

from src.administrations.utils import create_administrations
from src.auth.models import User
from src.auth.utils import create_user
from src.contacts.utils import create_contacts
from src.database.database import Base, get_async_session
from src.departments.utils import create_main_departments, create_sub_departments

from src.slider_main.utils import create_slides
from src.config import settings, IS_PROD
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
    folder_path = f"static/{model.__name__}"
    # os.makedirs(folder_path, exist_ok=True)
    # file_path = f"{folder_path}/{file.filename.replace(' ', '_')}"
    # async with aiofiles.open(file_path, "wb") as buffer:
    #     await buffer.write(await file.read())
    # return file_path
    upload_result = uploader.upload(file.file, folder=folder_path)
    return upload_result["url"]
