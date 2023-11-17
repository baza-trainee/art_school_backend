from typing import Optional

from pydantic import BaseModel, EmailStr, constr, AnyHttpUrl

from src.utils import as_form_patch


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


@as_form_patch
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
