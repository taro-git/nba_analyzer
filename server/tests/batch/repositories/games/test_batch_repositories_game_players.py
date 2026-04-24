import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from batch.repositories.games.game_players import (
    add_game_players_and_ignore_existing,
    get_game_players_by_game_id,
)
from common.models.games.game_players import GamePlayer
from common.models.games.games import Game
from common.types import PlayerPosition
from tests.batch.repositories.games.conftest import PLAYER_ID_1, PLAYER_ID_2


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> None:
    mocker.patch("batch.repositories.games.game_players.engine", engine)


def test_get_game_players_by_game_id_returns_players(
    mock_engine: None, seed_game: Game, seed_game_players: list[GamePlayer]
) -> None:
    assert seed_game.id is not None
    result = get_game_players_by_game_id(seed_game.id)
    assert len(result) == 2
    player_ids = {p.player_id for p in result}
    assert player_ids == {PLAYER_ID_1, PLAYER_ID_2}


def test_get_game_players_by_game_id_returns_empty_for_unknown_game(mock_engine: None, seed_game: Game) -> None:
    result = get_game_players_by_game_id(99999)
    assert result == []


def test_add_game_players_and_ignore_existing_and_ignore_existing_adds_one(
    mock_engine: None, seed_game: Game, seed_players: None, session: Session
) -> None:
    assert seed_game.id is not None
    players = [
        GamePlayer(
            game_id=seed_game.id,
            player_id=PLAYER_ID_1,
            jearsy_num="23",
            position=PlayerPosition.point_guard,
            is_home=True,
            is_starter=True,
            is_active=True,
        )
    ]
    add_game_players_and_ignore_existing(players)
    result = session.exec(select(GamePlayer)).all()
    assert len(result) == 1
    assert result[0].player_id == PLAYER_ID_1


def test_add_game_players_and_ignore_existing_and_ignore_existing_adds_many(
    mock_engine: None, seed_game: Game, seed_players: None, session: Session
) -> None:
    assert seed_game.id is not None
    players = [
        GamePlayer(
            game_id=seed_game.id,
            player_id=PLAYER_ID_1,
            jearsy_num="23",
            position=PlayerPosition.point_guard,
            is_home=True,
            is_starter=True,
            is_active=True,
        ),
        GamePlayer(
            game_id=seed_game.id,
            player_id=PLAYER_ID_2,
            jearsy_num="23",
            position=PlayerPosition.point_guard,
            is_home=True,
            is_starter=True,
            is_active=True,
        ),
    ]
    add_game_players_and_ignore_existing(players)
    result = session.exec(select(GamePlayer)).all()
    assert len(result) == 2
    assert {p.player_id for p in result} == {PLAYER_ID_1, PLAYER_ID_2}


def test_add_game_players_and_ignore_existing_and_ignore_existing_adds_only_new(
    mock_engine: None, seed_game_players: list[GamePlayer], session: Session
) -> None:
    game_id = seed_game_players[0].game_id
    seed_game_player_ids = {p.player_id for p in seed_game_players}
    player_id = sum(seed_game_player_ids)
    players = [
        GamePlayer(
            game_id=p.game_id,
            player_id=p.player_id,
            jearsy_num=p.jearsy_num,
            position=p.position,
            is_home=not p.is_home,
            is_starter=not p.is_starter,
            is_active=not p.is_active,
        )
        for p in seed_game_players
    ] + [
        GamePlayer(
            game_id=game_id,
            player_id=player_id,
            jearsy_num="new player",
            position=PlayerPosition.point_guard,
            is_home=True,
            is_starter=True,
            is_active=True,
        )
    ]
    add_game_players_and_ignore_existing(players)
    result = session.exec(select(GamePlayer)).all()
    assert len(result) == 3
    assert {p.player_id for p in result} == set([p.player_id for p in seed_game_players] + [player_id])
    result_is_home = {p.player_id: p.is_home for p in result if p.player_id in seed_game_player_ids}
    assert all([p.is_home == result_is_home[p.player_id] for p in seed_game_players])


def test_add_game_players_and_ignore_existing_error_on_starter_not_active(
    mock_engine: None, seed_game: Game, seed_players: None
) -> None:
    assert seed_game.id is not None
    with pytest.raises(IntegrityError):
        add_game_players_and_ignore_existing(
            [
                GamePlayer(
                    game_id=seed_game.id,
                    player_id=PLAYER_ID_1,
                    jearsy_num="23",
                    position=None,
                    is_home=True,
                    is_starter=True,
                    is_active=False,
                )
            ]
        )
