from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    ObjectNotFoundException,
    AllRoomsAreBookedException,
    ChekInDateIsLaterThenCheckOutDateException,
    ChekInDateIsTheSameAsCheckOutDateException,
)
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get(
    "",
    summary="Получение всех бронирований",
    description="<h3>В этой ручке мы получаем список всех бронирований<h3>",
)
async def get_all_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get(
    "/me",
    summary="Получение бронирований пользователя",
    description="<h3>В этой ручке мы получаем список всех бронирований залогиненного пользователя<h3>",
)
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    "",
    summary="Создание бронирования",
    description="<h3>В этой ручке мы создаём бронирование<h3>",
)
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest):
    try:
        if booking_data.date_from > booking_data.date_to:
            raise ChekInDateIsLaterThenCheckOutDateException()

        if booking_data.date_from == booking_data.date_to:
            raise ChekInDateIsTheSameAsCheckOutDateException()

        room: Room = await db.rooms.get_one(id=booking_data.room_id)

    except ChekInDateIsLaterThenCheckOutDateException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)

    except ChekInDateIsTheSameAsCheckOutDateException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)

    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    await db.commit()
    return {"status": "OK", "data": booking}
