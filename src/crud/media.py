from typing import Sequence, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models.media_model import Media
from src.crud.base_crud import BaseCrud


class MediaCrud(BaseCrud[Media]):
    async def get_list_by_media_ids(
            self, session: AsyncSession, media_ids: List[int] | None
    ) -> Sequence[Media] | None:
        """
        Функция получения списка медиа по id
        """
        if media_ids is None:
            return None
        stmt = (
            select(self.model)
            .filter(self.model.id.in_(media_ids))
        )

        result = await session.execute(stmt)
        return result.scalars().all()


media_crud = MediaCrud(Media)
