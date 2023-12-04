import json
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from fastapi import Body, Form, UploadFile


class SliderMainSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., max_length=150)
    description: Optional[str] = Field(..., max_length=150)
    photo: str


class SliderCreateSchema(BaseModel):
    photo: UploadFile = Field(...)
    title: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = Field(None, max_length=150)

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: Optional[str] = Form(max_length=150, default=None),
        description: Optional[str] = Form(max_length=150, default=None),
    ):
        return cls(photo=photo, title=title, description=description)


class SliderMainUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Body(max_length=150, default=None),
        description: Optional[str] = Body(max_length=150, default=None),
    ):
        return cls(title=title, description=description)

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value