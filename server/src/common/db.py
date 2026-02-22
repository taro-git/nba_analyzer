import os
from typing import Generator

from sqlmodel import Session, create_engine

HOST = os.environ.get("DB_HOST", "postgres")
PORT = os.environ.get("DB_PORT", "5432")
NAME = os.environ.get("DB_NAME", "nba_analyzer")
USER = os.environ.get("DB_USER", "nba_analyzer_user")
PASSWORD = os.environ.get("DB_PASSWORD", "nba_analyzer_password")

engine = create_engine(
    f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}",
    echo=False,
    pool_pre_ping=True,
)


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session
