from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rest_api.routes.base_route import api_router
from rest_api.settings import settings

BASE_DIR = Path(__file__).resolve().parents[3]
CLIENT_DIR = BASE_DIR / "client" / "build" / "client"

app = FastAPI()

app.include_router(api_router)

if settings.is_dev:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.mount(
    "/view/assets/",
    StaticFiles(directory=CLIENT_DIR / "assets"),
    name="react",
)


@app.get("/view/{path:path}")
async def route_client(path: str) -> FileResponse:
    return FileResponse(CLIENT_DIR / "index.html")
