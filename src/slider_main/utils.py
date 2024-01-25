import contextlib
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import SUCCESS_CREATE
from src.slider_main.models import SliderMain
from src.database.database import get_async_session


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_slides(slides_list: List[dict], session: AsyncSession):
    try:
        for data in slides_list:
            instance = SliderMain(**data)
            session.add(instance)
            print(SUCCESS_CREATE)
    except Exception as exc:
        raise exc
