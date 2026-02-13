from sqlmodel import Session, select

from common.models.teams.regular_season_team_standings import RegularSeasonTeamStanding
from rest_api.schemas.commons import Season


def get_regular_season_team_standings(session: Session, season: Season) -> list[RegularSeasonTeamStanding]:
    season_start_year = int(season.split("-")[0])
    return list(
        session.exec(
            select(RegularSeasonTeamStanding).where(RegularSeasonTeamStanding.season == season_start_year)
        ).all()
    )
