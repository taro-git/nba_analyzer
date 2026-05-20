from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from common.models.games.game_actions import GameAction
from common.models.games.game_players import GamePlayer as GamePlayerModel
from common.models.games.stats import Stats
from rest_api.schemas.games.game_summaries import GameSummarySchema
from rest_api.schemas.players.players import GamePlayer


class Play(BaseModel):
    """
    一つのプレイを示します.
    """

    action_number: int
    """アクション番号"""
    elapsed_ms: int
    """試合の経過時間(ミリ秒)"""
    team_id: int | None
    """チームID"""
    player_id: int | None
    """選手ID"""
    description: str
    """アクションの詳細"""
    home_score: int | None
    """ホームチームの得点数"""
    away_score: int | None
    """アウェイチームの得点数"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    @classmethod
    def from_game_action_and_game_players(cls, game_action: GameAction, game_players: list[GamePlayerModel]) -> "Play":
        return Play(
            action_number=game_action.action_number,
            elapsed_ms=game_action.elapsed_ms,
            team_id=game_action.team_id,
            player_id=next((gp.player_id for gp in game_players if gp.id == game_action.game_player_id), None),
            description=game_action.description,
            home_score=game_action.home_score,
            away_score=game_action.away_score,
        )


class Statics(BaseModel):
    """
    スタッツを示します.
    """

    elapsed_ms: int
    """試合の経過時間(ミリ秒)"""
    sec: int
    """出場時間(秒)"""
    points: int
    """得点"""
    offence_rebounds: int
    """オフェンスバウンド"""
    diffence_rebounds: int
    """ディフェンスバウンド"""
    assists: int
    """アシスト"""
    steals: int
    """スティール"""
    blocks: int
    """ブロック"""
    field_goal_attempts: int
    """フィールドゴール試行回数"""
    field_goal_made: int
    """フィールドゴール成功数"""
    three_point_attempts: int
    """三ポイント試行回数"""
    three_point_made: int
    """三ポイント成功数"""
    free_throw_attempts: int
    """フリースロー試行回数"""
    free_throw_made: int
    """フリースロー成功数"""
    turnovers: int
    """ターンオーバー"""
    blocked_shots_received: int | None
    """被ブロック数"""
    personal_fouls: int
    """パーソナルファール"""
    technical_fouls: int | None
    """テクニカルファール"""
    fouls_drawn: int | None
    """被ファール数"""
    plus: int | None
    """出場中のチーム全体の得点"""
    plus_minus: int
    """出場中のチーム全体の得失点差"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    @classmethod
    def from_Stats(cls, stats: Stats) -> "Statics":
        return Statics(
            elapsed_ms=stats.elapsed_ms,
            sec=stats.ms // 1000,
            points=stats.points,
            offence_rebounds=stats.offence_rebounds,
            diffence_rebounds=stats.diffence_rebounds,
            assists=stats.assists,
            steals=stats.steals,
            blocks=stats.blocks,
            field_goal_attempts=stats.field_goal_attempts,
            field_goal_made=stats.field_goal_made,
            three_point_attempts=stats.three_point_attempts,
            three_point_made=stats.three_point_made,
            free_throw_attempts=stats.free_throw_attempts,
            free_throw_made=stats.free_throw_made,
            turnovers=stats.turnovers,
            blocked_shots_received=stats.blocked_shots_received,
            personal_fouls=stats.personal_fouls,
            technical_fouls=stats.technical_fouls,
            fouls_drawn=stats.fouls_drawn,
            plus=stats.plus,
            plus_minus=stats.plus_minus,
        )


class PlayerStats(GamePlayer):
    """
    プレイヤーのスタッツを示します.
    """

    statics: list[Statics]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class TeamStats(BaseModel):
    """
    チームのスタッツを示します.
    """

    statics: list[Statics]
    players: list[PlayerStats]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class GameDetailSchema(GameSummarySchema):
    """
    試合の詳細を示します.
    """

    play_by_play: list[Play]
    home_team_stats: TeamStats
    away_team_stats: TeamStats

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
