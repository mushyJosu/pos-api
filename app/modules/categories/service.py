from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.categories import repository
from app.modules.categories.models import Category
from app.modules.categories.schemas import CategoryCreate


def list_categories(db: Session, owner_id: int) -> list[Category]:
    return repository.list_by_owner(db, owner_id)


def create_category(db: Session, owner_id: int, data: CategoryCreate) -> Category:
    if repository.get_by_name(db, owner_id, data.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya tienes una categoría con ese nombre")
    try:
        return repository.create(db, owner_id, data.name)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya tienes una categoría con ese nombre")