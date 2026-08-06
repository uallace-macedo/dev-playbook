from http import HTTPStatus

import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.restaurant_schemas import RestaurantCreate
from vfdelivery.services.restaurant_service import (
    RestaurantService,
    get_restaurant_service,
)


def test_create_restaurant(session):
    service: RestaurantService = get_restaurant_service(session)

    data = RestaurantCreate(
        name='test',
        email='test@email.com',
        password='secret'
    )

    result = service.create_restaurant(data)
    assert result.id is not None
    assert result.password != data.password


def test_create_restaurant_fails(session, restaurant):
    service: RestaurantService = get_restaurant_service(session)

    data = RestaurantCreate(
        name='test',
        email=restaurant.email,
        password='secret'
    )

    with pytest.raises(HTTPException) as e:
        service.create_restaurant(data)

    assert e.value.status_code == HTTPStatus.CONFLICT
    assert e.value.detail == 'Email already taken'


def test_login_restaurant(session, restaurant):
    service: RestaurantService = get_restaurant_service(session)

    data = OAuth2PasswordRequestForm(
        username=restaurant.email,
        password='secret'
    )

    result = service.login_restaurant(data)

    assert isinstance(result, Restaurant)
    assert result == restaurant


def test_login_customer_fail_no_user(session):
    service: RestaurantService = get_restaurant_service(session)

    data = OAuth2PasswordRequestForm(
        username='test@email.com',
        password='secret'
    )

    with pytest.raises(HTTPException) as e:
        service.login_restaurant(data)

    assert e.value.status_code == HTTPStatus.UNAUTHORIZED
    assert e.value.detail == 'Invalid email or password'


def test_login_customer_fail_wrong_password(session, restaurant):
    service: RestaurantService = get_restaurant_service(session)

    data = OAuth2PasswordRequestForm(
        username=restaurant.email,
        password='wrong-password'
    )

    with pytest.raises(HTTPException) as e:
        service.login_restaurant(data)

    assert e.value.status_code == HTTPStatus.UNAUTHORIZED
    assert e.value.detail == 'Invalid email or password'
