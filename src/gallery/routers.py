from typing import Union
import fastapi_users
from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
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
from .schemas import (
    GetPhotoSchema,
    GetVideoSchema,
    CreatePhotoSchema,
    CreateVideoSchema,
    DeleteResponseSchema,
    PositionEnum,
    GallerySubDepartmentEnum,
)

gallery_router = APIRouter(prefix="/gallery", tags=["Gallery"])

CURRENT_SUPERUSER = fastapi_users.current_user(
    active=True, verified=True, superuser=True
)

GET_PHOTO_RESPONSE = GetPhotoSchema
GET_VIDEO_RESPONSE = GetVideoSchema
POST_PHOTO_BODY = CreatePhotoSchema
POST_VIDEO_BODY = CreateVideoSchema
DELETE_RESPONSE = DeleteResponseSchema


@gallery_router.get("/photo", response_model=Page[GET_PHOTO_RESPONSE])
async def get_all_photo(
    is_pinned: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    is_video = False
    result = await get_all_media_by_type(Gallery, session, is_video, is_pinned)
    disable_installed_extensions_check()
    return paginate(result)


@gallery_router.get("/video", response_model=Page[GET_VIDEO_RESPONSE])
async def get_all_video(
    session: AsyncSession = Depends(get_async_session),
):
    is_video = True
    result = await get_all_media_by_type(Gallery, session, is_video)
    disable_installed_extensions_check()
    return paginate(result)


@gallery_router.get("/photo/{id}", response_model=GET_PHOTO_RESPONSE)
async def get_photo(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    is_video = False
    return await get_media_by_id(Gallery, session, id, is_video)


@gallery_router.get("/video/{id}", response_model=GET_VIDEO_RESPONSE)
async def get_video(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    is_video = True
    return await get_media_by_id(Gallery, session, id, is_video)


@gallery_router.post("/photo", response_model=GET_PHOTO_RESPONSE)
async def post_photo(
    pinned_position: PositionEnum = Form(default=None),
    sub_department: GallerySubDepartmentEnum = Form(default=None),
    gallery: POST_PHOTO_BODY = Depends(POST_PHOTO_BODY.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_photo(
        pinned_position, sub_department, gallery, Gallery, session
    )


@gallery_router.post("/video", response_model=GET_VIDEO_RESPONSE)
async def post_video(
    gallery: POST_VIDEO_BODY = Depends(POST_VIDEO_BODY.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_video(gallery, Gallery, session)


@gallery_router.patch("/photo/{id}", response_model=GET_PHOTO_RESPONSE)
async def patch_photo(
    id: int,
    pinned_position: PositionEnum = Form(default=None),
    sub_department: GallerySubDepartmentEnum = Form(default=None),
    description: str = Form(default=None),
    media: UploadFile = Form(default=None),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_photo(
        id, pinned_position, sub_department, description, media, Gallery, session
    )


@gallery_router.patch("/video/{id}", response_model=GET_VIDEO_RESPONSE)
async def patch_video(
    id: int,
    media: AnyHttpUrl = Form(),
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
