from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from cloudinary import uploader
from fastapi_pagination.utils import disable_installed_extensions_check

from src.auth.models import User
from src.database import get_async_session
from src.auth.auth_config import CURRENT_SUPERUSER
from .models import SliderMain
from .schemas import SliderMainSchema, SliderMainUpdateSchema
from .exceptions import (
    NO_DATA_FOUND,
    SERVER_ERROR,
    NO_RECORD,
    SUCCESS_DELETE,
)


slider_main_router = APIRouter(prefix="/slider_main", tags=["Slider ain"])


@slider_main_router.get("", response_model=List[SliderMainSchema])
async def get_slider_list(
    session: AsyncSession = Depends(get_async_session),
):
    query = select(SliderMain).order_by(SliderMain.id)
    slider = await session.execute(query)
    all_slides = slider.scalars().all()
    if not all_slides:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    disable_installed_extensions_check()
    return all_slides


@slider_main_router.patch("/{slide_id}", response_model=SliderMainSchema)
async def partial_update_slide(
    slide_id: int,
    photo: Annotated[UploadFile, File()] = None,
    slider_data: SliderMainSchema = Depends(SliderMainUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(SliderMain).where(SliderMain.id == slide_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    update_data = slider_data.model_dump(exclude_none=True)
    if photo:
        folder_path = f"static/{SliderMain.__name__}"
        # os.makedirs(folder_path, exist_ok=True)
        # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
        # async with aiofiles.open(file_path, "wb") as buffer:
        #     await buffer.write(await photo.read())
        # update_data["photo"] = file_path
        upload_result = uploader.upload(photo.file, folder=folder_path)
        update_data["photo"] = upload_result["url"]
    if not update_data:
        return Response(status_code=204)
    try:
        query = (
            update(SliderMain)
            .where(SliderMain.id == slide_id)
            .values(**update_data)
            .returning(SliderMain)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


@slider_main_router.delete("/{slide_id}")
async def delete_slide(
    slide_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    query = select(SliderMain).where(SliderMain.id == slide_id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)
    try:
        query = (
            update(SliderMain)
            .where(SliderMain.id == slide_id)
            .values(title=None, description=None)
        )
        await session.execute(query)
        await session.commit()
        return {"message": SUCCESS_DELETE % slide_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
