from typing import Optional
from pydantic import BaseModel, Field, validator
from fastapi import Form, UploadFile
from datetime import datetime



class NewsSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., max_length=300)
    text: Optional[str] = Field(..., max_length=2000)
    photo: str
    created_at: datetime


    # @validator("photo", pre=True)
    # def add_base_url(cls, v):
    #     return (
    #         f"{BASE_URL if BASE_URL else 'https://art-school-backend.vercel.app'}/{v}"
    #     )


class NewsCreateSchema(BaseModel):
    photo: UploadFile = Field(...)
    title: str = Field(..., max_length=300)
    text: str = Field(..., max_length=2000)

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        title: str = Form(max_length=300),
        text: str = Form(max_length=2000),
    ):
        return cls(photo=photo, title=title, text=text)


class NewsUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=300)
    text: Optional[str] = Field(None, max_length=2000)

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(max_length=300, default=None),
        text: Optional[str] = Form(max_length=2000, default=None),
    ):
        return cls(title=title, text=text)
