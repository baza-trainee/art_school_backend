from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import Contacts

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("")
async def get_contacts(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Contacts)
        result = await session.execute(query)
        return {"status": "success", "data": result.all(), "details": None}
    except Exception:
        raise HTTPException(
            status_code=500, detail={"status": "error", "data": None, "details": None}
        )
