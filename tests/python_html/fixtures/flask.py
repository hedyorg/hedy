"""Flask-related py.test fixtures for the Python/HTML tests."""
import json
import pytest
from flask.testing import FlaskClient

from app import create_app


class Client:
    """A wrapper for the standard FlaskClient object, but with more convenience methods.

    Things like encoding JSON and checking for success are built-in so they don't have
    to be repeated all the time.
    """

    def __init__(self, client: FlaskClient):
        self.client = client

    def get(self, *args, check=True, **kwargs):
        response = self.client.get(*args, **kwargs)
        if check:
            assert response.status_code == 200
        return response

    def post(self, *args, check=True, **kwargs):
        response = self.client.post(*args, **kwargs)
        if check:
            assert response.status_code == 200
        return response

    def post_json(self, endpoint, data, check=True):
        response = self.client.post('/auth/login', data=json.dumps(data), content_type='application/json')
        if check:
            assert response.status_code == 200
        return response


@pytest.fixture()
def app():
    return create_app()


@pytest.fixture()
def client(app) -> Client:
    return Client(app.test_client())
