from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from src.auth.auth_config import CURRENT_SUPERUSER
from src.database import get_async_session
from src.exceptions import PASSWORD_STRENGTH_ERROR
from src.auth.models import User
from src.database import get_async_session
from .manager import get_user_manager


password_router = APIRouter(prefix="/auth", tags=["Auth"])


@password_router.post("/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    new_password_confirm: str,
    user: User = Depends(CURRENT_SUPERUSER),
    session: AsyncSession = Depends(get_async_session),
    user_manager=Depends(get_user_manager),
):
    try:
        await user_manager.validate_password(password=new_password_confirm, user=user)
    except:
        raise HTTPException(status_code=400, detail=PASSWORD_STRENGTH_ERROR)
    password_helper = PasswordHelper()
    if new_password != new_password_confirm:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    verified, updated = password_helper.verify_and_update(
        old_password, user.hashed_password
    )
    if not verified:
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    query = (
        update(User)
        .where(User.id == user.id)
        .values(hashed_password=password_helper.hash(new_password))
    )
    await session.execute(query)
    await session.commit()
    return {"detail": "Successfully changed password"}
