import contextlib
import os
from typing import List

from sqlalchemy import select

from src.slider_main.models import SliderMain
from src.database.database import get_async_session


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_slide(title: str, description: str):
    async with get_async_session_context() as session:
        photo_filename = "first_slide.png"
        photo_path = os.path.join("static", "slider_main", photo_filename)

        query = select(SliderMain).where(SliderMain.title == title)
        result = await session.execute(query)
        slide = result.scalars().first()
        if not slide:
            slide = SliderMain(title=title, description=description, photo=photo_path)
            session.add(slide)
            await session.commit()
            print(f"Slide {slide.id} have been created successfully.")
        else:
            print(f"Slide with title:'{slide.title}' already exists")


async def create_slides(slides_list: List[dict]):
    for slide_data in slides_list:
        await create_slide(**slide_data)
