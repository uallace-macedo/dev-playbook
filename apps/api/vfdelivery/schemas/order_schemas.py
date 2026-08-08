from uuid import UUID

from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    quantity: int = Field(ge=1)


class OrderCreate(OrderBase):
    customer_id: UUID
    restaurant_id: UUID
    product_id: UUID
