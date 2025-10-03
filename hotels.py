from typing import Annotated

from fastapi import Query, APIRouter, Body, Depends

from dependencies import PaginationParams, PaginationDep
from schemas.hotels import Hotel, HotelPATCH
router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        name: str | None = Query(None, description="Какой то параметр"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue
        hotels_.append(hotel)
    start = (pagination.page - 1) * pagination.per_page
    stop = start + pagination.per_page
    hotels_ = hotels_[start:stop:]
    return hotels_


@router.post("")
def create_hotel(
        hotel_data: Hotel = Body(
            openapi_examples={"1": {"summary": "Сочи", "value":{
                "title": "Отель Сочи 5 звёзд у моря",
                "name": "sochi_u_morya",
            }},
                "2": {"summary": "Дубай", "value":{
                "title": "Отель Дубай у фонтана",
                "name": "dubi_fontain"
            }},
            }
        ),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return hotels[-1]


@router.put("/{hotel_id}")
def update_hotel(
        hotel_id: int,
        hotel_data: Hotel,

):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id]
    hotel[0]["title"] = hotel_data.title
    hotel[0]["name"] = hotel_data.name
    return hotel


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h2>В этой ручке мы частичного обновляем данные об отеле. Можем отправить title, а можем отправить name<h2>"
)
def update_patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return hotel


@router.delete("/{hotel_id}")
def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
