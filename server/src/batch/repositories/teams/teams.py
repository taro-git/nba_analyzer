from sqlmodel import Session, select

from common.db import engine
from common.models.teams.teams import Team


def get_teams() -> list[Team]:
    """
    チーム一覧を返します.
    """
    with Session(engine) as session:
        return list(session.exec(select(Team)).all())


def add_teams(teams: list[Team]) -> None:
    """
    Team のリストを DB に登録します.
    """
    with Session(engine) as session:
        session.add_all(teams)
        session.commit()
