from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.exceptions import SERVER_ERROR, NO_DATA_FOUND
from .schemas import ContactsSchema, ContactsUpdateSchema
from .models import Contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("", response_model=ContactsSchema)
async def get_contacts(
    session: AsyncSession = Depends(get_async_session),
) -> ContactsSchema:
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
    contacts_update: ContactsUpdateSchema = Depends(ContactsUpdateSchema.as_form_patch),
    session: AsyncSession = Depends(get_async_session),
) -> ContactsSchema:
    if not contacts_update.model_dump(exclude_none=True):
        return Response(status_code=204)
    try:
        query = (
            update(Contacts)
            .where(Contacts.id == 1)
            .values(**contacts_update.model_dump(exclude_none=True))
            .returning(Contacts)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
