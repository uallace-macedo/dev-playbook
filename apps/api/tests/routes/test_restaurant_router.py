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

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    assert response.json()['token_type'] == 'Bearer'


def test_get_restaurants(client, restaurant, customer_token):
    response = client.get(
        '/api/v1/restaurants',
        headers={'Authorization': f'Bearer {customer_token.access_token}'}
    )

    restaurant_public = RestaurantPublic.model_validate(
        restaurant
    ).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['restaurants'][0] == restaurant_public
