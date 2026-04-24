from datetime import datetime

from batch.services.games.games import (
    get_no_stats_games_by_start_datetime,
)
from common.models.games.games import Game
from common.types import GameStatus


def get_unninitialized_games_by_start_datetime(
    from_datetime: datetime, to_datetime: datetime, status: GameStatus = GameStatus.final
) -> list[Game]:
    """
    試合開始時刻の範囲を指定して初期化されていない Game 一覧を返します.
    """
    return get_no_stats_games_by_start_datetime(from_datetime, to_datetime, status)
