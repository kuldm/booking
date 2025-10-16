from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])
router_all_rooms = APIRouter(prefix="/rooms", tags=["Номера"])


@router_all_rooms.get(
    "",
    summary="Получение всех номеров",
    description="<h3>В этой ручке мы получаем список всех номеров. Можем фильтроваться по title<h3>",
)
async def get_all_rooms(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Местоположение номера"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all_rooms(
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение всех номеров конкретного отеля",
    description="<h3>В этой ручке мы получаем список всех номеров конкретного отеля. Можем фильтроваться по title<h3>",
)
async def get_all_hotel_rooms(
        pagination: PaginationDep,
        hotel_id: int,
        title: str | None = Query(None, description="Местоположение номера"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all_hotel_rooms(
            hotel_id=hotel_id,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение номера конкретного отеля",
    description="<h3>В этой ручке мы получаем номер конкретного отеля<h3>",
)
async def get_hotel_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )


@router.post(
    "/{hotel_id}/rooms",
    summary="Создание номера",
    description="<h3>В этой ручке мы создаём номер конкретного отеля<h3>",
)
async def create_room(
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {"summary": "Простая комната рядом с отелем", "value": {
                "title": "Простая комната рядом с отелем",
                "description": "Простая комната",
                "price": 15,
                "quantity": 15,
            }},
            "2": {"summary": "Сочи хорошая комната", "value": {
                "title": "Хорошая комната в отеле Сочи",
                "description": "Хорошая комната",
                "price": 50,
                "quantity": 5,
            }},
            "3": {"summary": "Сочи отличная комната", "value": {
                "title": "Отличная комната в отеле Сочи",
                "description": "Отличная комната",
                "price": 75,
                "quantity": 7,
            }},
            "4": {"summary": "Дубай комната", "value": {
                "title": "Роскошная комната в отеле Дубай",
                "description": "Роскошная комната",
                "price": 100,
                "quantity": 10,
            }},
            "5": {"summary": "Дубай королевская комната", "value": {
                "title": "Королевская комната в отеле Дубай",
                "description": "Королевская комната",
                "price": 1000,
                "quantity": 1,
            }},
        }
        ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"Status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных отеля",
    description="<h3>В этой ручке мы полностью обновляем данные отеля<h3>",
)
async def update_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).edit(id=room_id, hotel_id=hotel_id, data=_room_data)
        await session.commit()
    return {"Status": "OK", "data": room}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных отеля",
    description="<h3>В этой ручке мы можем частично обновить данные отеля<h3>",
)
async def update_patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        room = await RoomsRepository(session).edit(id=room_id, hotel_id=hotel_id, exclude_unset=True, data=_room_data)
        await session.commit()
    return {"Status": "OK", "data": room}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера конкретного отеля",
    description="<h3>В этой ручке мы удаляем номер конкретного отеля<h3>",
)
async def delete_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"Status": "OK"}
