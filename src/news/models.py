from sqlalchemy import Column, Integer, String

from src.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    photo = Column(String)
    
  