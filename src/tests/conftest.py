import os
import pytest
import asyncio

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

os.environ["START"] = "test"
from src.loader import app
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


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


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
        async with AsyncClient(transport=ASGITransport(app=manager.app), base_url="http://test") as client:
            yield client
