from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_all_bookings(
        db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_bookings(
        db: DBDep,
        user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    "",
    summary="Создание бронирования",
    description="<h3>В этой ручке мы создаём бронирование<h3>",
)
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"Status": "OK", "data": booking}
