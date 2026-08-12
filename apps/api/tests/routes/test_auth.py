from http import HTTPStatus

BASE_URL = '/api/v1/auth'


def test_register(client):
    response = client.post(
        f'{BASE_URL}/register',
        json={
            'name': 'test',
            'email': 'test@email.com',
            'role': 'customer',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()
    assert 'customer' in response.json()['role']
    assert 'password' not in response.json()


def test_login(client, user):
    response = client.post(
        f'{BASE_URL}/login',
        data={
            'username': user.email,
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'Bearer'
