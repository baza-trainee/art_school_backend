from typing import Annotated, List

from fastapi import APIRouter, Depends, File, UploadFile
import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.auth_config import fastapi_users

from src.database import get_async_session
from .utils import (
    create_department,
    delete_department,
    get_all_departments,
    get_department,
    update_department,
)
from .models import (
    MusicDepartment,
    VocalChoirDepartment,
    ChoreographicDepartment,
    FineArtsDepartment,
    TheatricalDepartment,
)
from .schemas import (
    DeleteResponseSchema,
    DepartmentBaseSchema,
    DepartmentCreateSchema,
    DepartmentUpdateSchema,
)


music_router = APIRouter(
    prefix="/departments/music_department", tags=["Music Department"]
)
vocal_choir_router = APIRouter(
    prefix="/departments/vocal_choir_department", tags=["Vocal Choir Department"]
)
choreographic_router = APIRouter(
    prefix="/departments/choreographic_department", tags=["Choreographic Department"]
)
fine_arts_router = APIRouter(
    prefix="/departments/fine_arts_department", tags=["Fine Arts Department"]
)
theatrical_router = APIRouter(
    prefix="/departments/theatrical_department", tags=["Theatrical Department"]
)

CURRENT_SUPERUSER = fastapi_users.current_user(
    active=True, verified=True, superuser=True
)

DEPARTMENT_RESPONSE = DepartmentBaseSchema
POST_BODY = DepartmentCreateSchema
UPDATE_BODY = DepartmentUpdateSchema
DELETE_RESPONSE = DeleteResponseSchema


class MusicDepartmentRoutes:
    @music_router.get("", response_model=List[DEPARTMENT_RESPONSE])
    async def get_all_music_departments(
        session: AsyncSession = Depends(get_async_session),
    ):
        return await get_all_departments(MusicDepartment, session)

    @music_router.post("", response_model=DEPARTMENT_RESPONSE)
    async def create_music_department(
        music_department: POST_BODY = Depends(POST_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await create_department(music_department, MusicDepartment, session)

    @music_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def get_music_department(
        id: int, session: AsyncSession = Depends(get_async_session)
    ):
        return await get_department(id, MusicDepartment, session)

    @music_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def update_music_department(
        id: int,
        photo: Annotated[UploadFile, File()] = None,
        department_data: UPDATE_BODY = Depends(UPDATE_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await update_department(
            id, department_data, photo, MusicDepartment, session
        )

    @music_router.delete("/{id}", response_model=DELETE_RESPONSE)
    async def delete_music_department(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await delete_department(id, MusicDepartment, session)


class VocalChoirDepartmentRoutes:
    @vocal_choir_router.get("", response_model=List[DEPARTMENT_RESPONSE])
    async def get_all_vocal_choir_departments(
        session: AsyncSession = Depends(get_async_session),
    ):
        return await get_all_departments(VocalChoirDepartment, session)

    @vocal_choir_router.post("", response_model=DEPARTMENT_RESPONSE)
    async def create_vocal_choir_department(
        vocal_choir_department: POST_BODY = Depends(POST_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await create_department(
            vocal_choir_department, VocalChoirDepartment, session
        )

    @vocal_choir_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def get_vocal_choir_department(
        id: int, session: AsyncSession = Depends(get_async_session)
    ):
        return await get_department(id, VocalChoirDepartment, session)

    @vocal_choir_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def update_vocal_choir_department(
        id: int,
        photo: Annotated[UploadFile, File()] = None,
        department_data: UPDATE_BODY = Depends(UPDATE_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await update_department(
            id, department_data, photo, VocalChoirDepartment, session
        )

    @vocal_choir_router.delete("/{id}", response_model=DELETE_RESPONSE)
    async def delete_vocal_choir_department(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await delete_department(id, VocalChoirDepartment, session)


class ChoreographicDepartmentRoutes:
    @choreographic_router.get("", response_model=List[DEPARTMENT_RESPONSE])
    async def get_all_choreographic_departments(
        session: AsyncSession = Depends(get_async_session),
    ):
        return await get_all_departments(ChoreographicDepartment, session)

    @choreographic_router.post("", response_model=DEPARTMENT_RESPONSE)
    async def create_choreographic_department(
        vocal_choir_department: POST_BODY = Depends(POST_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await create_department(
            vocal_choir_department, ChoreographicDepartment, session
        )

    @choreographic_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def get_choreographic_department(
        id: int, session: AsyncSession = Depends(get_async_session)
    ):
        return await get_department(id, ChoreographicDepartment, session)

    @choreographic_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def update_choreographic_department(
        id: int,
        photo: Annotated[UploadFile, File()] = None,
        department_data: UPDATE_BODY = Depends(UPDATE_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await update_department(
            id, department_data, photo, ChoreographicDepartment, session
        )

    @choreographic_router.delete("/{id}", response_model=DELETE_RESPONSE)
    async def delete_choreographic_department(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await delete_department(id, ChoreographicDepartment, session)


class FineArtsDepartmentRoutes:
    @fine_arts_router.get("", response_model=List[DEPARTMENT_RESPONSE])
    async def get_all_fine_arts_departments(
        session: AsyncSession = Depends(get_async_session),
    ):
        return await get_all_departments(FineArtsDepartment, session)

    @fine_arts_router.post("", response_model=DEPARTMENT_RESPONSE)
    async def create_fine_arts_department(
        vocal_choir_department: POST_BODY = Depends(POST_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await create_department(
            vocal_choir_department, FineArtsDepartment, session
        )

    @fine_arts_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def get_fine_arts_department(
        id: int, session: AsyncSession = Depends(get_async_session)
    ):
        return await get_department(id, FineArtsDepartment, session)

    @fine_arts_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def update_fine_arts_department(
        id: int,
        photo: Annotated[UploadFile, File()] = None,
        department_data: UPDATE_BODY = Depends(UPDATE_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await update_department(
            id, department_data, photo, FineArtsDepartment, session
        )

    @fine_arts_router.delete("/{id}", response_model=DELETE_RESPONSE)
    async def delete_fine_arts_department(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await delete_department(id, FineArtsDepartment, session)


class TheatricalDepartmentRoutes:
    @theatrical_router.get("", response_model=List[DEPARTMENT_RESPONSE])
    async def get_all_theatrical_department(
        session: AsyncSession = Depends(get_async_session),
    ):
        return await get_all_departments(TheatricalDepartment, session)

    @theatrical_router.post("", response_model=DEPARTMENT_RESPONSE)
    async def create_theatrical_department(
        vocal_choir_department: POST_BODY = Depends(POST_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await create_department(
            vocal_choir_department, TheatricalDepartment, session
        )

    @theatrical_router.get("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def get_theatrical_department(
        id: int, session: AsyncSession = Depends(get_async_session)
    ):
        return await get_department(id, TheatricalDepartment, session)

    @theatrical_router.patch("/{id}", response_model=DEPARTMENT_RESPONSE)
    async def update_theatrical_department(
        id: int,
        photo: Annotated[UploadFile, File()] = None,
        department_data: UPDATE_BODY = Depends(UPDATE_BODY),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await update_department(
            id, department_data, photo, TheatricalDepartment, session
        )

    @theatrical_router.delete("/{id}", response_model=DELETE_RESPONSE)
    async def delete_theatrical_department(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(CURRENT_SUPERUSER),
    ):
        return await delete_department(id, TheatricalDepartment, session)
