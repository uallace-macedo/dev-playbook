from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from vfdelivery.core.dependencies import CurrentUser
from vfdelivery.schemas.review import (
    ReviewCreate,
    ReviewFetch,
    ReviewPublic,
)
from vfdelivery.services.review import ReviewService, get_review_service

router = APIRouter(
    tags=['Reviews'],
)

review_service = Annotated[ReviewService, Depends(get_review_service)]
review_fetch_data = Annotated[ReviewFetch, Query()]


@router.post(
    '/orders/{order_id}/reviews',  # Atualizado para o plural /reviews
    status_code=HTTPStatus.CREATED,
    response_model=ReviewPublic,
)
def create_review(
    order_id: UUID,
    data: ReviewCreate,
    current_user: CurrentUser,
    service: review_service,
):
    """Creates a review for a delivered order (Customer Only)"""
    return service.create(
        customer_id=current_user.sub,
        order_id=order_id,
        data=data,
    )


@router.get(
    '/restaurants/{restaurant_id}/reviews',
    status_code=HTTPStatus.OK,
    response_model=list[ReviewPublic],
)
def get_reviews_by_restaurant(
    restaurant_id: UUID,
    queries: review_fetch_data,
    service: review_service,  # Removido 'current_user' para permitir acesso público
):
    """Get reviews by restaurant ID (Public Endpoint)"""
    return service.get_reviews_by_restaurant_id(restaurant_id, queries)
