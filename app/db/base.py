from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base SQLAlchemy de iiRules."""
    pass


# Import des modèles pour qu'ils soient enregistrés dans Base.metadata
# (même si on ne les utilise pas directement ici)
from app import models  # noqa: E402,F401
