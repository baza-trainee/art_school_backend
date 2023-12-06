import contextlib
from typing import List

from sqlalchemy import select

from src.departments.models import MainDepartment, SubDepartment
from src.database.database import get_async_session
from src.exceptions import (
    CREATE_MAIN,
    EXISTS_MAIN,
    SUB_DEP_EXISTS,
    SUCCESS_CREATE,
)


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_main_department(department_name: str):
    async with get_async_session_context() as session:
        query = select(MainDepartment).filter(
            MainDepartment.department_name == department_name
        )
        result = await session.execute(query)
        main_department = result.scalars().first()
        if not main_department:
            main_department = MainDepartment(department_name=department_name)
            session.add(main_department)
            await session.commit()
            print(CREATE_MAIN % department_name)
        else:
            print(EXISTS_MAIN % department_name)


async def create_sub_department(
    sub_department_name: str, description: str, main_department_id: int
):
    async with get_async_session_context() as session:
        query = select(SubDepartment).filter(
            SubDepartment.sub_department_name == sub_department_name,
            SubDepartment.main_department_id == main_department_id,
        )
        result = await session.execute(query)
        sub_department = result.scalars().first()
        if not sub_department:
            sub_department = SubDepartment(
                sub_department_name=sub_department_name,
                description=description,
                main_department_id=main_department_id,
            )
            session.add(sub_department)
            await session.commit()
            print(SUCCESS_CREATE % (sub_department_name, main_department_id))
        else:
            print(SUB_DEP_EXISTS % (sub_department_name, main_department_id))


async def create_main_departments(department_list: List[str]):
    for department_name in department_list:
        await create_main_department(department_name)


async def create_sub_departments(sub_department_list: List[dict]):
    for sub_department_data in sub_department_list:
        await create_sub_department(**sub_department_data)
