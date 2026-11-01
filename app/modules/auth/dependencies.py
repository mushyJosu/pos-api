from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.auth import repository
from app.modules.auth.models import User

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    user_id = decode_access_token(credentials.credentials)
    user = repository.get_by_id(db, user_id) if user_id else None
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user