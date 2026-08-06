from http import HTTPStatus

from vfdelivery.schemas.customer_schemas import CustomerPublic


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

    public_response = CustomerPublic.model_validate(response.json()).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert 'id' in public_response
    assert public_response['name'] == customer.name
    assert public_response['email'] == customer.email
