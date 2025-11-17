from fastapi import APIRouter
import socket

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine

router = APIRouter()


@router.get("", summary="Health check")
async def health():
    # Test DB
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "up"
    except SQLAlchemyError:
        db_status = "down"

    return {
        "status": "ok",
        "service": "iiRules-api",
        "version": "0.0.1",
        "hostname": socket.gethostname(),
        "db": db_status,
    }
