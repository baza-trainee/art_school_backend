from fastapi import APIRouter, BackgroundTasks, Depends, Form
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .service import (
    delete_media_by_id,
    get_all_media_by_filter,
    create_media,
    get_media_by_id,
    get_positions_status,
    update_media_by_id,
)
from .schemas import (
    GetPhotoSchema,
    GetTakenPositionsSchema,
    GetVideoSchema,
    CreatePhotoSchema,
    CreateVideoSchema,
    UpdatePhotoSchema,
    DeleteResponseSchema,
)


gallery_router = APIRouter(prefix="/gallery", tags=["Gallery"])


@gallery_router.get("/photo", response_model=Page[GetPhotoSchema])
async def get_all_photo(
    is_pinned: bool = None,
    reverse: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    record = await get_all_media_by_filter(
        is_pinned=is_pinned, reverse=reverse, is_video=False, session=session
    )
    disable_installed_extensions_check()
    return paginate(record)


@gallery_router.get("/video", response_model=Page[GetVideoSchema])
async def get_all_video(
    is_pinned: bool = None,
    reverse: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    record = await get_all_media_by_filter(
        is_pinned=is_pinned, reverse=reverse, is_video=True, session=session
    )
    disable_installed_extensions_check()
    return paginate(record)


@gallery_router.get("/photo/{id}", response_model=GetPhotoSchema)
async def get_photo(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_media_by_id(id=id, session=session)


@gallery_router.get("/positions", response_model=GetTakenPositionsSchema)
async def get_positions(
    is_video: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_positions_status(session=session, is_video=is_video)


@gallery_router.get("/video/{id}", response_model=GetVideoSchema)
async def get_video(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_media_by_id(id=id, session=session, is_video=True)


@gallery_router.post("/photo", response_model=GetPhotoSchema)
async def post_photo(
    background_tasks: BackgroundTasks,
    schema: CreatePhotoSchema = Depends(CreatePhotoSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_media(
        schema=schema,
        session=session,
        background_tasks=background_tasks,
    )


@gallery_router.post("/video", response_model=GetVideoSchema)
async def post_video(
    schema: CreateVideoSchema = Depends(CreateVideoSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_media(
        schema=schema,
        session=session,
        is_video=True,
    )


@gallery_router.put("/photo/{id}", response_model=GetPhotoSchema)
async def put_photo(
    id: int,
    background_tasks: BackgroundTasks,
    schema: UpdatePhotoSchema = Depends(UpdatePhotoSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_media_by_id(
        id=id,
        schema=schema,
        session=session,
        background_tasks=background_tasks,
    )


@gallery_router.put("/video/{id}", response_model=GetVideoSchema)
async def put_video(
    id: int,
    schema: CreateVideoSchema = Depends(CreateVideoSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_media_by_id(
        id=id,
        schema=schema,
        session=session,
        is_video=True,
    )


@gallery_router.delete("/{id}", response_model=DeleteResponseSchema)
async def delete_media(
    id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await delete_media_by_id(
        id=id, background_tasks=background_tasks, session=session
    )
