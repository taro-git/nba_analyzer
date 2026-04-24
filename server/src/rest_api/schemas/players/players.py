from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from common.types import PlayerPosition


class Player(BaseModel):
    """
    プレイヤーの基本情報を示します.
    """

    player_id: int
    """プレイヤーID"""
    team_id: int | None
    """所属チームID"""
    full_name: str
    """名称"""
    abbreviation: str
    """略称"""
    position: PlayerPosition | None
    """ポジション"""
    date_of_birth: date | None
    """生年月日"""
    draft_year: int | None
    """ドラフト年"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class GamePlayer(Player):
    jearsy_num: str
    """背番号"""
    is_home: bool
    """ホームチームか否か"""
    is_starter: bool
    """スターティングメンバーか否か"""
    is_active: bool
    """アクティブか否か"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
