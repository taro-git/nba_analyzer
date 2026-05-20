from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, distinct, select

from common.db import engine
from common.models.games.stats import Stats


def get_all_game_ids() -> list[int]:
    """
    Stats の試合の内部管理用ID 一覧を返します.
    """
    with Session(engine) as session:
        return [i for i in session.exec(select(distinct(Stats.game_id))).all() if i is not None]


def upsert_stats_list(stats_list: list[Stats]) -> None:
    """
    Stats 一覧を DB に UPSERT します.
    既存なら UPDATE、なければ INSERT.
    """
    if not stats_list:
        return
    player_stats = [s for s in stats_list if s.game_player_id is not None]
    team_stats = [s for s in stats_list if s.game_player_id is None]
    with Session(engine) as session:
        if player_stats:
            player_stmt = insert(Stats).values(
                [{k: v for k, v in a.model_dump().items() if k != "id"} for a in player_stats]
            )
            player_stmt = player_stmt.on_conflict_do_update(
                index_elements=[
                    "game_id",
                    "game_player_id",
                    "elapsed_ms",
                ],
                set_={
                    "ms": player_stmt.excluded.ms,
                    "points": player_stmt.excluded.points,
                    "offence_rebounds": player_stmt.excluded.offence_rebounds,
                    "diffence_rebounds": player_stmt.excluded.diffence_rebounds,
                    "assists": player_stmt.excluded.assists,
                    "steals": player_stmt.excluded.steals,
                    "blocks": player_stmt.excluded.blocks,
                    "field_goal_attempts": player_stmt.excluded.field_goal_attempts,
                    "field_goal_made": player_stmt.excluded.field_goal_made,
                    "three_point_attempts": player_stmt.excluded.three_point_attempts,
                    "three_point_made": player_stmt.excluded.three_point_made,
                    "free_throw_attempts": player_stmt.excluded.free_throw_attempts,
                    "free_throw_made": player_stmt.excluded.free_throw_made,
                    "turnovers": player_stmt.excluded.turnovers,
                    "blocked_shots_received": player_stmt.excluded.blocked_shots_received,
                    "personal_fouls": player_stmt.excluded.personal_fouls,
                    "technical_fouls": player_stmt.excluded.technical_fouls,
                    "fouls_drawn": player_stmt.excluded.fouls_drawn,
                    "plus": player_stmt.excluded.plus,
                    "plus_minus": player_stmt.excluded.plus_minus,
                },
            )
            session.exec(player_stmt)
        if team_stats:
            team_stmt = insert(Stats).values(
                [{k: v for k, v in a.model_dump().items() if k != "id"} for a in team_stats]
            )
            team_stmt = team_stmt.on_conflict_do_update(
                index_elements=[
                    "game_id",
                    "team_id",
                    "elapsed_ms",
                ],
                set_={
                    "ms": team_stmt.excluded.ms,
                    "points": team_stmt.excluded.points,
                    "offence_rebounds": team_stmt.excluded.offence_rebounds,
                    "diffence_rebounds": team_stmt.excluded.diffence_rebounds,
                    "assists": team_stmt.excluded.assists,
                    "steals": team_stmt.excluded.steals,
                    "blocks": team_stmt.excluded.blocks,
                    "field_goal_attempts": team_stmt.excluded.field_goal_attempts,
                    "field_goal_made": team_stmt.excluded.field_goal_made,
                    "three_point_attempts": team_stmt.excluded.three_point_attempts,
                    "three_point_made": team_stmt.excluded.three_point_made,
                    "free_throw_attempts": team_stmt.excluded.free_throw_attempts,
                    "free_throw_made": team_stmt.excluded.free_throw_made,
                    "turnovers": team_stmt.excluded.turnovers,
                    "blocked_shots_received": team_stmt.excluded.blocked_shots_received,
                    "personal_fouls": team_stmt.excluded.personal_fouls,
                    "technical_fouls": team_stmt.excluded.technical_fouls,
                    "fouls_drawn": team_stmt.excluded.fouls_drawn,
                    "plus": team_stmt.excluded.plus,
                    "plus_minus": team_stmt.excluded.plus_minus,
                },
            )
            session.exec(team_stmt)
        session.commit()
