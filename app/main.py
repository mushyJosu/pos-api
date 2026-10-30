from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

app = FastAPI(
    title="POS API",
    description="API de punto de venta: usuarios, categorías, productos y ventas.",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}