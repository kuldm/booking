import json

from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep, DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilityAdd, FacilityPATCH

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "",
    summary="Получение всех удобств",
    description="<h3>В этой ручке мы получаем список всех удобств. Можем фильтроваться по title<h3>",
)
async def get_all_facilities(
        db: DBDep,
):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f"{facilities_from_cache=}")
    if not facilities_from_cache:
        facilities =  await db.facilities.get_all_facilities()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts



@router.get(
    "/{facility_id}",
    summary="Получение удобства по ID",
    description="<h3>В этой ручке мы получаем данные об удобстве по его ID<h3>"
)
async def get_facility_by_id(
        db: DBDep,
        facility_id: int,
):
    return await db.facilities.get_one_or_none(id=facility_id)


@router.get(
    "/rooms/{room_id}",
    summary="Получение удобств комнаты по ID комнаты",
    description="<h3>В этой ручке мы получаем данные о всех удобствах комнаты по eё ID<h3>"
)
async def get_rooms_facilities(
        db: DBDep,
        room_id: int,
):
    return await db.rooms_facilities.get_room_facilities(room_id=room_id)


@router.post(
    "",
    summary="Создание удобства",
    description="<h3>В этой ручке мы частичного обновляем данные об отеле<h3>"
)
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd = Body(openapi_examples={
            "1": {"summary": "Кондеционер", "value": {
                "title": "Кондеционер"
            }},
            "2": {"summary": "Тропический душ", "value": {
                "title": "Тропический душ"
            }},
            "3": {"summary": "Wi-Fi", "value": {
                "title": "Wi-Fi"
            }},
        }
        ),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"Status": "OK", "data": facility}


@router.put(
    "/{facility_id}",
    summary="Полное обновление данных удобства",
    description="<h3>В этой ручке мы полностью обновляем данные об удобстве<h3>"
)
async def update_facility(
        db: DBDep,
        facility_id: int,
        facility_data: FacilityAdd,
):
    facility = await db.facilities.edit(id=facility_id, data=facility_data)
    await db.commit()
    return {"Status": "OK", "data": facility}


@router.patch(
    "/{facility_id}",
    summary="Частичное обновление данных удобства",
    description="<h3>В этой ручке мы частичного обновляем данные об удобстве<h3>"
)
async def update_patch_facility(
        db: DBDep,
        facility_id: int,
        facility_data: FacilityPATCH,
):
    facility = await db.facilities.edit(id=facility_id, exclude_unset=True, data=facility_data)
    await db.commit()
    return {"Status": "OK", "data": facility}


@router.delete(
    "/{facility_id}",
    summary="Удаление удобства",
    description="<h3>В этой ручке мы удаляем удобство об отеле<h3>",
)
async def delete_facility_by_id(
        db: DBDep,
        facility_id: int,
):
    await db.facilities.delete(id=facility_id)
    await db.commit()
    return {"Status": "OK"}
