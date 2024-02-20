from typing import Any, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from src.auth.auth_config import CURRENT_SUPERUSER
from src.auth.models import User
from .service import (
    create_sub_dep,
    delete_sub_dep,
    get_dep,
    get_main_dep,
    get_media_for_sub_dep,
    get_one_sub_dep,
    get_sub_dep_list,
    update_sub_dep,
)
from src.database.database import get_async_session
from src.gallery.models import Gallery
from src.achievements.models import Achievement
from .exceptions import DELETE_ERROR
from .models import MainDepartment, SubDepartment
from .schemas import (
    DepartmentEnum,
    DepartmentSchema,
    SubDepartmentAchievementSchema,
    SubDepartmentCreateSchema,
    SubDepartmentGallerySchema,
    SubDepartmentSchema,
    SubDepartmentUpdateSchema,
    SubDepartmentVideoSchema,
)


departments = APIRouter(prefix="/departments", tags=["Departments"])


@departments.get("", response_model=List[DepartmentSchema])
async def get_all_departments(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_dep(MainDepartment, session)


@departments.get("/{id}", response_model=List[SubDepartmentSchema])
async def get_sub_departments_by_department_id(
    id: DepartmentEnum,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_sub_dep_list(id, SubDepartment, session)


@departments.post("/sub_department", response_model=SubDepartmentSchema)
async def create_sub_department(
    data: SubDepartmentCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_sub_dep(data, SubDepartment, session)


@departments.get("/sub_department/{id}", response_model=SubDepartmentSchema)
async def get_sub_department_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_one_sub_dep(id, SubDepartment, session)


@departments.get(
    "/sub_department_gallery/{id}",
    response_model=Page[SubDepartmentGallerySchema],
)
async def get_gallery_for_sub_department(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    disable_installed_extensions_check()
    result = await get_media_for_sub_dep(id, Gallery, session, "photo")
    return paginate(result)


@departments.get(
    "/sub_department_achievement/{id}",
    response_model=Page[SubDepartmentAchievementSchema],
)
async def get_achievement_for_sub_department(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    disable_installed_extensions_check()
    result = await get_media_for_sub_dep(id, Achievement, session, "achievement")
    return paginate(result)


@departments.get(
    "/sub_department_video/{id}", response_model=Page[SubDepartmentVideoSchema]
)
async def get_video_for_sub_department(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    disable_installed_extensions_check()
    result = await get_media_for_sub_dep(id, Gallery, session, "video")
    return paginate(result)


@departments.patch("/sub_department/{id}", response_model=SubDepartmentSchema)
async def update_sub_department_by_id(
    id: int,
    department_data: SubDepartmentUpdateSchema = Body(None),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_sub_dep(id, department_data, SubDepartment, session)


@departments.delete("/sub_department/{id}")
async def delete_sub_department_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
) -> dict:
    sub_dep: SubDepartment = await get_one_sub_dep(id, SubDepartment, session)
    main_dep: MainDepartment = await get_main_dep(
        sub_dep.main_department_id, MainDepartment, session
    )
    if len(main_dep.sub_departments) <= 1:
        raise HTTPException(status_code=400, detail=DELETE_ERROR)
    await session.commit()
    return await delete_sub_dep(id, SubDepartment, session)
