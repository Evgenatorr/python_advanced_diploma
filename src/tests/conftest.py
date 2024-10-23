import os
import pytest

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

os.environ["START"] = "test"
from src.loader import app
from config import settings
from src.database.session_manager import db_manager
from src.database.models.base_model import MyBase


@pytest.fixture(scope="session")
async def init_db():
    """
    Фикстура для инициализации и очистки тестовой базы данных.
    """
    async with LifespanManager(app):
        async with db_manager.connect() as connection:
            await connection.run_sync(MyBase.metadata.drop_all)
            await connection.run_sync(MyBase.metadata.create_all)
        yield
        async with db_manager.connect() as connection:
            await connection.run_sync(MyBase.metadata.drop_all)


# @pytest.fixture(scope="session")
# async def db_session(test_db):
#     """
#     Фикстура для предоставления сессии базы данных в тестах.
#     """
#
#     async with db_manager.async_session() as session:
#         yield session


@pytest.fixture(scope="function")
async def async_client(init_db):
    """
    Фикстура для асинхронного клиента приложения.
    """
    async with LifespanManager(app) as manager:
        async with AsyncClient(transport=ASGITransport(app=manager.app), base_url=settings.APP_BASE_URL) as client:
            yield client
