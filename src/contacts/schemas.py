from typing import Annotated, Optional, Union

from fastapi import Form, UploadFile
from pydantic import (
    BaseModel,
    EmailStr,
    AnyHttpUrl,
    Field,
    FilePath,
    constr,
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
    email: Annotated[EmailStr, Field(max_length=MAIL_LEN)]
    facebook_url: Union[AnyHttpUrl, str] = Field(max_length=URL_LEN)
    youtube_url: Union[AnyHttpUrl, str] = Field(max_length=URL_LEN)
    statement_for_admission: Optional[Union[AnyHttpUrl, FilePath]] = Field(max_length=URL_LEN)
    official_info: Optional[Union[AnyHttpUrl, FilePath]] = Field(max_length=URL_LEN)


class ContactsUpdateSchema(BaseModel):
    map_url: Optional[Union[AnyHttpUrl, str]]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    facebook_url: Optional[Union[AnyHttpUrl, str]]
    youtube_url: Optional[Union[AnyHttpUrl, str]]
    statement_for_admission: Optional[UploadFile] = None
    official_info: Optional[UploadFile] = None

    @classmethod
    def as_form(
        cls,
        map_url: AnyHttpUrl = Form(None, max_length=URL_LEN),
        address: str = Form(None, max_length=ADDRESS_LEN),
        phone: str = Form(None, max_length=PHONE_LEN, pattern=r"^(\+?38)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$|^$"),
        email: EmailStr = Form(None, max_length=MAIL_LEN),
        facebook_url: AnyHttpUrl = Form(None, max_length=URL_LEN),
        youtube_url: AnyHttpUrl = Form(None, max_length=URL_LEN),
        statement_for_admission: UploadFile = None,
        official_info: UploadFile = None,
    ):
        return cls(
            map_url=map_url,
            address=address,
            phone=phone,
            email=email,
            facebook_url=facebook_url,
            youtube_url=youtube_url,
            statement_for_admission=statement_for_admission,
            official_info=official_info,
        )
