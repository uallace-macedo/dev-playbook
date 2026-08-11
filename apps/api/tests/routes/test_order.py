import uuid
from http import HTTPStatus

from vfdelivery.models.order import OrderStatus

BASE_URL = '/api/v1'


def test_create_order_success(
    client, token_customer, restaurant_owned, product
):
    headers = {'Authorization': f'Bearer {token_customer.access_token}'}
    payload = {
        'items': [
            {'product_id': str(product.id), 'quantity': 2}
        ]
    }

    expected_total = 40.00
    response = client.post(
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/orders',
        headers=headers,
        json=payload,
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert 'id' in data
    assert data['total_price'] == expected_total

    assert data['restaurant']['id'] == str(restaurant_owned.id)
    assert 'customer' in data
    assert len(data['items']) == 1
    assert data['items'][0]['product_id'] == str(product.id)
    assert 'product_name' in data['items'][0]
    assert 'subtotal' in data['items'][0]


def test_create_order_fails_unauthorized(client, restaurant_owned):
    payload = {
        'items': [
            {'product_id': str(uuid.uuid4()), 'quantity': 1}
        ]
    }

    response = client.post(
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/orders',
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_orders_by_restaurant_success(
    client, token_restaurant, restaurant_owned, order
):
    headers = {'Authorization': f'Bearer {token_restaurant.access_token}'}

    response = client.get(
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/orders',
        headers=headers,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'orders' in data
    assert len(data['orders']) == 1
    assert data['orders'][0]['id'] == str(order.id)


def test_get_orders_fails_not_owner(client, token_customer, restaurant_owned):
    headers = {'Authorization': f'Bearer {token_customer.access_token}'}

    response = client.get(
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/orders',
        headers=headers,
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_order_status_success(
    client, token_restaurant, order
):
    headers = {'Authorization': f'Bearer {token_restaurant.access_token}'}
    payload = {'status': OrderStatus.ACCEPTED.value}

    response = client.patch(
        f'{BASE_URL}/orders/{order.id}/status',
        headers=headers,
        json=payload,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == str(order.id)
    assert data['status'] == OrderStatus.ACCEPTED.value


def test_update_order_status_fails_not_found(
    client, token_restaurant
):
    headers = {'Authorization': f'Bearer {token_restaurant.access_token}'}
    fake_id = uuid.uuid4()

    response = client.patch(
        f'{BASE_URL}/orders/{fake_id}/status',
        headers=headers,
        json={'status': OrderStatus.ACCEPTED.value},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Order not found'
