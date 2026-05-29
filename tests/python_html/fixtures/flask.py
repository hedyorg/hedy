"""Flask-related py.test fixtures for the Python/HTML tests."""
import json
from flask import Flask, template_rendered
import pytest
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
        self._test_headers = {'X-Testing': '1'}

    def _merge_headers(self, kwargs):
        existing = dict(kwargs.pop('headers', {}))
        existing.update(self._test_headers)
        kwargs['headers'] = existing
        return kwargs

    def get(self, *args, check=True, **kwargs):
        response = self.client.get(*args, **self._merge_headers(kwargs))
        check_status_code(check, response)
        return response

    def post(self, *args, check=True, **kwargs):
        response = self.client.post(*args, **self._merge_headers(kwargs))
        check_status_code(check, response)
        return response

    def post_json(self, endpoint, data, check=True):
        response = self.client.post(
            endpoint,
            data=json.dumps(data),
            content_type='application/json',
            headers=self._test_headers,
        )
        check_status_code(check, response)
        return response

    def delete(self, *args, check=True, **kwargs):
        response = self.client.delete(*args, **self._merge_headers(kwargs))
        check_status_code(check, response)
        return response


@pytest.fixture()
def app():
    # for_testing=True makes Database use in-memory storage, avoiding persistent
    # dev_database.json state leaking across tests.
    return create_app(for_testing=True)


@pytest.fixture()
def client(app: Flask) -> Client:
    return Client(app.test_client())


def check_status_code(check, response):
    if check:
        assert 200 <= response.status_code < 300


@pytest.fixture
def template_variables(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append(context)

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
