from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.organisation import Organisation
from app.schemas.organisation import (
    OrganisationCreate,
    OrganisationRead,
    OrganisationUpdate,
)

router = APIRouter(
    prefix="/organisations",
    tags=["organisations"],
)


@router.get("/", response_model=List[OrganisationRead])
def list_organisations(db: Session = Depends(get_db)) -> List[OrganisationRead]:
    organisations = db.query(Organisation).order_by(Organisation.name).all()
    return organisations


@router.get("/{organisation_id}", response_model=OrganisationRead)
def get_organisation(
    organisation_id: int,
    db: Session = Depends(get_db),
) -> OrganisationRead:
    org = db.get(Organisation, organisation_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation not found",
        )
    return org


@router.post(
    "/",
    response_model=OrganisationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_organisation(
    payload: OrganisationCreate,
    db: Session = Depends(get_db),
) -> OrganisationRead:
    org = Organisation(
        name=payload.name,
        code_client=payload.code_client,
        contact_name=payload.contact_name,
        contact_email=payload.contact_email,
        contact_phone=payload.contact_phone,
        notes=payload.notes,
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@router.put("/{organisation_id}", response_model=OrganisationRead)
def update_organisation(
    organisation_id: int,
    payload: OrganisationUpdate,
    db: Session = Depends(get_db),
) -> OrganisationRead:
    org = db.get(Organisation, organisation_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation not found",
        )

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(org, field, value)

    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@router.delete(
    "/{organisation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_organisation(
    organisation_id: int,
    db: Session = Depends(get_db),
) -> None:
    org = db.get(Organisation, organisation_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation not found",
        )

    db.delete(org)
    db.commit()
    # 204 → pas de contenu à renvoyer
    return None
