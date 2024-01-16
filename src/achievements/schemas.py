from datetime import datetime
from typing import Annotated, Optional, Union

from pydantic import (
    AnyHttpUrl,
    Field,
    BaseModel,
    FilePath,
    UrlConstraints,
    conint,
    constr,
    validator,
)
from fastapi import Form, UploadFile
from pydantic_core import Url

from src.config import IS_PROD, settings
from src.exceptions import SUCCESS_DELETE
from .models import Achievement

MEDIA_LEN = Achievement.media.type.length
DESC_LEN = Achievement.description.type.length


class GetAchievementSchema(BaseModel):
    id: int
    media: AnyHttpUrl = Field(max_length=MEDIA_LEN)
    pinned_position: Optional[conint(ge=1, le=12)]
    sub_department: Optional[int]
    description: Optional[constr(max_length=DESC_LEN)]
    created_at: datetime

    @validator("media", pre=True)
    def add_base_url(cls, v, values):
        if IS_PROD:
            return f"{settings.BASE_URL}/{v}"
        else:
            return v


class GetTakenPositionsSchema(BaseModel):
    taken_positions: list[Optional[int]]
    free_positions: list[Optional[int]]


class CreateAchievementSchema(BaseModel):
    media: UploadFile
    pinned_position: Optional[int]
    sub_department: Optional[int]
    description: Optional[str]

    @classmethod
    def as_form(
        cls,
        media: UploadFile,
        pinned_position: int = Form(None, ge=1, le=12),
        sub_department: int = Form(None),
        description: str = Form(None, max_length=DESC_LEN),
    ):
        return cls(
            media=media,
            pinned_position=pinned_position,
            sub_department=sub_department,
            description=description,
        )


class UpdateAchievementSchema(CreateAchievementSchema):
    media: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        media: UploadFile = None,
        pinned_position: int = Form(None, ge=1, le=12),
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
