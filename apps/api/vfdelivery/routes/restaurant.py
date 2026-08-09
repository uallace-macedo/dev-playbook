from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from vfdelivery.core.dependencies import RequireRestaurantOwner
from vfdelivery.schemas.restaurant import RestaurantCreate, RestaurantPublic, RestaurantList, RestaurantFetch
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
    service: restaurant_service
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
    service: restaurant_service
):
    """Get restaurants"""
    result = service.get_restaurants(queries)
    return RestaurantList(restaurants=result)
