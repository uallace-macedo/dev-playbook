from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    quantity: int = Field(ge=1)


class OrderItemCreate(OrderItemBase):
    product_id: UUID


class OrderItemPublic(BaseModel):
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)
