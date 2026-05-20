from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, distinct, select

from common.db import engine
from common.models.games.game_actions import GameAction


def get_all_game_ids() -> list[int]:
    """
    GameAction の試合の内部管理用ID 一覧を返します.
    """
    with Session(engine) as session:
        return [i for i in session.exec(select(distinct(GameAction.game_id))).all()]


def upsert_game_actions(game_actions: list[GameAction]) -> None:
    """
    GameAction 一覧を DB に UPSERT します.
    既存なら UPDATE、なければ INSERT.
    """
    if not game_actions:
        return
    with Session(engine) as session:
        stmt = insert(GameAction).values([
            {k: v for k, v in a.model_dump().items() if k != "id"}
            for a in game_actions
        ])
        stmt = stmt.on_conflict_do_update(
            index_elements=["game_id", "action_number"],
            set_={
                "elapsed_ms": stmt.excluded.elapsed_ms,
                "game_player_id": stmt.excluded.game_player_id,
                "team_id": stmt.excluded.team_id,
                "description": stmt.excluded.description,
                "action_type": stmt.excluded.action_type,
                "sub_type": stmt.excluded.sub_type,
                "shot_value": stmt.excluded.shot_value,
                "home_score": stmt.excluded.home_score,
                "away_score": stmt.excluded.away_score,
                "x_legacy": stmt.excluded.x_legacy,
                "y_legacy": stmt.excluded.y_legacy,
            },
        )
        session.exec(stmt)
        session.commit()
