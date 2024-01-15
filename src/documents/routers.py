from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from fastapi_cache.decorator import cache

# from src.config import HALF_DAY
# from src.database.redis import invalidate_cache, my_key_builder
from src.auth.models import User
from src.database.database import get_async_session
from src.auth.auth_config import CURRENT_SUPERUSER
from .models import Documents
from .schemas import DocumentCreateSchema, DocumentSchema, DocumentUpdateSchema
from .service import (
    get_docs_list,
    get_doc_by_id,
    create_document,
    update_document,
    delete_record,
)


docs_router = APIRouter(prefix="/documents", tags=["Documents"])


@docs_router.get("", response_model=List[DocumentSchema])
# @cache(expire=HALF_DAY, key_builder=my_key_builder)
async def get_documents_list(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_docs_list(Documents, session)


@docs_router.get("/{id}", response_model=DocumentSchema)
# @cache(expire=HALF_DAY, key_builder=my_key_builder)
async def get_document_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_doc_by_id(Documents, session, id)


@docs_router.post("", response_model=DocumentSchema)
async def post_document(
    document: DocumentCreateSchema = Depends(DocumentCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_documents_list")
    return await create_document(document, Documents, session)


@docs_router.patch("/{id}", response_model=DocumentSchema)
async def partial_update_document(
    id: int,
    background_tasks: BackgroundTasks,
    document: DocumentUpdateSchema = Depends(DocumentUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_document_by_id", id)
    # await invalidate_cache("get_documents_list")
    return await update_document(id, document, Documents, session, background_tasks)


@docs_router.delete("/{id}")
async def delete_document(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_documents_list")
    # await invalidate_cache("get_document_by_id", id)
    return await delete_record(id, Documents, session)
