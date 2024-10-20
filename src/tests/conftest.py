import os
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings
from src.loader import app
from src.database.session_manager import db_manager
from src.database.models.base_model import MyBase
from asgi_lifespan import LifespanManager

from src.utils.get_db_url import get_database_url


@pytest.fixture(scope="session")
async def test_db():
    """
    Фикстура для инициализации и очистки тестовой базы данных.
    """
    # Устанавливаем переменную окружения для тестовой базы данных
    os.environ['START'] = "test"
    test_db_url = get_database_url()
    db_manager.init(test_db_url)

    async with db_manager.connect() as connection:
        await connection.run_sync(MyBase.metadata.drop_all)
        await connection.run_sync(MyBase.metadata.create_all)
    yield
    async with db_manager.connect() as connection:
        await connection.run_sync(MyBase.metadata.drop_all)


@pytest.fixture(scope="session")
async def db_session(test_db):
    """
    Фикстура для предоставления сессии базы данных в тестах.
    """
    async with db_manager.async_session() as session:
        yield session


@pytest.fixture(scope="session")
async def async_client():
    """
    Фикстура для асинхронного клиента приложения.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url=settings.APP_BASE_URL) as client:
        yield client
