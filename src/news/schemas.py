from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator
from fastapi import Form, UploadFile
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

    # @validator("photo", pre=True)
    # def add_base_url(cls, v):
    #     return (
    #         f"{BASE_URL if BASE_URL else 'https://art-school-backend.vercel.app'}/{v}"
    #     )


class NewsCreateSchema(BaseModel):
    photo: UploadFile
    title: str = Field(..., max_length=TITLE_LEN)
    text: str = Field(..., max_length=TEXT_LEN)

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: str = Form(max_length=TITLE_LEN),
        text: str = Form(max_length=TEXT_LEN),
    ):
        return cls(photo=photo, title=title, text=text)


class NewsUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=TITLE_LEN)
    text: Optional[str] = Field(None, max_length=TEXT_LEN)

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(max_length=TITLE_LEN, default=None),
        text: Optional[str] = Form(max_length=TEXT_LEN, default=None),
    ):
        return cls(title=title, text=text)
