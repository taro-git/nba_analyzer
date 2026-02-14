from sqlmodel import Session

from common.models.teams.teams import Team
from rest_api.repositories.teams.teams import get_teams_by_ids


def test_get_teams_by_ids_returns_matched_team(session: Session, seed_teams: dict[int, Team]) -> None:
    assert get_teams_by_ids(session, [1]) == [seed_teams[1]]


def test_get_teams_by_ids_returns_matched_teams(session: Session, seed_teams: dict[int, Team]) -> None:
    result = sorted([s.model_dump() for s in get_teams_by_ids(session, [1, 3])], key=lambda x: x["id"])
    expected = sorted([seed_teams[1].model_dump(), seed_teams[3].model_dump()], key=lambda x: x["id"])
    assert result == expected


def test_get_teams_by_ids_returns_empty_when_no_match(session: Session, seed_teams: dict[int, Team]) -> None:
    assert get_teams_by_ids(session, [999]) == []


def test_get_teams_by_ids_returns_empty_when_input_empty(session: Session, seed_teams: dict[int, Team]) -> None:
    assert get_teams_by_ids(session, []) == []


def test_get_teams_by_ids_return_partial_matched_team(session: Session, seed_teams: dict[int, Team]) -> None:
    assert get_teams_by_ids(session, [2, 999]) == [seed_teams[2]]
