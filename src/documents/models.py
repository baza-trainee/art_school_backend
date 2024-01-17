from sqlalchemy import Column, Integer, String, Boolean

from src.database.database import Base


class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    doc_name = Column(String(100), nullable=False, unique=True)
    doc_path = Column(String(300), nullable=False)
    is_pinned = Column(Boolean)
