import logging
from datetime import datetime

from nba_api.stats.endpoints.leaguestandingsv3 import LeagueStandingsV3

from batch.repositories.teams.regular_season_team_standings import upsert_regular_season_team_standings
from batch.services.nba_api.gateway import NbaApiGateway
from batch.types import Season
from common.models.teams.regular_season_team_standings import RegularSeasonTeamStanding

logger = logging.getLogger(__name__)


def _create_regular_season_team_standings_by_season(season: Season) -> list[RegularSeasonTeamStanding]:
    """
    シーズンを指定して、レギュラーシーズンのチーム成績一覧を作成します.
    """
    result_set = NbaApiGateway().fetch(LeagueStandingsV3, season=season.season_str).get("resultSets", [])[0]
    standings = result_set["rowSet"]
    headers = result_set["headers"]
    return [
        RegularSeasonTeamStanding(
            season=season.start_year,
            team_id=s[headers.index("TeamID")],
            rank=s[headers.index("PlayoffRank")],
            win=s[headers.index("WINS")],
            lose=s[headers.index("LOSSES")],
        )
        for s in standings
    ]


def sync_regular_season_team_standings_by_season(season: Season | None = None) -> None:
    """
    シーズンを指定して、最新のデータと DB のレギュラーシーズンの順位情報を同期する
    """
    try:
        if season is None:
            season = Season.from_datetime(datetime.now())
        upsert_regular_season_team_standings(_create_regular_season_team_standings_by_season(season))
    except Exception as e:
        logger.error(f"error in sync_regular_season_team_standings_by_season: {e}")
        raise
