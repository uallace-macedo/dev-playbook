from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from vfdelivery.models.order import OrderStatus
from vfdelivery.schemas.order_item import OrderItemCreate


class OrderCustomerPublic(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class OrderRestaurantPublic(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


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


class OrderItemPublic(BaseModel):
    id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)


class OrderPublic(BaseModel):
    id: UUID
    status: OrderStatus
    total_price: float
    created_at: datetime
    updated_at: datetime
    reviewed: bool

    customer: OrderCustomerPublic
    restaurant: OrderRestaurantPublic
    items: list[OrderItemPublic]

    model_config = ConfigDict(from_attributes=True)


class OrderList(BaseModel):
    orders: list[OrderPublic]


class OrderBatchDelete(BaseModel):
    orders_id: list[UUID]
