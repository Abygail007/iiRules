from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_health import router as health_router
from app.api.routes_organisations import router as organisations_router
from app.api.routes_folders import router as folders_router
from app.api.routes_devices import router as devices_router
from app.api.routes_agents import router as agents_router
from app.api.routes_users import router as users_router
from app.api.routes_auth import router as auth_router




app = FastAPI(
    title="iiRules API",
    version="0.0.1",
)

# CORS très permissif pour le dev (on ajustera plus tard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(health_router)
app.include_router(organisations_router)
app.include_router(folders_router)
app.include_router(devices_router)
app.include_router(agents_router)
app.include_router(users_router)
app.include_router(auth_router)
