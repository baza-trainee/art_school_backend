import os

import cloudinary
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig


load_dotenv()

IS_PROD = False

cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)


BASE_URL = os.environ.get("BASE_URL")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


if IS_PROD:
    DB_HOST = "postgres"
    REDIS_HOST = "redis"
    # REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    CACHE_PREFIX = "fastapi-cache"

HOUR = 3600
DAY = HOUR * 24
HALF_DAY = HOUR * 12
MONTH = DAY * 30

SECRET_AUTH = os.environ.get("SECRET_AUTH")

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

mail_config = ConnectionConfig(
    MAIL_USERNAME=EMAIL_USER,
    MAIL_PASSWORD=EMAIL_PASSWORD,
    MAIL_FROM=EMAIL_USER,
    MAIL_PORT=587,
    MAIL_SERVER=EMAIL_HOST,
    MAIL_FROM_NAME="Art School",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

ALLOW_METHODS = ["GET", "POST", "OPTIONS", "DELETE", "PATCH"]
ALLOW_HEADERS = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
]
# "https://art-school-frontend.vercel.app",
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

API_PREFIX = "/api/v1"
COOKIE_NAME = "art_school"
