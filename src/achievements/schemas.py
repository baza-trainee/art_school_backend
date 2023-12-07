from datetime import datetime
from typing import Optional, Union

from pydantic import AnyHttpUrl, BaseModel, conint, validator, FilePath, constr
from fastapi import UploadFile

from src.config import settings
from src.exceptions import SUCCESS_DELETE


class GetAchievementSchema(BaseModel):
    id: int
    media: Union[AnyHttpUrl, FilePath]
    pinned_position: Optional[int]
    sub_department: Optional[int]
    description: Optional[str]
    created_at: datetime
    # To save files locally
    # @validator("media", pre=True)
    # def add_base_url(cls, v, values):
    #     return v if values['is_video'] else f"{settings.BASE_URL}/{v}"


class CreateAchievementSchema(BaseModel):
    media: UploadFile
    pinned_position: Optional[conint(ge=1, le=12)] = None
    sub_department: Optional[int] = None
    description: Optional[constr(max_length=300)] = None


class UpdateAchievementSchema(BaseModel):
    pinned_position: Optional[conint(ge=1, le=12)] = None
    sub_department: Optional[int] = None
    description: Optional[constr(max_length=300)] = None


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
