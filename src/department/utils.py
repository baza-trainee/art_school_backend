import os
from typing import Optional, Type

import aiofiles
from sqlalchemy import delete, func, insert, select, update
from fastapi import HTTPException, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.department.schemas import DepartmentCreateSchema, DepartmentUpdateSchema
from src.exceptions import (
    DEPARTMENTS_EXISTS,
    NO_DATA_FOUND,
    NO_RECORD,
    SERVER_ERROR,
    SUCCESS_DELETE,
)
from cloudinary import uploader


async def get_department(id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def get_all_departments(model: Type[Base], session: AsyncSession):
    query = select(model)
    result = await session.execute(query)
    response = result.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_department(
    department: DepartmentCreateSchema, 
    model: Type[Base],
    session: AsyncSession
):
    query = select(model).where(
        func.lower(model.sub_department_name) == department.sub_department_name.lower()
    )
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=DEPARTMENTS_EXISTS % department.sub_department_name,
        )
    photo = department.photo
    folder_path = f"static/{model.__name__}"
    # os.makedirs(folder_path, exist_ok=True)
    # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
    # async with aiofiles.open(file_path, "wb") as buffer:
    #     await buffer.write(await photo.read())
    # department.photo = file_path
    upload_result = uploader.upload(photo.file, folder=folder_path)
    department.photo = upload_result["url"]
    query = insert(model).values(**department.model_dump()).returning(model)
    result = await session.execute(query)
    department = result.scalars().first()
    await session.commit()
    return {"message": SUCCESS_DELETE % id}


async def update_department(
    id: int,
    department_data: DepartmentUpdateSchema,
    photo: Optional[UploadFile],
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    update_data = department_data.model_dump(exclude_none=True)
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


async def delete_department(id: int, model: Type[Base], session: AsyncSession):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)
    query = delete(model).where(model.id == id)
    await session.execute(query)
    await session.commit()
    return {"message": f"Record with id {id} was successfully deleted."}
