import contextlib

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from .models import Documents
from .exceptions import SUCCESS_CREATE


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_docs(data: dict, session: AsyncSession):
    try:
        instance = Documents(**data)
        session.add(instance)
        print(SUCCESS_CREATE)
    except Exception as exc:
        raise exc
