from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.auth.utils import create_user
from src.config import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    CONTACTS,
    DEPARTMENTS,
    REDIS_HOST,
    REDIS_PORT,
    SUB_DEPARTMENTS,
    SLIDES,
)
from src.contacts.utils import create_contacts
from src.database import get_async_session
from src.departments.utils import create_main_departments, create_sub_departments
from src.slider_main.utils import create_slides


async def lifespan(app: FastAPI):
    async for s in get_async_session():
        async with s.begin():
            redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
            FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
            await create_user(email=ADMIN_USERNAME, password=ADMIN_PASSWORD)
            await create_main_departments(DEPARTMENTS)
            await create_sub_departments(SUB_DEPARTMENTS)
            await create_contacts(**CONTACTS)
            await create_slides(SLIDES)
    yield
