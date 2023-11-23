from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from sqlalchemy import desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import NO_DATA_FOUND, NO_RECORD, NO_SUB_DEPARTMENT, SERVER_ERROR
from src.database import get_async_session
from src.gallery.models import Gallery
from .models import MainDepartment, SubDepartment
from .schemas import (
    DepartmentEnum,
    DepartmentSchema,
    SubDepartmentEnum,
    SubDepartmentSchema,
    SubDepartmentUpdateSchema,
)


departments = APIRouter(prefix="/departments", tags=["Departments"])


@departments.get("", response_model=List[DepartmentSchema])
async def get_all_departments(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(MainDepartment).order_by(MainDepartment.id)
        departments = await session.execute(query)
        if not departments:
            raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
        return departments.scalars().all()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@departments.get("/{id}", response_model=List[SubDepartmentSchema])
async def get_sub_departments_by_department_id(
    id: DepartmentEnum,
    session: AsyncSession = Depends(get_async_session),
):
    query = (
        select(SubDepartment)
        .where(SubDepartment.main_department_id == id)
        .order_by(SubDepartment.id)
    )
    result = await session.execute(query)
    sub_departments = result.scalars().all()
    if not sub_departments:
        raise HTTPException(status_code=404, detail=NO_SUB_DEPARTMENT)
    return sub_departments


@departments.get("/sub_department/{id}", response_model=SubDepartmentSchema)
async def get_sub_department_by_id(
    id: SubDepartmentEnum,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(SubDepartment).where(SubDepartment.id == id)
        result = await session.execute(query)
        sub_department = result.scalars().first()
        if not sub_department:
            raise HTTPException(status_code=404, detail=NO_RECORD)
        return sub_department
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@departments.get("/sub_department_gallery/{id}")
async def get_gallery_for_sub_department(
    id: SubDepartmentEnum,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = (
            select(Gallery)
            .where(Gallery.sub_department == id)
            .order_by(desc(Gallery.created_at))
        )
        result = await session.execute(query)
        gallery = result.scalars().all()
        if not gallery:
            return HTTPException(status_code=404, detail=NO_RECORD)
        return gallery
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@departments.get("/sub_department_achivement/{id}")
async def get_achivement_for_sub_department(
    id: SubDepartmentEnum,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = (
            select(Gallery)
            .where(Gallery.sub_department == id, Gallery.is_achivement == True)
            .order_by(desc(Gallery.created_at))
        )
        result = await session.execute(query)
        gallery = result.scalars().all()
        if not gallery:
            return HTTPException(status_code=404, detail=NO_RECORD)
        return gallery
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@departments.patch("/sub_department/{id}", response_model=SubDepartmentSchema)
async def update_sub_department_by_id(
    id: SubDepartmentEnum,
    department_data: SubDepartmentUpdateSchema = Body(None),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        update_data = department_data.model_dump(exclude_none=True)
        if not update_data:
            return Response(status_code=204)
        query = select(SubDepartment).where(SubDepartment.id == id)
        result = await session.execute(query)
        record = result.scalars().first()
        if not record:
            return HTTPException(status_code=404, detail=NO_RECORD)
        query = (
            update(SubDepartment)
            .where(SubDepartment.id == id)
            .values(**update_data)
            .returning(SubDepartment)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@departments.delete("/sub_department/{id}", response_model=SubDepartmentSchema)
async def delete_sub_department_description_by_id(
    id: SubDepartmentEnum,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(SubDepartment).where(SubDepartment.id == id)
        result = await session.execute(query)
        record = result.scalars().first()
        if not record:
            return HTTPException(status_code=404, detail=NO_RECORD)
        query = (
            update(SubDepartment).where(SubDepartment.id == id).values(description=None)
        )
        await session.execute(query)
        await session.commit()
        return record
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
