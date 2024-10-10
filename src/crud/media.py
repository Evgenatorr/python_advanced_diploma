from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.media_model import Media


class MediaCrud:

    def __init__(self, model: Type[Media]) -> None:
        self.model: Type[Media] = model

    async def get(
        self, session: AsyncSession, media_id: int | list[int]
    ) -> Media | None:
        """
        Функция получения Media объекта из таблицы по первичному ключу
        :param session: асинхронная сессия базы данных
        :param media_id: первичный ключ таблицы
        :return: Media
        """

        query: Media | None = await session.get(self.model, media_id)
        return query

    async def post(self, session: AsyncSession, media_path) -> Media:
        """
        Функция добавления записи в таблицу media
        :param session: асинхронная сессия базы данных
        :param media_path: путь до картинки загруженная пользователем
        :return: Media
        """
        media: Media = self.model(
            file_link=media_path,
        )
        session.add(media)
        await session.commit()
        await session.refresh(media)
        return media

    async def delete(self, session: AsyncSession, media_id: int) -> Media | None:
        """
        Функция удаления записи из таблицы media по первичному ключу
        :param session: асинхронная сессия базы данных
        :param media_id: первичный ключ таблицы
        :return: Media | None
        """

        db_obj: Media | None = await self.get(session=session, media_id=media_id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()

        return db_obj


media_crud: MediaCrud = MediaCrud(Media)
