from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FolderBase(BaseModel):
    organisation_id: int
    name: str
    parent_id: Optional[int] = None
    type: Optional[str] = None


class FolderCreate(FolderBase):
    """
    Schéma utilisé en entrée pour créer un folder.
    → Pas de depth ici : il est calculé côté serveur.
    """
    pass


class FolderRead(FolderBase):
    """
    Schéma utilisé en sortie (API → client).
    """
    id: int
    depth: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # Pydantic v2
        from_attributes = True
