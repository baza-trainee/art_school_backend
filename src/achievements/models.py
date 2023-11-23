from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Boolean, func, ForeignKey

from src.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id: int = Column(Integer, primary_key=True)
    is_pinned: bool = Column(Boolean, nullable=False)
    media: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    sub_department: int = Column(Integer, ForeignKey("sub_departments.id"), nullable=True)
    created_at: datetime = Column(DateTime, default=func.now())
