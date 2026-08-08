import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.models.order import Order, OrderStatus
from vfdelivery.schemas.order_schemas import OrderCreate
from vfdelivery.services.order_service import get_order_service


def test_create_order(session, customer, restaurant, product):
    service = get_order_service(session)
    order_data = OrderCreate(
        quantity=2,
        customer_id=customer.id,
        restaurant_id=restaurant.id,
        product_id=product.id
    )

    result = service.create_order(order_data)
    assert isinstance(result, Order)
    assert result.id is not None
    assert result.status == OrderStatus.CREATED
    assert result.total_value == product.price * order_data.quantity
    assert result.created_at is not None


def test_create_order_fail_no_restaurant(session):
    service = get_order_service(session)
    order_data = OrderCreate(
        quantity=2,
        customer_id=uuid.uuid4(),
        restaurant_id=uuid.uuid4(),
        product_id=uuid.uuid4()
    )

    with pytest.raises(HTTPException) as e:
        service.create_order(order_data)

    assert e.value.status_code == HTTPStatus.NOT_FOUND
    assert e.value.detail == 'Restaurant not found'


def test_create_order_fail_no_product(session, restaurant):
    service = get_order_service(session)
    order_data = OrderCreate(
        quantity=2,
        customer_id=uuid.uuid4(),
        restaurant_id=restaurant.id,
        product_id=uuid.uuid4()
    )

    with pytest.raises(HTTPException) as e:
        service.create_order(order_data)

    assert e.value.status_code == HTTPStatus.NOT_FOUND
    assert e.value.detail == "The restaurant doesn't have this product"
