import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from common.db import get_session
from rest_api.controllers.games.game_summary import get_game_summaries_by_start_datetime, get_game_summaries_by_team_ids
from rest_api.schemas.games.game_summaries import GameSummarySchema

logger = logging.getLogger(__name__)

game_summaries_router = APIRouter()


@game_summaries_router.get("/game-summaries")
async def list_game_summaries_by_datetime(
    from_utc: Annotated[datetime | None, Query(alias="from_utc")] = None,
    to_utc: Annotated[datetime | None, Query(alias="to_utc")] = None,
    team_ids: Annotated[list[int] | None, Query(alias="team_ids")] = None,
    session: Session = Depends(get_session),
) -> list[GameSummarySchema]:
    if from_utc is not None and team_ids is None:
        if to_utc is None:
            to_utc = from_utc + timedelta(days=1)
        return get_game_summaries_by_start_datetime(session, from_utc, to_utc)
    if from_utc is None and team_ids is not None:
        return get_game_summaries_by_team_ids(session, team_ids)
    raise ValueError("from_utc or team_ids must be specified. and cannot be specified at the same time")
