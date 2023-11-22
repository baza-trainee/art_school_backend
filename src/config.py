import os

import cloudinary
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

load_dotenv()


cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)

COOKIE_NAME = "art_school"
API_PREFIX = "/api/v1"
BASE_URL = os.environ.get("BASE_URL")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

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

ALLOW_METHODS = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
ALLOW_HEADERS = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
]
ORIGINS = [
    "http://localhost:3000",
    "https://art-school-frontend.vercel.app",
]
SWAGGER_PARAMETERS = {
    "syntaxHighlight.theme": "obsidian",
    "tryItOutEnabled": True,
    "displayOperationId": True,
    "filter": True,
    "requestSnippets": True,
}
