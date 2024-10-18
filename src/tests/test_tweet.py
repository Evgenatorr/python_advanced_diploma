from httpx import AsyncClient


async def test_create_user(client: AsyncClient):
    response = await client.post('/api/users', json={
        'name': 'Evgeniy'
    })
    assert response.status_code == 201
    print(response.json())


async def test_tweet(client: AsyncClient):
    response = await client.get("/api/users/me", headers={"api-key": "test"})
    assert response.status_code == 200
    json_data = response.json()
    print(json_data)


async def test_create_tweet(client: AsyncClient):
    test_request_payload = {
        "tweet_data": "string",
        # "tweet_media_ids": [
        #     0
        # ],
    }
    test_response_payload = {"result": "true", "tweet_id": 1}

    response = await client.post("/api/tweets", json=test_request_payload, headers={"api-key": "test"})

    assert response.status_code == 201
    assert response.json() == test_response_payload


async def test_create_tweet_invalid_json(client: AsyncClient):
    response = await client.post("/api/tweets", json={"title": "something"})
    assert response.status_code == 422
