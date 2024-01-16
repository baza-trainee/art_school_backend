import contextlib

from sqlalchemy import select

from src.database.database import get_async_session
from .models import Documents
from .exceptions import SUCCESS_CREATE, ALREADY_EXISTS


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_docs(**kwargs):
    async with get_async_session_context() as session:
        query = select(Documents)
        result = await session.execute(query)
        doc = result.scalars().first()
        if not doc:
            doc = Documents(**kwargs)
            session.add(doc)
            await session.commit()
            print(SUCCESS_CREATE)
        else:
            print(ALREADY_EXISTS)
