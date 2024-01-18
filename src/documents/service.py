from typing import Type

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks, HTTPException, Response
from sqlalchemy import delete, insert, or_, select, update, func

from src.database.database import Base
from src.utils import save_photo, update_photo
from .exceptions import (
    DELETE_ERROR,
    DOCS_EXISTS,
    NO_DATA_FOUND,
    NO_DOC_FOUND,
    SERVER_ERROR,
    SUCCESS_DELETE,
)


async def get_docs_list(
    model: Type[Base],
    session: AsyncSession,
    is_pinned: bool = None,
):
    if is_pinned:
        query = select(model).where(model.is_pinned == True)
    else:
        query = (
            select(model)
            .where(or_(model.is_pinned == False, model.is_pinned == None))
            .order_by("id")
        )
    doc = await session.execute(query)
    response = doc.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def get_doc_by_id(model: Type[Base], session: AsyncSession, id: int):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DOC_FOUND % id)
    return response


async def create_document(document, model: Type[Base], session: AsyncSession):
    query = select(model).where(func.lower(model.doc_name) == document.doc_name.lower())
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=DOCS_EXISTS % document.doc_name,
        )
    document.doc_path = await save_photo(document.doc_path, model, is_file=True)
    query = insert(model).values(**document.model_dump()).returning(model)
    result = await session.execute(query)
    document = result.scalars().first()
    await session.commit()
    return document


async def update_document(
    id: int,
    schema: BaseModel,
    model: Type[Base],
    session: AsyncSession,
    background_tasks: BackgroundTasks,
):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DOC_FOUND)
    update_data = schema.model_dump(exclude_none=True)
    if not update_data:
        return Response(status_code=204)
    for key, data in update_data.items():
        if key == "doc_path":
            media = await update_photo(
                file=data,
                record=record,
                field_name=key,
                background_tasks=background_tasks,
                is_file=True,
            )
            update_data[key] = media
    try:
        query = (
            update(model).where(model.id == id).values(**update_data).returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=400, detail=DOCS_EXISTS % update_data.get("doc_name")
            )
        else:
            raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_record(id: int, model: Type[Base], session: AsyncSession) -> dict:
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DOC_FOUND)
    if record.is_pinned:
        raise HTTPException(status_code=400, detail=DELETE_ERROR)
    query = delete(model).where(model.id == id)
    await session.execute(query)
    await session.commit()
    return {"message": SUCCESS_DELETE % id}
