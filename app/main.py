from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db


# Importar los modelos para que SQLAlchemy los registre antes de create_all
from app.modules.auth import models as _auth_models  # noqa: F401
from app.modules.categories import models as _categories_models  # noqa: F401
from app.modules.products import models as _products_models  # noqa: F401
from app.modules.sales import models as _sales_models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="POS API",
    description="API de punto de venta: usuarios, categorías, productos y ventas.",
    version="1.0.0",
    lifespan=lifespan, #crea tables
)


@app.get("/health", tags=["Health"])
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}