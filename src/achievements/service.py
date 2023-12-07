from typing import Optional, Type

from sqlalchemy import delete, insert, select, update
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.achievements.schemas import CreateAchievementSchema, UpdateAchievementSchema
from src.achievements.models import Achievement
from src.departments.models import SubDepartment
from src.exceptions import (
    GALLERY_PINNED_EXISTS,
    INVALID_DEPARTMENT,
    NO_DATA_FOUND,
    NO_RECORD,
    SUCCESS_DELETE,
)
from src.utils import save_photo


async def get_all_achievements_by_filter(
    is_pinned: bool,
    session: AsyncSession,
):
    if is_pinned:
        query = (
            select(Achievement)
            .filter(Achievement.pinned_position.isnot(None))
            .order_by(Achievement.pinned_position)
        )
    else:
        query = select(Achievement).order_by(Achievement.created_at.desc())

    result = await session.execute(query)
    response = result.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def get_achievement_by_id(session: AsyncSession, id: int):
    record = await session.get(Achievement, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return record


async def create_achievement(
    schema: CreateAchievementSchema,
    session: AsyncSession,
):
    schema.media = await save_photo(schema.media, Achievement)
    schema_output = schema.model_dump()

    if schema.sub_department:
        query = select(SubDepartment).where(SubDepartment.id == schema.sub_department)
        result = await session.execute(query)
        record = result.scalars().first()
        if not record:
            raise HTTPException(
                status_code=404, detail=INVALID_DEPARTMENT % schema.sub_department
            )
        schema_output["sub_department"] = schema.sub_department

    if schema.pinned_position:
        query = select(Achievement).filter_by(pinned_position=schema.pinned_position)
        record = await session.execute(query)
        instance = record.scalars().first()
        if instance:
            raise HTTPException(
                status_code=400,
                detail=GALLERY_PINNED_EXISTS % schema.pinned_position,
            )

    query = insert(Achievement).values(**schema_output).returning(Achievement)
    result = await session.execute(query)
    record = result.scalars().first()
    await session.commit()
    return record


async def update_achievement(
    id: int,
    media: UploadFile,
    schema: UpdateAchievementSchema,
    session: AsyncSession,
):
    record = await session.get(Achievement, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    schema_output = schema.model_dump()

    if media:
        media = await save_photo(media, Achievement)
        schema_output["media"] = media

    if schema.sub_department and schema.sub_department != record.sub_department:
        query = select(SubDepartment).filter_by(id=schema.sub_department)
        result = await session.execute(query)
        sub_department = result.scalars().first()
        if not sub_department:
            raise HTTPException(
                status_code=404, detail=INVALID_DEPARTMENT % schema.sub_department
            )

    if schema.pinned_position and schema.pinned_position != record.pinned_position:
        query = select(Achievement).filter_by(pinned_position=schema.pinned_position)
        result = await session.execute(query)
        instance = result.scalars().one_or_none()
        if instance:
            raise HTTPException(
                status_code=400,
                detail=GALLERY_PINNED_EXISTS % schema.pinned_position,
            )

    for field, value in schema_output.items():
        setattr(record, field, value)
    await session.commit()
    return record


async def delete_achievement_by_id(id: int, session: AsyncSession):
    record = await session.get(Achievement, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    await session.delete(record)
    await session.commit()
    return {"message": SUCCESS_DELETE % id}
