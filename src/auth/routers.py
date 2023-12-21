from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi_users import InvalidPasswordException
from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from src.auth.auth_config import CURRENT_SUPERUSER, fastapi_users, auth_backend
from src.database.database import get_async_session
from src.exceptions import (
    OLD_PASS_INCORRECT,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_NOT_MATCH,
)
from src.auth.models import User
from src.database.database import get_async_session
from .manager import get_user_manager


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/change-password")
async def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    new_password_confirm: str = Form(...),
    user: User = Depends(CURRENT_SUPERUSER),
    session: AsyncSession = Depends(get_async_session),
    user_manager=Depends(get_user_manager),
):
    try:
        await user_manager.validate_password(password=new_password_confirm, user=user)
    except InvalidPasswordException as ex:
        raise HTTPException(status_code=400, detail=ex.reason)
    password_helper = PasswordHelper()
    if new_password != new_password_confirm:
        raise HTTPException(status_code=400, detail=PASSWORD_NOT_MATCH)
    verified, updated = password_helper.verify_and_update(
        old_password, user.hashed_password
    )
    if not verified:
        raise HTTPException(status_code=400, detail=OLD_PASS_INCORRECT)
    query = (
        update(User)
        .where(User.id == user.id)
        .values(hashed_password=password_helper.hash(new_password))
    )
    await session.execute(query)
    await session.commit()
    return {"detail": PASSWORD_CHANGE_SUCCESS}


auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True)
)
auth_router.include_router(fastapi_users.get_reset_password_router())
