from datetime import date

from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])
router_all_rooms = APIRouter(prefix="/rooms", tags=["Номера"])


@router_all_rooms.get(
    "",
    summary="Получение всех номеров",
    description="<h3>В этой ручке мы получаем список всех номеров. Можем фильтроваться по title<h3>",
)
async def get_all_rooms(
        db: DBDep,
        pagination: PaginationDep,
        title: str | None = Query(None, description="Местоположение номера"),
):
    per_page = pagination.per_page or 5
    return await db.rooms.get_all_rooms(
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
        db: DBDep,
        pagination: PaginationDep,
        hotel_id: int,
        title: str | None = Query(None, description="Местоположение номера"),
        date_from: date = Query(examples="2025-10-01"),
        date_to: date = Query(examples="2025-10-10"),
):
    per_page = pagination.per_page or 5
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        title=title,
        date_from=date_from,
        date_to=date_to,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение номера конкретного отеля",
    description="<h3>В этой ручке мы получаем номер конкретного отеля<h3>",
)
async def get_hotel_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    return await db.rooms.get_one_or_none_with_rels(
        id=room_id,
        hotel_id=hotel_id,
    )


@router.post(
    "/{hotel_id}/rooms",
    summary="Создание номера",
    description="<h3>В этой ручке мы создаём номер конкретного отеля<h3>",
)
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {"summary": "Простая комната рядом с отелем", "value": {
                "title": "Простая комната рядом с отелем",
                "description": "Простая комната",
                "price": 15,
                "quantity": 15,
                "facilities_ids": [],
            }},
            "2": {"summary": "Сочи хорошая комната", "value": {
                "title": "Хорошая комната в отеле Сочи",
                "description": "Хорошая комната",
                "price": 50,
                "quantity": 5,
                "facilities_ids": [],
            }},
            "3": {"summary": "Сочи отличная комната", "value": {
                "title": "Отличная комната в отеле Сочи",
                "description": "Отличная комната",
                "price": 75,
                "quantity": 7,
                "facilities_ids": [],
            }},
            "4": {"summary": "Дубай комната", "value": {
                "title": "Роскошная комната в отеле Дубай",
                "description": "Роскошная комната",
                "price": 100,
                "quantity": 10,
                "facilities_ids": [],
            }},
            "5": {"summary": "Дубай королевская комната", "value": {
                "title": "Королевская комната в отеле Дубай",
                "description": "Королевская комната",
                "price": 1000,
                "quantity": 1,
                "facilities_ids": [],
            }},
        }
        ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных комнаты конкретного отеля",
    description="<h3>В этой ручке мы полностью обновляем данные комнаты конкретного отеля<h3>",
)
async def update_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.edit(id=room_id, hotel_id=hotel_id, data=_room_data)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {"status": "OK", "data": room}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных комнаты конкретного отеля",
    description="<h3>В этой ручке мы можем частично обновить данные конкретного отеля<h3>",
)
async def update_patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    room = await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.commit()

    return {"status": "OK", "data": room}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера конкретного отеля",
    description="<h3>В этой ручке мы удаляем номер конкретного отеля<h3>",
)
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
