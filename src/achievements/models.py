from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey

from src.database.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id: int = Column(Integer, primary_key=True)
    media: str = Column(String(length=300), nullable=False)
    pinned_position: int = Column(Integer, nullable=True)
    description: str = Column(String(length=150), nullable=True)
    sub_department: int = Column(
        Integer, ForeignKey("sub_departments.id"), nullable=True
    )
    created_at: datetime = Column(DateTime, default=func.now())
