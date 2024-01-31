from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

# from fastapi_cache.decorator import cache

# from src.config import HALF_DAY
# from src.database.redis import invalidate_cache, my_key_builder
from src.auth.models import User
from src.database.database import get_async_session
from src.auth.auth_config import CURRENT_SUPERUSER
from .models import News
from .schemas import NewsSchema, NewsCreateSchema, NewsUpdateSchema
from .service import (
    get_news_order_by_list,
    get_news_by_id,
    create_news,
    update_news,
    delete_news_by_id,
)


news_router = APIRouter(prefix="/news", tags=["News"])


@news_router.get("", response_model=Page[NewsSchema])
# @cache(expire=HALF_DAY, key_builder=my_key_builder)
async def get_news_list(
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_news_order_by_list(News, session)
    disable_installed_extensions_check()
    return paginate(result)


@news_router.get("/{id}", response_model=NewsSchema)
# @cache(expire=HALF_DAY, key_builder=my_key_builder)
async def get_news(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_news_by_id(News, session, id)


@news_router.post("")
async def post_news(
    background_tasks: BackgroundTasks,
    news_data: NewsCreateSchema = Depends(NewsCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_news_list")
    return await create_news(news_data, News, session, background_tasks)


@news_router.patch("/{news_id}", response_model=NewsSchema)
async def partial_update_news(
    news_id: int,
    background_tasks: BackgroundTasks,
    photo: Annotated[UploadFile, File()] = None,
    news_data: NewsUpdateSchema = Depends(NewsUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_news", news_id)
    # await invalidate_cache("get_news_list")
    return await update_news(news_data, News, session, background_tasks, photo, news_id)


@news_router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_news_list")
    # await invalidate_cache("get_news", news_id)
    return await delete_news_by_id(news_id, News, session, background_tasks)
