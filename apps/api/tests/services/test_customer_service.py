from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.schemas.customer_schemas import CustomerCreate
from vfdelivery.services.customer_service import CustomerService, get_customer_service
from vfdelivery.models.customer import Customer

from fastapi.security import OAuth2PasswordRequestForm


def test_create_customer(session):
    service: CustomerService = get_customer_service(session)

    customer = CustomerCreate(
        name='test',
        email='test@email.com',
        password='secret'
    )

    result = service.create_customer(customer)

    assert result.id is not None
    assert result.password != customer.password


def test_create_customer_fail(session, customer):
    service: CustomerService = get_customer_service(session)

    customer = CustomerCreate(
        name='test',
        email=customer.email,
        password='secret'
    )

    with pytest.raises(HTTPException) as e:
        service.create_customer(customer)

    assert e.value.status_code == HTTPStatus.CONFLICT
    assert e.value.detail == 'Email already registered'


def test_login_customer(session, customer):
    service: CustomerService = get_customer_service(session)

    data = OAuth2PasswordRequestForm(
        username=customer.email,
        password='secret'
    )

    result = service.login_customer(data)

    assert isinstance(result, Customer)
    assert result == customer


def test_login_customer_fail_no_user(session):
    service: CustomerService = get_customer_service(session)
    
    data = OAuth2PasswordRequestForm(
        username='test@email.com',
        password='secret'
    )

    with pytest.raises(HTTPException) as e:
        service.login_customer(data)

    assert e.value.status_code == HTTPStatus.UNAUTHORIZED
    assert e.value.detail == 'Invalid email or password'


def test_login_customer_fail_wrong_password(session, customer):
    service: CustomerService = get_customer_service(session)
    
    data = OAuth2PasswordRequestForm(
        username=customer.email,
        password='wrong-password'
    )

    with pytest.raises(HTTPException) as e:
        service.login_customer(data)

    assert e.value.status_code == HTTPStatus.UNAUTHORIZED
    assert e.value.detail == 'Invalid email or password'
