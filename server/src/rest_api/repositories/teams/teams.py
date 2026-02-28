from sqlmodel import Session, col, select

from common.models.teams.teams import TeamProperty
from rest_api.schemas.commons import Season


def get_team_properties_by_ids(session: Session, season: Season, team_ids: list[int]) -> list[TeamProperty]:
    """
    チーム ID を指定してチーム情報を返します.
    """
    statement = select(TeamProperty).where(
        col(TeamProperty.team_id).in_(team_ids), col(TeamProperty.season) == int(season[:4])
    )
    return list(session.exec(statement).all())
