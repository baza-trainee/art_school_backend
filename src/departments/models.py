from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database.database import Base


class MainDepartment(Base):
    __tablename__ = "main_departments"

    id = Column(Integer, primary_key=True)
    department_name = Column(String(300))

    # Вказуємо, що це зовнішній ключ для SubDepartment
    sub_departments = relationship("SubDepartment", back_populates="main_department")


class SubDepartment(Base):
    __tablename__ = "sub_departments"

    id = Column(Integer, primary_key=True)
    sub_department_name = Column(String(300))
    description = Column(String(2000))

    # Вказуємо, що це зовнішній ключ для MainDepartment
    main_department_id = Column(Integer, ForeignKey("main_departments.id"))
    main_department = relationship("MainDepartment", back_populates="sub_departments")
