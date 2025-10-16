from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker, engine, session
from src.models.hotels import HotelsModel
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение всех отелей",
    description="<h3>В этой ручке мы получаем список всех отелей<h3>"
)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Местоположение отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get(
    "/{hotel_id}",
    summary="Получение отеля по ID",
    description="<h3>В этой ручке мы получаем данные об отеле по его ID<h3>"
)
async def get_hotel_by_id(
        db: DBDep,
        hotel_id: int,
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post(
    "",
    summary="Создание отеля",
    description="<h3>В этой ручке мы частичного обновляем данные об отеле<h3>"
)
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {"summary": "Сочи", "value": {
                "title": "Отель Сочи 5 звёзд у моря",
                "location": "sochi_u_morya",
            }},
            "2": {"summary": "Дубай", "value": {
                "title": "Отель Дубай у фонтана",
                "location": "dubi_fontain"
            }},
        }
        ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"Status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных отеля",
    description="<h3>В этой ручке мы полностью обновляем данные об отеле<h3>"
)
async def update_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd,
):
    hotel = await db.hotels.edit(id=hotel_id, data=hotel_data)
    await db.commit()
    return {"Status": "OK", "data": hotel}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных отеля",
    description="<h3>В этой ручке мы частичного обновляем данные об отеле. Можем отправить title, а можем отправить name<h3>",
)
async def update_patch_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH
):
    hotel = await db.hotels.edit(id=hotel_id, exclude_unset=True, data=hotel_data)
    await db.commit()
    return {"Status": "OK", "data": hotel}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="<h3>В этой ручке мы удаляем данные об отеле<h3>",
)
async def delete_hotel(
        db: DBDep,
        hotel_id: int
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"Status": "OK"}
