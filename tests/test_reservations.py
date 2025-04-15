import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from fastapi import status


async def create_table_and_reservation(client: AsyncClient):
    table_data = {
        "name": "Test Table",
        "seats": 4,
        "location": "Corner"
    }
    response = await client.post("/tables/", json=table_data)
    table_id = response.json()["id"]

    reservation_time = datetime.now().replace(minute=0, second=0, microsecond=0).isoformat()

    reservation_data = {
        "customer_name": "Alice",
        "table_id": table_id,
        "reservation_time": reservation_time,
        "duration_minutes": 60
    }

    res = await client.post("/reservations/", json=reservation_data)
    return res.json()


@pytest.mark.asyncio
async def test_create_reservation(async_client: AsyncClient):
    reservation = await create_table_and_reservation(async_client)
    assert reservation["customer_name"] == "Alice"
    assert reservation["duration_minutes"] == 60


@pytest.mark.asyncio
async def test_get_reservations(async_client: AsyncClient):
    await create_table_and_reservation(async_client)
    response = await async_client.get("/reservations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_delete_reservation(async_client: AsyncClient):
    reservation = await create_table_and_reservation(async_client)
    reservation_id = reservation["id"]

    response = await async_client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 204

    response = await async_client.get("/reservations/")
    remaining = [r for r in response.json() if r["id"] == reservation_id]
    assert len(remaining) == 0


@pytest.mark.asyncio
async def test_reservation_overlap(async_client: AsyncClient):
    # Создаем стол
    table_data = {
        "name": "Overlap Table",
        "seats": 2,
        "location": "Window"
    }
    response = await async_client.post("/tables/", json=table_data)
    assert response.status_code == 201
    table_id = response.json()["id"]

    # Время начала первого бронирования
    start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    start_iso = start_time.isoformat()

    # Бронирование №1
    reservation_data_1 = {
        "customer_name": "First",
        "table_id": table_id,
        "reservation_time": start_iso,
        "duration_minutes": 60
    }

    response1 = await async_client.post("/reservations/", json=reservation_data_1)
    assert response1.status_code == 201

    # Бронирование №2 — пересекается с первым
    reservation_data_2 = {
        "customer_name": "Second",
        "table_id": table_id,
        "reservation_time": (start_time + timedelta(minutes=30)).isoformat(),  # пересекается
        "duration_minutes": 60
    }

    response2 = await async_client.post("/reservations/", json=reservation_data_2)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST