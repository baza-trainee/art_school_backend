from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response
from fastapi_pagination import Page, paginate
from sqlalchemy import select, update, delete, func, insert
from sqlalchemy.ext.asyncio import AsyncSession
from cloudinary import uploader

from src.auth.models import User
from src.database import get_async_session
from src.auth.auth_config import CURRENT_SUPERUSER
from .models import Poster
from .schemas import PosterSchema, PosterCreateSchema, PosterUpdateSchema
from .exceptions import (
    POSTERS_EXISTS,
    NO_DATA_FOUND,
    SERVER_ERROR,
    NO_RECORD,
    NO_DATA_LIST_FOUND,
)


posters_router = APIRouter(prefix="/posters", tags=["Posters"])


@posters_router.get("", response_model=Page[PosterSchema])
async def get_posters_list(
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Poster).order_by(Poster.date)
    posters = await session.execute(query)
    all_posters = posters.scalars().all()
    if not all_posters:
        raise HTTPException(status_code=404, detail=NO_DATA_LIST_FOUND)
    return paginate(all_posters)


@posters_router.get("/{id}", response_model=PosterSchema)
async def get_posters_list(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Poster).where(Poster.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


@posters_router.post("", response_model=PosterSchema)
async def create_posters(
    poster_data: PosterCreateSchema = Depends(PosterCreateSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(Poster).where(func.lower(Poster.title) == poster_data.title.lower())
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=POSTERS_EXISTS % poster_data.title,
        )

    photo = poster_data.photo
    folder_path = f"static/{Poster.__name__}"
    # os.makedirs(folder_path, exist_ok=True)
    # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
    # async with aiofiles.open(file_path, "wb") as buffer:
    #     await buffer.write(await photo.read())
    # update_data["photo"] = file_path
    try:
        upload_result = uploader.upload(photo.file, folder=folder_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="cloudinary error")

    poster_data.photo = upload_result["url"]
    try:
        query = insert(Poster).values(**poster_data.model_dump()).returning(Poster)
        result = await session.execute(query)
        poster_data = result.scalars().first()
        await session.commit()
        return poster_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@posters_router.patch("/{poster_id}", response_model=PosterSchema)
async def partial_update_posters(
    poster_id: int,
    photo: Annotated[UploadFile, File()] = None,
    posters_data: PosterUpdateSchema = Depends(PosterUpdateSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(Poster).where(Poster.id == poster_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    update_data = posters_data.model_dump(exclude_none=True)
    if photo:
        folder_path = f"static/{Poster.__name__}"
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
            update(Poster)
            .where(Poster.id == poster_id)
            .values(**update_data)
            .returning(Poster)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@posters_router.delete("/{poster_id}")
async def delete_posters(
    poster_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(Poster).where(Poster.id == poster_id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)

    try:
        query = delete(Poster).where(Poster.id == poster_id)
        await session.execute(query)
        await session.commit()
        return {"message": "Record with id `%s`was successfully deleted." % poster_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
