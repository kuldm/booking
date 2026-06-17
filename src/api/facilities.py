from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.facilities import FacilityAdd, FacilityPATCH

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "",
    summary="Получение всех удобств",
    description="<h3>В этой ручке мы получаем список всех удобств. Можем фильтроваться по title<h3>",
)
async def get_all_facilities(
        db: DBDep,
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название удобства"),
):
    per_page = pagination.per_page or 5
    return await db.facilities.get_all_facilities(
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


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
