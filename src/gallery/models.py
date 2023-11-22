import datetime

from sqlalchemy import Column, DATETIME, Integer, String, Boolean, func

from src.database import Base


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True)
    is_video = Column(Boolean)
    pinned_position = Column(Integer, nullable=True)
    media = Column(String, nullable=False)
    created_at: datetime = Column(DATETIME, server_default=func.now())
