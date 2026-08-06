from http import HTTPStatus

from vfdelivery.schemas.restaurant_schemas import RestaurantPublic


def test_create_restaurant(client):
    response = client.post(
        '/api/v1/restaurants',
        json={
            'name': 'test',
            'email': 'test@email.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()


def test_login_restaurant(client, restaurant):
    response = client.post(
        '/api/v1/restaurants/login',
        data={
            'username': restaurant.email,
            'password': 'secret'
        }
    )

    public_response = RestaurantPublic.model_validate(response.json()).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert 'id' in public_response
    assert public_response['name'] == restaurant.name
    assert public_response['email'] == restaurant.email
