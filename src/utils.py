from fastapi import FastAPI

from src.auth.utils import create_user
from src.config import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    CONTACTS,
    DEPARTMENTS,
    SUB_DEPARTMENTS,
)
from src.contacts.utils import create_contacts
from src.database import get_async_session
from src.departments.utils import create_main_departments, create_sub_departments
from src.slider_main.utils import create_slide


async def lifespan(app: FastAPI):
    async for s in get_async_session():
        async with s.begin():
            await create_user(email=ADMIN_USERNAME, password=ADMIN_PASSWORD)
            await create_main_departments(DEPARTMENTS)
            await create_sub_departments(SUB_DEPARTMENTS)
            await create_contacts(**CONTACTS)
            await create_slide(title="Slide1", description="Slide1 Test description")
            await create_slide(title="Slide2", description="Slide2 Test description")
            await create_slide(title="Slide3", description="Slide3 Test description")
            await create_slide(title="Slide4", description="Slide4 Test description")
            await create_slide(title="Slide5", description="Slide5 Test description")

    yield
