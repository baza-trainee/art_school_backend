from dataclasses import Field
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Path, Query, UploadFile
import fastapi_users
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate

from src.auth.models import User
from src.auth.auth_config import fastapi_users

from src.database import get_async_session
from .utils import (
    delete_media_by_id,
    get_all_media_by_type,
    create_photo,
    create_video,
    get_media_by_id,
    update_photo,
    update_video,
    # update_video,
    # update_media,
)
from .models import (
    Gallery,
)
from .schemas import (
    MediaSchema,
    PhotoCreateSchema,
    PositionEnum,
    VideoCreateSchema,
    DeleteResponseSchema,
)

gallery_router = APIRouter(prefix="/gallery", tags=["Gallery"])

CURRENT_SUPERUSER = fastapi_users.current_user(
    active=True, verified=True, superuser=True
)

GALLERY_RESPONSE = MediaSchema
POST_PHOTO_BODY = PhotoCreateSchema
POST_VIDEO_BODY = VideoCreateSchema
DELETE_RESPONSE = DeleteResponseSchema


@gallery_router.get("", response_model=Page[GALLERY_RESPONSE])
async def get_all_media(
    is_video: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_media_by_type(Gallery, session, bool(is_video))
    return paginate(result)


@gallery_router.get("/{id}", response_model=GALLERY_RESPONSE)
async def get_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_media_by_id(id, Gallery, session)


@gallery_router.post("/photo", response_model=GALLERY_RESPONSE)
async def post_photo(
    gallery: POST_PHOTO_BODY = Depends(POST_PHOTO_BODY),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_photo(gallery, Gallery, session)


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


# class VocalChoirDepartmentRoutes:
#     @vocal_choir_router.get("", response_model=List[DEPARTMENT_RESPONSE])
#     async def get_all_vocal_choir_departments(
#         session: AsyncSession = Depends(get_async_session),
#     ):
#         return await get_all_departments(VocalChoirDepartment, session)

#     @vocal_choir_router.post("", response_model=DEPARTMENT_RESPONSE)
#     async def create_vocal_choir_department(
#         vocal_choir_department: POST_BODY = Depends(POST_BODY),
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await create_department(
#             vocal_choir_department, VocalChoirDepartment, session
#         )

#     @vocal_choir_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
#     async def get_vocal_choir_department(
#         id: int, session: AsyncSession = Depends(get_async_session)
#     ):
#         return await get_department(id, VocalChoirDepartment, session)

#     @vocal_choir_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
#     async def update_vocal_choir_department(
#         id: int,
#         photo: Annotated[UploadFile, File()] = None,
#         department_data: UPDATE_BODY = Depends(UPDATE_BODY),
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await update_department(
#             id, department_data, photo, VocalChoirDepartment, session
#         )

#     @vocal_choir_router.delete("/{id}", response_model=DELETE_RESPONSE)
#     async def delete_vocal_choir_department(
#         id: int,
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await delete_department(id, VocalChoirDepartment, session)


# class ChoreographicDepartmentRoutes:
#     @choreographic_router.get("", response_model=List[DEPARTMENT_RESPONSE])
#     async def get_all_choreographic_departments(
#         session: AsyncSession = Depends(get_async_session),
#     ):
#         return await get_all_departments(ChoreographicDepartment, session)

#     @choreographic_router.post("", response_model=DEPARTMENT_RESPONSE)
#     async def create_choreographic_department(
#         vocal_choir_department: POST_BODY = Depends(POST_BODY),
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await create_department(
#             vocal_choir_department, ChoreographicDepartment, session
#         )

#     @choreographic_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
#     async def get_choreographic_department(
#         id: int, session: AsyncSession = Depends(get_async_session)
#     ):
#         return await get_department(id, ChoreographicDepartment, session)

#     @choreographic_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
#     async def update_choreographic_department(
#         id: int,
#         photo: Annotated[UploadFile, File()] = None,
#         department_data: UPDATE_BODY = Depends(UPDATE_BODY),
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await update_department(
#             id, department_data, photo, ChoreographicDepartment, session
#         )

#     @choreographic_router.delete("/{id}", response_model=DELETE_RESPONSE)
#     async def delete_choreographic_department(
#         id: int,
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await delete_department(id, ChoreographicDepartment, session)


# class FineArtsDepartmentRoutes:
#     @fine_arts_router.get("", response_model=List[DEPARTMENT_RESPONSE])
#     async def get_all_fine_arts_departments(
#         session: AsyncSession = Depends(get_async_session),
#     ):
#         return await get_all_departments(FineArtsDepartment, session)

#     @fine_arts_router.post("", response_model=DEPARTMENT_RESPONSE)
#     async def create_fine_arts_department(
#         vocal_choir_department: POST_BODY = Depends(POST_BODY),
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await create_department(
#             vocal_choir_department, FineArtsDepartment, session
#         )

#     @fine_arts_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
#     async def get_fine_arts_department(
#         id: int, session: AsyncSession = Depends(get_async_session)
#     ):
#         return await get_department(id, FineArtsDepartment, session)

#     @fine_arts_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
#     async def update_fine_arts_department(
#         id: int,
#         photo: Annotated[UploadFile, File()] = None,
#         department_data: UPDATE_BODY = Depends(UPDATE_BODY),
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await update_department(
#             id, department_data, photo, FineArtsDepartment, session
#         )

#     @fine_arts_router.delete("/{id}", response_model=DELETE_RESPONSE)
#     async def delete_fine_arts_department(
#         id: int,
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await delete_department(id, FineArtsDepartment, session)


# class TheatricalDepartmentRoutes:
#     @theatrical_router.get("", response_model=List[DEPARTMENT_RESPONSE])
#     async def get_all_theatrical_department(
#         session: AsyncSession = Depends(get_async_session),
#     ):
#         return await get_all_departments(TheatricalDepartment, session)

#     @theatrical_router.post("", response_model=DEPARTMENT_RESPONSE)
#     async def create_theatrical_department(
#         vocal_choir_department: POST_BODY = Depends(POST_BODY),
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await create_department(
#             vocal_choir_department, TheatricalDepartment, session
#         )

#     @theatrical_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
#     async def get_theatrical_department(
#         id: int, session: AsyncSession = Depends(get_async_session)
#     ):
#         return await get_department(id, TheatricalDepartment, session)

#     @theatrical_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
#     async def update_theatrical_department(
#         id: int,
#         photo: Annotated[UploadFile, File()] = None,
#         department_data: UPDATE_BODY = Depends(UPDATE_BODY),
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await update_department(
#             id, department_data, photo, TheatricalDepartment, session
#         )

#     @theatrical_router.delete("/{id}", response_model=DELETE_RESPONSE)
#     async def delete_theatrical_department(
#         id: int,
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(CURRENT_SUPERUSER),
#     ):
#         return await delete_department(id, TheatricalDepartment, session)
