from re import match
from typing import Any, Optional, Union
from enum import Enum

from pydantic import (
    BaseModel,
    EmailStr,
    AnyHttpUrl,
    Field,
    field_validator,
    ValidationInfo,
)

from src.exceptions import INVALID_PHONE


class ContactsSchema(BaseModel):
    map_url: Union[AnyHttpUrl, Any]
    address: Union[str, Any]
    phone: Union[str, Any]
    email: Union[EmailStr, Any]
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
    phone: Optional[str] = None
    email: Optional[Union[EmailStr, str]] = None
    facebook_url: Optional[Union[AnyHttpUrl, str]] = None
    youtube_url: Optional[Union[AnyHttpUrl, str]] = None
    admission_info_url: Optional[Union[AnyHttpUrl, str]] = None
    statute_url: Optional[Union[AnyHttpUrl, str]] = None
    legal_info_url: Optional[Union[AnyHttpUrl, str]] = None

    @field_validator(
        "map_url",
        "facebook_url",
        "youtube_url",
        "admission_info_url",
        "statute_url",
        "legal_info_url",
        "email",
        "phone",
    )
    @classmethod
    def validate(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            return ""
        else:
            if info.field_name == "email":
                return EmailStr._validate(value)
            elif info.field_name == "phone":
                if not (match(r"^[\d\+\-\(\)]{10,20}$", value)):
                    raise ValueError(INVALID_PHONE)
                else:
                    return value
            else:
                return AnyHttpUrl(value)


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
