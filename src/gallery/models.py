from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Boolean, func, ForeignKey

from src.database import Base


class Gallery(Base):
    __tablename__ = "gallery"

    id: int = Column(Integer, primary_key=True)
    is_video: bool = Column(Boolean, nullable=False)
    is_achivement: bool = Column(Boolean, nullable=False)
    media: str = Column(String, nullable=False)
    pinned_position: int = Column(Integer, nullable=True)
    description: str = Column(String, nullable=True)
    sub_department: int = Column(Integer, ForeignKey("sub_departments.id"), nullable=True)
    created_at: datetime = Column(DateTime, default=func.now())
