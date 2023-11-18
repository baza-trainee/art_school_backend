import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from .models import News
from .schemas import NewsSchema, NewsCreateSchema
from sqlalchemy import select, update, delete, func, insert
from typing import Annotated, List
import aiofiles
from cloudinary import uploader


news_router = APIRouter(prefix="/news", tags=["news"])


@news_router.get("", response_model=List[NewsSchema])
async def get_news_list(
    session: AsyncSession = Depends(get_async_session),
) -> NewsSchema:
    try:
        query = select(News)
        news = await session.execute(query)
        all_news = news.scalars().all()
        if not all_news:
            raise HTTPException(status_code=404, detail="No news found")
        return all_news
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")


@news_router.post("", response_model=NewsCreateSchema)
async def create_news(
    news_data: NewsCreateSchema, 
    session: AsyncSession = Depends(get_async_session),
):
    query = select(News).where(
        func.lower(News.title) == news_data.title.lower()
    )
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail="News with name: `%s` already exists."% news_data.title,
        )
        
    photo = news_data.photo
    folder_path = f"static/{News.__name__}"
    # os.makedirs(folder_path, exist_ok=True)
    # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
    # async with aiofiles.open(file_path, "wb") as buffer:
    #     await buffer.write(await photo.read())
    # news_data.photo = file_path
    upload_result = uploader.upload(photo.file, folder=folder_path)
    department.photo = upload_result["url"]
    query = insert(model).values(**department.model_dump()).returning(model)
    result = await session.execute(query)
    department = result.scalars().first()
    
    query = insert(News).values(**news_data.model_dump()).returning(News)
    result = await session.execute(query)
    news_data = result.scalars().first()
    await session.commit()
    return news_data
    # try:
    #     new_news = News(**news_data.model_dump())
    #     print(new_news)
    #     session.add(new_news)
    #     await session.commit()
    #     return new_news
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Server error")


@news_router.patch("/{news_id}", response_model=NewsSchema)
async def partial_update_news(
    news_id: int,
    news_data: NewsSchema,
    session: AsyncSession = Depends(get_async_session),
) -> NewsSchema:
    try:
        query = (
            update(News)
            .where(News.id == news_id)
            .values(**news_data.dict(exclude_unset=True))
        )
        await session.execute(query)
        await session.commit()
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")


@news_router.delete("/{news_id}", response_model=dict)
async def delete_news(
    news_id: int, session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        query = delete(News).where(News.id == news_id)
        await session.execute(query)
        await session.commit()
        return {"message": "News deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")
