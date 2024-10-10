import contextlib
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._async_sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def init(self, db_url: str) -> None:
        """
        Функция инициализации базы данных
        :param db_url: url базы данных
        :return: None
        """
        # настроим аргументы подключения при необходимости
        if "postgresql" in db_url:
            connect_args: dict[str, int | str] = {
                # "statement_cache_size": 0,
                # "prepared_statement_cache_size": 0,
            }
        else:
            connect_args = {}
        self._engine = create_async_engine(
            url=db_url,
            pool_pre_ping=True,
            connect_args=connect_args,
            echo=False,
        )
        self._async_sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._async_sessionmaker = None

    @contextlib.asynccontextmanager
    async def async_session(self) -> AsyncIterator[AsyncSession]:
        if self._async_sessionmaker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._async_sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


db_manager: DatabaseSessionManager = DatabaseSessionManager()
