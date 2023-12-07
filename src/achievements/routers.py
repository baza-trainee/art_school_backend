from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session

# from src.database.redis import invalidate_cache
from .models import Achievement
from .service import (
    delete_achievement_by_id,
    get_all_achievements_by_filter,
    create_achievement,
    get_achievement_by_id,
    update_achievement,
)
from .schemas import (
    GetAchievementSchema,
    CreateAchievementSchema,
    UpdateAchievementSchema,
    DeleteResponseSchema,
)


achievements_router = APIRouter(prefix="/achievements", tags=["Achievements"])


@achievements_router.get("", response_model=Page[GetAchievementSchema])
async def get_all_achievements(
    is_pinned: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_achievements_by_filter(is_pinned=is_pinned, session=session)
    disable_installed_extensions_check()
    return paginate(result)


@achievements_router.get("/{id}", response_model=GetAchievementSchema)
async def get_achievement(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_achievement_by_id(id=id, session=session)


@achievements_router.post("", response_model=GetAchievementSchema)
async def post_achievement(
    schema: CreateAchievementSchema = Depends(CreateAchievementSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # if sub_department:
    #     await invalidate_cache("get_achievement_for_sub_department", sub_department)
    return await create_achievement(schema=schema, session=session)


@achievements_router.put("/{id}", response_model=GetAchievementSchema)
async def patch_achievement(
    id: int,
    media: UploadFile = None,
    schema: UpdateAchievementSchema = Depends(UpdateAchievementSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    result: Achievement = await update_achievement(
        id=id, media=media, schema=schema, session=session
    )
    # if x := result.sub_department:
    #     await invalidate_cache("get_achievement_for_sub_department", x)
    return result


@achievements_router.delete("/{id}", response_model=DeleteResponseSchema)
async def delete_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # media: Achievement = await get_media_by_id(Achievement, session, id)
    # await session.commit()
    # await invalidate_cache("get_achievement_for_sub_department", media.sub_department)
    return await delete_achievement_by_id(id, session)
