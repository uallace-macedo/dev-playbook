import uuid
from http import HTTPStatus

from vfdelivery.schemas.product_schemas import ProductPublic
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


def test_get_restaurants(client, restaurant):
    response = client.get(
        '/api/v1/restaurants'
    )

    restaurant_public = RestaurantPublic.model_validate(
        restaurant
    ).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['restaurants'][0] == restaurant_public


def test_create_product(client, restaurant_token):
    response = client.post(
        '/api/v1/restaurants/products',
        headers={'Authorization': f'Bearer {restaurant_token.access_token}'},
        json={
            'name': 'X-Burguer',
            'description': 'A big x-burguer',
            'price': 14.00
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()


def test_create_product_no_description(client, restaurant_token):
    response = client.post(
        '/api/v1/restaurants/products',
        headers={'Authorization': f'Bearer {restaurant_token.access_token}'},
        json={
            'name': 'X-Burguer',
            'price': 14.00
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()


def test_get_products(client, customer_token, product):
    response = client.get(
        f'/api/v1/restaurants/{product.restaurant_id}/products',
        headers={'Authorization': f'Bearer {customer_token.access_token}'}
    )

    product_public = ProductPublic.model_validate(product).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == 1
    assert response.json()['products'][0] == product_public
    assert response.json() == {'products': [product_public]}


def test_get_products_with_params(client, customer_token, product):
    response = client.get(
        f'/api/v1/restaurants/{product.restaurant_id}/products',
        headers={'Authorization': f'Bearer {customer_token.access_token}'},
        params={
            'limit': 10,
            'offset': 0,
        }
    )

    product_public = ProductPublic.model_validate(product).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == 1
    assert response.json()['products'][0] == product_public
    assert response.json() == {'products': [product_public]}

def test_get_products_by_name(client, customer_token, product):
    response = client.get(
        f'/api/v1/restaurants/{product.restaurant_id}/products',
        headers={'Authorization': f'Bearer {customer_token.access_token}'},
        params={
            'name': 'burguer',
            'limit': -2,
            'offset': -8
        }
    )

    product_public = ProductPublic.model_validate(product).model_dump(mode='json')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == 1
    assert response.json()['products'][0] == product_public
    assert response.json() == {'products': [product_public]}


def test_get_products_by_name_empty(client, customer_token, product):
    response = client.get(
        f'/api/v1/restaurants/{product.restaurant_id}/products',
        headers={'Authorization': f'Bearer {customer_token.access_token}'},
        params={
            'name': 'z'
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == 0
    assert response.json() == {'products': []}


def test_get_products_fails_no_restaurant(client, customer_token,):
    response = client.get(
        f'/api/v1/restaurants/{uuid.uuid4()}/products',
        headers={'Authorization': f'Bearer {customer_token.access_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Restaurant not found'
