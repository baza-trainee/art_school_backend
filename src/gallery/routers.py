from typing import Union
import fastapi_users
from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page, paginate
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import fastapi_users
from src.database import get_async_session
from .models import Gallery
from .utils import (
    delete_media_by_id,
    get_all_media_by_type,
    create_photo,
    create_video,
    get_media_by_id,
    update_photo,
    update_video,
)
from src.departments.schemas import SubDepartmentEnum
from .schemas import (
    MediaSchema,
    PhotoCreateSchema,
    PositionEnum,
    VideoCreateSchema,
    DeleteResponseSchema,
)

gallery_router = APIRouter(prefix="/gallery", tags=["Gallery"])

CURRENT_SUPERUSER = fastapi_users.current_user(active=True, verified=True, superuser=True)

GALLERY_RESPONSE = MediaSchema
POST_PHOTO_BODY = PhotoCreateSchema
POST_VIDEO_BODY = VideoCreateSchema
DELETE_RESPONSE = DeleteResponseSchema


@gallery_router.get("", response_model=Page[GALLERY_RESPONSE], response_model_exclude_none=True)
async def get_all_media(
    is_video: bool = False,
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_media_by_type(Gallery, session, is_video)
    return paginate(result)


@gallery_router.get("/{id}", response_model=GALLERY_RESPONSE, response_model_exclude_none=True)
async def get_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_media_by_id(id, Gallery, session)


@gallery_router.post("/photo")
async def post_photo(
    sub_department: SubDepartmentEnum = None,
    pinned_position: PositionEnum = None,
    gallery: POST_PHOTO_BODY = Depends(POST_PHOTO_BODY),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_photo(sub_department, pinned_position, gallery, Gallery, session)


@gallery_router.post("/video", response_model=GALLERY_RESPONSE)
async def post_photo(
    gallery: POST_VIDEO_BODY = Depends(POST_VIDEO_BODY),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_video(gallery, Gallery, session)


@gallery_router.patch("/photo/{id}", response_model=GALLERY_RESPONSE)
async def patch_photo(
    id: int,
    pinned_position: PositionEnum = None,
    media: UploadFile = None,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_photo(id, pinned_position, media, Gallery, session)


@gallery_router.patch("/video/{id}", response_model=GALLERY_RESPONSE)
async def patch_video(
    id: int,
    media: AnyHttpUrl = None,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_video(id, media, Gallery, session)


@gallery_router.delete("/{id}", response_model=DELETE_RESPONSE)
async def delete_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await delete_media_by_id(id, Gallery, session)
