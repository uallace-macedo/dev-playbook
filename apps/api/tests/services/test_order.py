import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.models.order import Order, OrderStatus
from vfdelivery.schemas.order import (
    OrderBatchDelete,
    OrderCreate,
    OrderFetch,
    OrderPatchStatus,
)
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

    assert result.customer.id == user.id
    assert result.restaurant.id == restaurant_owned.id
    assert result.items[0].product.id == product.id
    assert result.items[0].product_name == product.name


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
        user_restaurant.id,
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


def test_update_status_success(session, user_restaurant, restaurant_owned, order):
    service = get_order_service(session)
    patch_data = OrderPatchStatus(status=OrderStatus.ACCEPTED)

    updated_order = service.update_status(
        owner_id=user_restaurant.id,
        order_id=order.id,
        data=patch_data,
    )

    assert updated_order.id == order.id
    assert updated_order.status == OrderStatus.ACCEPTED


def test_update_status_fails_order_not_found(session, user_restaurant):
    service = get_order_service(session)
    patch_data = OrderPatchStatus(status=OrderStatus.DELIVERED)

    with pytest.raises(HTTPException) as exc_info:
        service.update_status(
            owner_id=user_restaurant.id,
            order_id=uuid.uuid4(),
            data=patch_data,
        )

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Order not found'


def test_batch_delete_orders_success(session, order):
    service = get_order_service(session)
    order.status = OrderStatus.REJECTED
    session.commit()

    data = OrderBatchDelete(orders_id=[order.id])

    service.batch_delete(data)
    deleted_order = session.get(Order, order.id)
    assert deleted_order is None


def test_batch_delete_orders_empty_or_non_existent_ids(session, order):
    service = get_order_service(session)
    data = OrderBatchDelete(orders_id=[uuid.uuid4()])
    service.batch_delete(data)

    existing_order = session.get(Order, order.id)
    assert existing_order is not None


def test_batch_delete_orders_ignores_active_orders(session, order):
    service = get_order_service(session)
    data = OrderBatchDelete(orders_id=[order.id])

    service.batch_delete(data)
    saved_order = session.get(Order, order.id)
    assert saved_order is not None


def test_cancel_order_success(session, user, order):
    service = get_order_service(session)
    service.cancel(customer_id=user.id, order_id=order.id)
    session.refresh(order)
    assert order.status == OrderStatus.CANCELED


def test_cancel_order_fails_not_found(session, user):
    service = get_order_service(session)
    fake_order_id = uuid.uuid4()

    with pytest.raises(HTTPException) as exc_info:
        service.cancel(customer_id=user.id, order_id=fake_order_id)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Order not found'


def test_cancel_order_fails_conflict_invalid_status(session, user, order):
    service = get_order_service(session)

    order.status = OrderStatus.ACCEPTED
    session.commit()

    with pytest.raises(HTTPException) as exc_info:
        service.cancel(customer_id=user.id, order_id=order.id)

    assert exc_info.value.status_code == HTTPStatus.CONFLICT
    assert exc_info.value.detail == 'Cannot cancel a accepted order'
