from __future__ import annotations

from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_organisations import router as organisations_router
from app.api.routes_folders import router as folders_router


app = FastAPI(
    title="iiRules API",
    version="0.0.1",
)


@app.get("/")
def read_root() -> dict:
    return {"message": "iiRules backend is running"}


# Routes health
app.include_router(health_router)

# Routes organisations
app.include_router(organisations_router)

# Routes folders
app.include_router(folders_router)
