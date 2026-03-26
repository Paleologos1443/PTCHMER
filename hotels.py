from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=['Отели'])


hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("", summary="Получение данных об отеле")
def get_hotels(
        hotel_id: int | None = Query(default=None, description="ID"),
        title: str | None = Query(default=None, description="Hotel's Name"),
        page: int = 1,
        per_page: int = 3,
):
    hotels_ = []
    if hotel_id or title:
        for hotel in hotels:
            if (hotel["id"] != hotel_id) and hotel["title"] != title:
                continue
            hotels_.append(hotel)
        return hotels_
    else:
        return hotels[(page - 1) * per_page: ((page - 1) * per_page) + per_page]


@router.post("", summary="Добавление нового отеля")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи Земля Иерихона",
        "name": "sochi_ierichon",
}}, "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай Кроксимо",
        "name": "dubai_kroks",
    }}})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.put("/{id}", summary="Полное обновление данных об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK", "hotel": hotel}


@router.patch("/{id}", summary="Частичное обновление данных об отеле")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "OK", "hotel": hotel}

@router.delete("/{hotel_id}", summary="Удалить отель из базы данных")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}