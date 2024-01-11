from typing import Optional

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field, constr

from src.exceptions import SUCCESS_DELETE
from .models import SchoolAdministration


PHOTO_LEN = SchoolAdministration.photo.type.length
POSITION_LEN = SchoolAdministration.position.type.length
FULL_NAME_LEN = SchoolAdministration.full_name.type.length


class AdministratorSchema(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    full_name: Optional[str] = Field(..., max_length=FULL_NAME_LEN)
    position: Optional[str] = Field(..., max_length=POSITION_LEN)
    photo: Optional[constr(max_length=PHOTO_LEN)]


class AdministratorCreateSchema(BaseModel):
    photo: UploadFile
    full_name: str
    position: str

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        full_name: str = Form(..., max_length=FULL_NAME_LEN),
        position: str = Form(..., max_length=POSITION_LEN),
    ):
        return cls(photo=photo, full_name=full_name, position=position)


class AdministratorUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    position: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        full_name: str = Form(None, max_length=FULL_NAME_LEN),
        position: str = Form(None, max_length=POSITION_LEN),
    ):
        return cls(full_name=full_name, position=position)


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
