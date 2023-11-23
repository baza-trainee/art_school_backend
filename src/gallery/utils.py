from typing import Optional, Type

from cloudinary import uploader
from pydantic import AnyHttpUrl
from sqlalchemy import delete, insert, select, update
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.gallery.schemas import (
    CreatePhotoSchema,
    PositionEnum,
    GallerySubDepartmentEnum,
    CreateVideoSchema,
)
from src.exceptions import (
    GALLERY_IS_NOT_A_PHOTO,
    GALLERY_IS_NOT_A_VIDEO,
    GALLERY_PINNED_EXISTS,
    NO_DATA_FOUND,
    NO_RECORD,
    SERVER_ERROR,
    SUCCESS_DELETE,
)


async def get_all_media_by_type(
    model: Type[Base],
    session: AsyncSession,
    is_video: bool,
):
    query = select(model).filter_by(is_video=is_video).order_by(model.created_at.desc())
    result = await session.execute(query)
    response = result.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def get_media_by_id(
    model: Type[Base], session: AsyncSession, id: int, is_video: bool
):
    query = select(model).filter_by(id=id, is_video=is_video)
    result = await session.execute(query)
    response = result.scalars().one_or_none()
    if not response:
        query = select(model).filter_by(id=id)
        result = await session.execute(query)
        response = result.scalars().one_or_none()
        if response:
            error_text = GALLERY_IS_NOT_A_VIDEO if is_video else GALLERY_IS_NOT_A_PHOTO
            raise HTTPException(status_code=404, detail=error_text)
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_photo(
    gallery: CreatePhotoSchema,
    model: Type[Base],
    session: AsyncSession,
):
    if gallery.pinned_position:
        query = select(model).filter_by(pinned_position=gallery.pinned_position)
        record = await session.execute(query)
        instance = record.scalars().first()
        if instance:
            raise HTTPException(
                status_code=400,
                detail=GALLERY_PINNED_EXISTS % gallery.pinned_position.value,
            )
        if gallery.pinned_position == 0:
            schema_output["pinned_position"] = None
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
    schema_output["is_video"] = False
    if gallery.sub_department == 0:
        schema_output["sub_department"] = None
    if gallery.pinned_position == 0:
        schema_output["pinned_position"] = None
    query = insert(model).values(**schema_output).returning(model)
    result = await session.execute(query)
    gallery = result.scalars().first()
    await session.commit()
    return gallery


async def create_video(
    gallery: CreateVideoSchema,
    model: Type[Base],
    session: AsyncSession,
):
    schema_output = gallery.model_dump()
    schema_output["sub_department"] = None
    schema_output["pinned_position"] = None
    schema_output["is_video"] = True
    schema_output["media"] = str(schema_output["media"])
    query = insert(model).values(**schema_output).returning(model)
    result = await session.execute(query)
    gallery = result.scalars().first()
    await session.commit()
    return gallery


async def update_photo(
    id: int,
    pinned_position: PositionEnum,
    sub_department: GallerySubDepartmentEnum,
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
    if record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_PHOTO)
    update_data = {
        "is_video": False,
        "description": description,
    }
    if not sub_department is None:
        if sub_department == 0:
            update_data["sub_department"] = None
        else:
            update_data["sub_department"] = sub_department
    if not pinned_position is None:
        if pinned_position != record.pinned_position:
            query = select(model).filter_by(pinned_position=pinned_position)
            record = await session.execute(query)
            instance = record.scalars().first()
            if instance:
                raise HTTPException(
                    status_code=400,
                    detail=GALLERY_PINNED_EXISTS % pinned_position.value,
                )
        if pinned_position == 0:
            update_data["pinned_position"] = None
        else:
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


async def update_video(
    id: int,
    media: Optional[AnyHttpUrl],
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record.is_video:
        raise HTTPException(status_code=404, detail=GALLERY_IS_NOT_A_VIDEO)
    update_data = {
        "is_video": True,
    }
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    if media:
        update_data["media"] = str(media)
    try:
        query = (
            update(model).where(model.id == id).values(**update_data).returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_media_by_id(id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)
    query = delete(model).where(model.id == id)
    await session.execute(query)
    await session.commit()
    return {"message": SUCCESS_DELETE % id}
