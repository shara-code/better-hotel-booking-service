import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status_code",
    [
        *[(4, "2029-10-01", "2029-10-15", 200)] * 8,
        *[(4, "2029-10-01", "2029-10-15", 409)] * 4,
    ],
)
async def test_add_and_get_booking(
    room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code


async def test_get_and_delete_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")
    existing_bookings = [booking["id"] for booking in response.json()]
    for booking_id in existing_bookings:
        response = await authenticated_ac.delete(
            f"bookings/{booking_id}",
        )
