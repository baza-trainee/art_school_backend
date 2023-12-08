import json
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Body, Form, UploadFile


class SliderMainSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., max_length=120)
    description: Optional[str] = Field(..., max_length=200)
    photo: str


class SliderCreateSchema(BaseModel):
    photo: UploadFile = Field(...)
    title: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = Field(None, max_length=200)

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: Optional[str] = Form(max_length=120, default=None),
        description: Optional[str] = Form(max_length=200, default=None),
    ):
        return cls(photo=photo, title=title, description=description)


class SliderMainUpdateSchema(BaseModel):
    title: Optional[str] = (Body(max_length=120, default=None),)
    description: Optional[str] = (Body(max_length=200, default=None),)

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Body(
            max_length=120,
            default=None,
            description="Залиште поле пустим, щоб видалити дані",
        ),
        description: Optional[str] = Body(
            max_length=200,
            default=None,
            description="Залиште поле пустим, щоб видалити дані",
        ),
    ):
        return cls(title=title, description=description)
