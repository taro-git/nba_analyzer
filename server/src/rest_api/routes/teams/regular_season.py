from fastapi import APIRouter, Depends
from sqlmodel import Session

from common.db import get_session
from common.types import Conference, Division
from rest_api.schemas.common import Season
from rest_api.schemas.teams.regular_season import RegularSeasonTeam, RegularSeasonTeamsSchema

regular_season_teams_router = APIRouter()


@regular_season_teams_router.get("/teams/regular-seasons/{season}")
async def list_regular_season_teams_by_season(
    season: Season, session: Session = Depends(get_session)
) -> RegularSeasonTeamsSchema:
    """
    シーズンを指定してレギュラーシーズンのチーム成績一覧を返します.
    """
    print(session)
    dummy_team = RegularSeasonTeam(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="CRE",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.east,
        division=Division.southeast,
        rank=1,
        win=1,
        lose=1,
    )
    dummy_team_2 = RegularSeasonTeam(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="IND",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.east,
        division=Division.southeast,
        rank=2,
        win=0,
        lose=1,
    )
    dummy_team_3 = RegularSeasonTeam(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="GSW",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.west,
        division=Division.southwest,
        rank=2,
        win=1,
        lose=1,
    )
    dummy_team_4 = RegularSeasonTeam(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="LAC",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.west,
        division=Division.southwest,
        rank=1,
        win=1,
        lose=0,
    )
    return RegularSeasonTeamsSchema(season=season, teams=[dummy_team, dummy_team_2, dummy_team_3, dummy_team_4])
