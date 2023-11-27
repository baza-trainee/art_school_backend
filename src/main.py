from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from src.utils import lifespan
from src.database import engine
from src.contacts.routers import router as router_contacts
from src.administrations.routers import school_admin_router
from src.news.routers import news_router
from src.posters.routers import posters_router
from src.slider_main.routers import slider_main_router
from src.gallery.routers import gallery_router
from src.achievements.routers import achievements_router
from src.auth.routers import auth_router
from src.departments.routers import departments
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

api_routers = [
    auth_router,
    router_contacts,
    gallery_router,
    achievements_router,
    news_router,
    posters_router,
    slider_main_router,
    departments,
    school_admin_router,
]
[app.include_router(router, prefix=API_PREFIX) for router in api_routers]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)

add_pagination(app)
