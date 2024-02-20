import contextlib
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.administrations.models import SchoolAdministration
from src.database.database import get_async_session
from .exceptions import SUCCESS


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_administrations(slides_list: List[dict], session: AsyncSession):
    try:
        for data in slides_list:
            instance = SchoolAdministration(**data)
            session.add(instance)
            print(SUCCESS % data["full_name"])
    except Exception as exc:
        raise exc
