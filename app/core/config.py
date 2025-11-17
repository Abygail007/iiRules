import os


class Settings:
    def __init__(self) -> None:
        self.APP_NAME = "iiRules API"
        self.APP_VERSION = "0.0.1"
        # URL par défaut pour la DB PostgreSQL locale (Docker)
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://iirules:iirules-dev@localhost:5432/iirules",
        )


settings = Settings()
