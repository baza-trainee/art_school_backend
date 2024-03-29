import os
import shutil
from uuid import uuid4
from typing import Type

import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile, BackgroundTasks
from sqlalchemy import func, select

from src.administrations.utils import create_administrations
from src.auth.models import User
from src.auth.utils import create_user
from src.contacts.utils import create_contacts
from src.documents.utils import create_docs
from src.database.database import Base, get_async_session
from src.departments.utils import create_main_departments, create_sub_departments
from src.exceptions import INVALID_FILE, INVALID_PHOTO, OVERSIZE_FILE
from src.slider_main.utils import create_slides
from src.config import FILE_FORMATS, PHOTO_FORMATS, settings, MAX_FILE_SIZE_MB
from src.database.fake_data import (
    CONTACTS,
    DEPARTMENTS,
    SUB_DEPARTMENTS,
    SLIDES,
    ADMINISTRATIONS,
    DOCUMENT,
)
from src.database.redis import init_redis, redis

lock = redis.lock("my_lock")


async def lifespan(app: FastAPI):
    await init_redis()
    await lock.acquire(blocking=True)
    async for s in get_async_session():
        async with s.begin():
            user_count = await s.execute(select(func.count()).select_from(User))
            if user_count.scalar() == 0:
                clear_media_path()
                await create_user(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
                await create_main_departments(DEPARTMENTS)
                await create_sub_departments(SUB_DEPARTMENTS)
                await create_contacts(CONTACTS, session=s)
                await create_docs(DOCUMENT, session=s)
                await create_slides(SLIDES, session=s)
                await create_administrations(ADMINISTRATIONS, session=s)
    await lock.release()
    yield


def clear_media_path():
    folder_path = os.path.join("static", "media")
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)


async def save_photo(
    file: UploadFile,
    model: Type[Base],
    background_tasks: BackgroundTasks,
    is_file=False,
) -> str:
    if not is_file and not file.content_type in PHOTO_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_PHOTO % (file.content_type, PHOTO_FORMATS)
        )
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=OVERSIZE_FILE)
    if is_file and not file.content_type in FILE_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_FILE % (file.content_type, FILE_FORMATS)
        )

    folder_path = os.path.join(
        "static", "media", model.__tablename__.lower().replace(" ", "_")
    )
    file_name = f'{uuid4().hex}.{file.filename.split(".")[-1]}'
    file_path = os.path.join(folder_path, file_name)

    async def _save_photo(file_path: str):
        os.makedirs(folder_path, exist_ok=True)
        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(await file.read())

    background_tasks.add_task(_save_photo, file_path)
    return file_path


async def delete_photo(path: str, background_tasks: BackgroundTasks) -> None:
    if "media" in path:
        path_exists = os.path.exists(path)
        if path_exists:
            background_tasks.add_task(os.remove, path)


async def update_photo(
    file: UploadFile,
    record: Type[Base],
    field_name: str,
    background_tasks: BackgroundTasks,
    is_file=False,
) -> str:
    old_photo_path = getattr(record, field_name, None)
    new_photo = await save_photo(file, record, background_tasks, is_file)
    if old_photo_path:
        await delete_photo(old_photo_path, background_tasks)
    return new_photo
