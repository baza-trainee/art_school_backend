from typing import Optional, Union
import fastapi_users
from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import fastapi_users
from src.database import get_async_session
from .models import Achievement
from .utils import (
    delete_achievement_by_id,
    get_all_achievements_by_filter,
    create_photo,
    get_media_by_id,
    update_photo,
)
from .schemas import (
    GetAchievementSchema,
    CreateAchievementSchema,
    DeleteResponseSchema,
    PositionEnum,
    GallerySubDepartmentEnum,
)

achievements_router = APIRouter(prefix="/achievements", tags=["Achievements"])

CURRENT_SUPERUSER = fastapi_users.current_user(
    active=True, verified=True, superuser=True
)

GET_ACHIEVEMENT_RESPONSE = GetAchievementSchema
POST_ACHIEVEMENT_BODY = CreateAchievementSchema
DELETE_RESPONSE = DeleteResponseSchema


@achievements_router.get("", response_model=Page[GET_ACHIEVEMENT_RESPONSE])
async def get_all_achievements(
    is_pinned: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_achievements_by_filter(Achievement, session, is_pinned)
    disable_installed_extensions_check()
    return paginate(result)


@achievements_router.get("/{id}", response_model=GET_ACHIEVEMENT_RESPONSE)
async def get_achievement(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_media_by_id(Achievement, session, id)


@achievements_router.post("", response_model=GET_ACHIEVEMENT_RESPONSE)
async def post_achievement(
    sub_department: GallerySubDepartmentEnum = None,
    pinned_position: PositionEnum = None,
    gallery: POST_ACHIEVEMENT_BODY = Depends(POST_ACHIEVEMENT_BODY),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_photo(
        pinned_position, sub_department, gallery, Achievement, session
    )


@achievements_router.patch("/{id}", response_model=GET_ACHIEVEMENT_RESPONSE)
async def patch_achievement(
    id: int,
    sub_department: GallerySubDepartmentEnum = None,
    pinned_position: PositionEnum = None,
    description: str = None,
    media: UploadFile = None,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_photo(
        id, pinned_position, sub_department, description, media, Achievement, session
    )


@achievements_router.delete("/{id}", response_model=DELETE_RESPONSE)
async def delete_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await delete_achievement_by_id(id, Achievement, session)
