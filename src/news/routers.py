from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from sqlalchemy import select, update, delete, func, insert
from cloudinary import uploader

from src.auth.models import User
from src.database import get_async_session
from src.auth.auth_config import CURRENT_SUPERUSER
from .models import News
from .schemas import NewsSchema, NewsCreateSchema, NewsUpdateSchema
from .exceptions import (
    NEWS_EXISTS,
    NO_DATA_FOUND,
    SERVER_ERROR,
    NO_RECORD,
    SUCCESS_DELETE,
)


news_router = APIRouter(prefix="/news", tags=["News"])


@news_router.get("", response_model=Page[NewsSchema])
async def get_news_list(
    session: AsyncSession = Depends(get_async_session),
):
    query = select(News).order_by(News.created_at)
    news = await session.execute(query)
    all_news = news.scalars().all()
    if not all_news:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return paginate(all_news)


@news_router.get("/{id}", response_model=NewsSchema)
async def get_news_list(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(News).where(News.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


@news_router.post("", response_model=NewsSchema)
async def create_news(
    news_data: NewsCreateSchema = Depends(NewsCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(News).where(func.lower(News.title) == news_data.title.lower())
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=NEWS_EXISTS % news_data.title,
        )

    photo = news_data.photo
    folder_path = f"static/{News.__name__}"
    # os.makedirs(folder_path, exist_ok=True)
    # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
    # async with aiofiles.open(file_path, "wb") as buffer:
    #     await buffer.write(await photo.read())
    # update_data["photo"] = file_path
    try:
        upload_result = uploader.upload(photo.file, folder=folder_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="cloudinary error")

    news_data.photo = upload_result["url"]
    try:
        query = insert(News).values(**news_data.model_dump()).returning(News)
        result = await session.execute(query)
        news_data = result.scalars().first()
        await session.commit()
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@news_router.patch("/{news_id}", response_model=NewsSchema)
async def partial_update_news(
    news_id: int,
    photo: Annotated[UploadFile, File()] = None,
    news_data: NewsUpdateSchema = Depends(NewsUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(News).where(News.id == news_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    update_data = news_data.model_dump(exclude_none=True)
    if photo:
        folder_path = f"static/{News.__name__}"
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
            update(News).where(News.id == news_id).values(**update_data).returning(News)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@news_router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(News).where(News.id == news_id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)

    try:
        query = delete(News).where(News.id == news_id)
        await session.execute(query)
        await session.commit()
        return {"message": SUCCESS_DELETE % news_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
