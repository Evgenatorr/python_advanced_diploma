from typing import Type

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.api_key_model import ApiKey


class ApiKeyCrud:

    def __init__(self, model: Type[ApiKey]) -> None:
        self.model: Type[ApiKey] = model

    async def get_by_apikey(self, session: AsyncSession, api_key: str) -> ApiKey | None:
        """
        Функция получения ApiKey объекта по столбцу api_key из базы данных
        :param api_key: ключ аутентификации пользователя
        :param session: асинхронная сессия базы данных
        :return: ApiKey
        """
        query: Result[tuple[ApiKey]] = await session.execute(
            select(self.model).where(self.model.api_key == api_key)
        )
        return query.scalar()

    async def post(self, session: AsyncSession, api_key_data: dict) -> ApiKey:
        """

        :param session: асинхронная сессия базы данных
        :param api_key_data: данные для добавления записи в таблицу
        :return: ApiKey
        """
        api_key_model: ApiKey = self.model(**api_key_data)
        session.add(api_key_model)
        await session.commit()
        await session.refresh(api_key_model)
        return api_key_model


api_key_crud: ApiKeyCrud = ApiKeyCrud(ApiKey)
