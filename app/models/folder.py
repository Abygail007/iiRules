from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import String, SmallInteger, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Folder(Base):
    __tablename__ = "folders"

    __table_args__ = (
        UniqueConstraint(
            "organisation_id",
            "parent_id",
            "name",
            name="uq_folder_name_per_parent",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # 1 organisation = 1 client
    organisation_id: Mapped[int] = mapped_column(nullable=False)

    # parent_id nullable pour la racine
    parent_id: Mapped[Optional[int]] = mapped_column(nullable=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Profondeur 0 à 3 (on contrôlera côté code)
    depth: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    # Optionnel : type de dossier (site, category, group, etc.)
    type: Mapped[Optional[str]] = mapped_column(String(50))

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
