from fastapi import Query, Body, APIRouter

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]


@router.get("")
def get_hotels(
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
    return hotels_


@router.post("")
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return hotels[-1]


@router.put("/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id]
    hotel[0]["title"] = title
    hotel[0]["name"] = name
    return hotel


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h2>В этой ручке мы частичного обновляем данные об отеле. Можем отправить title, а можем отправить name<h2>"
)
def update_patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id]
    if title:
        hotel[0]["title"] = title
    if name:
        hotel[0]["name"] = name
    return hotel


@router.delete("/{hotel_id}")
def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
