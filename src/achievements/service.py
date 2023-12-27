import asyncio
from sqlalchemy import insert, select
from fastapi import BackgroundTasks, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.achievements.schemas import (
    CreateAchievementSchema,
    UpdateAchievementSchema,
    GetTakenPositionsSchema,
)
from src.achievements.models import Achievement
from src.departments.models import SubDepartment
from src.utils import save_photo, update_photo, delete_photo
from .exceptions import INVALID_DEPARTMENT, GALLERY_PINNED_EXISTS
from src.exceptions import (
    NO_DATA_FOUND,
    NO_RECORD,
    SERVER_ERROR,
    SUCCESS_DELETE,
)


async def get_all_achievements_by_filter(
    is_pinned: bool,
    reverse: bool,
    session: AsyncSession,
):
    if is_pinned:
        query = (
            select(Achievement)
            .filter(Achievement.pinned_position.isnot(None))
            .order_by(Achievement.pinned_position)
        )
    else:
        if reverse:
            query = select(Achievement).order_by(Achievement.created_at.asc())
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


async def get_positions_status(session: AsyncSession):
    query = select(Achievement.pinned_position).filter(
        Achievement.pinned_position.isnot(None)
    )
    result = await session.execute(query)
    taken_positions = result.scalars().all()
    all_positions = set(range(1, 13))
    free_positions = all_positions - set(taken_positions)
    shema = GetTakenPositionsSchema(
        taken_positions=taken_positions, free_positions=free_positions
    )
    return shema


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

    if schema.pinned_position:
        query = select(Achievement).filter_by(pinned_position=schema.pinned_position)
        record = await session.execute(query)
        instance = record.scalars().first()
        if instance:
            raise HTTPException(
                status_code=400,
                detail=GALLERY_PINNED_EXISTS % schema.pinned_position,
            )
    try:
        query = insert(Achievement).values(**schema_output).returning(Achievement)
        result = await session.execute(query)
        record = result.scalars().first()
        await session.commit()
        return record
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def update_achievement(
    id: int,
    media: UploadFile,
    schema: UpdateAchievementSchema,
    session: AsyncSession,
    background_tasks: BackgroundTasks,
):
    record = await session.get(Achievement, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    schema_output = schema.model_dump()

    if media:
        media = await update_photo(
            file=media,
            record=record,
            field_name="media",
            background_tasks=background_tasks,
        )
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
    try:
        for field, value in schema_output.items():
            setattr(record, field, value)
        await session.commit()
        return record
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_achievement_by_id(
    id: int, session: AsyncSession, background_tasks: BackgroundTasks
):
    record = await session.get(Achievement, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    try:
        background_tasks.add_task(delete_photo, record.media)
        await session.delete(record)
        await session.commit()
        return {"message": SUCCESS_DELETE % id}
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
