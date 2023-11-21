from typing import Annotated, List

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from cloudinary import uploader
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database import get_async_session
from src.exceptions import (
    NO_DATA_FOUND,
    NO_RECORD,
    PERSON_EXISTS,
    SERVER_ERROR,
    SUCCESS_DELETE,
)
from .models import SchoolAdministration
from .schemas import (
    AdministratorSchema,
    AdministratorCreateSchema,
    AdministratorUpdateSchema,
    DeleteResponseSchema,
)


school_admin_router = APIRouter(
    prefix="/school_administration", tags=["School Administration"]
)


@school_admin_router.get("", response_model=List[AdministratorSchema])
async def get_all_school_administration(
    session: AsyncSession = Depends(get_async_session),
):
    query = select(SchoolAdministration)
    result = await session.execute(query)
    response = result.scalars().all()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


@school_admin_router.post("", response_model=AdministratorSchema)
async def create_school_administration(
    person: AdministratorCreateSchema = Depends(AdministratorCreateSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
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
    folder_path = "static/SchoolAdministration"
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


@school_admin_router.get("/{id}", response_model=AdministratorSchema)
async def get_school_administration(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(SchoolAdministration).where(SchoolAdministration.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    return response


@school_admin_router.patch("/{id}", response_model=AdministratorSchema)
async def update_school_administration(
    id: int,
    photo: Annotated[UploadFile, File()] = None,
    person: AdministratorUpdateSchema = Depends(AdministratorUpdateSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(SchoolAdministration).where(SchoolAdministration.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    update_data = person.model_dump(exclude_none=True)
    if photo:
        folder_path = "static/SchoolAdministration"
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
            update(SchoolAdministration)
            .where(SchoolAdministration.id == id)
            .values(**update_data)
            .returning(SchoolAdministration)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@school_admin_router.delete("/{id}", response_model=DeleteResponseSchema)
async def delete_school_administration(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(SchoolAdministration).where(SchoolAdministration.id == id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)
    query = delete(SchoolAdministration).where(SchoolAdministration.id == id)
    await session.execute(query)
    await session.commit()
    return {"message": SUCCESS_DELETE % id}
