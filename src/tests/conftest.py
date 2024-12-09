import os
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from logs_conf.log_utils import logger, setup_logging
from logs_conf.logging_test_conf import TEST_LOGGING_CONFIG
from src.database.models import base_model, user_model
from src.database.session_manager import db_manager
from src.loader import app

os.environ["MODE"] = "test"


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
        user2 = user_model.User(
            name='test_name2',
            api_key='test2'
        )
        db_session.add_all((user, user2, ))
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
