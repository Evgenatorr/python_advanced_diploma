from typing import AsyncGenerator

from src.database.session_manager import db_manager


async def get_async_session() -> AsyncGenerator:
    """
    Функция получения асинхронно сессии
    :return: AsyncSession
    """

    async with db_manager.async_session() as session:
        yield session
