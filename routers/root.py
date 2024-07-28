from fastapi import APIRouter, Depends
from typing import Annotated

from configs.app_settings import get_settings, Settings

root_router = APIRouter(tags=["root"])


@root_router.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]):
    return {"status": "ok", "detail": f"Welcome to the {settings.app_name} API."}
