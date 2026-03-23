import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from common.db import get_session
from rest_api.controllers.games.game_summary import get_game_summaries_by_start_datetime
from rest_api.schemas.games.game_summaries import GameSummarySchema

logger = logging.getLogger(__name__)

game_summaries_router = APIRouter()


@game_summaries_router.get("/game-summaries")
async def list_game_summaries_by_datetime(
    from_utc: Annotated[datetime, Query(alias="from_utc")],
    to_utc: Annotated[datetime | None, Query(alias="to_utc")] = None,
    session: Session = Depends(get_session),
) -> list[GameSummarySchema]:
    if to_utc is None:
        to_utc = from_utc + timedelta(days=1)
    return get_game_summaries_by_start_datetime(session, from_utc, to_utc)
