from typing import Optional, Union

from fastapi import Form, UploadFile
from pydantic import BaseModel, AnyHttpUrl, Field, FilePath, constr

from .models import Documents


DOC_NAME_LEN = Documents.doc_name.type.length


class DocumentSchema(BaseModel):
    id: int = Field(..., ge=1)
    doc_name: constr(max_length=DOC_NAME_LEN)
    doc_path: Optional[Union[AnyHttpUrl, FilePath]]


class DocumentCreateSchema(BaseModel):
    doc_name: str
    doc_path: UploadFile

    @classmethod
    def as_form(
        cls,
        doc_path: UploadFile,
        doc_name: str = Form(max_length=DOC_NAME_LEN),
    ):
        return cls(doc_name=doc_name, doc_path=doc_path)


class DocumentUpdateSchema(BaseModel):
    doc_name: Optional[str] = None
    doc_path: Optional[UploadFile] = None

    @classmethod
    def as_form(
        cls,
        doc_name: str = Form(None, max_length=DOC_NAME_LEN),
        doc_path: UploadFile = None,
    ):
        return cls(doc_name=doc_name, doc_path=doc_path)
