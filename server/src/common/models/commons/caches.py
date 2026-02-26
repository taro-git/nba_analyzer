from datetime import datetime
from typing import Any

from sqlalchemy import JSON, TIMESTAMP, BigInteger, Column
from sqlmodel import Field, SQLModel


class Cache(SQLModel, table=True):
    """
    外部API からのレスポンスをキャッシュするテーブル.
    """

    __tablename__ = "caches"  # type: ignore

    request_hash: int = Field(sa_column=Column(BigInteger, primary_key=True))
    """リクエストのハッシュ値"""
    response: dict[str, Any] = Field(sa_column=Column(JSON, nullable=False))
    """レスポンス"""
    expires_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
        )
    )
    """キャッシュ有効期限"""
