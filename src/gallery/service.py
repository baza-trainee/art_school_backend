from typing import Optional, Union

from sqlalchemy import and_, insert, select
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.departments.models import SubDepartment
from src.gallery.models import Gallery
from src.utils import delete_photo, save_photo, update_photo
from src.gallery.schemas import (
    CreatePhotoSchema,
    CreateVideoSchema,
    GetTakenPositionsSchema,
    UpdatePhotoSchema,
)
from src.exceptions import (
    NO_DATA_FOUND,
    NO_RECORD,
    SERVER_ERROR,
    SUCCESS_DELETE,
)
from .exceptions import (
    INVALID_DEPARTMENT,
    GALLERY_IS_NOT_A_PHOTO,
    GALLERY_IS_NOT_A_VIDEO,
    GALLERY_PINNED_EXISTS,
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
    pinned_position: Optional[int], session: AsyncSession, is_video=False
) -> None:
    query = select(Gallery).where(
        and_(Gallery.is_video == is_video, Gallery.pinned_position == pinned_position)
    )
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        raise HTTPException(
            status_code=400, detail=GALLERY_PINNED_EXISTS % pinned_position
        )


async def get_all_media_by_filter(
    is_pinned: bool,
    reverse: bool,
    is_video: bool,
    session: AsyncSession,
):
    if is_pinned:
        query = (
            select(Gallery)
            .where(
                and_(Gallery.is_video == is_video, Gallery.pinned_position.isnot(None))
            )
            .order_by(Gallery.pinned_position)
        )
    else:
        if reverse:
            query = (
                select(Gallery)
                .filter_by(is_video=is_video)
                .order_by(Gallery.created_at.asc())
            )
        else:
            query = (
                select(Gallery)
                .filter_by(is_video=is_video)
                .order_by(Gallery.created_at.desc())
            )

    result = await session.execute(query)
    response = result.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def get_media_by_id(id: int, session: AsyncSession, is_video=False):
    try:
        record = await session.get(Gallery, id)
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    elif not is_video and record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_PHOTO)
    elif is_video and not record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_VIDEO)
    return record


async def get_positions_status(session: AsyncSession, is_video=False):
    query = select(Gallery.pinned_position).where(
        and_(Gallery.is_video == is_video, Gallery.pinned_position.isnot(None)),
    )
    result = await session.execute(query)
    taken_positions = result.scalars().all()
    if is_video:
        all_positions = set(range(1, 6))
    else:
        all_positions = set(range(1, 8))
    free_positions = all_positions - set(taken_positions)
    shema = GetTakenPositionsSchema(
        taken_positions=taken_positions, free_positions=free_positions
    )
    return shema


async def create_media(
    schema: Union[CreatePhotoSchema, CreateVideoSchema],
    session: AsyncSession,
    background_tasks: BackgroundTasks = None,
    is_video=False,
):
    if schema.sub_department:
        await _check_department(schema.sub_department, session)
    if schema.pinned_position:
        await _check_pinned_position(schema.pinned_position, session, is_video)

    schema_output = schema.model_dump()
    schema_output["is_video"] = is_video
    if is_video:
        schema_output["media"] = str(schema.media)
    else:
        schema_output["media"] = await save_photo(
            schema.media, Gallery, background_tasks
        )

    try:
        query = insert(Gallery).values(**schema_output).returning(Gallery)
        result = await session.execute(query)
        record = result.scalars().first()
        await session.commit()
        return record
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def update_media_by_id(
    id: int,
    schema: UpdatePhotoSchema,
    session: AsyncSession,
    background_tasks: BackgroundTasks = None,
    is_video=False,
):
    try:
        record = await session.get(Gallery, id)
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    elif not is_video and record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_PHOTO)
    elif is_video and not record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_VIDEO)

    if schema.sub_department and schema.sub_department != record.sub_department:
        await _check_department(schema.sub_department, session)
    if schema.pinned_position and schema.pinned_position != record.pinned_position:
        await _check_pinned_position(schema.pinned_position, session, is_video=is_video)

    schema_output = schema.model_dump()
    if is_video:
        schema_output["media"] = str(schema.media)
    else:
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


async def delete_media_by_id(
    id: int, session: AsyncSession, background_tasks: BackgroundTasks
):
    record = await session.get(Gallery, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    try:
        await session.delete(record)
        await session.commit()
        if not record.is_video:
            await delete_photo(record.media, background_tasks)
        return {"message": SUCCESS_DELETE % id}
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
