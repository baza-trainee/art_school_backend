from sqlalchemy import Column, Integer, String

from src.database import Base


class DepartmentBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    sub_department_name = Column(String(300))
    description = Column(String(2000))
    photo = Column(String)


class MusicDepartment(DepartmentBase):
    __tablename__ = "music_department"


class VocalChoirDepartment(DepartmentBase):
    __tablename__ = "vocal_choir_department"


class ChoreographicDepartment(DepartmentBase):
    __tablename__ = "choreographic_department"


class FineArtsDepartment(DepartmentBase):
    __tablename__ = "fine_arts_department"


class TheatricalDepartment(DepartmentBase):
    __tablename__ = "theatrical_department"
