import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.models.product import Product
from vfdelivery.schemas.product import ProductCreate, ProductFetch, ProductUpdate
from vfdelivery.services.product import get_product_service


def test_create_product_success(session, user_restaurant, restaurant_owned):
    service = get_product_service(session)
    product_price = 45.90
    data = ProductCreate(
        name='  Pizza  ',
        price=product_price,
    )

    result = service.create(user_restaurant.id, restaurant_owned.id, data)

    assert isinstance(result, Product)
    assert result.id is not None
    assert result.restaurant_id == restaurant_owned.id
    assert result.name == 'Pizza'
    assert result.price == product_price


def test_create_product_fails_restaurant_not_found(session, user_restaurant):
    service = get_product_service(session)
    product_price = 25.00
    data = ProductCreate(
        name='Hamburguer',
        price=product_price,
    )

    with pytest.raises(HTTPException) as exc_info:
        service.create(user_restaurant.id, uuid.uuid4(), data)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Restaurant not found'


def test_create_product_fails_not_owner(session, restaurant_owned):
    service = get_product_service(session)
    product_price = 25.00
    data = ProductCreate(
        name='Hamburguer',
        price=product_price,
    )
    different_owner_id = uuid.uuid4()

    with pytest.raises(HTTPException) as exc_info:
        service.create(different_owner_id, restaurant_owned.id, data)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Restaurant not found'


def test_create_product_fails_name_already_taken(
    session, user_restaurant, restaurant_owned, product
):
    service = get_product_service(session)
    product_price = 9.00
    data = ProductCreate(
        name=product.name.upper(),
        price=product_price,
    )

    with pytest.raises(HTTPException) as exc_info:
        service.create(user_restaurant.id, restaurant_owned.id, data)

    assert exc_info.value.status_code == HTTPStatus.CONFLICT
    assert exc_info.value.detail == 'Name already taken'


def test_get_products_by_restaurant_id_success(
    session, restaurant_owned, product
):
    service = get_product_service(session)
    fetch_options = ProductFetch(limit=10, offset=0)

    result = service.get_products_by_restaurant_id(
        restaurant_owned.id, fetch_options
    )

    assert len(result) == 1
    assert isinstance(result[0], Product)
    assert result[0].name == product.name


def test_get_products_by_restaurant_id_with_name_filter(
    session, restaurant_owned, product
):
    service = get_product_service(session)
    search_query = product.name[:4].lower()
    fetch_options = ProductFetch(name=search_query, limit=10, offset=0)

    result = service.get_products_by_restaurant_id(
        restaurant_owned.id, fetch_options
    )

    assert len(result) == 1
    assert result[0].name == product.name


def test_get_products_by_restaurant_id_returns_empty(session, restaurant_owned):
    service = get_product_service(session)
    fetch_options = ProductFetch(name='No-Product', limit=10, offset=0)

    result = service.get_products_by_restaurant_id(
        restaurant_owned.id, fetch_options
    )

    assert result == []


def test_update_product_success(session, user_restaurant, restaurant_owned, product):
    service = get_product_service(session)
    updated_name = 'Updated Name'
    updated_price = 30.00
    update_data = ProductUpdate(name=f'  {updated_name}  ', price=updated_price)

    result = service.update(
        user_restaurant.id,
        restaurant_owned.id,
        product.id,
        update_data,
    )

    assert result.id == product.id
    assert result.name == updated_name
    assert result.price == updated_price


def test_update_product_partial_success(
    session, user_restaurant, restaurant_owned, product
):
    service = get_product_service(session)
    new_price = 25.00
    update_data = ProductUpdate(price=new_price)

    result = service.update(
        user_restaurant.id,
        restaurant_owned.id,
        product.id,
        update_data,
    )

    assert result.name == product.name
    assert result.price == new_price


def test_update_product_fails_restaurant_not_found(session, user_restaurant, product):
    service = get_product_service(session)
    data = ProductUpdate(price=30.00)

    with pytest.raises(HTTPException) as exc_info:
        service.update(
            owner_id=user_restaurant.id,
            restaurant_id=uuid.uuid4(),
            product_id=product.id,
            data=data,
        )

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Restaurant not found'


def test_update_product_fails_not_owner(session, user, restaurant_owned, product):
    service = get_product_service(session)
    data = ProductUpdate(price=30.00)

    with pytest.raises(HTTPException) as exc_info:
        service.update(
            owner_id=user.id,
            restaurant_id=restaurant_owned.id,
            product_id=product.id,
            data=data,
        )

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Restaurant not found'


def test_update_product_fails_product_not_found(
    session, user_restaurant, restaurant_owned
):
    service = get_product_service(session)
    new_price = 25.00
    update_data = ProductUpdate(price=new_price)

    with pytest.raises(HTTPException) as exc_info:
        service.update(
            user_restaurant.id,
            restaurant_owned.id,
            uuid.uuid4(),
            update_data,
        )

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Product not found'


def test_update_product_fails_name_already_taken(
    session, user_restaurant, restaurant_owned, product, product_alt
):
    service = get_product_service(session)
    update_data = ProductUpdate(name=product.name.lower())

    with pytest.raises(HTTPException) as exc_info:
        service.update(
            user_restaurant.id,
            restaurant_owned.id,
            product_alt.id,
            update_data,
        )

    assert exc_info.value.status_code == HTTPStatus.CONFLICT
    assert exc_info.value.detail == 'Name already taken'


def test_delete_product_success(
    session, user_restaurant, restaurant_owned, product
):
    service = get_product_service(session)

    service.delete(user_restaurant.id, restaurant_owned.id, product.id)

    db_product = session.get(Product, product.id)
    assert db_product is None


def test_delete_product_fails_restaurant_not_found(
    session, user_restaurant, product
):
    service = get_product_service(session)

    with pytest.raises(HTTPException) as exc_info:
        service.delete(user_restaurant.id, uuid.uuid4(), product.id)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Product not found'


def test_delete_product_fails_not_owner(session, restaurant_owned, product):
    service = get_product_service(session)
    different_owner_id = uuid.uuid4()

    with pytest.raises(HTTPException) as exc_info:
        service.delete(different_owner_id, restaurant_owned.id, product.id)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Product not found'


def test_delete_product_fails_product_not_found(
    session, user_restaurant, restaurant_owned
):
    service = get_product_service(session)

    with pytest.raises(HTTPException) as exc_info:
        service.delete(user_restaurant.id, restaurant_owned.id, uuid.uuid4())

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Product not found'
