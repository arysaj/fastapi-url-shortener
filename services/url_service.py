import secrets
import string

from fastapi import HTTPException, status, Request
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.url_schemas import URLInfoSchema, URLAddSchema, URLBaseSchema
from configs.app_settings import get_settings
from repositories.url_repository import URlRepository


class UrlService:
    def __init__(self, session: AsyncSession):
        self.repository = URlRepository(session)
        self.settings = get_settings()

    @staticmethod
    def raise_not_found(request: Request):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL {request.url} doesn't exist",
        )

    @classmethod
    def create_random_key(cls, length: int) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(chars) for _ in range(length))

    async def create_unique_random_key(self) -> str:
        key = self.create_random_key(self.settings.length_key)
        while await self.repository.get_url_by_key(key):
            key = self.create_random_key(self.settings.length_key)

        return key

    async def create_url(self, url: URLBaseSchema) -> URLInfoSchema:

        key = await self.create_unique_random_key()
        secret_key = "_".join(
            (key, self.create_random_key(self.settings.length_secret_key))
        )

        data = URLAddSchema(
            target_url=str(url.target_url), key=key, secret_key=secret_key
        )

        db_url = await self.repository.create(data)

        return URLInfoSchema(
            url=f"{self.settings.base_url}/url/{db_url.key}",
            admin_url=f"{self.settings.base_url}/admin/{db_url.secret_key}",
            target_url=db_url.target_url,
            is_active=db_url.is_active,
            clicks=db_url.clicks,
        )

    async def forward_to_target_url(
        self, url_key: str, request: Request
    ) -> RedirectResponse:
        db_url = await self.repository.get_url_by_key(url_key)

        if not db_url:
            self.raise_not_found(request)

        await self.repository.update_db_clicks(db_url)

        return RedirectResponse(db_url.target_url)
