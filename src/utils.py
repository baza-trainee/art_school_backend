from fastapi import FastAPI
from sqlalchemy import func, select

from src.auth.models import User
from src.auth.utils import create_user
from src.contacts.utils import create_contacts
from src.database import get_async_session
from src.departments.utils import create_main_departments, create_sub_departments

# from src.redis import init_redis, redis
from src.slider_main.utils import create_slides
from src.config import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    CONTACTS,
    DEPARTMENTS,
    SUB_DEPARTMENTS,
    SLIDES,
)


# lock = redis.lock("my_lock")


async def lifespan(app: FastAPI):
    # await init_redis()
    # await lock.acquire(blocking=True)
    async for s in get_async_session():
        async with s.begin():
            user_count = await s.execute(select(func.count()).select_from(User))
            if user_count.scalar() == 0:
                await create_user(email=ADMIN_USERNAME, password=ADMIN_PASSWORD)
                await create_main_departments(DEPARTMENTS)
                await create_sub_departments(SUB_DEPARTMENTS)
                await create_contacts(**CONTACTS)
                await create_slides(SLIDES)
    # await lock.release()
    yield
