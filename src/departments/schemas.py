from enum import Enum
from typing import Optional, Union
from datetime import datetime

from pydantic import BaseModel, Field, validator

from src.achievements.models import Achievement
from src.config import settings
from .models import SubDepartment, MainDepartment


SUB_DEP_NAME_LEN = SubDepartment.sub_department_name.type.length
SUB_DEP_DESC_LEN = SubDepartment.description.type.length
DEP_NAME_LEN = MainDepartment.department_name.type.length
ACHI_DESC_LEN = Achievement.description.type.length
ACHI_MEDIA_LEN = Achievement.media.type.length


class DepartmentEnum(int, Enum):
    music = 1
    vocal_choral = 2
    choreographic = 3
    theatrical = 4
    artistic = 5
    preschool = 6


class DepartmentSchema(BaseModel):
    id: int = Field(..., ge=1, le=6)
    department_name: str = Field(..., max_length=DEP_NAME_LEN)


class SubDepartmentSchema(BaseModel):
    id: int = Field(..., ge=1)
    sub_department_name: str = Field(..., min_length=2, max_length=SUB_DEP_NAME_LEN)
    description: Union[str, None] = Field(..., max_length=SUB_DEP_DESC_LEN)
    main_department_id: int = Field(..., ge=1, le=6)


class SubDepartmentCreateSchema(BaseModel):
    sub_department_name: str = Field(..., min_length=2, max_length=SUB_DEP_NAME_LEN)
    description: str = Field(None, max_length=SUB_DEP_DESC_LEN)
    main_department_id: int = Field(..., ge=1, le=6)


class SubDepartmentUpdateSchema(BaseModel):
    sub_department_name: str = Field(None, min_length=2, max_length=SUB_DEP_NAME_LEN)
    description: str = Field(None, max_length=SUB_DEP_DESC_LEN)


class SubDepartmentGallerySchema(BaseModel):
    id: int
    media: str = Field(..., max_length=ACHI_MEDIA_LEN)
    is_video: bool
    description: Optional[str] = Field(None, min_length=0, max_length=ACHI_DESC_LEN)
    sub_department: int = Field(..., ge=1)
    pinned_position: Optional[int] = Field(None, ge=1, le=12)
    created_at: datetime

    @validator("media", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


class SubDepartmentAchievementSchema(BaseModel):
    id: int
    media: str = Field(..., max_length=ACHI_MEDIA_LEN)
    description: Optional[str] = Field(None, min_length=0, max_length=ACHI_DESC_LEN)
    sub_department: int = Field(..., ge=1)
    pinned_position: Optional[int] = Field(..., ge=1, le=12)
    created_at: datetime

    @validator("media", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"
