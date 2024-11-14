from httpx import AsyncClient
from http import HTTPStatus


async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/api/create_user",
        data={
            "name": "test_name2",
            "api_key": "test2"
        }
    )
    user_id = 2
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['user_id'] == user_id


async def test_get_user(async_client: AsyncClient):
    response = await async_client.get("/api/users/me", headers={"api-key": "test"})
    assert response.status_code == HTTPStatus.OK


async def test_follow_user(async_client: AsyncClient):
    user_id_for_subscription = 2
    response = await async_client.post(
        f"/api/users/{user_id_for_subscription}/follow",
        headers={"api-key": "test"}
    )
    assert response.status_code == HTTPStatus.CREATED


async def test_unfollow_user(async_client: AsyncClient):
    user_id_for_unsubscribe = 2
    response = await async_client.delete(
        f"/api/users/{user_id_for_unsubscribe}/follow",
        headers={"api-key": "test"}
    )
    assert response.status_code == HTTPStatus.OK


async def test_get_user_invalid_header(async_client: AsyncClient):
    response = await async_client.get("/api/users/me", headers={"api-key": "test3"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
