from sqlalchemy import Column, Integer, String

from src.database.database import Base


class SliderMain(Base):
    __tablename__ = "slider_main"

    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    description = Column(String(150))
    photo = Column(String, nullable=False)

    # id = Column(Integer, primary_key=True)
    # title = Column(String, nullable=True)  # Поле может быть пустым в базе данных
    # description = Column(String, nullable=True)  # Также может быть пустым
    # photo = Column(String, nullable=False)
