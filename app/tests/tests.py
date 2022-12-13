import pytest


def test_index(client):
    response = client.get('/i/index/')
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_url(client):
    form_data = {'time_to_delete': '1', 'long_link': 'https://test.com'}
    response = client.post('/i/index/', data=form_data)
    assert response.status_code == 200
