import contextlib
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine,
                                    AsyncConnection)

from logs_conf.log_utils import logger


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
        logger.debug(f"Initializing DatabaseSessionManager with URL: {db_url}")

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        # self._engine = None
        # self._async_sessionmaker = None

    @contextlib.asynccontextmanager
    async def async_session(self) -> AsyncIterator[AsyncSession]:
        if self._async_sessionmaker is None:
            logger.debug("Attempting to access async_session without initialization.")
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._async_sessionmaker() as session:
            try:
                logger.debug("Session started")
                yield session
            except Exception as exc:
                logger.error(exc)
                await session.rollback()
                raise
            finally:
                await session.close()
                logger.debug("Session closed")

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            try:
                logger.debug("Connection started")
                yield connection
            except Exception as exc:
                logger.error("Connection error", exc_info=exc)
                await connection.rollback()
                raise
            finally:
                logger.debug("Connection closed")


db_manager: DatabaseSessionManager = DatabaseSessionManager()
