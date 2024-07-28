from fastapi import APIRouter, Request, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from configs.database import get_async_session
from schemas.url_schemas import URLInfoSchema
from services.admin_service import AdminService

admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.get("/{secret_key}", response_model=URLInfoSchema)
async def get_url_info(
    secret_key: str,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> URLInfoSchema:
    service = AdminService(db_session)
    return await service.get_url_info(secret_key, request)


@admin_router.delete("/{secret_key}")
async def delete_url(
    secret_key: str,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict:
    service = AdminService(db_session)
    return await service.delete_url(secret_key, request)
