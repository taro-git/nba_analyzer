from sqlmodel import CheckConstraint, Field, SQLModel


class Season(SQLModel, table=True):
    """
    NBA シーズンを表すテーブル.
    """

    __tablename__ = "seasons"  # type: ignore

    start_year: int = Field(primary_key=True)
    """シーズン開始年"""

    __table_args__ = (
        CheckConstraint(
            "start_year > 1970",
            name="check_start_year_gt_1970",
        ),
    )
