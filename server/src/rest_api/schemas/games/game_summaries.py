from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from rest_api.schemas.commons import GameCategory, GameStatus
from rest_api.schemas.teams.regular_season import Team


class GameSummarySchema(BaseModel):
    """
    試合の概要を示します.
    """

    game_id: str
    """ゲームID"""
    status: GameStatus
    """ゲームステータス"""
    category: GameCategory
    """ゲームカテゴリ"""
    start_datetime: datetime
    """ゲーム開始日時"""
    elapsed_sec: int
    """ゲーム経過秒数"""
    home_team: Team
    """ホームチーム"""
    away_team: Team
    """アウェイチーム"""
    home_team_score: int
    """ホームチームの得点"""
    away_team_score: int
    """アウェイチームの得点"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
