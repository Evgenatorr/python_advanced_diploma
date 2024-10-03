import contextlib
from typing import AsyncIterator, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._async_sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def init(self, db_url: str) -> None:
        # Just additional example of customization.
        # you can add parameters to init and so on
        if "postgresql" in db_url:
            # These settings are needed to work with pgbouncer in transaction mode
            # because you can't use prepared statements in such case
            connect_args = {
                "statement_cache_size": 0,
                "prepared_statement_cache_size": 0,
            }
        else:
            connect_args = {}
        self._engine = create_async_engine(
            url=db_url,
            pool_pre_ping=True,
            connect_args=connect_args,
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
    async def gen_async_session(self) -> AsyncIterator[AsyncSession]:
        if self._async_sessionmaker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._async_sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def async_session(self) -> AsyncSession:
        if self._async_sessionmaker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._async_sessionmaker() as session:
            return session


db_manager = DatabaseSessionManager()


async def get_async_session() -> AsyncSession:
    async with db_manager.gen_async_session() as session:
        yield session
