from sqlmodel import Session, col, select

from common.models.teams.teams import Team


def get_teams_by_ids(session: Session, team_ids: list[int]) -> list[Team]:
    """
    チーム ID を指定してチーム情報を返します.
    """
    statement = select(Team).where(col(Team.id).in_(team_ids))
    return list(session.exec(statement).all())
