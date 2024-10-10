from typing import Type

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.like_model import Like


class LikeCrud:

    def __init__(self, model: Type[Like]) -> None:
        self.model: Type[Like] = model

    async def get(self, session: AsyncSession, like_id: int) -> Like | None:
        """
        Функция получения объекта Like по первичному ключу
        :param session: асинхронная сессия базы данных
        :param like_id: первичный ключ таблицы
        :return: Like | None
        """

        query: Like | None = await session.get(self.model, like_id)
        return query

    async def get_by_user_id_and_tweet_id(
        self, session: AsyncSession, tweet_id: int, user_id: int
    ) -> Like | None:
        """
        Функция получения объекта Like по id пользователя и id твита
        :param session: асинхронная сессия базы данных
        :param tweet_id: id твита
        :param user_id: id пользователя
        :return: Like
        """

        query: Result[tuple[Like]] = await session.execute(
            select(self.model).where(
                self.model.tweet_id == tweet_id,
                self.model.user_id == user_id,
            )
        )
        return query.scalar()

    async def post(self, session: AsyncSession, like_data) -> Like:
        """
        Функция создания новой записи в таблице like
        :param session: асинхронная сессия базы данных
        :param like_data: данные для добавления записи в таблицу
        :return: Like
        """

        like: Like = self.model(
            **like_data,
        )
        session.add(like)
        await session.commit()
        await session.refresh(like)
        return like

    async def delete(self, session: AsyncSession, like_id: int) -> Like | None:
        """
        Функция удаления записи из таблицы like по первичному ключу
        :param session: асинхронная сессия базы данных
        :param like_id: первичный ключ таблицы
        :return: Like | None
        """

        db_obj: Like | None = await session.get(self.model, like_id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()

        return db_obj


like_crud: LikeCrud = LikeCrud(Like)
