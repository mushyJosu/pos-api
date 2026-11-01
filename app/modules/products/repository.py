from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.products.models import Product


def list_by_owner(
    db: Session, owner_id: int, search: str | None, limit: int, offset: int
) -> list[Product]:
    query = select(Product).where(Product.owner_id == owner_id)
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    query = query.order_by(Product.id).limit(limit).offset(offset)
    return list(db.scalars(query))


def get_by_id(db: Session, product_id: int, owner_id: int) -> Product | None:
    return db.scalar(
        select(Product).where(Product.id == product_id, Product.owner_id == owner_id)
    )


def create(db: Session, owner_id: int, values: dict) -> Product:
    product = Product(owner_id=owner_id, **values)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update(db: Session, product: Product, values: dict) -> Product:
    for field, value in values.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()