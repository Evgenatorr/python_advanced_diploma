from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.media_model import Media


class MediaCrud:

    def __init__(self, model: Type[Media]):
        self.model = model

    async def get(self, session: AsyncSession, media_id: int):
        query = await session.get(self.model, media_id)
        return query

    async def post(self, session: AsyncSession, media_path):
        media = self.model(
            file_link=media_path,
        )
        session.add(media)
        await session.commit()
        await session.refresh(media)
        return media

    async def delete(self, session: AsyncSession, media_id: int):
        db_obj = await session.get(self.model, media_id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()

        return db_obj


media_crud = MediaCrud(Media)
