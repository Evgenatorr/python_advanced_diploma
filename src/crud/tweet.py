from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from src.crud.base_crud import BaseCrud
from src.database.models.tweet_model import Tweet
from src.database.models.like_model import Like


class TweetCrud(BaseCrud[Tweet]):
    async def get_list_by_user_id(
            self, session: AsyncSession, user_id: int
    ) -> Sequence[Tweet]:
        """
        Функция получения объекта Tweet из таблицы по id пользователя
        """
        query = await session.execute(
            select(self.model).where(self.model.author_id == user_id)
        )
        return query.scalars().all()

    async def get_tweets_with_tweets_you_follow(
        self, session: AsyncSession, users_id: list[int]
    ) -> Sequence[Tweet]:
        """
        Функция получения твитов с твитами на кого подписан пользователь
        """
        stmt = (
            select(self.model)
            .outerjoin(Like, Like.tweet_id == self.model.id)
            .filter(self.model.author_id.in_(users_id))
            .group_by(self.model.id)
            .order_by(desc(func.count(Like.id)))
        )

        result = await session.execute(stmt)
        return result.scalars().all()


tweet_crud = TweetCrud(Tweet)
