"""Database preparation."""
import json
import uuid

from .flask import Client
from website.database import Database
from website import auth
import pytest
import utils


def unique_id():
    return str(uuid.uuid4())


def now_javascript():
    """Return the current time in milliseconds, or a faked time if configured."""
    return utils.timems()


class Given:
    """A helper that wraps an in-memory database."""

    def __init__(self, client: Client, db: Database):
        self.client = client
        self.db = db
        self.student_ctr = 1
        self.teacher_ctr = 1

    def a_student_account(self, username=None, password=None, teacher_username=None, language='en'):
        """Create a student account."""
        if username is None:
            username = f'student{self.student_ctr}'
            self.student_ctr += 1
        password = password or unique_id()
        student = {
            'username': username,
            'password': password,
            'language': language,
            'keyword_language': language,
        }
        auth.store_new_student_account(self.db, student, teacher_username)
        return {'username': username, 'password': password}

    def a_teacher_account(self, username=None, password=None, teacher_username=None, language='en'):
        """Create a student account."""
        if username is None:
            username = f'student{self.teacher_ctr}'
            self.teacher_ctr += 1
        password = password or unique_id()
        username, hashed, _ = auth.prepare_user_db(username, password)
        teacher = {
            'username': username,
            'password': hashed,
            'language': language,
            'keyword_language': language,
            'is_teacher': 1,
            'created': now_javascript(),
            'last_login': now_javascript(),
        }
        self.db.store_user(teacher)
        return {'username': username, 'password': password}

    def assign_second_teacher(self, username, class_id):
        user = self.db.user_by_username(username)
        cls = self.db.get_class(class_id)
        self.db.add_second_teacher_to_class(cls, user)

    def logged_in_as_new_student(self, username=None):
        """Make sure that we are logged in."""
        user = self.a_student_account(username)
        self.logged_in_as(user)
        return user

    def logged_in_as_new_teacher(self, username=None):
        """Make sure that we are logged in as a teacher."""
        user = self.a_teacher_account(username)
        self.logged_in_as(user)
        return user

    def logged_in_as(self, user):
        response = self.client.post('/auth/login', data=json.dumps({
            'username': user['username'],
            'password': user['password'],
        }), content_type='application/json')
        assert response.status_code == 200

    def a_class(self, teacher):
        data = {
            'id': unique_id(),
            'date': now_javascript(),
            'teacher': teacher,
            'name': unique_id(),
            'link': "R0dgrqL",
        }
        self.db.store_class(data)
        return data

    def some_saved_program(self, username, **kwargs):
        """Save a program for the given user."""
        program = {
            'id': unique_id(),
            'session': username,
            'username': username,
            'date': now_javascript(),
            'lang': 'en',
            'level': 1,
            'code': 'print TestProgram',
            'adventure_name': 'default',
            'name': 'TestProgram',
        }
        program.update(**kwargs)
        return self.db.store_program(program)

    def some_saved_adventure(self, owner, level='1', **kwargs):
        """Save an adventure for the given owner."""
        adventure = {
            "id": uuid.uuid4().hex,
            "name": 'An adventure',
            "content": 'Some adventure content',
            "public": 0,
            "creator": owner,
            "author": owner,
            "date": now_javascript(),
            "level": level,
            "levels": [level],
            "language": 'en',
            "is_teacher_adventure": True,
        }
        adventure.update(**kwargs)
        return self.db.store_adventure(adventure)


@pytest.fixture()
def given(client, app) -> Given:
    db = app.config['hedy_globals']['DATABASE']
    return Given(client, db)
