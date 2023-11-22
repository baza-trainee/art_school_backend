from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import AnyHttpUrl, BaseModel, validator, FilePath
from fastapi import UploadFile

from src.config import BASE_URL
from src.exceptions import SUCCESS_DELETE


class MediaSchema(BaseModel):
    id: int
    is_video: bool
    pinned_position: int
    media: Union[AnyHttpUrl, FilePath]
    created_at: datetime
    # To save files locally
    # @validator("media", pre=True)
    # def add_base_url(cls, v, values):
    #     return v if values['is_video'] else f"{BASE_URL}/{v}"


class PositionEnum(int, Enum):
    position_0 = 0
    position_1 = 1
    position_2 = 2
    position_3 = 3
    position_4 = 4
    position_5 = 5
    position_6 = 6
    position_7 = 7
    position_8 = 8


class PhotoCreateSchema(BaseModel):
    pinned_position: PositionEnum
    media: UploadFile


class VideoCreateSchema(BaseModel):
    media: AnyHttpUrl


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
