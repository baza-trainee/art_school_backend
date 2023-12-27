from typing import Optional

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field

from src.exceptions import SUCCESS_DELETE


class AdministratorSchema(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    full_name: Optional[str] = Field(..., max_length=150)
    position: Optional[str] = Field(..., max_length=2000)
    photo: Optional[str]


class AdministratorCreateSchema(BaseModel):
    photo: UploadFile = Field(...)
    full_name: str = Field(..., max_length=150)
    position: str = Field(..., max_length=2000)

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        full_name: str = Form(...),
        position: str = Form(...),
    ):
        return cls(photo=photo, full_name=full_name, position=position)


class AdministratorUpdateSchema(BaseModel):
    full_name: Optional[str] = Field(None, max_length=150)
    position: Optional[str] = Field(None, max_length=2000)

    @classmethod
    def as_form(
        cls,
        full_name: str = Form(None),
        position: str = Form(None),
    ):
        return cls(full_name=full_name, position=position)


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
