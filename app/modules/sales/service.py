from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.products import repository as products_repository
from app.modules.sales import repository
from app.modules.sales.models import Sale
from app.modules.sales.schemas import SaleCreate


def create_sale(db: Session, owner_id: int, data: SaleCreate) -> Sale:
    # 1. Si el mismo producto viene repetido, sumamos sus cantidades
    quantities: dict[int, int] = {}
    for item in data.items:
        quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity

    # 2. Traemos y bloqueamos los productos (solo los del usuario)
    products = products_repository.get_many_for_update(db, owner_id, list(quantities))
    products_by_id = {product.id: product for product in products}

    missing = sorted(set(quantities) - set(products_by_id))
    if missing:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Producto(s) no encontrado(s): {missing}"
        )

    # 3. Primero validamos TODO el stock, sin modificar nada
    for product_id, quantity in quantities.items():
        product = products_by_id[product_id]
        if product.stock < quantity:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Stock insuficiente para '{product.name}' (disponible: {product.stock})",
            )

    # 4. Ahora sí: descontamos stock, armamos las líneas y calculamos el total
    total = Decimal("0")
    lines: list[dict] = []
    for product_id, quantity in quantities.items():
        product = products_by_id[product_id]
        product.stock -= quantity
        total += product.price * quantity
        lines.append(
            {"product_id": product_id, "quantity": quantity, "unit_price": product.price}
        )

    # 5. Un solo commit: o se guarda todo, o no se guarda nada
    try:
        sale_id = repository.create(db, owner_id, total, lines)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "No se pudo registrar la venta, intenta de nuevo"
        )

    return get_sale(db, owner_id, sale_id)


def get_sale(db: Session, owner_id: int, sale_id: int) -> Sale:
    sale = repository.get_by_id(db, sale_id, owner_id)
    if not sale:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Venta no encontrada")
    return sale


def list_sales(db: Session, owner_id: int, limit: int, offset: int) -> list[Sale]:
    return repository.list_by_owner(db, owner_id, limit, offset)
