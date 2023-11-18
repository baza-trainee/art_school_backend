from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from .models import News
from .schemas import NewsSchema
from sqlalchemy import select, update, delete


router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=NewsSchema)
async def get_news_list(
    session: AsyncSession = Depends(get_async_session),
) -> NewsSchema:
    try:
        query = select(News)
        news = await session.execute(query)
        all_news = news.scalars().all()
        print(all_news)
        if not all_news:
            raise HTTPException(status_code=404, detail="No news found")
        return all_news
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")


@router.post("", response_model=NewsSchema)
async def create_news(
    news_data: NewsSchema,
    session: AsyncSession = Depends(get_async_session)
) -> NewsSchema:
    try:
        new_news = News(**news_data.model_dump())
        print(new_news)
        session.add(new_news)
        await session.commit()
        return new_news
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")


@router.patch("/{news_id}", response_model=NewsSchema)
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


@router.delete("/{news_id}", response_model=dict)
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
