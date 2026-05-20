import pytest
from sqlmodel import Session

from common.models.commons.seasons import Season
from common.models.games.game_players import GamePlayer
from common.models.games.games import Game
from common.models.players.players import Player
from common.models.teams.teams import Team
from common.types import GameCategory, GameStatus, PlayerPosition

HOME_TEAM_ID = 1610612765
AWAY_TEAM_ID = 1610612756
GAME_ID = "0022500500"
PLAYER_ID_1 = 1001
PLAYER_ID_2 = 1002


def _create_games(season: int) -> list[Game]:
    data: list[Game] = []
    for category_id in [1, 2, 3, 4, 5, 6, 9]:
        for status_id in [1, 2, 3]:
            game_id = f"00{category_id}{season % 100:02d}{status_id:05d}"
            category = GameCategory.from_game_id(game_id)
            data.append(
                Game(
                    game_id=game_id,
                    season=season,
                    start_epoc_sec=1767193200,
                    elapsed_sec=0,
                    status=GameStatus.from_status_id(status_id),
                    category=category,
                    home_team_id=HOME_TEAM_ID,
                    away_team_id=AWAY_TEAM_ID,
                    home_score=0,
                    away_score=0,
                    playoff_label="Playoffs" if category == GameCategory.playoffs else None,
                )
            )
    return data


@pytest.fixture
def seed_season(session: Session) -> None:
    session.add(Season(start_year=2025))
    session.commit()


@pytest.fixture
def seed_teams(session: Session) -> None:
    session.add_all([Team(id=HOME_TEAM_ID), Team(id=AWAY_TEAM_ID)])
    session.commit()


@pytest.fixture
def seed_players(session: Session, seed_teams: None) -> None:
    session.add_all(
        [
            Player(id=PLAYER_ID_1, updated_at=1767193200, full_name="Player One", abbreviation="P. One"),
            Player(id=PLAYER_ID_2, updated_at=1767193200, full_name="Player Two", abbreviation="P. Two"),
        ]
    )
    session.commit()


@pytest.fixture
def seed_games(session: Session, seed_season: None, seed_teams: None) -> dict[str, Game]:
    """
    Game のテスト用データ
    """
    games = _create_games(2025)
    session.add_all(games)
    session.commit()

    return {g.game_id: g for g in games}


@pytest.fixture
def seed_game(session: Session, seed_season: None, seed_teams: None) -> Game:
    """
    単一 Game のテスト用データ
    """
    game = Game(
        game_id=GAME_ID,
        season=2025,
        start_epoc_sec=1767193200,
        elapsed_sec=0,
        status=GameStatus.final,
        category=GameCategory.regular_season,
        home_team_id=HOME_TEAM_ID,
        away_team_id=AWAY_TEAM_ID,
        home_score=110,
        away_score=105,
        playoff_label=None,
    )
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@pytest.fixture
def seed_game_players(session: Session, seed_game: Game, seed_players: None) -> list[GamePlayer]:
    """
    GamePlayer のテスト用データ
    """
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
            jearsy_num="11",
            position=PlayerPosition.small_forward,
            is_home=False,
            is_starter=True,
            is_active=True,
        ),
    ]
    session.add_all(players)
    session.commit()
    for p in players:
        session.refresh(p)
    return players
