from typing import Union
import fastapi_users
from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page, paginate
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import fastapi_users
from src.database import get_async_session
from .models import Achievement
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
    GetPhotoSchema,
    CreatePhotoSchema,
    DeleteResponseSchema,
    PositionEnum,
)

gallery_router = APIRouter(prefix="/achievements", tags=["Achievements"])

CURRENT_SUPERUSER = fastapi_users.current_user(active=True, verified=True, superuser=True)

GET_PHOTO_RESPONSE = GetPhotoSchema
POST_PHOTO_BODY = CreatePhotoSchema
DELETE_RESPONSE = DeleteResponseSchema


@gallery_router.get("/photo", response_model=Page[GET_PHOTO_RESPONSE])
async def get_all_photo(
    session: AsyncSession = Depends(get_async_session),
):
    is_video = False
    result = await get_all_achievements(Achievement, session, is_video)
    return paginate(result)


@gallery_router.get("/photo/{id}", response_model=GET_PHOTO_RESPONSE)
async def get_photo(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    is_video = False
    return await get_media_by_id(Achievement, session, id, is_video)


@gallery_router.post("/photo", response_model=GET_PHOTO_RESPONSE)
async def post_photo(
    gallery: POST_PHOTO_BODY = Depends(POST_PHOTO_BODY),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_photo(gallery, Achievement, session)


@gallery_router.patch("/photo/{id}", response_model=GET_PHOTO_RESPONSE)
async def patch_photo(
    id: int,
    sub_department: SubDepartmentEnum = None,
    pinned_position: PositionEnum = None,
    description: str = None,
    media: UploadFile = None,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_photo(id, pinned_position, sub_department, description, media, Achievement, session)


@gallery_router.delete("/{id}", response_model=DELETE_RESPONSE)
async def delete_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await delete_media_by_id(id, Achievement, session)
