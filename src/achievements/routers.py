from fastapi import APIRouter, Depends, UploadFile, Form
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database import get_async_session

# from src.redis import invalidate_cache
from .models import Achievement
from .service import (
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
)


achievements_router = APIRouter(prefix="/achievements", tags=["Achievements"])

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
    sub_department: int = Form(default=None),
    pinned_position: PositionEnum = Form(default=None),
    gallery: POST_ACHIEVEMENT_BODY = Depends(POST_ACHIEVEMENT_BODY.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # if sub_department:
    #     await invalidate_cache("get_achievement_for_sub_department", sub_department)
    return await create_photo(
        pinned_position, sub_department, gallery, Achievement, session
    )


@achievements_router.patch("/{id}", response_model=GET_ACHIEVEMENT_RESPONSE)
async def patch_achievement(
    id: int,
    sub_department: int = Form(default=None),
    pinned_position: PositionEnum = Form(default=None),
    description: str = Form(default=None, max_length=300),
    media: UploadFile = Form(default=None),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    result: Achievement = await update_photo(
        id, pinned_position, sub_department, description, media, Achievement, session
    )
    # if x := result.sub_department:
    #     await invalidate_cache("get_achievement_for_sub_department", x)
    return result


@achievements_router.delete("/{id}", response_model=DELETE_RESPONSE)
async def delete_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # media: Achievement = await get_media_by_id(Achievement, session, id)
    # await session.commit()
    # await invalidate_cache("get_achievement_for_sub_department", media.sub_department)
    return await delete_achievement_by_id(id, Achievement, session)
