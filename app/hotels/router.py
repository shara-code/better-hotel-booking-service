import asyncio
from datetime import date
from typing import List, Optional

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter

from app.exceptions import (CannotBookHotelForLongPeriod,
                            DateFromCannotBeAfterDateTo)
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelInfo

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date,
    date_to: date,
):  # -> List[SHotelInfo]:
    await asyncio.sleep(3)
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    hotels_json = TypeAdapter(List[SHotelInfo]).validate_python(hotels)
    return hotels_json


@router.get("/id/{hotel_id}", include_in_schema=True)
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    return await HotelDAO.find_one_or_none(id=hotel_id)
