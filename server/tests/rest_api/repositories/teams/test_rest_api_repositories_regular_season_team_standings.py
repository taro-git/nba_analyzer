from sqlmodel import Session

from common.models.teams.regular_season_team_standings import RegularSeasonTeamStanding
from rest_api.repositories.teams.regular_season_team_standings import get_regular_season_team_standings
from rest_api.schemas.commons import Season


def test_get_regular_season_team_standings_returns_matched_season_data(
    session: Session,
    seed_standings: dict[int, list[RegularSeasonTeamStanding]],
) -> None:
    result = sorted(
        [s.model_dump() for s in get_regular_season_team_standings(session, Season("2023-24"))],
        key=lambda x: x["team_id"],
    )
    expected = sorted([s.model_dump() for s in seed_standings[2023]], key=lambda x: x["team_id"])
    assert result == expected


def test_get_regular_season_team_standings_returns_empty_when_no_match(
    session: Session,
    seed_standings: dict[int, list[RegularSeasonTeamStanding]],
) -> None:
    assert get_regular_season_team_standings(session, Season("2021-22")) == []
