from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import AnyHttpUrl, BaseModel, validator, FilePath
from fastapi import UploadFile

from src.departments.schemas import SubDepartmentEnum
from src.config import BASE_URL
from src.database import get_async_session
from src.exceptions import SUCCESS_DELETE


class MediaSchema(BaseModel):
    id: int
    is_video: bool
    is_achivement : bool
    media: Union[AnyHttpUrl, FilePath]
    pinned_position: Optional[int]
    description: Optional[str]
    sub_department: Optional[SubDepartmentEnum]
    created_at: datetime

    # To save files locally
    # @validator("media", pre=True)
    # def add_base_url(cls, v, values):
    #     return v if values['is_video'] else f"{BASE_URL}/{v}"


class PositionEnum(int, Enum):
    position_1 = 1
    position_2 = 2
    position_3 = 3
    position_4 = 4
    position_5 = 5
    position_6 = 6
    position_7 = 7
    position_8 = 8


class PhotoCreateSchema(BaseModel):
    # pinned_position: PositionEnum
    media: UploadFile
    is_achivement : bool = False
    # sub_department: Optional[SubDepartmentEnum] = None 
    description: Optional[str] = None


class VideoCreateSchema(BaseModel):
    media: AnyHttpUrl


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
