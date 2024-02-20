from sqlalchemy import Column, Integer, String

from src.database.database import Base


class SliderMain(Base):
    __tablename__ = "slider_main"

    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    description = Column(String(200))
    photo = Column(String(500), nullable=False)
