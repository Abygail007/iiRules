from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String,
    DateTime,
    func,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Agent(Base):
    __tablename__ = "agents"

    __table_args__ = (
        # 1 seul agent par device
        UniqueConstraint("device_id", name="uq_agents_device_id"),
        # Clé d'installation unique
        UniqueConstraint("install_key", name="uq_agents_install_key"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id"),
        nullable=False,
    )

    # Clé d’enregistrement / installation de l’agent
    install_key: Mapped[str] = mapped_column(String(128), nullable=False)

    version: Mapped[Optional[str]] = mapped_column(String(50))
    os_name: Mapped[Optional[str]] = mapped_column(String(255))
    os_arch: Mapped[Optional[str]] = mapped_column(String(50))

    last_seen_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # IP récemment vue par l'agent (string pour simplifier)
    last_ip: Mapped[Optional[str]] = mapped_column(String(45))

    # never_seen / online / offline / maintenance / etc.
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="never_seen",
        server_default="never_seen",
    )

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
