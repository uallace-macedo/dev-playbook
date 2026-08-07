from http import HTTPStatus


def test_create_customer(client):
    response = client.post(
        '/api/v1/customers',
        json={
            'name': 'test',
            'email': 'test@email.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()


def test_login_customer(client, customer):
    response = client.post(
        '/api/v1/customers/login',
        data={
            'username': customer.email,
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    assert response.json()['token_type'] == 'Bearer'
