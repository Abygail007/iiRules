from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class OrganisationBase(BaseModel):
    name: str
    code_client: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    notes: Optional[str] = None


class OrganisationCreate(OrganisationBase):
    """Données nécessaires pour créer une organisation."""
    pass


class OrganisationUpdate(BaseModel):
    """Données pour mettre à jour une organisation (tous les champs optionnels)."""

    name: Optional[str] = None
    code_client: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    notes: Optional[str] = None


class OrganisationRead(OrganisationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # permet de partir d'un modèle SQLAlchemy
