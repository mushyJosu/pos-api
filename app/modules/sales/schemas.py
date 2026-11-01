from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.core.types import Money


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=10_000)


class SaleCreate(BaseModel):
    items: list[SaleItemCreate] = Field(min_length=1, max_length=50)


class SaleItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int
    unit_price: Money


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total: Money
    created_at: datetime
    items: list[SaleItemResponse]