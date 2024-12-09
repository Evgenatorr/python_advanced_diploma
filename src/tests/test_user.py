from http import HTTPStatus

from httpx import AsyncClient


async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/api/create_user",
        data={
            "name": "test_name3",
            "api_key": "test3"
        }
    )
    user_id = 3
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
    invalid_api_key = 'test4'
    response = await async_client.get(
        "/api/users/me", headers={"api-key": invalid_api_key}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
