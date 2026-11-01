from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.modules.auth import repository
from app.modules.auth.models import User
from app.modules.auth.schemas import LoginRequest, RegisterRequest

# Hash de relleno: se usa cuando el correo no existe, para que el login tarde
# lo mismo y no revele qué correos están registrados.
_DUMMY_HASH = hash_password("relleno-no-usar")


def register(db: Session, data: RegisterRequest) -> User:
    email = data.email.lower()
    if repository.get_by_email(db, email):
        raise HTTPException(status.HTTP_409_CONFLICT, "El correo ya está registrado")
    try:
        return repository.create(db, email, data.full_name, hash_password(data.password))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "El correo ya está registrado")


def login(db: Session, data: LoginRequest) -> str:
    user = repository.get_by_email(db, data.email.lower())
    hashed = user.password_hash if user else _DUMMY_HASH
    password_ok = verify_password(data.password, hashed)

    if not user or not password_ok:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token(user.id)