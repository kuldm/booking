from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsModel
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
        query = select(HotelsModel)
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.strip().lower()))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        hotels = result.scalars().all()
        print(type(hotels), hotels)
        return hotels



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
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"Status": "OK"}


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
