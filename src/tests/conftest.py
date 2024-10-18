import os

import asyncio

from src.utils.get_db_url import get_database_url

os.environ["START"] = "test"
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import pytest
from httpx import AsyncClient, ASGITransport
from src.database.session_manager import db_manager
from config import settings
from src.loader import app
from src.database.models.base_model import MyBase


# @pytest.fixture(scope='session')
# async def init_db():
#     db_manager.init(get_database_url())
#     yield
#     await db_manager.close()


@pytest.fixture(scope='session')
async def create_db():
    engine = create_async_engine(url=settings.db_test.test_url_db_asyncpg, pool_pre_ping=True, )
    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False,)
    session = session_maker()
    await session.close()
    await engine.dispose()
    async with engine.begin() as conn:
        await conn.run_sync(MyBase.metadata.drop_all)
        await conn.run_sync(MyBase.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(MyBase.metadata.drop_all)


@pytest.fixture(scope='function')
async def client(create_db):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url=settings.APP_BASE_URL
    ) as c:
        yield c
