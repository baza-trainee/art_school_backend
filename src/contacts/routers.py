from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_core import Url

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database import get_async_session
from src.exceptions import INVALID_FIELD, SERVER_ERROR, NO_DATA_FOUND
from .schemas import ContactField, ContactsSchema, ContactsUpdateSchema
from .models import Contacts


router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("", response_model=ContactsSchema)
async def get_contacts(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Contacts)
        contacts = await session.execute(query)
        if not contacts:
            raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
        return contacts.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@router.patch("", response_model=ContactsSchema)
async def update_contacts(
    contacts_update: ContactsUpdateSchema = Depends(ContactsUpdateSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    contacts_data = contacts_update.model_dump(exclude_none=True)
    if not contacts_data:
        return Response(status_code=204)
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


@router.delete("/{field}", response_model=ContactsSchema)
async def clear_field(
    field: ContactField,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    if field not in Contacts.__table__.columns:
        raise HTTPException(status_code=400, detail=INVALID_FIELD)
    try:
        query = (
            update(Contacts)
            .where(Contacts.id == 1)
            .values({field: None})
            .returning(Contacts)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
