from http import HTTPStatus


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
