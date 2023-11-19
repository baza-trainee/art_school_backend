from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from src.config import COOKIE_NAME, SECRET_AUTH
from .manager import get_user_manager
from .models import User


lifetime = 60 * 60 * 24 * 15  # 15 days

cookie_transport = CookieTransport(cookie_name=COOKIE_NAME, cookie_max_age=lifetime)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=lifetime)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()