import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.models.product import Product
from vfdelivery.schemas.product_schemas import ProductCreate
from vfdelivery.services.product_service import get_product_service


def test_create_product(session, restaurant):
    service = get_product_service(session)
    product_data = ProductCreate(
        name='X-Burguer',
        price=14.00
    )

    result = service.create_product(
        restaurant_id=restaurant.id,
        product_data=product_data
    )

    assert isinstance(result, Product)
    assert result.restaurant_id == restaurant.id
    assert result.created_at is not None


def test_create_product_fail_no_restaurant(session):
    service = get_product_service(session)
    product_data = ProductCreate(
        name='X-Burguer',
        price=14.00
    )

    with pytest.raises(HTTPException) as e:
        service.create_product(
            restaurant_id=uuid.uuid4(),
            product_data=product_data
        )

    assert e.value.status_code == HTTPStatus.NOT_FOUND
    assert e.value.detail == 'Restaurant not found'


def test_create_product_fail_product_already_exists(session, product):
    service = get_product_service(session)
    product_data = ProductCreate(
        name=product.name,
        price=product.price
    )

    with pytest.raises(HTTPException) as e:
        service.create_product(
            restaurant_id=product.restaurant_id,
            product_data=product_data
        )

    assert e.value.status_code == HTTPStatus.CONFLICT
    assert e.value.detail == 'A product with this name already exists'


def test_get_products_by_restaurant(session, product):
    service = get_product_service(session)

    result = service.get_products_by_restaurant(product.restaurant_id)

    assert len(result) == 1
    assert result == [product]
    assert result[0].restaurant_id == product.restaurant_id


def test_get_products_by_restaurant_fail(session):
    service = get_product_service(session)

    with pytest.raises(HTTPException) as e:
        service.get_products_by_restaurant(uuid.uuid4())

    assert e.value.status_code == HTTPStatus.NOT_FOUND
    assert e.value.detail == 'Restaurant not found'


def test_get_products_by_restaurant_with_name(session, product):
    service = get_product_service(session)

    result = service.get_products_by_restaurant(
        product.restaurant_id,
        name='burguer'
    )

    assert len(result) == 1
    assert result == [product]
    assert result[0].restaurant_id == product.restaurant_id


def test_get_products_by_restaurant_with_name_empty(session, product):
    service = get_product_service(session)

    result = service.get_products_by_restaurant(
        product.restaurant_id,
        name='z'
    )

    assert len(result) == 0
    assert result == []
