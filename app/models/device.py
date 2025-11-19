from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String,
    Boolean,
    Text,
    DateTime,
    func,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Client / organisation propriétaire de l'équipement
    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisations.id"),
        nullable=False,
    )

    # Dossier (site / catégorie / sous-groupe), optionnel
    folder_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("folders.id"),
        nullable=True,
    )

    # Infos de base
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hostname: Mapped[Optional[str]] = mapped_column(String(255))
    fqdn: Mapped[Optional[str]] = mapped_column(String(255))


    # Type logique : server, workstation, vm, nas, printer, switch, firewall, etc.
    type: Mapped[str] = mapped_column(String(50), nullable=False)

    manufacturer: Mapped[Optional[str]] = mapped_column(String(255))
    model: Mapped[Optional[str]] = mapped_column(String(255))
    serial_number: Mapped[Optional[str]] = mapped_column(String(255))

    # IP / MAC principales (stockées en string pour rester simple)
    primary_ip: Mapped[Optional[str]] = mapped_column(String(45))
    primary_mac: Mapped[Optional[str]] = mapped_column(String(50))

    os_name: Mapped[Optional[str]] = mapped_column(String(255))
    os_version: Mapped[Optional[str]] = mapped_column(String(255))
    is_virtual: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # Tags libres, simple string "prod,tse,hyperv" pour l'instant
    tags: Mapped[Optional[str]] = mapped_column(String(255))

    notes: Mapped[Optional[str]] = mapped_column(Text())


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# Index utiles pour les filtres
Index("idx_devices_org", Device.organisation_id)
Index("idx_devices_folder", Device.folder_id)
