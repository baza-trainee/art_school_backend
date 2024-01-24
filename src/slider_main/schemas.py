from typing import Optional

from pydantic import BaseModel, Field, validator
from fastapi import Body, Form, UploadFile
from src.config import settings

from src.slider_main.exceptions import SCHEMA_DESC
from .models import SliderMain


TITLE_LEN = SliderMain.title.type.length
DESCR_LEN = SliderMain.description.type.length


class SliderMainSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., max_length=TITLE_LEN)
    description: Optional[str] = Field(..., max_length=DESCR_LEN)
    photo: str

    @validator("photo", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


class SliderCreateSchema(BaseModel):
    photo: UploadFile
    title: Optional[str]
    description: Optional[str]

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: str = Form(None, max_length=TITLE_LEN),
        description: str = Form(None, max_length=DESCR_LEN),
    ):
        return cls(photo=photo, title=title, description=description)


class SliderMainUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]

    @classmethod
    def as_form(
        cls,
        title: str = Body(
            max_length=TITLE_LEN,
            default=None,
            description=SCHEMA_DESC,
        ),
        description: str = Body(
            max_length=DESCR_LEN,
            default=None,
            description=SCHEMA_DESC,
        ),
    ):
        return cls(title=title, description=description)
