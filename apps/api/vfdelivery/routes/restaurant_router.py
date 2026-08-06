from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from vfdelivery.core.deps import LOGIN_FORM_DATA
from vfdelivery.schemas.restaurant_schemas import RestaurantCreate, RestaurantPublic
from vfdelivery.services.restaurant_service import (
    RestaurantService,
    get_restaurant_service,
)

router = APIRouter(prefix='/restaurants', tags=['Restaurant'])
RESTAURANT_SERVICE = Annotated[RestaurantService, Depends(get_restaurant_service)]


@router.post(
    '',
    status_code=HTTPStatus.CREATED,
    response_model=RestaurantPublic
)
def create_restaurant(data: RestaurantCreate, service: RESTAURANT_SERVICE):
    """Creates a restaurant"""
    return service.create_restaurant(data)


@router.post(
    '/login',
    status_code=HTTPStatus.OK,
    response_model=RestaurantPublic
)
def login_restaurant(data: LOGIN_FORM_DATA, service: RESTAURANT_SERVICE):
    """Login a restaurant"""
    return service.login_restaurant(data)
