from sqlalchemy import Column, Integer, String

from src.database.database import Base


class SchoolAdministration(Base):
    __tablename__ = "school_administrations"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(length=60))
    position = Column(String(length=120))
    photo = Column(String(length=500))
