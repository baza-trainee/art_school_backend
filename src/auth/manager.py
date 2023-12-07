from re import search
from typing import Optional, Union

from fastapi import BackgroundTasks, Depends, HTTPException, Request, Response, status
from fastapi_users import BaseUserManager, IntegerIDMixin, InvalidPasswordException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from src.config import settings
from src.database.database import get_async_session
from src.auth.schemas import UserCreate
from src.exceptions import (
    AFTER_LOGIN,
    AFTER_REGISTER,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_LEN_ERROR,
    PASSWORD_STRENGTH_ERROR,
    PASSWORD_UNIQUE_ERROR,
)


def check_password_strength(password: str):
    """
    Checks if password is a combination of
    lowercase, uppercase, number and special symbol.
    """
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!])[A-Za-z\d@#$%^&+=!]*$"
    if not search(regex, password):
        return False
    return True


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_AUTH
    verification_token_secret = settings.SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(AFTER_REGISTER % user.email)

    async def validate_password(
        self, password: str, user: Union[UserCreate, User]
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(reason=PASSWORD_LEN_ERROR)
        if user.email in password:
            raise InvalidPasswordException(reason=PASSWORD_UNIQUE_ERROR)

        if not check_password_strength(password):
            raise InvalidPasswordException(reason=PASSWORD_STRENGTH_ERROR)

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ) -> None:
        print(AFTER_LOGIN)

    def write_notification(email: str, message=""):
        with open("log.txt", mode="w") as email_file:
            content = f"notification for {email}: {message}"
            email_file.write(content)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
        background_tasks: BackgroundTasks = BackgroundTasks(),
    ):
        from src.auth.utils import send_reset_email

        # background_tasks.add_task(await send_reset_email(user.email, token))  #  Uncomment this for production
        raise HTTPException(
            status_code=200, detail={"status": "success", "message": f"{token}"}
        )

    async def on_after_reset_password(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        raise HTTPException(
            status_code=200,
            detail={"status": "success", "message": PASSWORD_CHANGE_SUCCESS},
        )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
