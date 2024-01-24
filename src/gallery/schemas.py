from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, AnyHttpUrl, Field, FilePath, conint, constr, validator
from fastapi import Form, UploadFile

from src.config import settings
from src.exceptions import SUCCESS_DELETE
from .models import Gallery

MEDIA_LEN = Gallery.media.type.length
DESC_LEN = Gallery.description.type.length


class GetPhotoSchema(BaseModel):
    id: int
    media: AnyHttpUrl = Field(max_length=MEDIA_LEN)
    pinned_position: Optional[conint(ge=1, le=7)]
    sub_department: Optional[int]
    description: Optional[constr(max_length=DESC_LEN)]
    created_at: datetime

    @validator("media", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


class GetTakenPositionsSchema(BaseModel):
    taken_positions: list[Optional[int]]
    free_positions: list[Optional[int]]


class GetVideoSchema(BaseModel):
    id: int
    media: Union[AnyHttpUrl, FilePath]
    created_at: datetime


class CreatePhotoSchema(BaseModel):
    media: UploadFile
    pinned_position: Optional[int]
    sub_department: Optional[int]
    description: Optional[str]

    @classmethod
    def as_form(
        cls,
        media: UploadFile,
        pinned_position: int = Form(None, ge=1, le=7),
        sub_department: int = Form(None),
        description: str = Form(None, max_length=DESC_LEN),
    ):
        return cls(
            media=media,
            pinned_position=pinned_position,
            sub_department=sub_department,
            description=description,
        )


class UpdatePhotoSchema(CreatePhotoSchema):
    media: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        media: UploadFile = None,
        pinned_position: int = Form(None, ge=1, le=7),
        sub_department: int = Form(None),
        description: str = Form(None, max_length=DESC_LEN),
    ):
        return cls(
            media=media,
            pinned_position=pinned_position,
            sub_department=sub_department,
            description=description,
        )


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
