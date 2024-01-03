from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func

from src.database.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    text = Column(String(2000))
    photo = Column(String(300))
    created_at: datetime = Column(DateTime, default=func.now())
