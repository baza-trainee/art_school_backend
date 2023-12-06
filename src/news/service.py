from typing import Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile, Response
from sqlalchemy import delete, insert, select, update, desc, func

from src.database.database import Base
from src.news.schemas import (
    NewsCreateSchema,
    NewsUpdateSchema,
)
from src.utils import save_photo
from .exceptions import (
    NEWS_EXISTS,
    NO_DATA_FOUND,
    SERVER_ERROR,
    NO_RECORD,
    SUCCESS_DELETE,
)


async def get_news_order_by_list(
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).order_by(desc(model.created_at))
    news = await session.execute(query)
    response = news.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def get_news_by_id(model: Type[Base], session: AsyncSession, id: int):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_news(
    news_data: NewsCreateSchema,
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(func.lower(model.title) == news_data.title.lower())
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=NEWS_EXISTS % news_data.title,
        )

    news_data.photo = await save_photo(news_data.photo, model)
    try:
        news_data = news_data.model_dump()
        query = insert(model).values(**news_data).returning(model)
        result = await session.execute(query)
        news_data = result.scalars().first()
        await session.commit()
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def update_news(
    news_data: NewsUpdateSchema,
    model: Type[Base],
    session: AsyncSession,
    photo: Optional[UploadFile],
    news_id: int,
):
    query = select(model).where(model.id == news_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    update_data = news_data.model_dump(exclude_none=True)
    if photo:
        update_data["photo"] = await save_photo(photo, model)
    if not update_data:
        return Response(status_code=204)
    try:
        query = (
            update(model)
            .where(model.id == news_id)
            .values(**update_data)
            .returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_news_by_id(news_id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == news_id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)

    try:
        query = delete(model).where(model.id == news_id)
        await session.execute(query)
        await session.commit()
        return {"message": SUCCESS_DELETE % news_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
