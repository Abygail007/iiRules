from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    organisation_id: int
    folder_id: Optional[int] = None

    name: str
    hostname: Optional[str] = None
    type: str  # server, workstation, vm, nas, printer, switch, firewall, etc.

    os_name: Optional[str] = None
    os_version: Optional[str] = None
    serial_number: Optional[str] = None

    # Tags simples stockés en string pour l’instant ("prod,tse", "infra,hyperv", etc.)
    tags: Optional[str] = None


class DeviceCreate(DeviceBase):
    """Payload pour créer un device."""
    pass


class DeviceUpdate(BaseModel):
    """Payload pour mise à jour partielle d’un device."""
    organisation_id: Optional[int] = None
    folder_id: Optional[int] = None

    name: Optional[str] = None
    hostname: Optional[str] = None
    type: Optional[str] = None

    os_name: Optional[str] = None
    os_version: Optional[str] = None
    serial_number: Optional[str] = None

    tags: Optional[str] = None


class DeviceOut(DeviceBase):
    """Ce qu’on renvoie à l’API (lecture)."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
