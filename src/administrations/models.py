from sqlalchemy import Column, Integer, String

from src.database.database import Base


class SchoolAdministration(Base):
    __tablename__ = "school_administrations"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(length=150))
    position = Column(String(length=2000))
    photo = Column(String(length=300))
