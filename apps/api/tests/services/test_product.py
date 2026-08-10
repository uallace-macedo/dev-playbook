import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.models.product import Product
from vfdelivery.schemas.product import ProductCreate, ProductFetch
from vfdelivery.services.product import get_product_service


def test_create_product_success(session, user_restaurant, restaurant_owned):
    service = get_product_service(session)
    price = 45.90
    data = ProductCreate(
        name='  Pizza  ',
        price=price,
    )

    result = service.create(user_restaurant.id, restaurant_owned.id, data)

    assert isinstance(result, Product)
    assert result.id is not None
    assert result.restaurant_id == restaurant_owned.id
    assert result.name == 'Pizza'
    assert result.price == price


def test_create_product_fails_restaurant_not_found(session, user_restaurant):
    service = get_product_service(session)
    data = ProductCreate(
        name='Hamburguer',
        price=25.00,
    )

    with pytest.raises(HTTPException) as exc_info:
        service.create(user_restaurant.id, uuid.uuid4(), data)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Restaurant not found'


def test_create_product_fails_not_owner(session, restaurant_owned):
    service = get_product_service(session)
    data = ProductCreate(
        name='Hamburguer',
        price=25.00,
    )

    different_owner_id = uuid.uuid4()

    with pytest.raises(HTTPException) as exc_info:
        service.create(different_owner_id, restaurant_owned.id, data)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Restaurant not found'


def test_create_product_fails_name_already_taken(
    session, user_restaurant, restaurant_owned
):
    service = get_product_service(session)

    data1 = ProductCreate(
        name='orange juice',
        price=8.00,
    )
    service.create(user_restaurant.id, restaurant_owned.id, data1)

    data2 = ProductCreate(
        name='ORANGE JUICE',
        price=9.00,
    )

    with pytest.raises(HTTPException) as exc_info:
        service.create(user_restaurant.id, restaurant_owned.id, data2)

    assert exc_info.value.status_code == HTTPStatus.CONFLICT
    assert exc_info.value.detail == 'Name already taken'


def test_get_products_by_restaurant_id_success(
    session, user_restaurant, restaurant_owned
):
    service = get_product_service(session)

    data = ProductCreate(
        name='Coca-Cola',
        price=6.00,
    )
    service.create(user_restaurant.id, restaurant_owned.id, data)

    fetch_options = ProductFetch(limit=10, offset=0)
    result = service.get_products_by_restaurant_id(
        restaurant_owned.id, fetch_options
    )

    assert len(result) == 1
    assert isinstance(result[0], Product)
    assert result[0].name == 'Coca-Cola'


def test_get_products_by_restaurant_id_with_name_filter(
    session, user_restaurant, restaurant_owned
):
    service = get_product_service(session)

    service.create(
        user_restaurant.id,
        restaurant_owned.id,
        ProductCreate(
            name='Pizza X',
            price=30.0,
        ),
    )
    service.create(
        user_restaurant.id,
        restaurant_owned.id,
        ProductCreate(
            name='Hamburguer Y',
            price=20.0,
        ),
    )

    fetch_options = ProductFetch(name='pizza', limit=10, offset=0)
    result = service.get_products_by_restaurant_id(
        restaurant_owned.id, fetch_options
    )

    assert len(result) == 1
    assert result[0].name == 'Pizza X'


def test_get_products_by_restaurant_id_returns_empty(session, restaurant_owned):
    service = get_product_service(session)

    fetch_options = ProductFetch(name='No-Product', limit=10, offset=0)
    result = service.get_products_by_restaurant_id(
        restaurant_owned.id, fetch_options
    )

    assert result == []
