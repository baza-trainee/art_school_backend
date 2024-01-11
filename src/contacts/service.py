from typing import Type

from fastapi import BackgroundTasks, HTTPException, Response, UploadFile
from pydantic_core import Url
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.contacts.models import Contacts

from src.database.database import Base
from src.exceptions import (
    NO_RECORD,
    SERVER_ERROR,
)
from src.utils import update_photo
from .exceptions import INVALID_FIELD
from .schemas import ContactsUpdateSchema


async def get_record(model: Type[Base], session: AsyncSession):
    try:
        query = select(model)
        result = await session.execute(query)
        response = result.scalars().first()
        if not response:
            raise HTTPException(status_code=404, detail=NO_RECORD)
        return response
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def update_record(
    schema: ContactsUpdateSchema,
    session: AsyncSession,
    background_tasks: BackgroundTasks,
):
    record = await session.get(Contacts, 1)

    contacts_data = schema.model_dump(exclude_none=True)
    if not contacts_data:
        return Response(status_code=204)

    for key, data in contacts_data.items():
        if key in ["statement_for_admission", "official_info"]:
            media = await update_photo(
                file=data,
                record=record,
                field_name=key,
                background_tasks=background_tasks,
                is_file=True,
            )
            contacts_data[key] = media

    for key, value in contacts_data.items():
        if isinstance(value, Url):
            contacts_data[key] = str(value)

    try:
        query = (
            update(Contacts)
            .where(Contacts.id == 1)
            .values(**contacts_data)
            .returning(Contacts)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
