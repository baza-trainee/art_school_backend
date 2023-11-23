from typing import Optional
from enum import Enum
from fastapi import Form

from pydantic import BaseModel, EmailStr, constr, AnyHttpUrl


class ContactsSchema(BaseModel):
    map_url: Optional[AnyHttpUrl]
    address: Optional[str]
    phone: Optional[constr(max_length=50)]
    email: Optional[EmailStr]
    facebook_url: Optional[AnyHttpUrl]
    youtube_url: Optional[AnyHttpUrl]
    admission_info_url: Optional[AnyHttpUrl]
    statute_url: Optional[AnyHttpUrl]
    legal_info_url: Optional[AnyHttpUrl]

    class Config:
        from_attributes = True


class ContactsUpdateSchema(BaseModel):
    map_url: Optional[AnyHttpUrl] = None
    address: Optional[str] = None
    phone: Optional[constr(max_length=15)] = None
    email: Optional[EmailStr] = None
    facebook_url: Optional[AnyHttpUrl] = None
    youtube_url: Optional[AnyHttpUrl] = None
    admission_info_url: Optional[AnyHttpUrl] = None
    statute_url: Optional[AnyHttpUrl] = None
    legal_info_url: Optional[AnyHttpUrl] = None

    @classmethod
    def as_form(
        cls,
        map_url: Optional[AnyHttpUrl] = Form(None),
        address: Optional[str] = Form(None),
        phone: Optional[constr(max_length=15)] = Form(None),
        email: Optional[EmailStr] = Form(None),
        facebook_url: Optional[AnyHttpUrl] = Form(None),
        youtube_url: Optional[AnyHttpUrl] = Form(None),
        admission_info_url: Optional[AnyHttpUrl] = Form(None),
        statute_url: Optional[AnyHttpUrl] = Form(None),
        legal_info_url: Optional[AnyHttpUrl] = Form(None),
    ):
        return cls(
            map_url=map_url,
            address=address,
            phone=phone,
            email=email,
            facebook_url=facebook_url,
            youtube_url=youtube_url,
            admission_info_url=admission_info_url,
            statute_url=statute_url,
            legal_info_url=legal_info_url,
        )


class ContactField(str, Enum):
    map_url = "map_url"
    address = "address"
    phone = "phone"
    email = "email"
    facebook_url = "facebook_url"
    youtube_url = "youtube_url"
    admission_info_url = "admission_info_url"
    statute_url = "statute_url"
    legal_info_url = "legal_info_url"
