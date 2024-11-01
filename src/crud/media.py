from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.media_model import Media
from src.crud.base_crud import BaseCrud


class MediaCrud(BaseCrud[Media]):
    async def post(self, session: AsyncSession, media_path: str) -> Media:
        """
        Функция добавления записи в таблицу media
        """
        media: Media = self.model(file_link=media_path)
        session.add(media)
        await session.commit()
        await session.refresh(media)
        return media


media_crud = MediaCrud(Media)
