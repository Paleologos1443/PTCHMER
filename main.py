from fastapi import FastAPI, Query, Body, Path
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

from hotels import router as router_hotels

app = FastAPI()

app.include_router(router_hotels)


@app.get(path = "/docs", include_in_schema=False)
async def custom_swagger_ui_html():...


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)