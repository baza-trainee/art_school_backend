from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime

from src.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(300))
    text = Column(String(2000))
    photo = Column(String)
    created_at: datetime = Column(DateTime, default=func.now())
