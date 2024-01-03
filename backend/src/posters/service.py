from typing import Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile, Response
from sqlalchemy import delete, insert, select, update, desc, func

from src.database.database import Base
from src.posters.schemas import PosterCreateSchema, PosterUpdateSchema
from src.utils import save_photo
from .exceptions import (
    POSTERS_EXISTS,
    NO_DATA_FOUND,
    SERVER_ERROR,
    NO_RECORD,
    NO_DATA_LIST_FOUND,
    SUCCESS_DELETE,
)


async def get_all_posters(model: Type[Base], session: AsyncSession):
    query = select(model).order_by(desc(model.created_at))
    posters = await session.execute(query)
    all_posters = posters.scalars().all()
    if not all_posters:
        raise HTTPException(status_code=404, detail=NO_DATA_LIST_FOUND)
    return all_posters


async def get_poster_by_id(model: Type[Base], session: AsyncSession, id: int):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_poster(
    poster_data: PosterCreateSchema,
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(func.lower(model.title) == poster_data.title.lower())
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=POSTERS_EXISTS % poster_data.title,
        )
    poster_data.photo = await save_photo(poster_data.photo, model)
    try:
        query = insert(model).values(**poster_data.model_dump()).returning(model)
        result = await session.execute(query)
        poster_data = result.scalars().first()
        await session.commit()
        return poster_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def patch_poster(
    posters_data: PosterUpdateSchema,
    model: Type[Base],
    session: AsyncSession,
    photo: Optional[UploadFile],
    poster_id: int,
):
    query = select(model).where(model.id == poster_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    update_data = posters_data.model_dump(exclude_none=True)
    if photo:
        update_data["photo"] = await save_photo(photo, model)
    if not update_data:
        return Response(status_code=204)
    try:
        query = (
            update(model)
            .where(model.id == poster_id)
            .values(**update_data)
            .returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_poster_by_id(poster_id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == poster_id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)

    try:
        query = delete(model).where(model.id == poster_id)
        await session.execute(query)
        await session.commit()
        return {"message": SUCCESS_DELETE % poster_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
