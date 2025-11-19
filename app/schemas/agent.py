from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AgentCreate(BaseModel):
    """
    Payload pour la création d'un agent.
    Pour l'instant on ne demande que device_id + install_key.
    Le reste sera mis à jour par l'agent lui-même quand il check-in.
    """
    device_id: int
    install_key: str


class AgentUpdate(BaseModel):
    """
    Payload pour mettre à jour les infos d'un agent existant
    (version, OS, dernier check-in, statut, etc.).
    Tous les champs sont optionnels.
    """
    version: Optional[str] = None
    os_name: Optional[str] = None
    os_arch: Optional[str] = None
    last_seen_at: Optional[datetime] = None
    last_ip: Optional[str] = None
    status: Optional[str] = None


class AgentOut(BaseModel):
    """
    Schéma de sortie pour un agent (ce qu'on renvoie via l'API).
    Doit matcher les colonnes du modèle SQLAlchemy + from_attributes=True.
    """
    id: int
    device_id: int
    install_key: str
    version: Optional[str] = None
    os_name: Optional[str] = None
    os_arch: Optional[str] = None
    last_seen_at: Optional[datetime] = None
    last_ip: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
