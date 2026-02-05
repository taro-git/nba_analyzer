from fastapi import APIRouter

# from fastapi import Depends
# from sqlmodel import Session, select
# from common.db import get_session

api_router = APIRouter(prefix="/api")


@api_router.get("/test")
async def test() -> dict[str, str]:
    return {"Hello": "World"}


# @api_router.get("/notfound/{path:path}")
# async def not_found(session: Session = Depends(get_session)):
#     return session.exec(select(SQLModel)).all()


# from nba_api.live.nba.endpoints import playbyplay
# from nba_api.stats.endpoints import playbyplayv3


# @api_router.get("/live/playbyplay/{game_id}")
# async def get_live_playbyplay(game_id: str):
#     return playbyplay.PlayByPlay(game_id)


# @api_router.get("/stats/playbyplay/{game_id}")
# async def get_stats_playbyplay(game_id: str):
#     return playbyplayv3.PlayByPlayV3(game_id)
