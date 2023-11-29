import os

from faker import Faker
import cloudinary
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig


load_dotenv()
faker = Faker()
desc = faker.text()

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
}

API_PREFIX = "/api/v1"
COOKIE_NAME = "art_school"
DEPARTMENTS = [
    "Музичне відділення",
    "Вокально-хорове відділення",
    "Хореографічне відділення",
    "Театральне відділення",
    "Образотворче відділення",
    "Дошкільне та підготовче відділення",
]
SUB_DEPARTMENTS = [
    # Музичне відділення
    {
        "sub_department_name": "Струнний відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Духовий відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Народний відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Теоретичний відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Джазовий відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Відділ спеціалізованого та загального фортепіано",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Відділ концертмейстрів",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Відділ камерного ансамблю",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Історія мистецтв",
        "description": desc,
        "main_department_id": 1,
    },
    # Вокально-хорове відділення
    {
        "sub_department_name": "Хоровий відділ",
        "description": desc,
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ сольного співу",
        "description": desc,
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ естрадного вокалу",
        "description": desc,
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ народного співу",
        "description": desc,
        "main_department_id": 2,
    },
    # Хореографічне відділення
    {
        "sub_department_name": "Відділ класичного танцю",
        "description": desc,
        "main_department_id": 3,
    },
    {
        "sub_department_name": "Відділ народного танцю",
        "description": desc,
        "main_department_id": 3,
    },
    {
        "sub_department_name": "Відділ сучасного танцю",
        "description": desc,
        "main_department_id": 3,
    },
    # Театральне відділення
    {
        "sub_department_name": "Псевдо відділ Театрального відділення",
        "description": desc,
        "main_department_id": 4,
    },
    # Образотворче відділення
    {
        "sub_department_name": "Розвиток образотворчої уяви та мислення 1-4 класи",
        "description": desc,
        "main_department_id": 5,
    },
    {
        "sub_department_name": "Живопис 4-7 класи",
        "description": desc,
        "main_department_id": 5,
    },
    {
        "sub_department_name": "Дизайнерсько-графічний напрямок 4-7 класи",
        "description": desc,
        "main_department_id": 5,
    },
    # Дошкільне та підготовче відділення
    {
        "sub_department_name": "Псевдо відділ Дошкільного та підготовчого відділення",
        "description": desc,
        "main_department_id": 6,
    },
]
CONTACTS = {"address": "вул.Бульварно-Кудрявська, 2", "phone": "+38(097)290-79-40"}

SLIDES = [
    {
        "title": "Slide1",
        "description": "Slide1 Test description",
    },
    {
        "title": " Slide2",
        "description": "Slide2 Test description",
    },
]
