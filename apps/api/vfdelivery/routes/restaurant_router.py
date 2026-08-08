from http import HTTPStatus
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select

from vfdelivery.core.deps import LOGIN_FORM_DATA, PAGINATION, SESSION
from vfdelivery.core.token import get_current_customer, get_current_restaurant
from vfdelivery.models.customer import Customer
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.product_schemas import ProductCreate, ProductList, ProductPublic
from vfdelivery.schemas.public_schemas import AuthToken
from vfdelivery.schemas.restaurant_schemas import (
    RestaurantCreate,
    RestaurantList,
    RestaurantPublic,
)
from vfdelivery.services.product_service import ProductService, get_product_service
from vfdelivery.services.restaurant_service import (
    RestaurantService,
    get_restaurant_service,
)

router = APIRouter(prefix='/restaurants', tags=['Restaurant'])
RESTAURANT_SERVICE = Annotated[RestaurantService, Depends(get_restaurant_service)]
PRODUCT_SERVICE = Annotated[ProductService, Depends(get_product_service)]
CURRENT_RESTAURANT = Annotated[Restaurant, Depends(get_current_restaurant)]
CURRENT_CUSTOMER = Annotated[Customer, Depends(get_current_customer)]


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
    response_model=AuthToken
)
def login_restaurant(data: LOGIN_FORM_DATA, service: RESTAURANT_SERVICE):
    """Login a restaurant"""
    return service.login_restaurant(data)


@router.get(
    '',
    status_code=HTTPStatus.OK,
    response_model=RestaurantList
)
def get_restaurants(
    session: SESSION,
    params: PAGINATION
):
    params.limit = max(1, params.limit)
    params.offset = max(params.offset, 0)

    restaurants = session.scalars(
        select(Restaurant).limit(params.limit).offset(params.offset)
    )

    return RestaurantList(restaurants=restaurants)


@router.post(
    '/products',
    status_code=HTTPStatus.CREATED,
    response_model=ProductPublic
)
def create_product(
    current_restaurant: CURRENT_RESTAURANT,
    product_service: PRODUCT_SERVICE,
    product_data: ProductCreate
):
    return product_service.create_product(
        restaurant_id=current_restaurant.id,
        product_data=product_data
    )


@router.get(
    '/{restaurant_id}/products',
    status_code=HTTPStatus.OK,
    response_model=ProductList
)
def get_products(
    current_customer: CURRENT_CUSTOMER,
    product_service: PRODUCT_SERVICE,
    restaurant_id: UUID,
    *,
    params: PAGINATION,
    name: Optional[str] = None
):
    params.limit = max(1, params.limit)
    params.offset = max(params.offset, 0)

    result = product_service.get_products_by_restaurant(
        restaurant_id,
        limit=params.limit,
        offset=params.offset,
        name=name
    )

    return {'products': result}
