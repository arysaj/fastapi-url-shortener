from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import RedirectResponse

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.url_schemas import URLBaseSchema, URLInfoSchema
from services.url_service import UrlService
from configs.database import get_async_session

url_router = APIRouter(prefix="/url", tags=["url"])


@url_router.post("/", status_code=201, response_model=URLInfoSchema)
async def create_url(
    url: Annotated[URLBaseSchema, Body()],
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> URLInfoSchema:
    service = UrlService(db_session)
    return await service.create_url(url)


@url_router.get("/{url_key}", status_code=302, response_class=RedirectResponse)
async def forward_to_target_url(
    url_key: str,
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    request: Request,
) -> RedirectResponse:
    service = UrlService(db_session)
    return await service.forward_to_target_url(url_key, request)
