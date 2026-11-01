from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.modules.auth.router import router as auth_router
from fastapi.responses import RedirectResponse
from app.core.database import Base, engine, get_db


# Importar los modelos para que SQLAlchemy los registre antes de create_all
from app.modules.auth import models as _auth_models  # noqa: F401
from app.modules.categories import models as _categories_models  # noqa: F401
from app.modules.products import models as _products_models  # noqa: F401
from app.modules.sales import models as _sales_models  # noqa: F401
from app.modules.categories.router import router as categories_router
from app.modules.products.router import router as products_router
from app.modules.sales.router import router as sales_router
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

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(sales_router)

@app.get("/health", tags=["Health"])
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs") #Redirecciona a la documentación de la API