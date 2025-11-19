from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


class DeviceBase(BaseModel):
    organisation_id: int = Field(..., ge=1)
    folder_id: Optional[int] = Field(None, ge=1)

    name: str = Field(..., max_length=255)
    hostname: Optional[str] = Field(None, max_length=255)

    # IMPORTANT : on utilise "type" (comme en base)
    type: Literal[
        "server",
        "workstation",
        "laptop",
        "network",
        "printer",
        "mobile",
        "other",
    ] = "server"

    os_name: Optional[str] = Field(None, max_length=255)
    os_version: Optional[str] = Field(None, max_length=255)

    serial_number: Optional[str] = Field(None, max_length=255)
    tags: Optional[str] = Field(None, max_length=255)


class DeviceCreate(DeviceBase):
    """Payload pour la création de device."""
    pass


class DeviceUpdate(BaseModel):
    """Payload pour la mise à jour (tous les champs optionnels)."""

    folder_id: Optional[int] = Field(None, ge=1)

    name: Optional[str] = Field(None, max_length=255)
    hostname: Optional[str] = Field(None, max_length=255)

    type: Optional[
        Literal[
            "server",
            "workstation",
            "laptop",
            "network",
            "printer",
            "mobile",
            "other",
        ]
    ] = None

    os_name: Optional[str] = Field(None, max_length=255)
    os_version: Optional[str] = Field(None, max_length=255)

    serial_number: Optional[str] = Field(None, max_length=255)
    tags: Optional[str] = Field(None, max_length=255)


class DeviceRead(DeviceBase):
    """Ce qu'on renvoie au client."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # équivalent de orm_mode=True en Pydantic v2
