from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, AnyHttpUrl, FilePath, conint, constr, validator
from fastapi import UploadFile

from src.config import IS_PROD, settings
from src.exceptions import SUCCESS_DELETE
from .models import Gallery


DESC_LEN = Gallery.description.type.length


class GetPhotoSchema(BaseModel):
    id: int
    media: Union[AnyHttpUrl, FilePath]
    pinned_position: Optional[int]
    sub_department: Optional[int]
    description: Optional[str]
    created_at: datetime

    @validator("media", pre=True)
    def add_base_url(cls, v, values):
        if IS_PROD:
            return f"{settings.BASE_URL}/{v}"
        else:
            return v


class GetTakenPositionsSchema(BaseModel):
    taken_positions: Optional[list[int]] = None
    free_positions: Optional[list[int]] = None


class GetVideoSchema(BaseModel):
    id: int
    media: Union[AnyHttpUrl, FilePath]
    created_at: datetime


class CreatePhotoSchema(BaseModel):
    media: UploadFile
    pinned_position: Optional[conint(ge=1, le=7)] = None
    sub_department: Optional[int] = None
    description: Optional[constr(max_length=DESC_LEN)] = None


class CreateVideoSchema(BaseModel):
    media: AnyHttpUrl


class UpdatePhotoSchema(BaseModel):
    pinned_position: Optional[conint(ge=1, le=7)] = None
    sub_department: Optional[int] = None
    description: Optional[constr(max_length=DESC_LEN)] = None


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
