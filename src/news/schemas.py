from typing import Optional
from pydantic import BaseModel, Field


class NewsSchema(BaseModel):
    
    title: Optional[str] = Field(..., max_length=300)
    text: Optional[str] = Field(..., max_length=2000)
    photo: Optional[str]
