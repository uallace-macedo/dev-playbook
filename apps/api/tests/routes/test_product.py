from http import HTTPStatus
from uuid import uuid4

from vfdelivery.models.product import Product

BASE_URL = '/api/v1'


def test_create_product_success(client, token_restaurant, restaurant_owned):
    price = 45.90
    response = client.post(
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/products',
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
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/products',
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
        f'{BASE_URL}/restaurants/{random_id}/products',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        json={
            'restaurant_id': str(random_id),
            'name': 'Pizza Margherita',
            'price': 45.90,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Restaurant not found'


def test_get_products_by_restaurant_success(client, restaurant_owned, product):
    response = client.get(
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/products'
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'products' in data
    assert isinstance(data['products'], list)
    assert len(data['products']) == 1
    assert data['products'][0]['name'] == product.name


def test_get_products_by_restaurant_with_query_params(
    client, restaurant_owned, product
):
    response = client.get(
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/products',
        params={
            'limit': 5,
            'offset': 0,
            'name': product.name[:4],
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['products']) == 1
    assert data['products'][0]['name'] == product.name


def test_get_products_by_restaurant_returns_empty_when_not_found(
    client, restaurant_owned
):
    response = client.get(
        f'{BASE_URL}/restaurants/{restaurant_owned.id}/products',
        params={'name': 'unexisting-product'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['products'] == []


def test_update_product_success(client, token_restaurant, restaurant_owned, product):
    new_price = 28.50

    response = client.patch(
        f'{BASE_URL}/products/{product.id}',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        params={'restaurant_id': str(restaurant_owned.id)},
        json={
            'name': 'X-Burguer Updated',
            'price': new_price,
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == str(product.id)
    assert data['name'] == 'X-Burguer Updated'
    assert data['price'] == new_price


def test_update_product_fails_no_valid_role(
    client, token_customer, restaurant_owned, product
):
    response = client.patch(
        f'{BASE_URL}/products/{product.id}',
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        params={'restaurant_id': str(restaurant_owned.id)},
        json={'price': 25.00},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Access denied'


def test_update_product_fails_restaurant_not_found(
    client, token_restaurant, product
):
    random_restaurant_id = uuid4()

    response = client.patch(
        f'{BASE_URL}/products/{product.id}',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        params={'restaurant_id': str(random_restaurant_id)},
        json={'price': 25.00},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Restaurant not found'


def test_update_product_fails_product_not_found(
    client, token_restaurant, restaurant_owned
):
    random_product_id = uuid4()

    response = client.patch(
        f'{BASE_URL}/products/{random_product_id}',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        params={'restaurant_id': str(restaurant_owned.id)},
        json={'price': 25.00},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'


def test_update_product_fails_name_already_taken(
    client, token_restaurant, restaurant_owned, product, product_alt
):
    response = client.patch(
        f'{BASE_URL}/products/{product_alt.id}',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        params={'restaurant_id': str(restaurant_owned.id)},
        json={'name': product.name},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Name already taken'


def test_delete_product_success(
    client, token_restaurant, restaurant_owned, product, session
):
    response = client.delete(
        f'{BASE_URL}/products/{product.id}',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        params={'restaurant_id': str(restaurant_owned.id)},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    db_product = session.get(Product, product.id)
    assert db_product is None


def test_delete_product_fails_no_valid_role(
    client, token_customer, restaurant_owned, product
):
    response = client.delete(
        f'{BASE_URL}/products/{product.id}',
        headers={'Authorization': f'Bearer {token_customer.access_token}'},
        params={'restaurant_id': str(restaurant_owned.id)},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Access denied'


def test_delete_product_fails_restaurant_not_found(
    client, token_restaurant, product
):
    random_restaurant_id = uuid4()

    response = client.delete(
        f'{BASE_URL}/products/{product.id}',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        params={'restaurant_id': str(random_restaurant_id)},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Restaurant not found'


def test_delete_product_fails_product_not_found(
    client, token_restaurant, restaurant_owned
):
    random_product_id = uuid4()

    response = client.delete(
        f'{BASE_URL}/products/{random_product_id}',
        headers={'Authorization': f'Bearer {token_restaurant.access_token}'},
        params={'restaurant_id': str(restaurant_owned.id)},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'
