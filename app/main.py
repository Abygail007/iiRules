from fastapi import FastAPI
from app.api.routes_health import router as health_router

app = FastAPI(
    title="iiRules API",
    version="0.0.1",
    description="Backend API pour le RMM iiRules",
)


@app.get("/")
async def root():
    return {"message": "iiRules backend is running"}


# Route de santé
app.include_router(health_router, prefix="/health", tags=["health"])
