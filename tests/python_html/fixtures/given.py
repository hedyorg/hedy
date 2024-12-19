"""Database preparation."""
import json
import uuid

from .flask import Client
from website.database import Database
from website import auth
import pytest


class Given:
    """A helper that wraps an in-memory database."""

    def __init__(self, client: Client, db: Database):
        self.client = client
        self.db = db
        self.student_ctr = 1

    def a_student_account(self, username=None, password=None, teacher_username=None, language='en'):
        """Create a student account."""
        if username is None:
            username = f'student{self.student_ctr}'
            self.student_ctr += 1
        password = password or str(uuid.uuid4())
        student = {
            'username': username,
            'password': password,
            'language': language,
            'keyword_language': language,
        }
        auth.store_new_student_account(self.db, student, teacher_username)
        return {'username': username, 'password': password}

    def logged_in_as_student(self, username=None):
        """Make sure that we are logged in."""
        user = self.a_student_account(username)

        response = self.client.post('/auth/login', data=json.dumps({
            'username': user['username'],
            'password': user['password'],
        }), content_type='application/json')
        assert response.status_code == 200


@pytest.fixture()
def given(client, app) -> Given:
    db = app.config['hedy_globals']['DATABASE']
    return Given(client, db)
