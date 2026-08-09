from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from vfdelivery.core.dependencies import LoginFormData
from vfdelivery.schemas.auth import AuthRegister, AuthToken
from vfdelivery.schemas.user import UserPublic
from vfdelivery.services.auth import AuthService, get_auth_service

router = APIRouter(prefix='/auth', tags=['Auth'])
auth_service = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    '/register',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic
)
def register(
    data: AuthRegister,
    service: auth_service
):
    """Register a user"""
    return service.register(data)


@router.post(
    '/login',
    status_code=HTTPStatus.OK,
    response_model=AuthToken
)
def login(
    data: LoginFormData,
    service: auth_service
):
    """Login a user using `OAuth2PasswordRequestForm`"""
    return service.login(data)
