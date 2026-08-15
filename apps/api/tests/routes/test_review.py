import uuid
from http import HTTPStatus

from vfdelivery.models.order import OrderStatus

BASE_URL = '/api/v1'


def test_create_review_success(session, client, user, token_customer, order):
    order.status = OrderStatus.DELIVERED
    order.customer_id = user.id
    session.commit()

    rating = 5

    url = f'{BASE_URL}/orders/{order.id}/reviews'
    response = client.post(
        url,
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        json={
            'rating': rating,
            'comment': 'Awesome food!',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['order_id'] == str(order.id)
    assert data['rating'] == rating
    assert data['comment'] == 'Awesome food!'
    assert 'id' in data


def test_create_review_fails_order_not_found(client, token_customer):
    random_order_id = uuid.uuid4()
    url = f'{BASE_URL}/orders/{random_order_id}/reviews'

    response = client.post(
        url,
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        json={
            'rating': 5,
            'comment': 'Great',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Order not found'


def test_create_review_fails_unauthorized(client, order):
    url = f'{BASE_URL}/orders/{order.id}/reviews'

    response = client.post(
        url,
        json={
            'rating': 5,
            'comment': 'Great',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_reviews_by_restaurant_success(
    client, restaurant_owned, review
):
    url = f'{BASE_URL}/restaurants/{restaurant_owned.id}/reviews'

    response = client.get(
        url,
        params={'limit': 10, 'offset': 0},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == str(review.id)


def test_get_reviews_by_restaurant_not_found(client):
    random_restaurant_id = uuid.uuid4()
    url = f'{BASE_URL}/restaurants/{random_restaurant_id}/reviews'

    response = client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Restaurant not found'


def test_get_reviews_by_restaurant_empty(client, restaurant_owned):
    url = f'{BASE_URL}/restaurants/{restaurant_owned.id}/reviews'

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == []
