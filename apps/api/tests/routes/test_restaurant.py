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


def test_get_restaurants_with_query_params(client, restaurant):
    response = client.get(
        BASE_URL,
        params={
            'limit': 5,
            'offset': 0,
            'name': restaurant.name,
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['restaurants']) == 1
    assert data['restaurants'][0]['name'] == restaurant.name


def test_get_restaurants_returns_empty_when_not_found(client):
    response = client.get(
        BASE_URL,
        params={'name': 'no-restaurant'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['restaurants'] == []

