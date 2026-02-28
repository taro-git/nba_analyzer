from sqlmodel import Session

from common.models.teams.teams import TeamProperty
from rest_api.repositories.teams.teams import get_team_properties_by_ids
from rest_api.schemas.commons import Season


def test_get_teams_by_ids_returns_matched_team(session: Session, seed_teams: dict[int, TeamProperty]) -> None:
    assert get_team_properties_by_ids(session, Season("2022-23"), [1]) == [seed_teams[1]]


def test_get_teams_by_ids_returns_matched_teams(session: Session, seed_teams: dict[int, TeamProperty]) -> None:
    result = sorted(
        [s.model_dump() for s in get_team_properties_by_ids(session, Season("2022-23"), [1, 3])],
        key=lambda x: x["team_id"],
    )
    expected = sorted([seed_teams[1].model_dump(), seed_teams[3].model_dump()], key=lambda x: x["team_id"])
    assert result == expected


def test_get_teams_by_ids_returns_empty_when_no_match(session: Session, seed_teams: dict[int, TeamProperty]) -> None:
    assert get_team_properties_by_ids(session, Season("2022-23"), [999]) == []


def test_get_teams_by_ids_returns_empty_when_input_empty(session: Session, seed_teams: dict[int, TeamProperty]) -> None:
    assert get_team_properties_by_ids(session, Season("2022-23"), []) == []


def test_get_teams_by_ids_return_partial_matched_team(session: Session, seed_teams: dict[int, TeamProperty]) -> None:
    assert get_team_properties_by_ids(session, Season("2022-23"), [2, 999]) == [seed_teams[2]]
