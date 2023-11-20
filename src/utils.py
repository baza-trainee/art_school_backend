from fastapi import FastAPI

from src.auth.utils import create_user
from src.config import ADMIN_PASSWORD, ADMIN_USERNAME
from src.contacts.utils import create_contacts
from src.database import get_async_session


async def lifespan(app: FastAPI):
    print("lifespan start")
    async for s in get_async_session():
        async with s.begin():
            # await create_user(email=ADMIN_USERNAME, password=ADMIN_PASSWORD)
            await create_contacts(
                address="вул.Бульварно-Кудрявська, 2", phone="+38(097)290-79-40"
            )
    yield
    print("lifespan end")
