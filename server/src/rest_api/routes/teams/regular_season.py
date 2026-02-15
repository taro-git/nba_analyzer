from fastapi import APIRouter, Depends
from sqlmodel import Session

from common.db import get_session
from rest_api.controllers.teams.regular_season import get_regular_season_teams_by_season
from rest_api.schemas.commons import Season
from rest_api.schemas.teams.regular_season import RegularSeasonTeamsSchema

regular_season_teams_router = APIRouter()


@regular_season_teams_router.get("/teams/regular-seasons/{season}")
async def list_regular_season_teams_by_season(
    season: Season, session: Session = Depends(get_session)
) -> RegularSeasonTeamsSchema:
    """
    シーズンを指定してレギュラーシーズンのチーム成績一覧を返します.
    """
    return RegularSeasonTeamsSchema(season=season, teams=get_regular_season_teams_by_season(session, season))
