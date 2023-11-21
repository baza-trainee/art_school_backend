from sqlalchemy import Column, Integer, String

from src.database import Base


class Poster(Base):
    __tablename__ = "posters"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    photo = Column(String)
