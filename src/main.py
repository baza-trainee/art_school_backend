from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from admin import ContactsView
from src.contacts.routers import router as router_contacts
from src.department.routers import router as router_departments
from src.contacts.utils import lifespan
from src.database import engine


app = FastAPI(title="School", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_contacts, prefix="/api/v1")
app.include_router(router_departments, prefix="/api/v1")

admin = Admin(app=app, engine=engine, title="Художня Школа")
admin.add_view(ContactsView)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
