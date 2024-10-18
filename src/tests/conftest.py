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

test_base = MyBase
# @pytest.fixture(scope='session')
# async def init_db():
#     db_manager.init(get_database_url())
#     yield
#     await db_manager.close()

@pytest.fixture(scope='session')
async def init_db():
    print(os.environ["START"])
    engine = create_async_engine(url=settings.db_test.test_url_db_pgsync, pool_pre_ping=True,)
    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False,)
    session = session_maker()

    async with engine.begin() as conn:
        await conn.run_sync(MyBase.metadata.create_all)
    await session.close()
    await engine.dispose()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(MyBase.metadata.drop_all)

@pytest.fixture(scope='function')
async def client(init_db):
# def client() -> TestClient:
#     with TestClient(
#             app=app, base_url=settings.APP_BASE_URL
#     ) as c:
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url=settings.APP_BASE_URL
    ) as c:
        yield c
