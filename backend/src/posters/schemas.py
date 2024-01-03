from typing import Optional
from pydantic import BaseModel, Field, validator
from fastapi import Form, UploadFile
from datetime import datetime
from .models import Poster


TITLE_LEN = Poster.title.type.length


class PosterSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., max_length=TITLE_LEN)
    photo: Optional[str]
    created_at: datetime

    # @validator("photo", pre=True)
    # def add_base_url(cls, v):
    #     return (
    #         f"{settings.BASE_URL if settings.BASE_URL else 'https://art-school-backend.vercel.app'}/{v}"
    #     )


class PosterCreateSchema(BaseModel):
    photo: UploadFile = Field(...)
    title: str = Field(..., max_length=TITLE_LEN)

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: str = Form(max_length=TITLE_LEN),
    ):
        return cls(photo=photo, title=title)


class PosterUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=TITLE_LEN)

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(max_length=TITLE_LEN, default=None),
    ):
        return cls(title=title)
