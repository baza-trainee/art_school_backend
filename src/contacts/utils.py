import contextlib

from sqlalchemy import select

from src.contacts.models import Contacts
from src.database.database import get_async_session
from .exceptions import CONTACTS_ALREADY_EXISTS, CONTACTS_SUCCESS_CREATE


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_contacts(address: str, phone: str):
    async with get_async_session_context() as session:
        query = select(Contacts)
        result = await session.execute(query)
        contacts = result.scalars().first()
        if not contacts:
            contacts = Contacts(address=address, phone=phone)
            session.add(contacts)
            await session.commit()
            print(CONTACTS_SUCCESS_CREATE)
        else:
            print(CONTACTS_ALREADY_EXISTS)
