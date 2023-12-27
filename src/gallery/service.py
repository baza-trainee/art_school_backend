from sqlalchemy import insert, select
from fastapi import BackgroundTasks, HTTPException, UploadFile
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


async def get_all_media_by_filter(
    is_pinned: bool,
    reverse: bool,
    is_video: bool,
    session: AsyncSession,
):
    if is_pinned:
        query = (
            select(Gallery)
            .filter(Gallery.pinned_position.isnot(None))
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


async def get_photo_by_id(id: int, session: AsyncSession):
    record = await session.get(Gallery, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    elif record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_PHOTO)
    return record


async def get_video_by_id(id: int, session: AsyncSession):
    record = await session.get(Gallery, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    elif not record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_VIDEO)
    return record


async def get_positions_status(session: AsyncSession):
    query = select(Gallery.pinned_position).filter(Gallery.pinned_position.isnot(None))
    result = await session.execute(query)
    taken_positions = result.scalars().all()
    all_positions = set(range(1, 8))
    free_positions = all_positions - set(taken_positions)
    shema = GetTakenPositionsSchema(
        taken_positions=taken_positions, free_positions=free_positions
    )
    return shema


async def create_photo(
    schema: CreatePhotoSchema,
    session: AsyncSession,
):
    schema.media = await save_photo(schema.media, Gallery)
    schema_output = schema.model_dump()
    schema_output["is_video"] = False

    if schema.sub_department:
        query = select(SubDepartment).where(SubDepartment.id == schema.sub_department)
        result = await session.execute(query)
        record = result.scalars().first()
        if not record:
            raise HTTPException(
                status_code=404, detail=INVALID_DEPARTMENT % schema.sub_department
            )

    if schema.pinned_position:
        query = select(Gallery).filter_by(pinned_position=schema.pinned_position)
        record = await session.execute(query)
        instance = record.scalars().first()
        if instance:
            raise HTTPException(
                status_code=400,
                detail=GALLERY_PINNED_EXISTS % schema.pinned_position,
            )
    try:
        query = insert(Gallery).values(**schema_output).returning(Gallery)
        result = await session.execute(query)
        record = result.scalars().first()
        await session.commit()
        return record
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def create_video(
    schema: CreatePhotoSchema,
    session: AsyncSession,
):
    try:
        schema_output = schema.model_dump()
        schema_output["is_video"] = True
        schema_output["media"] = str(schema_output["media"])
        query = insert(Gallery).values(**schema_output).returning(Gallery)
        result = await session.execute(query)
        record = result.scalars().first()
        await session.commit()
        return record
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def update_photo_by_id(
    id: int,
    media: UploadFile,
    schema: UpdatePhotoSchema,
    session: AsyncSession,
    background_tasks: BackgroundTasks,
):
    record = await session.get(Gallery, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    elif record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_PHOTO)
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
        query = select(Gallery).filter_by(pinned_position=schema.pinned_position)
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


async def update_video_by_id(
    id: int,
    schema: CreateVideoSchema,
    session: AsyncSession,
):
    record = await session.get(Gallery, id)
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    elif not record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_VIDEO)
    schema_output = schema.model_dump()
    schema_output["is_video"] = True

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
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    try:
        background_tasks.add_task(delete_photo, record.media)
        await session.delete(record)
        await session.commit()
        return {"message": SUCCESS_DELETE % id}
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
