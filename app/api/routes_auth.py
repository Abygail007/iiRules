from datetime import datetime, timedelta
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import AuthLoginIn, AuthLoginOut
from app.schemas.user import UserOut


def hash_password(password: str) -> str:
    """
    Même algo que dans routes_users.py.
    Plus tard on passera sur bcrypt/argon2 dans un module commun.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=AuthLoginOut)
def login(payload: AuthLoginIn, db: Session = Depends(get_db)) -> AuthLoginOut:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )

    if user.hashed_password != hash_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )

    # Token très simpliste pour l’instant (juste pour tester le flux)
    # Plus tard: vrai JWT / session signée, etc.
    issued_at = datetime.utcnow()
    token = f"dev-{user.id}-{int(issued_at.timestamp())}"
    expires_at = issued_at + timedelta(hours=8)

    user_out = UserOut.model_validate(user, from_attributes=True)


    return AuthLoginOut(
        access_token=token,
        token_type="bearer",
        user=user_out,
        issued_at=issued_at,
        expires_at=expires_at,
    )
