from typing import Annotated, Any, Optional, Union
from enum import Enum

from pydantic import BaseModel, EmailStr, constr, AnyHttpUrl, validator


class ContactsSchema(BaseModel):
    map_url: Union[AnyHttpUrl, Any]
    address: str
    phone: constr(max_length=15)
    email: Union[EmailStr, str]
    facebook_url: Union[AnyHttpUrl, Any]
    youtube_url: Union[AnyHttpUrl, Any]
    admission_info_url: Union[AnyHttpUrl, Any]
    statute_url: Union[AnyHttpUrl, Any]
    legal_info_url: Union[AnyHttpUrl, Any]

    class Config:
        from_attributes = True


class ContactsUpdateSchema(BaseModel):
    map_url: Optional[Union[AnyHttpUrl, str]] = None
    address: Optional[str] = None
    phone: Optional[constr(max_length=15)] = None
    email: Optional[Union[EmailStr, str]] = None
    facebook_url: Optional[Union[AnyHttpUrl, str]] = None
    youtube_url: Optional[Union[AnyHttpUrl, str]] = None
    admission_info_url: Optional[Union[AnyHttpUrl, str]] = None
    statute_url: Optional[Union[AnyHttpUrl, str]] = None
    legal_info_url: Optional[Union[AnyHttpUrl, str]] = None

    @validator(
        "map_url",
        "facebook_url",
        "youtube_url",
        "admission_info_url",
        "statute_url",
        "legal_info_url",
        pre=True,
    )
    def validate_url(cls, v):
        if not v:
            return ""
        else:
            return AnyHttpUrl(v)

    @validator("email", pre=True)
    def validate_email(cls, v):
        if not v:
            return ""
        else:
            return EmailStr._validate(v)


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
