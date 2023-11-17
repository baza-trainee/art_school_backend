from typing import Type
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base


async def get_department(id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail="No data found")
    return response
