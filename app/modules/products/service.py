from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.categories import repository as categories_repository
from app.modules.products import repository
from app.modules.products.models import Product
from app.modules.products.schemas import ProductCreate


def _check_category(db: Session, owner_id: int, category_id: int | None) -> None:
    if category_id is not None and not categories_repository.get_by_id(
        db, category_id, owner_id
    ):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoría no encontrada")


def list_products(
    db: Session, owner_id: int, search: str | None, limit: int, offset: int
) -> list[Product]:
    return repository.list_by_owner(db, owner_id, search, limit, offset)


def get_product(db: Session, owner_id: int, product_id: int) -> Product:
    product = repository.get_by_id(db, product_id, owner_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Producto no encontrado")
    return product


def create_product(db: Session, owner_id: int, data: ProductCreate) -> Product:
    _check_category(db, owner_id, data.category_id)
    return repository.create(db, owner_id, data.model_dump())


def update_product(
    db: Session, owner_id: int, product_id: int, data: ProductCreate
) -> Product:
    product = get_product(db, owner_id, product_id)
    _check_category(db, owner_id, data.category_id)
    return repository.update(db, product, data.model_dump())


def delete_product(db: Session, owner_id: int, product_id: int) -> None:
    product = get_product(db, owner_id, product_id)
    try:
        repository.delete(db, product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "El producto tiene ventas registradas y no puede eliminarse",
        )