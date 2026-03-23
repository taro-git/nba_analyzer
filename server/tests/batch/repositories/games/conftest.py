import pytest
from sqlmodel import Session

from common.models.games.games import Game
from common.types import GameCategory, GameStatus


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
                    home_team_id=1610612765,
                    away_team_id=1610612756,
                    home_score=0,
                    away_score=0,
                    playoff_label="Playoffs" if category == GameCategory.playoffs else None,
                )
            )
    return data


@pytest.fixture
def seed_games(session: Session) -> dict[str, Game]:
    """
    Game のテスト用データ
    """

    games = _create_games(2025)
    session.add_all(games)
    session.commit()

    return {g.game_id: g for g in games}
