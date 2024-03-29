from typing import Optional

from sqlalchemy import insert, select
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.achievements.schemas import (
    CreateAchievementSchema,
    UpdateAchievementSchema,
    GetTakenPositionsSchema,
)
from src.achievements.models import Achievement
from src.departments.models import SubDepartment
from src.utils import save_photo, update_photo, delete_photo
from .exceptions import INVALID_DEPARTMENT, ACHIEVEMENT_PINNED_EXISTS
from src.exceptions import (
    NO_DATA_FOUND,
    NO_RECORD,
    SERVER_ERROR,
    SUCCESS_DELETE,
)


async def _check_department(
    sub_department: Optional[int], session: AsyncSession
) -> None:
    query = select(SubDepartment).where(SubDepartment.id == sub_department)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=INVALID_DEPARTMENT % sub_department)


async def _check_pinned_position(
    pinned_position: Optional[int], session: AsyncSession
) -> None:
    query = select(Achievement).filter_by(pinned_position=pinned_position)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        raise HTTPException(
            status_code=400, detail=ACHIEVEMENT_PINNED_EXISTS % pinned_position
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
    background_tasks: BackgroundTasks,
):
    if schema.sub_department:
        await _check_department(schema.sub_department, session)
    if schema.pinned_position:
        await _check_pinned_position(schema.pinned_position, session)

    schema_output = schema.model_dump()
    schema_output["media"] = await save_photo(
        schema.media, Achievement, background_tasks
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
    schema: UpdateAchievementSchema,
    session: AsyncSession,
    background_tasks: BackgroundTasks,
):
    record = await session.get(Achievement, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)

    if schema.sub_department and schema.sub_department != record.sub_department:
        await _check_department(schema.sub_department, session)
    if schema.pinned_position and schema.pinned_position != record.pinned_position:
        await _check_pinned_position(schema.pinned_position, session)

    schema_output = schema.model_dump()
    media = schema_output.get("media", None)
    if media:
        schema_output["media"] = await update_photo(
            file=media,
            record=record,
            field_name="media",
            background_tasks=background_tasks,
        )
    else:
        del schema_output["media"]

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
        await session.delete(record)
        await session.commit()
        await delete_photo(record.media, background_tasks)
        return {"message": SUCCESS_DELETE % id}
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
