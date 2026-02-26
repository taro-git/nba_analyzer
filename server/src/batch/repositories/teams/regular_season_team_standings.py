from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from common.db import engine
from common.models.teams.regular_season_team_standings import RegularSeasonTeamStanding


def upsert_regular_season_team_standings(
    regular_season_team_standings: list[RegularSeasonTeamStanding],
) -> None:
    """
    レギュラーシーズンのチーム成績一覧を UPSERT します。
    既存なら UPDATE、なければ INSERT。
    """
    if not regular_season_team_standings:
        return

    with Session(engine) as session:
        stmt = insert(RegularSeasonTeamStanding).values(
            [
                {
                    "season": s.season,
                    "team_id": s.team_id,
                    "rank": s.rank,
                    "win": s.win,
                    "lose": s.lose,
                }
                for s in regular_season_team_standings
            ]
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["season", "team_id"],
            set_={
                "rank": stmt.excluded.rank,
                "win": stmt.excluded.win,
                "lose": stmt.excluded.lose,
            },
        )

        session.exec(stmt)
        session.commit()
