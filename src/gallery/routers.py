from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .models import Gallery
from .service import (
    delete_media_by_id,
    get_all_media_by_filter,
    create_photo,
    create_video,
    get_photo_by_id,
    get_positions_status,
    get_video_by_id,
    update_photo,
    update_video,
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

# from src.database.redis import invalidate_cache

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
    reverse: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    record = await get_all_media_by_filter(
        is_pinned=False, reverse=reverse, is_video=True, session=session
    )
    disable_installed_extensions_check()
    return paginate(record)


@gallery_router.get("/photo/{id}", response_model=GetPhotoSchema)
async def get_photo(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_photo_by_id(id=id, session=session)


@gallery_router.get("/positions", response_model=GetTakenPositionsSchema)
async def get_positions(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_positions_status(session=session)


@gallery_router.get("/video/{id}", response_model=GetVideoSchema)
async def get_video(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_video_by_id(id=id, session=session)


@gallery_router.post("/photo", response_model=GetPhotoSchema)
async def post_photo(
    schema: CreatePhotoSchema = Depends(CreatePhotoSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    record = await create_photo(schema=schema, session=session)
    # if record.sub_department:
    #    await invalidate_cache("get_gallery_for_sub_department", record.sub_department)

    return record


@gallery_router.post("/video", response_model=GetVideoSchema)
async def post_video(
    schema: CreateVideoSchema = Depends(CreateVideoSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_video(schema=schema, session=session)


@gallery_router.put("/photo/{id}", response_model=GetPhotoSchema)
async def put_photo(
    id: int,
    media: UploadFile = None,
    schema: UpdatePhotoSchema = Depends(UpdatePhotoSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    record: Gallery = await update_photo(
        id=id, media=media, schema=schema, session=session
    )
    # if record.sub_department:
    #     await invalidate_cache("get_achievement_for_sub_department", record.sub_department)
    return record


@gallery_router.put("/video/{id}", response_model=GetVideoSchema)
async def put_video(
    id: int,
    schema: CreateVideoSchema = Depends(CreateVideoSchema),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_video(id=id, schema=schema, session=session)


@gallery_router.delete("/{id}", response_model=DeleteResponseSchema)
async def delete_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # record: Gallery = await session.get(Gallery, id)
    # if record.sub_department:
    #     await invalidate_cache("get_achievement_for_sub_department", record.sub_department)
    return await delete_media_by_id(id=id, session=session)
