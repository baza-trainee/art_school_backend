from typing import Optional
from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    sub_department_name: Optional[str] = Field(..., max_length=300)
    description: Optional[str] = Field(..., max_length=2000)
    photo: Optional[str]


class MusicDepartmentSchema(DepartmentBase):
    pass


class VocalChoirDepartmentSchema(DepartmentBase):
    pass


class ChoreographicDepartmentSchema(DepartmentBase):
    pass


class FineArtsDepartmentSchema(DepartmentBase):
    pass


class TheatricalDepartmentSchema(DepartmentBase):
    pass
