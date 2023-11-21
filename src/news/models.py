from sqlalchemy import Column, Integer, String, Date
from datetime import date

from src.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    photo = Column(String)
    created_at = Column(Date, default=date.today)
