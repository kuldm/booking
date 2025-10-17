import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

# Эта конструкция нужна чтобы определить путь текущего файла, определить его родителя (папка src) и определить родителя (папки src)
# И добавить её в пути с которыми может работать интерпритатор. После этого интерпритатор будет понимать что такое src.
# Иначе при запуске программы python src/main.py будет писать ошибку ModuleNotFoundError: No module named 'src'
sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms, router_all_rooms
from src.api.bookings import router as router_bookings

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_all_rooms)
app.include_router(router_bookings)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
