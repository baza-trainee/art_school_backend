from typing import Optional

from pydantic import BaseModel, Field
from fastapi import Body, Form, UploadFile

from src.slider_main.exceptions import SCHEMA_DESC
from .models import SliderMain


TITLE_LEN = SliderMain.title.type.length
DESCR_LEN = SliderMain.description.type.length


class SliderMainSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., max_length=TITLE_LEN)
    description: Optional[str] = Field(..., max_length=DESCR_LEN)
    photo: str


class SliderCreateSchema(BaseModel):
    photo: UploadFile = Field(...)
    title: Optional[str] = Field(None, max_length=TITLE_LEN)
    description: Optional[str] = Field(None, max_length=DESCR_LEN)

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: Optional[str] = Form(max_length=TITLE_LEN, default=None),
        description: Optional[str] = Form(max_length=DESCR_LEN, default=None),
    ):
        return cls(photo=photo, title=title, description=description)


class SliderMainUpdateSchema(BaseModel):
    title: Optional[str] = (Body(max_length=TITLE_LEN, default=None),)
    description: Optional[str] = (Body(max_length=DESCR_LEN, default=None),)

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Body(
            max_length=TITLE_LEN,
            default=None,
            description=SCHEMA_DESC,
        ),
        description: Optional[str] = Body(
            max_length=DESCR_LEN,
            default=None,
            description=SCHEMA_DESC,
        ),
    ):
        return cls(title=title, description=description)
