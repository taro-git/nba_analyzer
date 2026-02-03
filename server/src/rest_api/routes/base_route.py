from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from common.db import get_session

api_router = APIRouter(prefix="/api")


@api_router.get("/test")
async def test():
    return {"Hello": "World"}


@api_router.get("/{path:path}")
async def not_found(session: Session = Depends(get_session)):
    return session.exec(select(SQLModel)).all()
