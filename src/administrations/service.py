from typing import List, Optional, Type

from cloudinary import uploader
from fastapi import HTTPException, Response, UploadFile
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.exceptions import (
    NO_DATA_FOUND,
    NO_RECORD,
    PERSON_EXISTS,
    SERVER_ERROR,
    SUCCESS_DELETE,
)
from .models import SchoolAdministration
from .schemas import AdministratorCreateSchema, AdministratorUpdateSchema


async def get_all_administration(
    model: Type[Base], session: AsyncSession,
) -> List[SchoolAdministration]:
    query = select(model)
    result = await session.execute(query)
    response = result.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_administration(
    person: AdministratorCreateSchema, model: Type[Base], session: AsyncSession
) -> SchoolAdministration:
    query = select(SchoolAdministration).where(
        func.lower(SchoolAdministration.full_name) == person.full_name.lower()
    )
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=PERSON_EXISTS % person.full_name,
        )
    photo = person.photo
    folder_path = f"static/{model.__name__}"
    # os.makedirs(folder_path, exist_ok=True)
    # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
    # async with aiofiles.open(file_path, "wb") as buffer:
    #     await buffer.write(await photo.read())
    # department.photo = file_path
    upload_result = uploader.upload(photo.file, folder=folder_path)
    person.photo = upload_result["url"]
    query = (
        insert(SchoolAdministration)
        .values(**person.model_dump())
        .returning(SchoolAdministration)
    )
    result = await session.execute(query)
    person = result.scalars().first()
    await session.commit()
    return person


async def get_one_administrator(
    id: int, model: Type[Base], session: AsyncSession
) -> SchoolAdministration:
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    return response


async def update_administration(
    id: int,
    person: AdministratorUpdateSchema,
    photo: Optional[UploadFile],
    model: Type[Base],
    session: AsyncSession,
) -> SchoolAdministration:
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    update_data = person.model_dump(exclude_none=True)
    if photo:
        folder_path = f"static/{model.__name__}"
        # os.makedirs(folder_path, exist_ok=True)
        # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
        # async with aiofiles.open(file_path, "wb") as buffer:
        #     await buffer.write(await photo.read())
        # update_data["photo"] = file_path
        upload_result = uploader.upload(photo.file, folder=folder_path)
        update_data["photo"] = upload_result["url"]
    if not update_data:
        return Response(status_code=204)
    try:
        query = (
            update(model).where(model.id == id).values(**update_data).returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_administration(id: int, model: Type[Base], session: AsyncSession) -> dict:
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)
    query = delete(model).where(model.id == id)
    await session.execute(query)
    await session.commit()
    return {"message": SUCCESS_DELETE % id}
