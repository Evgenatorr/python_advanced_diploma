from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.database.models.media_model import Media


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
