import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from batch.repositories.games.game_actions import add_game_actions
from common.models.games.game_actions import GameAction
from common.models.games.game_players import GamePlayer
from common.models.games.games import Game

HOME_TEAM_ID = 1610612765


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> None:
    mocker.patch("batch.repositories.games.game_actions.engine", engine)


def _make_action(
    game_id: int,
    action_number: int = 0,
    elapsed_ms: int = 0,
    game_player_id: int | None = None,
    team_id: int | None = None,
    description: str = "desc",
    action_type: str = "2pt",
    sub_type: str | None = None,
    shot_value: int | None = 2,
    home_score: int | None = None,
    away_score: int | None = None,
    x_legacy: int | None = None,
    y_legacy: int | None = None,
) -> GameAction:
    return GameAction(
        game_id=game_id,
        action_number=action_number,
        elapsed_ms=elapsed_ms,
        game_player_id=game_player_id,
        team_id=team_id,
        description=description,
        action_type=action_type,
        sub_type=sub_type,
        shot_value=shot_value,
        home_score=home_score,
        away_score=away_score,
        x_legacy=x_legacy,
        y_legacy=y_legacy,
    )


def test_add_game_actions_adds_one(
    mock_engine: None, seed_game: Game, seed_game_players: list[GamePlayer], session: Session
) -> None:
    assert seed_game.id is not None
    add_game_actions([_make_action(seed_game.id, action_number=0)])
    result = session.exec(select(GameAction)).all()
    assert len(result) == 1
    assert result[0].game_id == seed_game.id
    assert result[0].action_number == 0


def test_add_game_actions_adds_many(
    mock_engine: None, seed_game: Game, seed_game_players: list[GamePlayer], session: Session
) -> None:
    assert seed_game.id is not None
    actions = [_make_action(seed_game.id, action_number=i) for i in range(5)]
    add_game_actions(actions)
    result = session.exec(select(GameAction)).all()
    assert len(result) == 5


def test_add_game_actions_no_action_if_empty(mock_engine: None, seed_game: Game, session: Session) -> None:
    add_game_actions([])
    result = session.exec(select(GameAction)).all()
    assert len(result) == 0


def test_add_game_actions_error_on_duplicate_action_number(
    mock_engine: None, seed_game: Game, session: Session
) -> None:
    assert seed_game.id is not None
    add_game_actions([_make_action(seed_game.id, action_number=0)])
    with pytest.raises(IntegrityError):
        add_game_actions([_make_action(seed_game.id, action_number=0)])


def test_add_game_actions_with_game_player_id(
    mock_engine: None, seed_game: Game, seed_game_players: list[GamePlayer], session: Session
) -> None:
    assert seed_game.id is not None
    gp = seed_game_players[0]
    add_game_actions([_make_action(seed_game.id, action_number=0, game_player_id=gp.id)])
    result = session.exec(select(GameAction)).all()
    assert result[0].game_player_id == gp.id


def test_add_game_actions_with_team_id(mock_engine: None, seed_game: Game, session: Session) -> None:
    assert seed_game.id is not None
    add_game_actions([_make_action(seed_game.id, action_number=0, team_id=HOME_TEAM_ID)])
    result = session.exec(select(GameAction)).all()
    assert result[0].team_id == HOME_TEAM_ID


def test_add_game_actions_error_on_negative_elapsed_ms(mock_engine: None, seed_game: Game, session: Session) -> None:
    assert seed_game.id is not None
    with pytest.raises(IntegrityError):
        add_game_actions([_make_action(seed_game.id, action_number=0, elapsed_ms=-1)])


def test_add_game_actions_error_on_invalid_shot_value(mock_engine: None, seed_game: Game, session: Session) -> None:
    assert seed_game.id is not None
    with pytest.raises(IntegrityError):
        add_game_actions([_make_action(seed_game.id, action_number=0, shot_value=4)])
