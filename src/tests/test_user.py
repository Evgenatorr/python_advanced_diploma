from httpx import AsyncClient
from http import HTTPStatus


async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/api/users",
        params={"name": "test_name2"}
    )
    user_id = 2
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['user_id'] == user_id


async def test_get_user(async_client: AsyncClient):
    response = await async_client.get("/api/users/me", headers={"api-key": "test"})
    assert response.status_code == HTTPStatus.OK


async def test_get_user_invalid_header(async_client: AsyncClient):
    response = await async_client.get("/api/users/me", headers={"api-key": "test3"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
