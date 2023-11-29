from typing import Optional, Type

from cloudinary import uploader
from sqlalchemy import delete, insert, select, update
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.achievements.schemas import (
    CreateAchievementSchema,
    PositionEnum,
)
from src.departments.models import SubDepartment
from src.exceptions import (
    GALLERY_PINNED_EXISTS,
    INVALID_DEPARTMENT,
    NO_DATA_FOUND,
    NO_RECORD,
    SERVER_ERROR,
    SUCCESS_DELETE,
)


async def get_all_achievements_by_filter(
    model: Type[Base],
    session: AsyncSession,
    is_pinned: bool,
):
    if is_pinned:
        query = (
            select(model)
            .filter(model.pinned_position.isnot(None))
            .order_by(model.pinned_position)
        )
    else:
        query = select(model).order_by(model.created_at.desc())
    result = await session.execute(query)
    response = result.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def get_media_by_id(model: Type[Base], session: AsyncSession, id: int):
    query = select(model).filter_by(id=id)
    result = await session.execute(query)
    response = result.scalars().one_or_none()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_photo(
    pinned_position: PositionEnum,
    sub_department: int,
    gallery: CreateAchievementSchema,
    model: Type[Base],
    session: AsyncSession,
):
    photo = gallery.media
    folder_path = f"static/{model.__name__}"
    # os.makedirs(folder_path, exist_ok=True)
    # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
    # async with aiofiles.open(file_path, "wb") as buffer:
    #     await buffer.write(await photo.read())
    # department.photo = file_path
    upload_result = uploader.upload(photo.file, folder=folder_path)
    gallery.media = upload_result["url"]
    schema_output = gallery.model_dump()

    if sub_department:
        query = select(SubDepartment).where(SubDepartment.id == sub_department)
        result = await session.execute(query)
        record = result.scalars().first()
        if not record:
            raise HTTPException(
                status_code=404, detail=INVALID_DEPARTMENT % sub_department
            )
        schema_output["sub_department"] = sub_department

    if not pinned_position:
        schema_output["pinned_position"] = None
    else:
        query = select(model).filter_by(pinned_position=pinned_position)
        record = await session.execute(query)
        instance = record.scalars().first()
        if instance:
            raise HTTPException(
                status_code=400,
                detail=GALLERY_PINNED_EXISTS % pinned_position.value,
            )
        schema_output["pinned_position"] = pinned_position

    query = insert(model).values(**schema_output).returning(model)
    result = await session.execute(query)
    gallery = result.scalars().first()
    await session.commit()
    return gallery


async def update_photo(
    id: int,
    pinned_position: PositionEnum,
    sub_department: int,
    description: str,
    media: Optional[UploadFile],
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)

    update_data = {
        "description": description if description else record.description,
    }
    if not sub_department is None:
        if sub_department == 0:
            update_data["sub_department"] = None
        else:
            query = select(SubDepartment).where(SubDepartment.id == sub_department)
            result = await session.execute(query)
            record = result.scalars().first()
            if not record:
                raise HTTPException(
                    status_code=404, detail=INVALID_DEPARTMENT % sub_department
                )
            update_data["sub_department"] = sub_department

    if not pinned_position is None:
        if pinned_position == 0:
            update_data["pinned_position"] = None
        else:
            if pinned_position != record.pinned_position:
                query = select(model).filter_by(pinned_position=pinned_position)
                record = await session.execute(query)
                instance = record.scalars().first()
                if instance:
                    raise HTTPException(
                        status_code=400,
                        detail=GALLERY_PINNED_EXISTS % pinned_position.value,
                    )
            update_data["pinned_position"] = pinned_position

    if media:
        folder_path = f"static/{model.__name__}"
        # os.makedirs(folder_path, exist_ok=True)
        # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
        # async with aiofiles.open(file_path, "wb") as buffer:
        #     await buffer.write(await photo.read())
        # update_data["photo"] = file_path
        upload_result = uploader.upload(media.file, folder=folder_path)
        update_data["media"] = upload_result["url"]
    try:
        query = (
            update(model).where(model.id == id).values(**update_data).returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_achievement_by_id(id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)
    query = delete(model).where(model.id == id)
    await session.execute(query)
    await session.commit()
    return {"message": SUCCESS_DELETE % id}
