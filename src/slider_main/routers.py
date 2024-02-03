from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.utils import disable_installed_extensions_check

from src.auth.models import User
from src.database.database import get_async_session
from src.auth.auth_config import CURRENT_SUPERUSER
from .models import SliderMain
from .schemas import SliderMainSchema, SliderMainUpdateSchema, SliderCreateSchema
from .service import (
    get_all_slides,
    new_slide,
    update_slide,
    delete_slide_by_id,
)


slider_main_router = APIRouter(prefix="/slider_main", tags=["Slider main"])


@slider_main_router.get("", response_model=List[SliderMainSchema])
async def get_slider_list(
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_slides(SliderMain, session)
    disable_installed_extensions_check()
    return result


@slider_main_router.post("", response_model=SliderMainSchema)
async def create_slide(
    background_tasks: BackgroundTasks,
    slide_data: SliderCreateSchema = Depends(SliderCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await new_slide(slide_data, SliderMain, session, background_tasks)


@slider_main_router.put("/{slide_id}", response_model=SliderMainSchema)
async def partial_update_slide(
    slide_id: int,
    background_tasks: BackgroundTasks,
    photo: UploadFile = None,
    slider_data: SliderMainUpdateSchema = Depends(SliderMainUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_slide(
        slider_data, SliderMain, session, background_tasks, photo, slide_id
    )


@slider_main_router.delete("/{slide_id}")
async def delete_slide(
    slide_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await delete_slide_by_id(SliderMain, session, background_tasks, slide_id)
