import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_table(async_client: AsyncClient):
    payload = {
        "name": "Test Table",
        "seats": 4,
        "location": "By the window"
    }

    response = await async_client.post("/tables/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["seats"] == payload["seats"]
    assert data["location"] == payload["location"]

@pytest.mark.asyncio
async def test_get_tables(async_client: AsyncClient):
    response = await async_client.get("/tables/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_delete_table(async_client: AsyncClient):
    response = await async_client.post("/tables/", json={
        "name": "ToDelete",
        "seats": 2,
        "location": "Corner"
    })
    assert response.status_code == 201
    table_id = response.json()["id"]

    delete_response = await async_client.delete(f"/tables/{table_id}")
    assert delete_response.status_code == 204

    get_response = await async_client.get("/tables/")
    ids = [t["id"] for t in get_response.json()]
    assert table_id not in ids
