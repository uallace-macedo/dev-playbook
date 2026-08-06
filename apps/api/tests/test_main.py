from http import HTTPStatus


def test_root(client):
    response = client.get('/api/v1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'status': 'OK'
    }
