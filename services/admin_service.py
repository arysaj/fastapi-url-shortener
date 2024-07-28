from fastapi import HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.url_repository import URlRepository
from schemas.url_schemas import URLInfoSchema
from configs.app_settings import get_settings


class AdminService:
    def __init__(self, session: AsyncSession):
        self.repository = URlRepository(session)
        self.settings = get_settings()

    @staticmethod
    def raise_not_found(request: Request):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL {request.url} doesn't exist",
        )

    async def get_url_info(self, secret_key: str, request: Request) -> URLInfoSchema:
        db_url = await self.repository.get_url_by_secret_key(secret_key)

        if not db_url:
            self.raise_not_found(request)

        return URLInfoSchema(
            url=f"{self.settings.base_url}/url/{db_url.key}",
            admin_url=f"{self.settings.base_url}/admin/{db_url.secret_key}",
            target_url=db_url.target_url,
            is_active=db_url.is_active,
            clicks=db_url.clicks,
        )

    async def delete_url(self, secret_key: str, request: Request) -> dict:
        db_url = await self.repository.get_url_by_secret_key(secret_key)

        if not db_url:
            self.raise_not_found(request)

        await self.repository.deactivate_url(db_url)

        return {
            "status": "ok",
            "detail": f"Successfully deleted shortened URL for {db_url.target_url}",
        }
