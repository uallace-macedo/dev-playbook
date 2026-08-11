import uuid
from http import HTTPStatus

from vfdelivery.models.order import OrderStatus


def test_create_review_success(session, client, user, token_customer, order):
    order.status = OrderStatus.DELIVERED
    order.customer_id = user.id
    session.commit()

    rating = 5

    url = f'/api/v1/orders/{order.id}/review'
    response = client.post(
        url,
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        json={
            'order_id': str(order.id),
            'rating': 5,
            'comment': 'Awesome food!'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['order_id'] == str(order.id)
    assert data['rating'] == rating
    assert data['comment'] == 'Awesome food!'
    assert 'id' in data


def test_create_review_fails_order_not_found(client, token_customer):
    random_order_id = uuid.uuid4()
    url = f'/api/v1/orders/{random_order_id}/review'

    response = client.post(
        url,
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        json={
            'order_id': str(random_order_id),
            'rating': 5,
            'comment': 'Great'
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Order not found'


def test_create_review_fails_unauthorized(client, order):
    url = f'/api/v1/orders/{order.id}/review'

    response = client.post(
        url,
        json={
            'order_id': str(order.id),
            'rating': 5,
            'comment': 'Great'
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_reviews_by_restaurant_success(
    client,
    token_customer,
    restaurant_owned,
    review
):
    url = f'/api/v1/restaurants/{restaurant_owned.id}/reviews'
    response = client.get(
        url,
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        params={'limit': 10, 'offset': 0}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == str(review.id)


def test_get_reviews_by_restaurant_not_found(client, token_customer):
    random_restaurant_id = uuid.uuid4()
    url = f'/api/v1/restaurants/{random_restaurant_id}/reviews'

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {token_customer.access_token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Restaurant not found'


def test_get_reviews_by_restaurant_empty(
    client,
    token_customer,
    restaurant_owned
):
    url = f'/api/v1/restaurants/{restaurant_owned.id}/reviews'

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {token_customer.access_token}'}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == []
