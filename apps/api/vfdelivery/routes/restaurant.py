from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from vfdelivery.core.dependencies import OptionalCurrentUser, RequireRestaurantOwner
from vfdelivery.models.user import UserRole
from vfdelivery.schemas.restaurant import (
    RestaurantCreate,
    RestaurantFetch,
    RestaurantList,
    RestaurantPublic,
)
from vfdelivery.services.restaurant import RestaurantService, get_restaurant_service

router = APIRouter(prefix='/restaurants', tags=['Restaurants'])
restaurant_service = Annotated[RestaurantService, Depends(get_restaurant_service)]
restaurant_fetch_data = Annotated[RestaurantFetch, Query()]


@router.post(
    '',
    status_code=HTTPStatus.CREATED,
    response_model=RestaurantPublic,
)
def create(
    data: RestaurantCreate,
    current_user: RequireRestaurantOwner,
    service: restaurant_service,
):
    """Creates a restaurant based on authenticated User"""
    return service.create(current_user.sub, data)


@router.get(
    '',
    status_code=HTTPStatus.OK,
    response_model=RestaurantList
)
def get_restaurants(
    queries: restaurant_fetch_data,
    service: restaurant_service,
    current_user: OptionalCurrentUser = None
):
    """Get restaurants"""
    owner_id = None
    if current_user and current_user.role == UserRole.RESTAURANT_OWNER:
        owner_id = current_user.sub

    result = service.get_restaurants(queries, owner_id)
    return RestaurantList(restaurants=result)


@router.get(
    '/{restaurant_id}',
    status_code=HTTPStatus.OK,
    response_model=RestaurantPublic
)
def get_restaurant_by_id(
    restaurant_id: UUID,
    service: restaurant_service
):
    """Get a restaurant"""
    return service.get_restaurant_by_id(restaurant_id)
