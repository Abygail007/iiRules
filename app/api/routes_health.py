from fastapi import APIRouter
import socket

router = APIRouter()


@router.get("", summary="Health check")
async def health():
    return {
        "status": "ok",
        "service": "iiRules-api",
        "version": "0.0.1",
        "hostname": socket.gethostname(),
    }
