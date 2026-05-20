import logging

from fastapi import APIRouter, Depends
from sqlmodel import Session

from common.db import get_session
from rest_api.controllers.games.game_detail import get_game_detail_by_game_id
from rest_api.schemas.games.game_detail import GameDetailSchema

logger = logging.getLogger(__name__)

game_detail_router = APIRouter()


@game_detail_router.get("/games/{game_id}")
async def get_game_detail(game_id: str, session: Session = Depends(get_session)) -> GameDetailSchema:
    return get_game_detail_by_game_id(session, game_id)
