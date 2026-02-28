from sqlmodel import Session, col, select

from batch.types import Season
from common.db import engine
from common.models.teams.teams import Team, TeamProperty


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


def get_team_properties_by_season(season: Season) -> list[TeamProperty]:
    """
    シーズンを指定して、チーム情報一覧を返します.
    """
    with Session(engine) as session:
        statement = select(TeamProperty).where(col(TeamProperty.season) == season.start_year)
        return list(session.exec(statement).all())


def add_team_properties(team_properties: list[TeamProperty]) -> None:
    """
    TeamProperty のリストを DB に登録します.
    """
    with Session(engine) as session:
        session.add_all(team_properties)
        session.commit()
