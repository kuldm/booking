from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine, session
from src.models.hotels import HotelsModel
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Местоположение отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("")
async def create_hotel(
        hotel_data: Hotel = Body(
            openapi_examples={"1": {"summary": "Сочи", "value": {
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"Status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        hotel_data: Hotel,

):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(id=hotel_id, data=hotel_data)
        await session.commit()
        return {"Status": "OK", "data": hotel}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h2>В этой ручке мы частичного обновляем данные об отеле. Можем отправить title, а можем отправить name<h2>"
)
async def update_patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"Status": "OK", "data": hotel}

