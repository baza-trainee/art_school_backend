from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator
from fastapi import Form, UploadFile

from src.config import settings
from .models import News


TITLE_LEN = News.title.type.length
TEXT_LEN = News.text.type.length
PHOTO_LEN = News.title.type.length


class NewsSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., max_length=TITLE_LEN)
    text: Optional[str] = Field(..., max_length=TEXT_LEN)
    photo: str = Field(..., max_length=PHOTO_LEN)
    created_at: datetime

    @validator("photo", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


class NewsCreateSchema(BaseModel):
    photo: UploadFile
    title: str
    text: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: str = Form(max_length=TITLE_LEN),
        text: str = Form(None, max_length=TEXT_LEN),
    ):
        return cls(photo=photo, title=title, text=text)


class NewsUpdateSchema(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(None, max_length=TITLE_LEN),
        text: str = Form(None, max_length=TEXT_LEN),
    ):
        return cls(title=title, text=text)
