from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_organisations import router as organisations_router
from app.api.routes_folders import router as folders_router
from app.api.routes_devices import router as devices_router
from app.api.routes_agents import router as agents_router


app = FastAPI(
    title="iiRules API",
    version="0.0.1",
)


@app.get("/")
def read_root():
    return {"message": "iiRules backend is running"}


# /health
app.include_router(health_router)

# /organisations
app.include_router(organisations_router)

# /folders
app.include_router(folders_router)

# /devices
app.include_router(devices_router)

# /agents
app.include_router(agents_router)
