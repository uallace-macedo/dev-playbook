from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

import pytest
from fastapi import HTTPException
from jwt import decode, encode

from vfdelivery.core.token import (
    ALGORITHM,
    SECRET_KEY,
    generate_access_token,
    get_current_customer,
    get_current_restaurant,
    get_email_from_token,
)
from vfdelivery.models.customer import Customer
from vfdelivery.models.restaurant import Restaurant


def test_generate_access_token():
    data = {'sub': 'test@email.com'}

    result = generate_access_token(data)
    decoded = decode(result, key=SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == 'test@email.com'
    assert 'exp' in decoded


def test_get_email_from_token_success():
    token = generate_access_token({'sub': 'cliente@email.com'})
    email = get_email_from_token(token)

    assert email == 'cliente@email.com'


def test_get_email_from_token_missing_sub():
    token = generate_access_token({'role': 'admin'})

    with pytest.raises(HTTPException) as exc_info:
        get_email_from_token(token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc_info.value.detail == 'Could not validate credentials'


def test_get_email_from_token_invalid():
    invalid_token = 'token.totalmente.invalido'

    with pytest.raises(HTTPException) as exc_info:
        get_email_from_token(invalid_token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


def test_get_email_from_token_expired():
    past_exp = datetime.now(tz=ZoneInfo('UTC')) - timedelta(minutes=10)
    expired_token = encode(
        {'sub': 'expired@email.com', 'exp': past_exp},
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_email_from_token(expired_token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


def test_get_current_customer_success(session, customer):
    token = generate_access_token({'sub': customer.email})
    current_customer = get_current_customer(session, token)

    assert isinstance(current_customer, Customer)
    assert current_customer.id == customer.id
    assert current_customer.email == 'test@email.com'


def test_get_current_customer_not_found(session):
    token = generate_access_token({'sub': 'invalid@email.com'})

    with pytest.raises(HTTPException) as exc_info:
        get_current_customer(session, token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc_info.value.detail == 'Could not validate credentials'


def test_get_current_restaurant_success(session, restaurant):
    token = generate_access_token({'sub': restaurant.email})
    current_restaurant = get_current_restaurant(session, token)

    assert isinstance(current_restaurant, Restaurant)
    assert current_restaurant.id == restaurant.id
    assert current_restaurant.email == 'test@email.com'


def test_get_current_restaurant_not_found(session):
    token = generate_access_token({'sub': 'invalid@email.com'})

    with pytest.raises(HTTPException) as exc_info:
        get_current_restaurant(session, token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc_info.value.detail == 'Could not validate credentials'
