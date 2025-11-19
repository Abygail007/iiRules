from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


class AgentBase(BaseModel):
    device_id: int = Field(..., ge=1)
    install_key: str = Field(..., max_length=128)

    version: Optional[str] = Field(None, max_length=50)
    os_name: Optional[str] = Field(None, max_length=255)
    os_arch: Optional[str] = Field(None, max_length=50)

    last_seen_at: Optional[datetime] = None
    last_ip: Optional[str] = Field(None, max_length=45)

    status: Literal["never_seen", "online", "offline", "maintenance"] = "never_seen"


class AgentCreate(BaseModel):
    """Ce que l'agent enverra pour s'enregistrer la 1ère fois."""

    device_id: int = Field(..., ge=1)
    install_key: str = Field(..., max_length=128)


class AgentUpdate(BaseModel):
    """Ce qu'on pourra mettre à jour côté serveur (heartbeat, etc.)."""

    version: Optional[str] = Field(None, max_length=50)
    os_name: Optional[str] = Field(None, max_length=255)
    os_arch: Optional[str] = Field(None, max_length=50)

    last_seen_at: Optional[datetime] = None
    last_ip: Optional[str] = Field(None, max_length=45)

    status: Optional[str] = None


class AgentRead(AgentBase):
    """Ce qu'on renvoie quand on lit un agent."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
