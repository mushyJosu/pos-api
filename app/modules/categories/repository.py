from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.categories.models import Category


def list_by_owner(db: Session, owner_id: int) -> list[Category]:
    query = select(Category).where(Category.owner_id == owner_id).order_by(Category.name)
    return list(db.scalars(query))


def get_by_id(db: Session, category_id: int, owner_id: int) -> Category | None:
    return db.scalar(
        select(Category).where(Category.id == category_id, Category.owner_id == owner_id)
    )


def get_by_name(db: Session, owner_id: int, name: str) -> Category | None:
    return db.scalar(
        select(Category).where(Category.owner_id == owner_id, Category.name == name)
    )


def create(db: Session, owner_id: int, name: str) -> Category:
    category = Category(owner_id=owner_id, name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category