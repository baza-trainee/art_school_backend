from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from fastapi_pagination import add_pagination

from admin import ContactsView
from src.utils import lifespan
from src.database import engine
from src.auth.auth_config import auth_backend, fastapi_users
from src.contacts.routers import router as router_contacts
from src.administrations.routers import school_admin_router
from src.news.routers import news_router
from src.posters.routers import posters_router
from src.gallery.routers import gallery_router
from src.auth.routers import password_router
from src.department.routers import (
    music_router,
    fine_arts_router,
    theatrical_router,
    vocal_choir_router,
    choreographic_router,
)
from src.config import (
    ALLOW_HEADERS,
    ALLOW_METHODS,
    API_PREFIX,
    ORIGINS,
    SWAGGER_PARAMETERS,
)

app = FastAPI(
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title="School",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

for router in [
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    fastapi_users.get_reset_password_router(),
]:
    app.include_router(router, tags=["Auth"], prefix=API_PREFIX)
for router in [
    router_contacts,
    music_router,
    fine_arts_router,
    theatrical_router,
    vocal_choir_router,
    choreographic_router,
    news_router,
    posters_router,
    school_admin_router,
    password_router,
    gallery_router,
]:
    app.include_router(router, prefix=API_PREFIX)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)
admin = Admin(app=app, engine=engine, title="Художня Школа")
admin.add_view(ContactsView)
add_pagination(app)
