import contextlib

from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.models import Contacts
from src.database.database import get_async_session
from .exceptions import CONTACTS_SUCCESS_CREATE


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_contacts(data: dict, session: AsyncSession):
    try:
        instance = Contacts(**data)
        session.add(instance)
        print(CONTACTS_SUCCESS_CREATE)
    except Exception as exc:
        raise exc
