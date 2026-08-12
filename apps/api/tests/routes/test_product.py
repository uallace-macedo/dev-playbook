from http import HTTPStatus
from uuid import uuid4

BASE_URL = '/api/v1/restaurants'


def test_create_product_success(client, token_restaurant, restaurant_owned):
    price = 45.90
    response = client.post(
        f'{BASE_URL}/{restaurant_owned.id}/products',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        json={
            'restaurant_id': str(restaurant_owned.id),
            'name': 'Pizza Margherita',
            'price': price,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert 'id' in data
    assert data['name'] == 'Pizza Margherita'
    assert data['price'] == price


def test_create_product_fails_no_valid_role(client, token_customer, restaurant_owned):
    response = client.post(
        f'{BASE_URL}/{restaurant_owned.id}/products',
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        json={
            'restaurant_id': str(restaurant_owned.id),
            'name': 'Pizza Margherita',
            'price': 45.90,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Access denied'


def test_create_product_fails_restaurant_not_found(client, token_restaurant):
    random_id = uuid4()
    response = client.post(
        f'{BASE_URL}/{random_id}/products',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        json={
            'restaurant_id': str(random_id),
            'name': 'Pizza Margherita',
            'price': 45.90,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Restaurant not found'


def test_get_products_by_restaurant_success(
    client, token_restaurant, restaurant_owned
):
    client.post(
        f'{BASE_URL}/{restaurant_owned.id}/products',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        json={
            'restaurant_id': str(restaurant_owned.id),
            'name': 'Coca-Cola',
            'price': 6.00,
        },
    )

    response = client.get(f'{BASE_URL}/{restaurant_owned.id}/products')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'products' in data
    assert isinstance(data['products'], list)
    assert len(data['products']) == 1
    assert data['products'][0]['name'] == 'Coca-Cola'


def test_get_products_by_restaurant_with_query_params(
    client, token_restaurant, restaurant_owned
):
    client.post(
        f'{BASE_URL}/{restaurant_owned.id}/products',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        json={
            'restaurant_id': str(restaurant_owned.id),
            'name': 'Suco de Laranja',
            'price': 8.00,
        },
    )

    response = client.get(
        f'{BASE_URL}/{restaurant_owned.id}/products',
        params={
            'limit': 5,
            'offset': 0,
            'name': 'Laranja',
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['products']) == 1
    assert data['products'][0]['name'] == 'Suco de Laranja'


def test_get_products_by_restaurant_returns_empty_when_not_found(
    client, restaurant_owned
):
    response = client.get(
        f'{BASE_URL}/{restaurant_owned.id}/products',
        params={'name': 'no-product'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['products'] == []
