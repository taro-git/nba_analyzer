from sqlmodel import Session

from rest_api.repositories.teams.regular_season_team_standings import get_regular_season_team_standings
from rest_api.repositories.teams.teams import get_teams_by_ids
from rest_api.schemas.commons import Season
from rest_api.schemas.teams.regular_season import RegularSeasonTeam


def get_regular_season_teams_by_season(session: Session, season: Season) -> list[RegularSeasonTeam]:
    """
    シーズンを指定してチーム情報およびレギュラーシーズンの成績一覧を返します
    """
    team_standings = get_regular_season_team_standings(session, season)

    team_ids = [standing.team_id for standing in team_standings]
    team_infos = get_teams_by_ids(session, team_ids)
    team_infos_by_id = {team.id: team for team in team_infos}

    result: list[RegularSeasonTeam] = []

    for standing in team_standings:
        team = team_infos_by_id.get(standing.team_id)
        if team is None:
            raise ValueError(f"Team id {standing.team_id} not found in teams info")

        result.append(
            RegularSeasonTeam(
                team_id=team.id,
                team_name=team.team_name,
                team_tricode=team.team_tricode,
                team_logo=f"https://cdn.nba.com/logos/nba/{team.id}/global/L/logo.svg",
                conference=team.conference,
                division=team.division,
                rank=standing.rank,
                win=standing.win,
                lose=standing.lose,
            )
        )

    return result
