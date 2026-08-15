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

    result = service.create(user.id, data)

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
    assert result[0]['id'] == restaurant.id
    assert result[0]['name'] == restaurant.name
    assert result[0]['rating_average'] == 0.0
    assert result[0]['total_reviews'] == 0


def test_get_restaurant_by_id_success(session, restaurant):
    service = get_restaurant_service(session)

    result = service.get_restaurant_by_id(restaurant.id)

    assert result['id'] == restaurant.id
    assert result['name'] == restaurant.name
    assert result['description'] == restaurant.description
    assert result['rating_average'] == 0.0
    assert result['total_reviews'] == 0


def test_get_restaurant_by_id_not_found(session):
    service = get_restaurant_service(session)
    random_id = uuid.uuid4()

    with pytest.raises(HTTPException) as e:
        service.get_restaurant_by_id(random_id)

    assert e.value.status_code == HTTPStatus.NOT_FOUND
    assert e.value.detail == 'Restaurant not found'
