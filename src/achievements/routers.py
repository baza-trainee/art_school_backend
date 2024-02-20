from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .service import (
    delete_achievement_by_id,
    get_all_achievements_by_filter,
    get_positions_status,
    create_achievement,
    get_achievement_by_id,
    update_achievement,
)
from .schemas import (
    GetAchievementSchema,
    GetTakenPositionsSchema,
    CreateAchievementSchema,
    UpdateAchievementSchema,
    DeleteResponseSchema,
)


achievements_router = APIRouter(prefix="/achievements", tags=["Achievements"])


@achievements_router.get("", response_model=Page[GetAchievementSchema])
async def get_all_achievements(
    is_pinned: bool = None,
    reverse: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    record = await get_all_achievements_by_filter(
        is_pinned=is_pinned, reverse=reverse, session=session
    )
    disable_installed_extensions_check()
    return paginate(record)


@achievements_router.get("/positions", response_model=GetTakenPositionsSchema)
async def get_positions(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_positions_status(session=session)


@achievements_router.get("/{id}", response_model=GetAchievementSchema)
async def get_achievement(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_achievement_by_id(id=id, session=session)


@achievements_router.post("", response_model=GetAchievementSchema)
async def post_achievement(
    background_tasks: BackgroundTasks,
    schema: CreateAchievementSchema = Depends(CreateAchievementSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_achievement(
        schema=schema, session=session, background_tasks=background_tasks
    )


@achievements_router.put("/{id}", response_model=GetAchievementSchema)
async def put_achievement(
    id: int,
    background_tasks: BackgroundTasks,
    schema: UpdateAchievementSchema = Depends(UpdateAchievementSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_achievement(
        id=id,
        schema=schema,
        session=session,
        background_tasks=background_tasks,
    )


@achievements_router.delete("/{id}", response_model=DeleteResponseSchema)
async def delete_achivement(
    id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await delete_achievement_by_id(
        id=id, background_tasks=background_tasks, session=session
    )
