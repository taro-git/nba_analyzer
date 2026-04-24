from sqlmodel import Session

from common.models.players.players import Player
from rest_api.repositories.players.players import get_players_by_player_ids


def test_get_players_by_player_ids_returns_matched_player(session: Session, seed_players: dict[int, Player]) -> None:
    player_id = list(seed_players.keys())[0]
    result = get_players_by_player_ids(session, [player_id])
    assert len(result) == 1 and result[0].id == player_id


def test_get_players_by_player_ids_returns_matched_players(session: Session, seed_players: dict[int, Player]) -> None:
    player_ids = list(seed_players.keys())
    result = get_players_by_player_ids(session, player_ids)
    assert {p.id for p in result} == set(player_ids)


def test_get_players_by_player_ids_returns_only_matched_player(
    session: Session, seed_players: dict[int, Player]
) -> None:
    player_ids = [list(seed_players.keys())[0], -1]
    result = get_players_by_player_ids(session, player_ids)
    assert len(result) == 1 and result[0].id == player_ids[0]


def test_get_players_by_player_ids_returns_empty_list_if_not_found(
    session: Session, seed_players: dict[int, Player]
) -> None:
    player_ids = [-1]
    result = get_players_by_player_ids(session, player_ids)
    assert len(result) == 0


def test_get_players_by_player_ids_returns_empty_list_if_input_empty_list(
    session: Session, seed_players: dict[int, Player]
) -> None:
    player_ids: list[int] = []
    result = get_players_by_player_ids(session, player_ids)
    assert len(result) == 0
