from fastapi import FastAPI, Query, Body, Path
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "Сочи"},
    {"id": 2, "title": "Dubai", "name": "Дубай"}
]


@app.get("/hotels", summary="Получение данных об отеле")
def get_hotels(
        id: int | None = Query(default=None, description="ID"),
        title: str | None = Query(default=None, description="Hotel's Name"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels", summary="Добавление нового отеля")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title ,
    })
    return {"status": "OK"}


@app.put("/hotels/{id}", summary="Полное обновление данных об отеле")
def put_hotel(
        id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK", "hotel": hotel}


@app.patch("/hotels/{id}", summary="Частичное обновление данных об отеле")
def patch_hotel(
        id: int,
        title: str | None = Body(default=None, embed=True),
        name: str | None = Body(default=None, embed=True),
):
    for hotel in hotels:
        if hotel["id"] == id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "OK", "hotel": hotel}

@app.delete("/hotel/{hotel_id}", summary="Удалить отель из базы данных")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@app.get(path = "/docs", include_in_schema=False)
async def custom_swagger_ui_html():...


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)