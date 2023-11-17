from sqlalchemy import Column, Integer, String

from src.database import Base


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    map_url = Column(String)
    address = Column(String)
    phone = Column(String(length=50))
    email = Column(String(length=50))
    facebook_url = Column(String)
    youtube_url = Column(String)
    admission_info_url = Column(String)
    statute_url = Column(String)
    legal_info_url = Column(String)
