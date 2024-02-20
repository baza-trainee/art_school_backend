from typing import Annotated, List

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.administrations.service import (
    create_administration,
    delete_administration,
    get_all_administration,
    get_one_administrator,
    update_administration,
)
from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .models import SchoolAdministration
from .schemas import (
    AdministratorSchema,
    AdministratorCreateSchema,
    AdministratorUpdateSchema,
    DeleteResponseSchema,
)


school_admin_router = APIRouter(
    prefix="/school_administration", tags=["School Administration"]
)


@school_admin_router.get("", response_model=List[AdministratorSchema])
async def get_all_school_administration(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_all_administration(SchoolAdministration, session)


@school_admin_router.post("", response_model=AdministratorSchema)
async def create_school_administration(
    background_tasks: BackgroundTasks,
    person: AdministratorCreateSchema = Depends(AdministratorCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_administration(
        person, SchoolAdministration, session, background_tasks
    )


@school_admin_router.get("/{id}", response_model=AdministratorSchema)
async def get_school_administration(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_one_administrator(id, SchoolAdministration, session)


@school_admin_router.patch("/{id}", response_model=AdministratorSchema)
async def update_school_administration(
    id: int,
    background_tasks: BackgroundTasks,
    photo: Annotated[UploadFile, File()] = None,
    person: AdministratorUpdateSchema = Depends(AdministratorUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_administration(
        id, person, photo, SchoolAdministration, session, background_tasks
    )


@school_admin_router.delete("/{id}", response_model=DeleteResponseSchema)
async def delete_school_administration(
    id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await delete_administration(
        id, SchoolAdministration, session, background_tasks
    )
