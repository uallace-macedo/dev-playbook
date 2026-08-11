import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.models.order import Order, OrderStatus
from vfdelivery.schemas.order import OrderCreate, OrderFetch, OrderPatchStatus
from vfdelivery.schemas.order_item import OrderItemCreate
from vfdelivery.services.order import get_order_service


def test_create_order_success(session, user, restaurant_owned, product):
    service = get_order_service(session)
    quantity = 2
    data = OrderCreate(
        items=[OrderItemCreate(product_id=product.id, quantity=quantity)]
    )

    expected_total = 40.00
    result = service.create(user.id, restaurant_owned.id, data)

    assert isinstance(result, Order)
    assert result.id is not None
    assert result.customer_id == user.id
    assert result.restaurant_id == restaurant_owned.id
    assert result.total_price == expected_total
    assert result.status == OrderStatus.CREATED
    assert len(result.items) == 1
    assert result.items[0].product_id == product.id
    assert result.items[0].quantity == quantity


def test_create_order_fails_product_not_found(session, user, restaurant_owned):
    service = get_order_service(session)
    data = OrderCreate(
        items=[OrderItemCreate(product_id=uuid.uuid4(), quantity=1)]
    )

    with pytest.raises(HTTPException) as exc_info:
        service.create(user.id, restaurant_owned.id, data)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'One or more products were not found'


def test_get_orders_by_restaurant_id_success(
    session, user_restaurant, restaurant_owned, order
):
    service = get_order_service(session)
    fetch_options = OrderFetch(limit=10, offset=0)

    result = service.get_orders_by_restaurant_id(
        user_restaurant.id, restaurant_owned.id, fetch_options
    )

    assert len(result) == 1
    assert isinstance(result[0], Order)
    assert result[0].id == order.id


def test_get_orders_by_restaurant_id_with_status_filter(
    session, user_restaurant, restaurant_owned, order
):
    service = get_order_service(session)
    service.update_status(
        restaurant_owned.id,
        order.id,
        OrderPatchStatus(status=OrderStatus.ACCEPTED),
    )

    fetch_options = OrderFetch(status=OrderStatus.ACCEPTED, limit=10, offset=0)
    result = service.get_orders_by_restaurant_id(
        user_restaurant.id, restaurant_owned.id, fetch_options
    )

    assert len(result) == 1
    assert result[0].status == OrderStatus.ACCEPTED


def test_get_orders_by_restaurant_id_fails_restaurant_not_found(
    session, user_restaurant
):
    service = get_order_service(session)
    fetch_options = OrderFetch(limit=10, offset=0)

    with pytest.raises(HTTPException) as exc_info:
        service.get_orders_by_restaurant_id(
            user_restaurant.id, uuid.uuid4(), fetch_options
        )

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Restaurant not found'


def test_update_status_success(session, restaurant_owned, order):
    service = get_order_service(session)
    patch_data = OrderPatchStatus(status=OrderStatus.ACCEPTED)

    updated_order = service.update_status(
        restaurant_id=restaurant_owned.id,
        order_id=order.id,
        data=patch_data,
    )

    assert updated_order.id == order.id
    assert updated_order.status == OrderStatus.ACCEPTED


def test_update_status_fails_order_not_found(session, restaurant_owned):
    service = get_order_service(session)
    patch_data = OrderPatchStatus(status=OrderStatus.DELIVERED)

    with pytest.raises(HTTPException) as exc_info:
        service.update_status(
            restaurant_id=restaurant_owned.id,
            order_id=uuid.uuid4(),
            data=patch_data,
        )

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Order not found'
