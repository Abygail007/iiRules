from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.folder import Folder
from app.schemas.folder import FolderCreate, FolderRead

router = APIRouter(
    prefix="/folders",
    tags=["folders"],
)


@router.post("/", response_model=FolderRead)
def create_folder(folder: FolderCreate, db: Session = Depends(get_db)) -> Folder:
    """
    Crée un folder.
    - depth est calculé automatiquement :
      * 0 si pas de parent
      * parent.depth + 1 si parent
    """

    # Vérification basique : on pourrait plus tard vérifier que l'orga existe
    if folder.parent_id is not None:
        parent = (
            db.query(Folder)
            .filter(
                Folder.id == folder.parent_id,
                Folder.organisation_id == folder.organisation_id,
            )
            .first()
        )
        if parent is None:
            raise HTTPException(
                status_code=400,
                detail="Parent folder introuvable pour cette organisation",
            )
        depth = parent.depth + 1
    else:
        depth = 0

    db_folder = Folder(
        organisation_id=folder.organisation_id,
        parent_id=folder.parent_id,
        name=folder.name,
        depth=depth,
        type=folder.type,
    )

    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder


@router.get("/", response_model=List[FolderRead])
def list_folders(
    organisation_id: Optional[int] = Query(
        None,
        description="Filtrer par organisation (optionnel)",
    ),
    db: Session = Depends(get_db),
) -> List[Folder]:
    """
    Liste des folders.
    - Si organisation_id est fourni → on filtre par orga
    - Sinon → tous les folders
    """
    query = db.query(Folder)
    if organisation_id is not None:
        query = query.filter(Folder.organisation_id == organisation_id)
    return query.order_by(Folder.organisation_id, Folder.depth, Folder.id).all()
