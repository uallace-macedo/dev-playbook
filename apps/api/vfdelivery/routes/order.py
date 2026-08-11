from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from vfdelivery.core.dependencies import CurrentUser, RequireRestaurantOwner
from vfdelivery.schemas.order import (
    OrderCreate,
    OrderFetch,
    OrderList,
    OrderPatchStatus,
    OrderPublic,
)
from vfdelivery.services.order import OrderService, get_order_service

router = APIRouter(
    tags=['Orders'],
)

order_service = Annotated[OrderService, Depends(get_order_service)]
order_fetch_data = Annotated[OrderFetch, Query()]


@router.post(
    '/restaurants/{restaurant_id}/orders',
    status_code=HTTPStatus.CREATED,
    response_model=OrderPublic,
)
def create(
    restaurant_id: UUID,
    data: OrderCreate,
    current_user: CurrentUser,
    service: order_service,
):
    """Creates an order for a specific restaurant (Requires Customer Authentication)"""
    return service.create(
        customer_id=current_user.sub,
        restaurant_id=restaurant_id,
        data=data,
    )


@router.get(
    '/restaurants/{restaurant_id}/orders',
    status_code=HTTPStatus.OK,
    response_model=OrderList,
)
def get_orders_by_restaurant(
    restaurant_id: UUID,
    queries: order_fetch_data,
    current_user: RequireRestaurantOwner,
    service: order_service,
):
    """Get all orders from a restaurant (Requires Restaurant Owner Authentication)"""
    orders = service.get_orders_by_restaurant_id(
        owner_id=current_user.sub,
        restaurant_id=restaurant_id,
        options=queries,
    )

    return OrderList(orders=orders)


@router.patch(
    '/restaurants/{restaurant_id}/orders/{order_id}/status',
    status_code=HTTPStatus.OK,
    response_model=OrderPublic,
)
def update_status(
    restaurant_id: UUID,
    order_id: UUID,
    data: OrderPatchStatus,
    _: RequireRestaurantOwner,
    service: order_service,
):
    """Update order status (Requires Restaurant Owner Authentication)"""
    return service.update_status(
        restaurant_id=restaurant_id,
        order_id=order_id,
        data=data,
    )
