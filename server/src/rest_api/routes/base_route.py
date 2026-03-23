from fastapi import APIRouter

from rest_api.routes.games.game_summaries import game_summaries_router
from rest_api.routes.teams.regular_season import regular_season_teams_router

api_router = APIRouter(prefix="/api")
api_router.include_router(game_summaries_router)
api_router.include_router(regular_season_teams_router)


@api_router.get("/test")
async def test() -> dict[str, str]:
    return {"Hello": "World"}
