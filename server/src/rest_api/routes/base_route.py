from fastapi import APIRouter

api_router = APIRouter(prefix="/api")


@api_router.get("/test")
async def test():
    return {"Hello": "World"}


@api_router.get("/{path:path}")
async def not_found():
    return {"error": "not found"}
