from http import HTTPStatus
from io import BytesIO

from httpx import AsyncClient


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

    response = await async_client.post(
        "/api/tweets",
        json={"tweet_data": "This is a test tweet3"},
        headers={"api-key": "test2"}
    )
    tweet_id = 3
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['tweet_id'] == tweet_id


async def test_load_media_for_tweet(async_client: AsyncClient):
    # Создаем временный файл-изображение
    file_data = BytesIO(b"test image data")
    file_data.name = "test_image.jpg"
    response = await async_client.post(
        "/api/medias",
        files={"file": (file_data.name, file_data, "image/jpeg")},
        headers={"api-key": "test"},
    )
    media_id = 1
    assert response.status_code == HTTPStatus.CREATED
    json_response = response.json()
    assert json_response["media_id"] == media_id


async def test_get_tweets(async_client: AsyncClient):
    api_key = "test"
    response = await async_client.get(
        "/api/tweets",
        headers={"api-key": api_key}
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['tweets']) == 2


async def test_get_tweets_with_invalid_apikey(async_client: AsyncClient):
    invalid_api_key = "test4"
    response = await async_client.get(
        "/api/tweets",
        headers={"api-key": invalid_api_key}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Missing or invalid API key'


async def test_like_tweet(async_client: AsyncClient):
    tweet_id = 1
    response = await async_client.post(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": "test"},
    )
    assert response.status_code == HTTPStatus.CREATED


async def test_like_non_existent_tweet(async_client: AsyncClient):
    invalid_tweet_id = 4
    response = await async_client.post(
        f"/api/tweets/{invalid_tweet_id}/likes", headers={"api-key": "test"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_delete_like(async_client: AsyncClient):
    tweet_id = 1
    response = await async_client.delete(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": "test"},
    )
    assert response.status_code == HTTPStatus.OK


async def test_delete_like_non_existent_tweet(async_client: AsyncClient):
    invalid_tweet_id = 4
    response = await async_client.delete(
        f"/api/tweets/{invalid_tweet_id}/likes", headers={"api-key": "test"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


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


async def test_deleting_someone_tweet(async_client: AsyncClient):
    api_key = "test"
    tweet_id_another_user = 3  # id твита другого пользователя
    response = await async_client.delete(
        f"/api/tweets/{tweet_id_another_user}", headers={"api-key": api_key},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


async def test_deleting_non_existent_tweet(async_client: AsyncClient):
    api_key = "test"
    invalid_tweet_id = 4
    response = await async_client.delete(
        f"/api/tweets/{invalid_tweet_id}", headers={"api-key": api_key},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
