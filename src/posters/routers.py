from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.utils import disable_installed_extensions_check

# from fastapi_cache.decorator import cache

# from src.config import HALF_DAY
# from src.database.redis import invalidate_cache, my_key_builder
from src.auth.models import User
from src.database.database import get_async_session
from src.auth.auth_config import CURRENT_SUPERUSER
from .models import Poster
from .schemas import PosterSchema, PosterCreateSchema, PosterUpdateSchema
from .service import (
    get_all_posters,
    get_poster_by_id,
    create_poster,
    patch_poster,
    delete_poster_by_id,
)


posters_router = APIRouter(prefix="/posters", tags=["Posters"])


@posters_router.get("", response_model=Page[PosterSchema])
# @cache(expire=HALF_DAY, key_builder=my_key_builder)
async def get_posters_list(
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_posters(Poster, session)
    disable_installed_extensions_check()
    return paginate(result)


@posters_router.get("/{id}", response_model=PosterSchema)
# @cache(expire=HALF_DAY, key_builder=my_key_builder)
async def get_poster(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_poster_by_id(Poster, session, id)


@posters_router.post("", response_model=PosterSchema)
async def post_poster(
    poster_data: PosterCreateSchema = Depends(PosterCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_posters_list")
    return await create_poster(poster_data, Poster, session)


@posters_router.patch("/{poster_id}", response_model=PosterSchema)
async def partial_update_poster(
    poster_id: int,
    photo: Annotated[UploadFile, File()] = None,
    posters_data: PosterUpdateSchema = Depends(PosterUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_poster", poster_id)
    # await invalidate_cache("get_posters_list")
    return await patch_poster(posters_data, Poster, session, photo, poster_id)


@posters_router.delete("/{poster_id}")
async def delete_poster(
    poster_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_poster", poster_id)
    # await invalidate_cache("get_posters_list")
    return await delete_poster_by_id(poster_id, Poster, session)
