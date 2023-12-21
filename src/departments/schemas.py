from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class DepartmentEnum(int, Enum):
    music = 1
    vocal_choral = 2
    choreographic = 3
    theatrical = 4
    artistic = 5
    preschool = 6


class DepartmentSchema(BaseModel):
    id: Optional[int]
    department_name: Optional[str]


class SubDepartmentSchema(BaseModel):
    id: Optional[int]
    sub_department_name: Optional[str]
    description: Optional[str]
    main_department_id: Optional[int]


class SubDepartmentCreateSchema(BaseModel):
    sub_department_name: str
    description: str = Field(..., max_length=2000)
    main_department_id: int = Field(..., ge=1, le=6)


class SubDepartmentUpdateSchema(BaseModel):
    sub_department_name: Optional[str] = Field(None, max_length=300)
    description: Optional[str] = Field(None, max_length=2000)


class SubDepartmentGallerySchema(BaseModel):
    id: int
    media: str
    is_video: bool
    description: Optional[str]
    sub_department: Optional[int]
    pinned_position: Optional[int]
    created_at: datetime


class SubDepartmentAchievementSchema(BaseModel):
    id: int
    media: str
    description: Optional[str]
    sub_department: Optional[int]
    pinned_position: Optional[int]
    created_at: datetime
