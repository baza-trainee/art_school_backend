from sqlalchemy import Column, Integer, String

from src.database.database import Base


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    map_url = Column(String(length=1000))
    address = Column(String(length=300))
    phone = Column(String(length=50))
    email = Column(String(length=50))
    facebook_url = Column(String(length=1000))
    youtube_url = Column(String(length=1000))
    statement_for_admission = Column(String(length=1000))
    official_info = Column(String(length=1000))
