from httpx import AsyncClient


async def test_tweet(client: AsyncClient):
    print(1)
    response = await client.get("/api/users/me", headers={"Api-Key": "test"})
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

    response = await client.post("/api/tweets", json=test_request_payload, headers={"Api-Key": "test"})

    assert response.status_code == 201
    assert response.json() == test_response_payload
#
#
# def test_create_tweet_invalid_json(test_app):
#     response = test_app.post("/api/tweets", content=json.dumps({"title": "something"}))
#     assert response.status_code == 422
