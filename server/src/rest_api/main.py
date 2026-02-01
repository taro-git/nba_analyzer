from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rest_api.routes.base_route import api_router

BASE_DIR = Path(__file__).resolve().parents[3]
CLIENT_DIR = BASE_DIR / "client" / "build" / "client"

app = FastAPI()

app.include_router(api_router)

app.mount(
    "/view/assets/",
    StaticFiles(directory=CLIENT_DIR / "assets"),
    name="react",
)


@app.get("/view/{path:path}")
async def route_client(path: str):
    return FileResponse(CLIENT_DIR / "index.html")
