from typing import AsyncGenerator
import os
import pytest
import asyncio

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from src.loader import app
from src.database.session_manager import db_manager
from src.database.models import user_model, base_model
from logs_conf.logging_test_conf import TEST_LOGGING_CONFIG
from logs_conf.log_utils import logger, setup_logging
os.environ["MODE"] = "test"


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def configure_logging_for_tests():
    """
    Фикстура для настройки логирования во время тестов.
    """

    setup_logging(TEST_LOGGING_CONFIG)
    logger.info("Logging initialized for tests")
    yield
    logger.info("Logging for tests finished")


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator:
    """
    Фикстура для предоставления сессии базы данных в тестах.
    """
    async with LifespanManager(app):
        async with db_manager.async_session() as session:
            yield session


@pytest.fixture(scope="session")
async def init_db(db_session: AsyncSession):
    """
    Фикстура для инициализации и очистки тестовой базы данных.
    """
    async with LifespanManager(app):
        async with db_manager.connect() as connection:
            await connection.run_sync(base_model.MyBase.metadata.drop_all)
            await connection.run_sync(base_model.MyBase.metadata.create_all)

        user = user_model.User(
            name='test_name',
            api_key='test'
        )
        db_session.add(user)
        await db_session.commit()

        yield
        async with db_manager.connect() as connection:
            await connection.run_sync(base_model.MyBase.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_client(init_db):
    """
    Фикстура для асинхронного клиента приложения.
    """
    async with LifespanManager(app) as manager:
        async with AsyncClient(
                transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as client:
            yield client
