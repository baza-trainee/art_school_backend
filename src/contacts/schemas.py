from typing import Optional, Union
from fastapi import Form, UploadFile

from pydantic import (
    BaseModel,
    EmailStr,
    AnyHttpUrl,
    constr,
)

from src.exceptions import INVALID_PHONE


class ContactsSchema(BaseModel):
    map_url: Union[AnyHttpUrl, str]
    address: str
    phone: str
    email: str
    facebook_url: Union[AnyHttpUrl, str]
    youtube_url: Union[AnyHttpUrl, str]
    statement_for_admission: Optional[str]
    official_info: Optional[str]


class ContactsUpdateSchema(ContactsSchema):
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
        map_url: Optional[Union[AnyHttpUrl, constr(pattern=r"^$")]] = Form(None),
        address: Optional[str] = Form(None),
        phone: Optional[
            Union[
                constr(
                    max_length=50,
                    pattern=r"^(\+?38)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$",
                ),
                constr(pattern=r"^$"),
            ]
        ] = Form(None),
        email: Optional[Union[EmailStr, constr(pattern=r"^$")]] = Form(None),
        facebook_url: Optional[Union[AnyHttpUrl, constr(pattern=r"^$")]] = Form(None),
        youtube_url: Optional[Union[AnyHttpUrl, constr(pattern=r"^$")]] = Form(None),
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
