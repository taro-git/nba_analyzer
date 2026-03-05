import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from common.db import get_session
from rest_api.schemas.commons import GameCategory, GameStatus
from rest_api.schemas.games.game_summaries import GameSummarySchema
from rest_api.schemas.teams.regular_season import Team

logger = logging.getLogger(__name__)

game_summaries_router = APIRouter()


@game_summaries_router.get("/game-summaries")
async def list_game_summaries_by_datetime(
    from_utc: Annotated[datetime, Query(alias="from_utc")],
    to_utc: Annotated[datetime | None, Query(alias="to_utc")] = None,
    session: Session = Depends(get_session),
) -> list[GameSummarySchema]:
    # TODO: 実装
    if to_utc is None:
        to_utc = from_utc + timedelta(days=1)
    team = Team(
        team_id=1610612764,
        team_name="team_name",
        team_tricode="TRI",
        team_logo="https://cdn.nba.com/logos/nba/1610612764/global/L/logo.svg",
    )
    print(session)
    return [
        GameSummarySchema(
            game_id="1",
            status=GameStatus("Scheduled"),
            category=GameCategory("Regular Season"),
            start_datetime=from_utc.astimezone(),
            elapsed_sec=0,
            home_team=team,
            away_team=team,
            home_team_score=0,
            away_team_score=0,
        ),
        GameSummarySchema(
            game_id="1",
            status=GameStatus("Live"),
            category=GameCategory("Regular Season"),
            start_datetime=to_utc.astimezone(),
            elapsed_sec=0,
            home_team=team,
            away_team=team,
            home_team_score=0,
            away_team_score=0,
        ),
    ]
