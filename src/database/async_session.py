from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session_manager import db_manager


async def get_async_session() -> AsyncSession:
    """
    Функция получения асинхронно сессии
    :return: AsyncSession
    """

    async with db_manager.gen_async_session() as session:
        yield session
