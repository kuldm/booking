from datetime import date

from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])



@router.post(
    "",
    summary="Создание бронирования",
    description="<h3>В этой ручке мы создаём бронирование<h3>",
)
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        room_id: int,
        date_from: date,
        date_to: date,
):
    room = await db.rooms.get_one_or_none(id=room_id)
    _booking_data = BookingAdd(user_id=user_id, room_id=room_id, date_from=date_from, date_to=date_to)
    booking= await db.bookings.add(_booking_data)
    await db.commit()
    return {"Status": "OK", "data": booking}
