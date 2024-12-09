from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.database.models.like_model import Like


class LikeCrud(BaseCrud[Like]):
    async def get_by_user_id_and_tweet_id(
            self, session: AsyncSession, tweet_id: int, user_id: int
    ) -> Optional[Like]:
        """
        Функция получения объекта Like по id пользователя и id твита
        """
        query = await session.execute(
            select(self.model).where(
                self.model.tweet_id == tweet_id,
                self.model.user_id == user_id,
            )
        )
        return query.scalar()


like_crud = LikeCrud(Like)
