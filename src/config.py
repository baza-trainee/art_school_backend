import cloudinary
from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


IS_PROD = False

PHOTO_FORMATS = [
    "application/pdf",
    "image/webp",
    "image/png",
    "image/jpeg",
]


class Settings(BaseSettings):
    # BASE_URL: str
    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    SECRET_AUTH: str
    EMAIL_HOST: str
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    # REDIS_HOST: str
    # REDIS_PORT: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

PROJECT_NAME = "Art School"
COOKIE_NAME = "Art_School"
API_PREFIX = "/api/v1"
DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET,
)

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USER,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_USER,
    MAIL_PORT=587,
    MAIL_SERVER=settings.EMAIL_HOST,
    MAIL_FROM_NAME=PROJECT_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

if IS_PROD:
    DB_HOST = "postgres"
    REDIS_HOST = "redis"
    REDIS_PORT = settings.REDIS_PORT
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    CACHE_PREFIX = "fastapi-cache"

HOUR = 3600
DAY = HOUR * 24
HALF_DAY = HOUR * 12
MONTH = DAY * 30

ALLOW_METHODS = ["GET", "POST", "PUT", "OPTIONS", "DELETE", "PATCH"]
ALLOW_HEADERS = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
]
ORIGINS = ["*"]
SWAGGER_PARAMETERS = {
    "syntaxHighlight.theme": "obsidian",
    "tryItOutEnabled": True,
    "displayOperationId": True,
    "filter": True,
    "requestSnippets": True,
    "defaultModelsExpandDepth": -1,
    "docExpansion": "none",
}
