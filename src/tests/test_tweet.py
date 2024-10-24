import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import models
from config import settings


# @pytest.mark.asyncio
# async def test_create_user_and_tweet(async_client: AsyncClient, db_session: AsyncSession):
#     # Создаём тестового пользователя
#     user = models.user_model.User(name="test_user")
#     db_session.add(user)
#     await db_session.commit()
#
#     # Создаём твит
#     response = await async_client.post(
#         "/api/tweets",
#         json={"tweet_data": "Hello, this is a test tweet!"},
#         headers={"api-key": "test"}
#     )
#     assert response.status_code == 200
#     assert response.json()["content"] == "Hello, this is a test tweet!"


async def test_create_user_and_tweet(async_client: AsyncClient):
    response = await async_client.post(
        "/api/users",
        params={"name": "test_user"}
    )
    assert response.status_code == 201
    response = await async_client.post(
        "/api/tweets",
        json={"tweet_data": "This is a test tweet"},
        headers={"api-key": "test"}
    )
    assert response.status_code == 201


async def test_get_user(async_client: AsyncClient):
    response = await async_client.get("/api/users/me", headers={"api-key": "test"})
    assert response.status_code == 200


# async def test_create_tweet_invalid_json(async_client: AsyncClient):
#     response = await async_client.post("/api/tweets", json={"title": "something"})
#     assert response.status_code == 422
