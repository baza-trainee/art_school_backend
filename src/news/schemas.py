from typing import Optional
from pydantic import BaseModel, Field, validator
from src.config import BASE_URL
from fastapi import UploadFile


class NewsSchema(BaseModel):
    id: int
    title: Optional[str] = Field(..., max_length=300)
    text: Optional[str] = Field(..., max_length=2000)
    photo: Optional[str]

    # @validator("photo", pre=True)
    # def add_base_url(cls, v):
    #     return (
    #         f"{BASE_URL if BASE_URL else 'https://art-school-backend.vercel.app'}/{v}"
    #     )


class NewsCreateSchema(BaseModel):
    photo: UploadFile = Field(...)
    title: str = Field(..., max_length=300)
    text: str = Field(..., max_length=2000)


class NewsUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=300)
    text: Optional[str] = Field(None, max_length=2000)


# class DeleteNewsResponseSchema(BaseModel):
#     message: str = "Record with id 1 was successfully deleted."
