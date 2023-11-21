from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from admin import ContactsView
from src.utils import lifespan
from src.database import engine
from src.auth.auth_config import auth_backend, fastapi_users
from src.contacts.routers import router as router_contacts
from src.department.routers import (
    music_router,
    fine_arts_router,
    theatrical_router,
    vocal_choir_router,
    choreographic_router,
)

from src.news.routers import news_router
from src.posters.routers import posters_router


app = FastAPI(title="School", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_contacts, prefix="/api/v1")
app.include_router(music_router, prefix="/api/v1")
app.include_router(fine_arts_router, prefix="/api/v1")
app.include_router(theatrical_router, prefix="/api/v1")
app.include_router(vocal_choir_router, prefix="/api/v1")
app.include_router(choreographic_router, prefix="/api/v1")
app.include_router(news_router, prefix="/api/v1")
app.include_router(posters_router, prefix="/api/v1")


origins = [
    "http://localhost:3000",
    "https://art-school-frontend.vercel.app",
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
admin = Admin(app=app, engine=engine, title="Художня Школа")
admin.add_view(ContactsView)
