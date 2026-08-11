import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.models.order import OrderStatus
from vfdelivery.models.review import Review
from vfdelivery.schemas.review import ReviewCreate, ReviewFetch
from vfdelivery.services.review import get_review_service


def test_create_review_success(session, order):
    order.status = OrderStatus.DELIVERED
    session.commit()

    service = get_review_service(session)
    data = ReviewCreate(
        rating=5,
        comment='Awesome food!',
    )

    result = service.create(order.customer_id, order.id, data)

    assert isinstance(result, Review)
    assert result.id is not None
    assert result.order_id == order.id
    assert result.customer_id == order.customer_id


def test_create_review_fails_order_not_found(session, user):
    service = get_review_service(session)
    data = ReviewCreate(
        rating=5,
        comment='Pretty good',
    )
    random_order_id = uuid.uuid4()

    with pytest.raises(HTTPException) as e:
        service.create(user.id, random_order_id, data)

    assert e.value.status_code == HTTPStatus.NOT_FOUND
    assert e.value.detail == 'Order not found'


def test_create_review_fails_order_not_delivered(session, user, order):
    service = get_review_service(session)
    data = ReviewCreate(
        rating=4,
        comment='Fast delivery',
    )

    with pytest.raises(HTTPException) as e:
        service.create(user.id, order.id, data)

    assert e.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert e.value.detail == 'Order is not delivered yet'


def test_create_review_fails_already_reviewed(session, user, order):
    order.status = OrderStatus.DELIVERED
    session.commit()

    service = get_review_service(session)
    data = ReviewCreate(
        rating=5,
        comment='First review',
    )

    service.create(user.id, order.id, data)

    with pytest.raises(HTTPException) as e:
        service.create(user.id, order.id, data)

    assert e.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert e.value.detail == 'Order already reviewed'


def test_get_reviews_by_restaurant_id_success(session, restaurant_owned, review):
    service = get_review_service(session)
    options = ReviewFetch(limit=10, offset=0)

    result = service.get_reviews_by_restaurant_id(restaurant_owned.id, options)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == review.id
    assert result[0].restaurant_id == restaurant_owned.id


def test_get_reviews_by_restaurant_id_fails_restaurant_not_found(session):
    service = get_review_service(session)
    options = ReviewFetch(limit=10, offset=0)

    with pytest.raises(HTTPException) as e:
        service.get_reviews_by_restaurant_id(uuid.uuid4(), options)

    assert e.value.status_code == HTTPStatus.NOT_FOUND
    assert e.value.detail == 'Restaurant not found'


def test_get_reviews_by_restaurant_id_empty(session, restaurant):
    service = get_review_service(session)
    options = ReviewFetch(limit=10, offset=0)

    result = service.get_reviews_by_restaurant_id(restaurant.id, options)

    assert isinstance(result, list)
    assert len(result) == 0
