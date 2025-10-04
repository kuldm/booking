from fastapi import FastAPI
import time
import asyncio
import threading

app = FastAPI()

@app.get("/sync/{id}")
def sync_rout(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time(): .2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time(): .2f}")


@app.get("/async/{id}")
async def async_rout(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time(): .2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time(): .2f}")


# @app.post("")
# async def create_hotel(
#         hotel_data: Hotel = Body(
#             openapi_examples={"1": {"summary": "Сочи", "value":{
#                 "title": "Отель Сочи 5 звёзд у моря",
#                 "location": "sochi_u_morya",
#             }},
#                 "2": {"summary": "Дубай", "value":{
#                 "title": "Отель Дубай у фонтана",
#                 "location": "dubi_fontain"
#             }},
#             }
#         ),
# ):
#     async with async_session_maker() as session:
#         add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
# Это принт отобразит запрос чнерез орм в запрос sql. Если какие то ошибки, то подойдёт для дебага, чтобы посомтреть
# какой запрос вообще по факту отправляется и протестить его в самой базе
#         print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
#         await session.execute(add_hotel_stmt)
#         await session.commit()
#     return {"Status": "OK"}