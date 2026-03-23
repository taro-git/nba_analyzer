from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from common.db import engine
from common.models.games.games import Game


def upsert_games(games: list[Game]) -> None:
    """
    試合一覧を UPSERT します.
    既存なら UPDATE、なければ INSERT.
    """
    if not games:
        return

    with Session(engine) as session:
        stmt = insert(Game).values(
            [
                {
                    "game_id": g.game_id,
                    "season": g.season,
                    "category": g.category,
                    "status": g.status,
                    "start_epoc_sec": g.start_epoc_sec,
                    "elapsed_sec": g.elapsed_sec,
                    "home_team_id": g.home_team_id,
                    "away_team_id": g.away_team_id,
                    "home_score": g.home_score,
                    "away_score": g.away_score,
                    "playoff_label": g.playoff_label,
                }
                for g in games
            ]
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["game_id"],
            set_={
                "season": stmt.excluded.season,
                "category": stmt.excluded.category,
                "status": stmt.excluded.status,
                "start_epoc_sec": stmt.excluded.start_epoc_sec,
                "elapsed_sec": stmt.excluded.elapsed_sec,
                "home_team_id": stmt.excluded.home_team_id,
                "away_team_id": stmt.excluded.away_team_id,
                "home_score": stmt.excluded.home_score,
                "away_score": stmt.excluded.away_score,
                "playoff_label": stmt.excluded.playoff_label,
            },
        )

        session.exec(stmt)
        session.commit()
