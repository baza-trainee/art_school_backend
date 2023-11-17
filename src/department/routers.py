from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .utils import get_department
from .models import (
    MusicDepartment,
    VocalChoirDepartment,
    ChoreographicDepartment,
    FineArtsDepartment,
    TheatricalDepartment,
)
from .schemas import (
    MusicDepartmentSchema,
    VocalChoirDepartmentSchema,
    ChoreographicDepartmentSchema,
    FineArtsDepartmentSchema,
    TheatricalDepartmentSchema,
)


router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/music_department/{id}", response_model=MusicDepartmentSchema)
async def get_music_department(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_department(id, MusicDepartment, session)


@router.get("/vocal_choir_department/{id}", response_model=VocalChoirDepartmentSchema)
async def get_vocal_choir_department(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_department(id, VocalChoirDepartment, session)


@router.get(
    "/choreographic_department/{id}", response_model=ChoreographicDepartmentSchema
)
async def get_choreographic_department(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_department(id, ChoreographicDepartment, session)


@router.get("/fine_arts_department/{id}", response_model=FineArtsDepartmentSchema)
async def get_fine_arts_department(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_department(id, FineArtsDepartment, session)


@router.get("/theatrical_department/{id}", response_model=TheatricalDepartmentSchema)
async def get_theatrical_department(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_department(id, TheatricalDepartment, session)
