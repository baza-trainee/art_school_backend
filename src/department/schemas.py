from typing import Optional

from pydantic import BaseModel, Field, validator
from fastapi import Form, UploadFile

from src.config import BASE_URL


class DepartmentBaseSchema(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    sub_department_name: Optional[str] = Field(..., max_length=300)
    description: Optional[str] = Field(..., max_length=2000)
    photo: Optional[str]

    @validator("photo", pre=True)
    def add_base_url(cls, v):
        return f"{BASE_URL if BASE_URL else 'https://art-school-backend.vercel.app'}/{v}"


class DepartmentCreateSchema(BaseModel):
    photo: UploadFile = Form(...)
    sub_department_name: str = Field(..., max_length=300)
    description: str = Field(..., max_length=2000)


class DepartmentUpdateSchema(BaseModel):
    sub_department_name: Optional[str] = Form(None, max_length=300)
    description: Optional[str] = Form(None, max_length=2000)


class DeleteResponseSchema(BaseModel):
    message: str = "Record with id 1 was successfully deleted."
