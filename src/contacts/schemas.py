from pydantic import BaseModel


class ContactsSchema(BaseModel):
    map_url: str
    address: str
    phone: str
    email: str
    facebook_url: str
    youtube_url: str
    admission_info_url: str
    statute_url: str
    legal_info_url: str
