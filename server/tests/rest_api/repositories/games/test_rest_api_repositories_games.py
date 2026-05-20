from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlmodel import Session

from common.models.games.games import Game
from rest_api.repositories.games.games import get_game_by_game_id, get_games_by_start_datetime, get_games_by_team_ids


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


def test_get_game_by_game_id_returns_game(session: Session, seed_games: dict[str, Game]) -> None:
    game_id = list(seed_games.keys())[0]
    result = get_game_by_game_id(session, game_id)
    assert result is not None and result.game_id == game_id


def test_get_game_by_game_id_returns_none_if_not_found(session: Session, seed_games: dict[str, Game]) -> None:
    game_id = "not_found"
    result = get_game_by_game_id(session, game_id)
    assert result is None


def test_get_games_by_team_ids_returns_matched_games(session: Session, seed_games: dict[str, Game]) -> None:
    team_ids = [1610612765, 1610612756]
    result_ids = [g.game_id for g in get_games_by_team_ids(session, team_ids)]
    expected_ids = [
        seed_games[id].game_id
        for id in seed_games.keys()
        if seed_games[id].home_team_id in team_ids and seed_games[id].away_team_id in team_ids
    ]
    assert sorted(result_ids) == sorted(expected_ids)


def test_get_games_by_team_ids_returns_matched_games_for_single_team(
    session: Session, seed_games: dict[str, Game]
) -> None:
    team_ids = [1610612765]
    result_ids = [g.game_id for g in get_games_by_team_ids(session, team_ids)]
    # 単一チームIDの場合、ホームとアウェイの両方がそのチームIDである試合のみ（通常は存在しない）
    expected_ids = [
        seed_games[id].game_id
        for id in seed_games.keys()
        if seed_games[id].home_team_id in team_ids and seed_games[id].away_team_id in team_ids
    ]
    assert sorted(result_ids) == sorted(expected_ids)


def test_get_games_by_team_ids_returns_empty_list_if_no_match(session: Session, seed_games: dict[str, Game]) -> None:
    team_ids = [9999]
    result_ids = [g.game_id for g in get_games_by_team_ids(session, team_ids)]
    assert result_ids == []


def test_get_games_by_team_ids_returns_empty_list_if_empty_input(session: Session, seed_games: dict[str, Game]) -> None:
    team_ids: list[int] = []
    result_ids = [g.game_id for g in get_games_by_team_ids(session, team_ids)]
    assert result_ids == []
