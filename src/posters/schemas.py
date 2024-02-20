from typing import Optional
from pydantic import BaseModel, Field, validator
from fastapi import Form, UploadFile
from datetime import datetime

from src.config import settings
from .models import Poster


TITLE_LEN = Poster.title.type.length


class PosterSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., min_length=2, max_length=TITLE_LEN)
    photo: Optional[str]
    created_at: datetime

    @validator("photo", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


class PosterCreateSchema(BaseModel):
    photo: UploadFile
    title: str

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: str = Form(min_length=2, max_length=TITLE_LEN),
    ):
        return cls(photo=photo, title=title)


class PosterUpdateSchema(BaseModel):
    title: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(None, min_length=2, max_length=TITLE_LEN),
    ):
        return cls(title=title)
