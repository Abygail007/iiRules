from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserOut


class AuthLoginIn(BaseModel):
    email: str
    password: str


class AuthLoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
    issued_at: datetime
    expires_at: Optional[datetime] = None  # plus tard on fera un vrai expiry
