from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.modules.sales.models import Sale, SaleItem


def create(db: Session, owner_id: int, total: Decimal, lines: list[dict]) -> int:
    sale = Sale(
        owner_id=owner_id,
        total=total,
        items=[SaleItem(**line) for line in lines],
    )
    db.add(sale)
    db.flush()  # asigna el id sin cerrar la transacción
    sale_id = sale.id
    db.commit()  # guarda venta, líneas y stock descontado en un solo paso
    return sale_id


def get_by_id(db: Session, sale_id: int, owner_id: int) -> Sale | None:
    query = (
        select(Sale)
        .options(selectinload(Sale.items))
        .where(Sale.id == sale_id, Sale.owner_id == owner_id)
    )
    return db.scalar(query)


def list_by_owner(db: Session, owner_id: int, limit: int, offset: int) -> list[Sale]:
    query = (
        select(Sale)
        .options(selectinload(Sale.items))
        .where(Sale.owner_id == owner_id)
        .order_by(Sale.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(query))