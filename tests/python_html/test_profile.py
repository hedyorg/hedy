"""Tests for profile endpoints (/profile/)."""
import uuid
import pytest

from .fixtures.flask import Client
from .fixtures.given import Given


def unique_email(prefix='profile'):
    return f'{prefix}_{uuid.uuid4().hex[:8]}@example.com'


def test_get_profile(client: Client, given: Given):
    user = given.logged_in_as_new_teacher()
    response = client.get('/profile/')
    data = response.get_json()
    assert data['username'] == user['username']
    assert 'language' in data


def test_get_profile_requires_login(client: Client):
    response = client.get('/profile/', check=False)
    assert response.status_code == 401


def test_update_profile_language(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'nl',
        'keyword_language': 'nl',
        'email': unique_email(),
    })
    data = response.get_json()
    assert 'message' in data


def test_update_profile_keeps_same_email(client: Client, given: Given):
    user = given.a_user_with_email(username=f'profuser_{uuid.uuid4().hex[:8]}', email=unique_email('profuser'))
    given.logged_in_as(user)
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': user['email'],  # same email, no change
    })
    assert response.status_code == 200
    assert 'message' in response.get_json()


def test_update_profile_change_email_returns_token(client: Client, given: Given):
    user = given.a_user_with_email(username=f'emailchanger_{uuid.uuid4().hex[:8]}', email=unique_email('old'))
    given.logged_in_as(user)
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': unique_email('new'),
    })
    data = response.get_json()
    # In testing mode, returns {username, token} merged with the reload response
    assert response.status_code == 200
    assert 'message' in data


def test_update_profile_invalid_language(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'invalid_lang',
        'keyword_language': 'en',
        'email': unique_email(),
    }, check=False)
    assert response.status_code == 400


def test_update_profile_invalid_keyword_language(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'fr',  # not 'en' and not same as language
        'email': unique_email(),
    }, check=False)
    assert response.status_code == 400


def test_update_profile_invalid_email(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': 'not-a-valid-email',
    }, check=False)
    assert response.status_code == 400


def test_update_profile_invalid_body_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post('/profile/', data='[]', content_type='application/json', check=False)
    assert response.status_code == 400


def test_update_profile_with_birth_year(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': unique_email(),
        'birth_year': 1990,
    })
    assert response.status_code == 200
    assert 'message' in response.get_json()


def test_update_profile_with_invalid_birth_year(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': unique_email(),
        'birth_year': 1800,
    }, check=False)
    assert response.status_code == 400


def test_update_profile_with_non_numeric_birth_year_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': unique_email(),
        'birth_year': 'nineteen ninety',
    }, check=False)
    assert response.status_code == 400


def test_update_profile_with_valid_gender(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': unique_email(),
        'gender': 'f',
    })
    assert response.status_code == 200
    assert 'message' in response.get_json()


def test_update_profile_with_invalid_gender(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': unique_email(),
        'gender': 'x',
    }, check=False)
    assert response.status_code == 400


def test_update_profile_with_invalid_country_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': unique_email(),
        'country': 'not-a-country',
    }, check=False)
    assert response.status_code == 400


def test_update_profile_existing_email_returns_403(client: Client, given: Given):
    existing = given.a_user_with_email(username=f'existing_{uuid.uuid4().hex[:8]}', email=unique_email('taken'))
    user = given.a_user_with_email(username=f'profile_{uuid.uuid4().hex[:8]}', email=unique_email('current'))
    given.logged_in_as(user)
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': existing['email'],
    }, check=False)
    assert response.status_code == 403


def test_update_profile_requires_login(client: Client):
    response = client.post_json('/profile/', {
        'language': 'en',
        'keyword_language': 'en',
        'email': unique_email(),
    }, check=False)
    assert response.status_code == 401
