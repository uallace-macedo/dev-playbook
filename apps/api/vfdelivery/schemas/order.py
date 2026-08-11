from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from vfdelivery.models.order import OrderStatus
from vfdelivery.schemas.order_item import OrderItemCreate, OrderItemPublic


class OrderBase(BaseModel):
    status: OrderStatus
    total_price: float = Field(ge=0, default=0)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderPatchStatus(BaseModel):
    status: OrderStatus


class OrderFetch(BaseModel):
    limit: int = Field(ge=0, default=10)
    offset: int = Field(ge=0, default=0)
    status: Optional[OrderStatus] = Field(default=None)


class OrderPublic(OrderBase):
    id: UUID
    customer_id: UUID
    restaurant_id: UUID
    total_price: float
    status: OrderStatus
    created_at: datetime
    items: list[OrderItemPublic]

    model_config = ConfigDict(from_attributes=True)


class OrderList(BaseModel):
    orders: list[OrderPublic]
