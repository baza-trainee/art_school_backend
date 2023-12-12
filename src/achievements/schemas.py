from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, constr, validator
from fastapi import UploadFile

from src.config import IS_PROD, settings
from src.exceptions import SUCCESS_DELETE


class GetAchievementSchema(BaseModel):
    id: int
    media: str
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
