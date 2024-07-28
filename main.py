from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import root_router, url_router, admin_router
from metadata.tags import tags
from configs.app_settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, openapi_tags=tags)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://hochu_otdohnut.serveo.net:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(url_router)
app.include_router(admin_router)
