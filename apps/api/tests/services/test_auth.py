from http import HTTPStatus

import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from vfdelivery.models.user import User, UserRole
from vfdelivery.schemas.auth import AuthRegister
from vfdelivery.services.auth import get_auth_service


def test_register(session):
    service = get_auth_service(session)
    data = AuthRegister(
        name='test',
        email='test@email.com',
        role=UserRole.CUSTOMER,
        password='secret'
    )

    result = service.register(data)

    assert isinstance(result, User)
    assert result.id is not None
    assert result.password != data.password


def test_register_fails_email_already_taken(session, user):
    service = get_auth_service(session)
    data: AuthRegister = AuthRegister(
        name='test',
        email=user.email,
        role=UserRole.CUSTOMER,
        password='secret'
    )

    with pytest.raises(HTTPException) as e:
        service.register(data)

    assert e.value.status_code == HTTPStatus.CONFLICT
    assert e.value.detail == 'Email already taken'


def test_login(session, user):
    service = get_auth_service(session)
    data = OAuth2PasswordRequestForm(
        username=user.email,
        password='secret'
    )

    result = service.login(data)

    assert result.access_token is not None
    assert result.token_type == 'Bearer'


def test_login_fails_no_user(session):
    service = get_auth_service(session)
    data = OAuth2PasswordRequestForm(
        username='test@email.com',
        password='secret'
    )

    with pytest.raises(HTTPException) as e:
        service.login(data)

    assert e.value.status_code == HTTPStatus.UNAUTHORIZED
    assert e.value.detail == 'Invalid credentials'


def test_login_fails_wrong_password(session, user):
    service = get_auth_service(session)
    data = OAuth2PasswordRequestForm(
        username=user.email,
        password='wrong-password'
    )

    with pytest.raises(HTTPException) as e:
        service.login(data)

    assert e.value.status_code == HTTPStatus.UNAUTHORIZED
    assert e.value.detail == 'Invalid credentials'
