from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from random import randint

import pytest
from sqlmodel import Session

from common.models.games.game_actions import GameAction
from common.models.games.game_players import GamePlayer
from common.models.games.games import Game
from common.models.games.stats import Stats
from common.types import GameCategory, GameStatus


def _create_games(from_utc: datetime, to_utc: datetime) -> list[Game]:
    data: list[Game] = []
    if to_utc < from_utc:
        return data
    for days in [i for i in range((to_utc - from_utc).days + 1)]:
        game_date = from_utc + timedelta(days=days)
        season = game_date.year if game_date.month >= 10 else game_date.year - 1
        game_id = f"002{season % 100:02d}{days:05d}"
        data.append(
            Game(
                game_id=game_id,
                season=season,
                start_epoc_sec=int(game_date.timestamp()),
                elapsed_sec=0,
                status=GameStatus.scheduled,
                category=GameCategory.from_game_id(game_id),
                home_team_id=1610612765,
                away_team_id=1610612756,
                home_score=0,
                away_score=0,
                playoff_label=None,
            )
        )
    return data


@pytest.fixture
def seed_games(session: Session) -> dict[str, Game]:
    """
    Game のテスト用データ
    2025-09-01T00:00:00Z から 2026-01-31T00:00:00Z まで24時間ごとに1試合ずつ
    """

    games = _create_games(datetime(2025, 9, 1, tzinfo=timezone.utc), datetime(2026, 1, 31, tzinfo=timezone.utc))
    session.add_all(games)
    session.commit()

    return {g.game_id: g for g in games}


@dataclass
class GameDataSeed:
    game: Game
    game_actions: list[GameAction] = field(default_factory=list[GameAction])
    game_players: list[GamePlayer] = field(default_factory=list[GamePlayer])
    stats: list[Stats] = field(default_factory=list[Stats])


@pytest.fixture
def seed_game_actions(session: Session, seed_games: dict[str, Game]) -> list[GameDataSeed]:
    """
    GameAction のテスト用データ
    """
    max_actions_per_game = 10
    actions_seeds: list[GameDataSeed] = [
        GameDataSeed(
            game=g,
            game_actions=[
                GameAction(
                    game_id=g.id,
                    action_number=i,
                    elapsed_ms=i * 1000,
                    description=f"action {i}",
                    action_type=f"action type {i}",
                )
                for i in range(randint(1, max_actions_per_game))
            ],
        )
        for g in seed_games.values()
        if g.id is not None
    ]
    seeds: list[GameAction] = []
    for s in actions_seeds:
        seeds.extend(s.game_actions)
    session.add_all(seeds)
    session.commit()
    return actions_seeds


@pytest.fixture
def seed_game_players(session: Session, seed_games: dict[str, Game]) -> list[GameDataSeed]:
    """
    GamePlayer のテスト用データ
    """
    max_players_per_game = 10
    game_player_seeds: list[GameDataSeed] = [
        GameDataSeed(
            game=g,
            game_players=[
                GamePlayer(
                    game_id=g.id,
                    player_id=i,
                    jearsy_num=str(i),
                    position=None,
                    is_home=True,
                    is_starter=False,
                    is_active=True,
                )
                for i in range(randint(1, max_players_per_game))
            ],
        )
        for g in seed_games.values()
        if g.id is not None
    ]
    seeds: list[GamePlayer] = []
    for p in game_player_seeds:
        seeds.extend(p.game_players)
    session.add_all(seeds)
    session.commit()
    return game_player_seeds


@pytest.fixture
def seed_stats(session: Session, seed_games: dict[str, Game]) -> list[GameDataSeed]:
    """
    Stats のテスト用データ
    """
    max_players_per_game = 10
    stats_seeds: list[GameDataSeed] = [
        GameDataSeed(
            game=g,
            stats=[
                Stats(
                    game_id=g.id,
                    game_player_id=i,
                    elapsed_ms=0,
                    ms=0,
                    points=0,
                    offence_rebounds=0,
                    diffence_rebounds=0,
                    assists=0,
                    steals=0,
                    blocks=0,
                    field_goal_attempts=0,
                    field_goal_made=0,
                    three_point_attempts=0,
                    three_point_made=0,
                    free_throw_attempts=0,
                    free_throw_made=0,
                    turnovers=0,
                    blocked_shots_received=0,
                    personal_fouls=0,
                    technical_fouls=0,
                    fouls_drawn=0,
                    plus=0,
                    plus_minus=0,
                )
                for i in range(randint(1, max_players_per_game))
            ],
        )
        for g in seed_games.values()
        if g.id is not None
    ]
    seeds: list[Stats] = []
    for s in stats_seeds:
        seeds.extend(s.stats)
    session.add_all(seeds)
    session.commit()
    return stats_seeds
