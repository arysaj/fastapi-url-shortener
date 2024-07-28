from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.url import URL
from schemas.url_schemas import URLAddSchema


class URlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: URLAddSchema) -> URL:
        db_url = URL(**data.model_dump())
        self.session.add(db_url)
        await self.session.commit()
        await self.session.refresh(db_url)

        return db_url

    async def get_url_by_key(self, key: str) -> URL | None:
        stmt = select(URL).filter(and_(URL.key == key, URL.is_active))
        res = await self.session.scalars(stmt)
        return res.first()

    async def get_url_by_secret_key(self, secret_key: str) -> URL | None:
        stmt = select(URL).filter(and_(URL.secret_key == secret_key, URL.is_active))
        res = await self.session.scalars(stmt)

        return res.first()

    async def update_db_clicks(self, db_url: URL) -> URL:
        db_url.clicks += 1
        await self.session.commit()
        await self.session.refresh(db_url)

        return db_url

    async def deactivate_url(self, db_url: URL) -> URL:
        db_url.is_active = False
        await self.session.commit()
        await self.session.refresh(db_url)

        return db_url
