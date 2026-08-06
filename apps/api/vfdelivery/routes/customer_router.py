from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from vfdelivery.schemas.customer_schemas import (
    CustomerCreate,
    CustomerPublic,
)
from vfdelivery.services.customer_service import (
    CustomerService,
    get_customer_service,
)

router = APIRouter(prefix='/customers', tags=['Customers'])
CUSTOMER_SERVICE = Annotated[CustomerService, Depends(get_customer_service)]
LOGIN_FORM_DATA = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post(
    '',
    status_code=HTTPStatus.CREATED,
    response_model=CustomerPublic
)
def create_customer(data: CustomerCreate, service: CUSTOMER_SERVICE):
    """Creates a customer"""
    return service.create_customer(data)


@router.post(
    '/login',
    status_code=HTTPStatus.OK,
    response_model=CustomerPublic
)
def login_customer(data: LOGIN_FORM_DATA, service: CUSTOMER_SERVICE):
    """Login customer"""
    return service.login_customer(data)
