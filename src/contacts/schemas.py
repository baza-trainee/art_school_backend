from re import match
from typing import Annotated, Optional, Union

from pydantic import (
    BaseModel,
    EmailStr,
    AnyHttpUrl,
    Field,
    ValidationInfo,
    constr,
    field_validator,
)

from src.exceptions import INVALID_PHONE
from .models import Contacts


PHONE_LEN = Contacts.phone.type.length
MAIL_LEN = Contacts.email.type.length
ADDRESS_LEN = Contacts.address.type.length
URL_LEN = Contacts.map_url.type.length


class ContactsSchema(BaseModel):
    map_url: Union[AnyHttpUrl, str] = Field(max_length=URL_LEN)
    address: constr(max_length=ADDRESS_LEN)
    phone: constr(
        max_length=PHONE_LEN,
        pattern=r"^(\+?38)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$|^$",
    )
    email: Union[EmailStr, str] = Field(max_length=MAIL_LEN)
    facebook_url: Union[AnyHttpUrl, str] = Field(max_length=URL_LEN)
    youtube_url: Union[AnyHttpUrl, str] = Field(max_length=URL_LEN)


class ContactsUpdateSchema(BaseModel):
    map_url: Optional[
        Union[AnyHttpUrl, constr(max_length=URL_LEN, pattern=r"^$")]
    ] = None
    address: constr(max_length=ADDRESS_LEN) = None
    phone: Optional[
        constr(
            max_length=50,
            pattern=r"^(\+?38)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$|^$",
        )
    ] = None
    email: Optional[Union[EmailStr, constr(max_length=MAIL_LEN, pattern=r"^$")]] = None
    facebook_url: Optional[
        Union[AnyHttpUrl, constr(max_length=URL_LEN, pattern=r"^$")]
    ] = None
    youtube_url: Optional[
        Union[AnyHttpUrl, constr(max_length=URL_LEN, pattern=r"^$")]
    ] = None

    @field_validator(
        "map_url",
        "facebook_url",
        "youtube_url",
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
                if not (
                    match(
                        r"^(\+?38)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$", value
                    )
                ):
                    raise ValueError(INVALID_PHONE)
                else:
                    return value
            else:
                return AnyHttpUrl(value)
