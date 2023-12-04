from typing import Any, List, Union

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from fastapi_cache.decorator import cache

# from src.config import HOUR, MONTH
from src.departments.service import (
    create_sub_dep,
    delete_sub_dep,
    get_achievement_list,
    get_dep,
    get_galery_list,
    get_one_sub_dep,
    get_sub_dep_list,
    update_sub_dep,
)
from src.database import get_async_session
from src.gallery.models import Gallery
from src.achievements.models import Achievement

# from src.redis import invalidate_cache, my_key_builder
from .models import MainDepartment, SubDepartment
from .schemas import (
    DepartmentEnum,
    DepartmentSchema,
    SubDepartmentAchievementSchema,
    SubDepartmentCreateSchema,
    SubDepartmentGallerySchema,
    SubDepartmentSchema,
    SubDepartmentUpdateSchema,
)


departments = APIRouter(prefix="/departments", tags=["Departments"])


@departments.get("", response_model=List[DepartmentSchema])
# @cache(expire=MONTH, key_builder=my_key_builder)
async def get_all_departments(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_dep(MainDepartment, session)


@departments.get("/{id}", response_model=List[SubDepartmentSchema])
# @cache(expire=HOUR, key_builder=my_key_builder)
async def get_sub_departments_by_department_id(
    id: DepartmentEnum,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_sub_dep_list(id, SubDepartment, session)


@departments.post("/sub_department", response_model=SubDepartmentSchema)
async def create_sub_department(
    data: SubDepartmentCreateSchema,
    session: AsyncSession = Depends(get_async_session),
):
    # await invalidate_cache(
    #     "get_sub_departments_by_department_id", data.main_department_id
    # )
    return await create_sub_dep(data, SubDepartment, session)


@departments.get("/sub_department/{id}", response_model=SubDepartmentSchema)
async def get_sub_department_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_one_sub_dep(id, SubDepartment, session)


@departments.get(
    "/sub_department_gallery/{id}",
    response_model=Union[List[SubDepartmentGallerySchema], Any],
)
# @cache(expire=HOUR, key_builder=my_key_builder)
async def get_gallery_for_sub_department(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_galery_list(id, Gallery, session)


@departments.get(
    "/sub_department_achievement/{id}",
    response_model=Union[List[SubDepartmentAchievementSchema], Any],
)
# @cache(expire=HOUR, key_builder=my_key_builder)
async def get_achievement_for_sub_department(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_achievement_list(id, Achievement, session)


@departments.patch("/sub_department/{id}", response_model=SubDepartmentSchema)
async def update_sub_department_by_id(
    id: int,
    department_data: SubDepartmentUpdateSchema = Body(None),
    session: AsyncSession = Depends(get_async_session),
):
    response: SubDepartment = await update_sub_dep(
        id, department_data, SubDepartment, session
    )
    # await invalidate_cache(
    #     "get_sub_departments_by_department_id", response.main_department_id
    # )
    return response


@departments.delete("/sub_department/{id}")
async def delete_sub_department_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    # sub_dep: SubDepartment = await get_one_sub_dep(id, SubDepartment, session)
    # await session.commit()
    # await invalidate_cache(
    #     "get_sub_departments_by_department_id",
    #     sub_dep.main_department_id,
    # )
    return await delete_sub_dep(id, SubDepartment, session)
