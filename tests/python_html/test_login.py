# https://werkzeug.palletsprojects.com/en/stable/test/
from .fixtures.given import Given
from .fixtures.flask import Client
import json
import pytest


def test_login(client: Client, given: Given):
    """Check that logging in works."""
    # GIVEN
    given.a_student_account('user1', 'pass1')

    # WHEN
    response = client.post_json('/auth/login', {
        'username': 'user1',
        'password': 'pass1',
    })

    # THEN - it succeeds


STUDENT_PROTECTED_ENDPOINTS = ['/programs']


@pytest.mark.parametrize('endpoint', STUDENT_PROTECTED_ENDPOINTS)
def test_student_pages_protected(client: Client, endpoint):
    """Check that these endpoints return 302 if not logged in."""
    response = client.get(endpoint, check=False)
    assert response.status_code == 302


@pytest.mark.parametrize('endpoint', STUDENT_PROTECTED_ENDPOINTS)
def test_student_pages_available(client: Client, given: Given, endpoint):
    """Check that these endpoints work if we are logged in as students."""
    # GIVEN
    given.logged_in_as_student()

    # WHEN
    response = client.get(endpoint)

    # THEN - it succeeds
