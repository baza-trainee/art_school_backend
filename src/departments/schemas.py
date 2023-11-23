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


class SubDepartmentEnum(int, Enum):
    string = 1
    wind = 2
    folk = 3
    theoretical = 4
    jazz = 5
    specialized_piano = 6
    concertmasters = 7
    chamber_ensemble = 8
    art_history = 9
    choral = 10
    solo_singing = 11
    pop_vocals = 12
    folk_singing = 13
    classical_dance = 14
    folk_dance = 15
    modern_dance = 16
    imagination_development = 17
    painting = 18
    design_graphic = 19


class DepartmentSchema(BaseModel):
    id: Optional[int]
    department_name: Optional[str]


class SubDepartmentSchema(BaseModel):
    id: Optional[int]
    sub_department_name: Optional[str]
    description: Optional[str]
    main_department_id: Optional[int]


class SubDepartmentUpdateSchema(BaseModel):
    description: Optional[str] = Field(None, max_length=2000)


class SubDepartmentGallerySchema(BaseModel):
    id: int
    media: str
    is_video: bool
    description: Optional[str]
    sub_department: Optional[int]
    is_achivement: bool
    pinned_position: Optional[int]
    created_at: datetime
