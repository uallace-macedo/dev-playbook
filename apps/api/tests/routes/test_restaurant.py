import uuid
from http import HTTPStatus

BASE_URL = '/api/v1/restaurants'


def test_create(client, token_restaurant):
    response = client.post(
        BASE_URL,
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        json={
            'name': 'Test Restaurant',
            'description': 'Test description'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()


def test_create_fails_no_valid_role(client, token_customer):
    response = client.post(
        BASE_URL,
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        json={
            'name': 'Test Restaurant',
            'description': 'Test description'
        }
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Access denied'


def test_get_restaurants_success(client, restaurant):
    response = client.get(BASE_URL)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'restaurants' in data
    assert isinstance(data['restaurants'], list)
    assert len(data['restaurants']) >= 1


def test_get_restaurant_by_id_success(client, restaurant):
    response = client.get(f'{BASE_URL}/{restaurant.id}')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == str(restaurant.id)
    assert data['name'] == restaurant.name
    assert 'rating_average' in data
    assert 'total_reviews' in data


def test_get_restaurant_by_id_not_found(client):
    random_id = uuid.uuid4()
    response = client.get(f'{BASE_URL}/{random_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Restaurant not found'
