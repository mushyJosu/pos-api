"""Crea un usuario de demostración con categorías y productos de ejemplo.

Uso (desde la raíz del proyecto, con el entorno virtual activo):
    DEMO_PASSWORD=una_clave_segura python -m scripts.seed_demo
"""
import os
import sys
from decimal import Decimal

import app.main  # noqa: F401  (importarlo registra todos los modelos)
from app.core.database import SessionLocal
from app.modules.auth import repository as auth_repository
from app.modules.auth import service as auth_service
from app.modules.auth.schemas import RegisterRequest
from app.modules.categories import service as categories_service
from app.modules.categories.schemas import CategoryCreate
from app.modules.products import service as products_service
from app.modules.products.schemas import ProductCreate

DEMO_EMAIL = "demo@posapi.dev"

PRODUCTS = {
    "Bebidas": [
        ("Café americano", "35.00", 50),
        ("Té helado", "30.00", 40),
        ("Agua natural", "15.00", 100),
    ],
    "Alimentos": [
        ("Sándwich de jamón", "55.00", 25),
        ("Torta de pollo", "65.00", 20),
    ],
    "Postres": [
        ("Pastel de chocolate", "45.00", 15),
        ("Galleta artesanal", "20.00", 60),
    ],
}


def main() -> None:
    password = os.getenv("DEMO_PASSWORD")
    if not password or len(password) < 8:
        sys.exit("Define DEMO_PASSWORD con al menos 8 caracteres.")

    with SessionLocal() as db:
        if auth_repository.get_by_email(db, DEMO_EMAIL):
            sys.exit("El usuario demo ya existe, no se creó nada.")

        user = auth_service.register(
            db,
            RegisterRequest(email=DEMO_EMAIL, full_name="Usuario Demo", password=password),
        )

        for category_name, items in PRODUCTS.items():
            category = categories_service.create_category(
                db, user.id, CategoryCreate(name=category_name)
            )
            for name, price, stock in items:
                products_service.create_product(
                    db,
                    user.id,
                    ProductCreate(
                        name=name,
                        price=Decimal(price),
                        stock=stock,
                        category_id=category.id,
                    ),
                )

    print(f"Listo. Usuario demo: {DEMO_EMAIL}")


if __name__ == "__main__":
    main()