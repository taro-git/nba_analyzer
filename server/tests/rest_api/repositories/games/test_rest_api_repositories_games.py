from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlmodel import Session

from common.models.games.games import Game
from rest_api.repositories.games.games import get_games_by_start_datetime


def test_get_games_by_start_datetime_returns_matched_team(session: Session, seed_games: dict[str, Game]) -> None:
    from_datetime = datetime(2025, 9, 1, tzinfo=timezone.utc)
    to_datetime = datetime(2025, 9, 11, tzinfo=timezone.utc)
    result_ids = [g.game_id for g in get_games_by_start_datetime(session, from_datetime, to_datetime)]
    expected_ids = [
        seed_games[id].game_id
        for id in seed_games.keys()
        if seed_games[id].start_epoc_sec >= int(from_datetime.timestamp())
        and seed_games[id].start_epoc_sec <= int(to_datetime.timestamp())
    ]
    assert sorted(result_ids) == sorted(expected_ids)


def test_get_games_by_start_datetime_returns_matched_team_if_not_utc(
    session: Session, seed_games: dict[str, Game]
) -> None:
    from_datetime = datetime(2025, 9, 1, tzinfo=timezone.utc).astimezone(ZoneInfo("Asia/Tokyo"))
    to_datetime = datetime(2025, 9, 11, tzinfo=timezone.utc).astimezone(ZoneInfo("US/Pacific"))
    result_ids = [g.game_id for g in get_games_by_start_datetime(session, from_datetime, to_datetime)]
    expected_ids = [
        seed_games[id].game_id
        for id in seed_games.keys()
        if seed_games[id].start_epoc_sec >= int(from_datetime.timestamp())
        and seed_games[id].start_epoc_sec <= int(to_datetime.timestamp())
    ]
    assert sorted(result_ids) == sorted(expected_ids)


def test_get_games_by_start_datetime_returns_matched_team_if_from_equal_to(
    session: Session, seed_games: dict[str, Game]
) -> None:
    from_datetime = datetime(2025, 9, 1, tzinfo=timezone.utc)
    to_datetime = datetime(2025, 9, 1, tzinfo=timezone.utc)
    result_ids = [g.game_id for g in get_games_by_start_datetime(session, from_datetime, to_datetime)]
    expected_ids = [
        seed_games[id].game_id
        for id in seed_games.keys()
        if seed_games[id].start_epoc_sec >= int(from_datetime.timestamp())
        and seed_games[id].start_epoc_sec <= int(to_datetime.timestamp())
    ]
    assert sorted(result_ids) == sorted(expected_ids)


def test_get_games_by_start_datetime_returns_empty_list_if_no_match(session: Session) -> None:
    from_datetime = datetime(2024, 9, 1, tzinfo=timezone.utc)
    to_datetime = datetime(2024, 9, 11, tzinfo=timezone.utc)
    result_ids = [g.game_id for g in get_games_by_start_datetime(session, from_datetime, to_datetime)]
    assert result_ids == []


def test_get_games_by_start_datetime_returns_empty_list_if_from_is_larger_than_to(session: Session) -> None:
    from_datetime = datetime(2025, 9, 11, tzinfo=timezone.utc)
    to_datetime = datetime(2025, 9, 1, tzinfo=timezone.utc)
    result_ids = [g.game_id for g in get_games_by_start_datetime(session, from_datetime, to_datetime)]
    assert result_ids == []
