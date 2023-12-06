import contextlib
from typing import List

from sqlalchemy import select

from src.administrations.models import SchoolAdministration
from src.database.database import get_async_session
from src.exceptions import PERSON_EXISTS, SUCCESS


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_administrator(admin: dict):
    async with get_async_session_context() as session:
        query = select(SchoolAdministration).filter(
            SchoolAdministration.full_name == admin["full_name"]
        )
        result = await session.execute(query)
        administrator = result.scalars().first()
        if not administrator:
            administrator = SchoolAdministration(**admin)
            session.add(administrator)
            await session.commit()
            print(SUCCESS % admin["full_name"])
        else:
            print(PERSON_EXISTS % admin["full_name"])


async def create_administrations(admins: List[dict]):
    for admin in admins:
        await create_administrator(admin)
