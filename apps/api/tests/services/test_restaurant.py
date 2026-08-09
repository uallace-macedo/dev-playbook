import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.restaurant import RestaurantCreate, RestaurantFetch
from vfdelivery.services.restaurant import get_restaurant_service


def test_create(session, user):
    service = get_restaurant_service(session)
    data = RestaurantCreate(
        name='IFood',
        description='Description'
    )

    result = service.create(user.email, data)

    assert isinstance(result, Restaurant)
    assert result.id is not None
    assert result.owner_id == user.id
    assert result.created_at is not None


def test_create_fails_user_not_found(session):
    service = get_restaurant_service(session)
    data = RestaurantCreate(
        name='IFood',
        description='Description'
    )

    with pytest.raises(HTTPException) as e:
        service.create(uuid.uuid4(), data)

    assert e.value.status_code == HTTPStatus.NOT_FOUND
    assert e.value.detail == 'User not found'


def test_get_restaurants(session, restaurant):
    service = get_restaurant_service(session)
    fetch_data = RestaurantFetch()

    result = service.get_restaurants(fetch_data)

    assert len(result) == 1
    assert result[0] == restaurant


def test_get_restaurants_by_name(session):
    service = get_restaurant_service(session)
    fetch_data = RestaurantFetch(name='z')

    result = service.get_restaurants(fetch_data)

    assert len(result) == 0
