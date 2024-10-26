from httpx import AsyncClient


async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/api/users",
        params={"name": "test_name2"}
    )
    assert response.status_code == 201
    assert response.json()['user_id'] == 2


async def test_get_user(async_client: AsyncClient):
    response = await async_client.get("/api/users/me", headers={"api-key": "test"})
    assert response.status_code == 200


async def test_get_user_invalid_header(async_client: AsyncClient):
    response = await async_client.get("/api/users/me", headers={"api-key": "test3"})
    assert response.status_code == 401  # Unauthorized
