from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response

from vfdelivery.core.dependencies import RequireRestaurantOwner
from vfdelivery.schemas.product import (
    ProductCreate,
    ProductFetch,
    ProductList,
    ProductPublic,
)
from vfdelivery.services.product import (
    ProductService,
    ProductUpdate,
    get_product_service,
)

router = APIRouter(
    tags=['Products'],
)

product_service = Annotated[ProductService, Depends(get_product_service)]
product_fetch_data = Annotated[ProductFetch, Query()]


@router.post(
    '/restaurants/{restaurant_id}/products',
    status_code=HTTPStatus.CREATED,
    response_model=ProductPublic,
)
def create(
    restaurant_id: UUID,
    data: ProductCreate,
    current_user: RequireRestaurantOwner,
    service: product_service,
):
    """Creates a product for a specific restaurant"""
    return service.create(current_user.sub, restaurant_id, data)


@router.get(
    '/restaurants/{restaurant_id}/products',
    status_code=HTTPStatus.OK,
    response_model=ProductList,
)
def get_products_by_restaurant(
    restaurant_id: UUID,
    queries: product_fetch_data,
    service: product_service,
):
    """Get products by restaurant ID"""
    result = service.get_products_by_restaurant_id(restaurant_id, queries)
    return ProductList(products=result)


@router.patch(
    '/restaurants/{restaurant_id}/products/{product_id}',
    status_code=HTTPStatus.OK,
    response_model=ProductPublic,
)
def update_product(
    product_id: UUID,
    restaurant_id: UUID,
    data: ProductUpdate,
    current_user: RequireRestaurantOwner,
    service: product_service,
):
    """Updates a product of a specific restaurant"""
    return service.update(
        owner_id=current_user.sub,
        restaurant_id=restaurant_id,
        product_id=product_id,
        data=data,
    )


@router.delete(
    '/restaurants/{restaurant_id}/products/{product_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_product(
    product_id: UUID,
    restaurant_id: UUID,
    current_user: RequireRestaurantOwner,
    service: product_service,
):
    """Deletes a product of a specific restaurant"""
    service.delete(
        owner_id=current_user.sub,
        restaurant_id=restaurant_id,
        product_id=product_id,
    )

    return Response(status_code=HTTPStatus.NO_CONTENT)
