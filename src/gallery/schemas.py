from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import AnyHttpUrl, BaseModel, validator, FilePath
from fastapi import Form, UploadFile

from src.config import settings
from src.exceptions import SUCCESS_DELETE


class GetPhotoSchema(BaseModel):
    id: int
    media: Union[AnyHttpUrl, FilePath]
    pinned_position: Optional[int]
    description: Optional[str]
    sub_department: Optional[int]
    created_at: datetime
    # To save files locally
    # @validator("media", pre=True)
    # def add_base_url(cls, v, values):
    #     return v if values['is_video'] else f"{settings.BASE_URL}/{v}"


class GetVideoSchema(BaseModel):
    id: int
    media: Union[AnyHttpUrl, FilePath]
    created_at: datetime


class PositionEnum(int, Enum):
    default_position = 0
    position_1 = 1
    position_2 = 2
    position_3 = 3
    position_4 = 4
    position_5 = 5
    position_6 = 6
    position_7 = 7
    position_8 = 8


class CreatePhotoSchema(BaseModel):
    media: UploadFile
    description: Optional[str] = Form(default=None, max_length=300)

    @classmethod
    def as_form(
        cls,
        media: UploadFile,
        description: Optional[str] = Form(default=None, max_length=300),
    ):
        return cls(media=media, description=description)


class CreateVideoSchema(BaseModel):
    media: AnyHttpUrl

    @classmethod
    def as_form(
        cls,
        media: AnyHttpUrl = Form(),
    ):
        return cls(media=media)


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
