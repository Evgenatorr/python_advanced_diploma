from httpx import AsyncClient
from http import HTTPStatus


async def test_create_tweet(async_client: AsyncClient):
    response = await async_client.post(
        "/api/tweets",
        json={"tweet_data": "This is a test tweet"},
        headers={"api-key": "test"}
    )
    tweet_id = 1
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['tweet_id'] == tweet_id

    response = await async_client.post(
        "/api/tweets",
        json={"tweet_data": "This is a test tweet2"},
        headers={"api-key": "test"}
    )
    tweet_id = 2
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['tweet_id'] == tweet_id


async def test_get_tweets(async_client: AsyncClient):
    response = await async_client.get(
        "/api/tweets",
        headers={"api-key": "test"}
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['tweets']) == 2


async def test_create_tweet_invalid_json(async_client: AsyncClient):
    response = await async_client.post(
        "/api/tweets", json={"title": "something"},
        headers={"api-key": "test"}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_create_tweet_invalid_header(async_client: AsyncClient):
    response = await async_client.post(
        "/api/tweets", json={"tweet_data": "This is a test tweet"},
        headers={"api-key": "test3"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_delete_tweet(async_client: AsyncClient):
    tweet_id = 1
    response = await async_client.delete(
        f"/api/tweets/{tweet_id}", headers={"api-key": "test"},
    )
    assert response.status_code == HTTPStatus.OK

    # проверяем что твит удалился и из двух остался один твит
    response = await async_client.get(
        "/api/tweets",
        headers={"api-key": "test"}
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['tweets']) == 1
