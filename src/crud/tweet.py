from typing import Type, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, func, desc
from fastapi.encoders import jsonable_encoder

from src.database.models.tweet_model import Tweet
from src.schemas.tweet import TweetUpdateRequest


class TweetCrud:

    def __init__(self, model: Type[Tweet]) -> None:
        self.model: Type[Tweet] = model

    async def get(self, session: AsyncSession, tweet_id: int) -> Tweet | None:
        """
        Функция получения Tweet объекта из таблицы по первичному ключу
        :param session: асинхронная сессия базы данных
        :param tweet_id: первичный ключ таблицы
        :return: Tweet
        """

        query: Tweet | None = await session.get(self.model, tweet_id)
        return query

    async def get_list_by_user_id(self, session: AsyncSession, user_id: int) -> Sequence[Tweet]:
        """
        Функция получения объекта Tweet из таблицы по id пользователя
        :param session: асинхронная сессия базы данных
        :param user_id: id пользователя
        :return: Sequence[Tweet]
        """

        query: Result[tuple[Tweet]] = await session.execute(
            select(self.model)
            .where(self.model.author_id == user_id)
        )
        return query.scalars().all()

    async def get_list(self, session: AsyncSession) -> Sequence[Tweet]:
        """
        Функция получения списка объектов Tweet из таблицы
        :param session: асинхронная сессия базы данных
        :return: Sequence[Tweet]
        """

        query: Result[tuple[Tweet]] = await session.execute(select(self.model))
        return query.scalars().all()

    async def post(self, session: AsyncSession, tweet_data, author_id: int) -> Tweet:
        """
        Функция создания новой записи в таблице tweet
        :param session: асинхронная сессия базы данных
        :param tweet_data: данные для добавления записи в таблицу
        :param author_id: id автора твита
        :return: Tweet
        """

        tweet: Tweet = self.model(
            **tweet_data
        )
        tweet.author_id = author_id
        session.add(tweet)
        await session.commit()
        await session.refresh(tweet)
        return tweet

    async def delete(self, session: AsyncSession, tweet_id: int) -> Tweet | None:
        """
        Функция удаления записи из таблицы tweet по первичному ключу
        :param session: асинхронная сессия базы данных
        :param tweet_id: первичный ключ таблицы
        :return: Tweet | None
        """

        db_obj: Tweet | None = await self.get(session=session, tweet_id=tweet_id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()

        return db_obj

    @staticmethod
    async def update(session: AsyncSession, current_tweet_data: Tweet, new_tweet_data: TweetUpdateRequest) -> Tweet:
        """
        Функция обновления записи в таблице tweet
        :param session: асинхронная сессия базы данных
        :param current_tweet_data: старые данные из таблицы
        :param new_tweet_data: новые данные из таблицы
        :return: Tweet
        """

        tweet_data = jsonable_encoder(current_tweet_data)
        update_data: dict = new_tweet_data.model_dump(exclude_unset=True)

        for field in tweet_data:
            if field in update_data:
                setattr(current_tweet_data, field, update_data[field])  # current_tweet_data.field = update_data[field]

        session.add(current_tweet_data)
        await session.commit()
        await session.refresh(current_tweet_data)
        return current_tweet_data


tweet_crud: TweetCrud = TweetCrud(Tweet)
