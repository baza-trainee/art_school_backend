from typing import Type

from sqlalchemy import and_, delete, desc, func, insert, select, update
from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.achievements.models import Achievement
from src.database.database import Base
from src.exceptions import NO_DATA_FOUND, NO_RECORD
from src.gallery.models import Gallery
from .exceptions import (
    EXISTS_SUB_NAME,
    INVALID,
    NO_MEDIA,
    NO_SUB_DEPARTMENT,
    SUB_DEP_EXISTS,
    SUCCESS_DELETE,
)


async def get_dep(model: Type[Base], session: AsyncSession):
    query = select(model).order_by(model.id)
    departments = await session.execute(query)
    if not departments:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return departments.scalars().all()


async def get_sub_dep_list(id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.main_department_id == id).order_by(model.id)
    result = await session.execute(query)
    sub_departments = result.scalars().all()
    if not sub_departments:
        raise HTTPException(status_code=404, detail=NO_SUB_DEPARTMENT)
    return sub_departments


async def create_sub_dep(data, model: Type[Base], session: AsyncSession):
    query = select(model).where(
        func.lower(model.sub_department_name) == data.sub_department_name.lower()
    )
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=SUB_DEP_EXISTS % (data.sub_department_name, data.main_department_id),
        )
    query = insert(model).values(**data.model_dump()).returning(model)
    result = await session.execute(query)
    sub_department = result.scalars().first()
    await session.commit()
    return sub_department


async def get_one_sub_dep(id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    sub_department = result.scalars().first()
    if not sub_department:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    return sub_department


async def get_main_dep(id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    department = result.scalars().first()
    if not department:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    return department


async def get_media_for_sub_dep(
    id: int, model: Type[Base], session: AsyncSession, list_type: str
):
    query = select(model).order_by(desc(model.created_at))
    match list_type:
        case "photo":
            query = query.where(
                and_(model.sub_department == id, model.is_video == False)
            )
        case "video":
            query = query.where(
                and_(model.sub_department == id, model.is_video == True)
            )
        case "achievement":
            query = query.where(model.sub_department == id)
        case _:
            raise HTTPException(status_code=400, detail=INVALID)

    result = await session.execute(query)
    list_of_media = result.scalars().all()
    if not list_of_media:
        raise HTTPException(status_code=404, detail=NO_MEDIA)
    return list_of_media


async def update_sub_dep(
    id,
    department_data,
    model: Type[Base],
    session: AsyncSession,
):
    update_data = department_data.model_dump(exclude_none=True)
    if not update_data:
        return Response(status_code=204)

    if "sub_department_name" in update_data:
        query = select(model).where(
            model.sub_department_name == update_data["sub_department_name"]
        )
        result = await session.execute(query)
        record = result.scalars().first()
        if record and record.id != id:
            raise HTTPException(
                status_code=400,
                detail=EXISTS_SUB_NAME % update_data["sub_department_name"],
            )

    query = select(model).where(model.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    query = update(model).where(model.id == id).values(**update_data).returning(model)
    result = await session.execute(query)
    await session.commit()
    return result.scalars().first()


async def delete_sub_dep(id, model: Type[Base], session: AsyncSession):
    async with session.begin():
        gallery_query = (
            update(Gallery)
            .where(Gallery.sub_department == id)
            .values(sub_department=None)
        )
        achievement_query = (
            update(Achievement)
            .where(Achievement.sub_department == id)
            .values(sub_department=None)
        )
        await session.execute(gallery_query)
        await session.execute(achievement_query)
        query = delete(model).where(model.id == id)
        result = await session.execute(query)
        if not result.rowcount:
            raise HTTPException(status_code=404, detail=NO_RECORD)
    return {"detail": SUCCESS_DELETE}
