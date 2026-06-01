"""Tests for authentication endpoints (/auth/*)."""
import uuid
import pytest
from website.auth import TOKEN_COOKIE_NAME

from .fixtures.flask import Client
from .fixtures.given import Given

# A minimal valid signup body that satisfies all required fields.
VALID_SIGNUP = {
    'username': 'newuser',
    'email': 'newuser@example.com',
    'password': 'password123',
    'password_repeat': 'password123',
    'language': 'en',
    'agree_terms': 'yes',
    'keyword_language': 'en',
}


def signup_body(**overrides):
    unique = uuid.uuid4().hex[:8]
    body = {
        **VALID_SIGNUP,
        'username': f'newuser_{unique}',
        'email': f'newuser_{unique}@example.com',
    }
    body.update(overrides)
    return body


# ---------------------------------------------------------------------------
# Signup
# ---------------------------------------------------------------------------

def test_signup_success(client: Client):
    response = client.post_json('/auth/signup', signup_body())
    data = response.get_json()
    assert data['username'].startswith('newuser_')
    assert 'token' in data


def test_signup_duplicate_username(client: Client, given: Given):
    body = signup_body(username='existinguser', email='existinguser@example.com')
    given.a_teacher_account(username='existinguser')
    response = client.post_json('/auth/signup', body, check=False)
    assert response.status_code == 403


def test_signup_duplicate_email(client: Client):
    body = signup_body()
    client.post_json('/auth/signup', body)
    response = client.post_json(
        '/auth/signup', {**signup_body(username='anotheruser'), 'email': body['email']}, check=False)
    assert response.status_code == 403


def test_signup_password_mismatch(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'password_repeat': 'different'}, check=False)
    assert response.status_code == 400


def test_signup_invalid_language(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'language': 'invalid_lang'}, check=False)
    assert response.status_code == 400


def test_signup_invalid_keyword_language(client: Client):
    # keyword_language must be 'en' or the same as language
    response = client.post_json('/auth/signup', {**signup_body(), 'keyword_language': 'fr'}, check=False)
    assert response.status_code == 400


def test_signup_missing_agree_terms(client: Client):
    body = {k: v for k, v in signup_body().items() if k != 'agree_terms'}
    response = client.post_json('/auth/signup', body, check=False)
    assert response.status_code == 400


def test_signup_with_valid_birth_year(client: Client):
    body = {**signup_body(), 'birth_year': 2000}
    response = client.post_json('/auth/signup', body)
    assert 'token' in response.get_json()


def test_signup_with_invalid_birth_year(client: Client):
    body = {**signup_body(), 'birth_year': 1800}
    response = client.post_json('/auth/signup', body, check=False)
    assert response.status_code == 400


def test_signup_with_valid_gender(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'gender': 'm'})
    assert 'token' in response.get_json()


def test_signup_with_invalid_gender(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'gender': 'x'}, check=False)
    assert response.status_code == 400


def test_signup_with_invalid_country(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'country': 'ZZ'}, check=False)
    assert response.status_code == 400


def test_signup_with_valid_prog_experience(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'prog_experience': 'yes'})
    assert 'token' in response.get_json()


def test_signup_with_invalid_prog_experience(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'prog_experience': 'maybe'}, check=False)
    assert response.status_code == 400


def test_signup_with_valid_experience_languages(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'experience_languages': ['python']})
    assert 'token' in response.get_json()


def test_signup_with_invalid_experience_languages(client: Client):
    response = client.post_json('/auth/signup', {**signup_body(), 'experience_languages': ['cobol']}, check=False)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def test_login_success(client: Client, given: Given):
    given.a_teacher_account(username='loginuser', password='mypassword')
    response = client.post_json('/auth/login', {'username': 'loginuser', 'password': 'mypassword'})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert TOKEN_COOKIE_NAME in response.headers.get('Set-Cookie', '')


def test_login_wrong_password(client: Client, given: Given):
    given.a_teacher_account(username='logintest', password='correctpassword')
    response = client.post_json('/auth/login', {'username': 'logintest', 'password': 'wrongpassword'}, check=False)
    assert response.status_code == 403


def test_login_unknown_user(client: Client):
    response = client.post_json('/auth/login', {'username': 'nobody', 'password': 'anything'}, check=False)
    assert response.status_code == 403


def test_login_no_body(client: Client):
    response = client.post_json('/auth/login', None, check=False)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Email verification
# ---------------------------------------------------------------------------

def test_verify_email_success(client: Client):
    resp = client.post_json('/auth/signup', signup_body())
    data = resp.get_json()
    response = client.get(f'/auth/verify?username={data["username"]}&token={data["token"]}', check=False)
    # Successful verification redirects to /hedy
    assert response.status_code == 302


def test_verify_email_bad_token(client: Client):
    resp = client.post_json('/auth/signup', signup_body())
    data = resp.get_json()
    response = client.get(f'/auth/verify?username={data["username"]}&token=badtoken', check=False)
    assert response.status_code == 403


def test_verify_email_missing_token(client: Client):
    response = client.get('/auth/verify?username=someone', check=False)
    assert response.status_code == 400


def test_verify_email_missing_username(client: Client):
    response = client.get('/auth/verify?token=sometoken', check=False)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Logout / destroy
# ---------------------------------------------------------------------------

def test_logout(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post('/auth/logout')
    assert response.status_code == 204


def test_destroy_account(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post('/auth/destroy')
    assert response.status_code == 204


def test_destroy_requires_login(client: Client):
    response = client.post('/auth/destroy', check=False)
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Password recovery
# ---------------------------------------------------------------------------

def test_recover_returns_token(client: Client, given: Given):
    # a_user_with_email creates an account that has an email field, avoiding
    # a KeyError in the recover handler when not in testing mode.
    given.a_user_with_email(username='recoverme')
    response = client.post_json('/auth/recover', {'username': 'recoverme'})
    data = response.get_json()
    assert data['username'] == 'recoverme'
    assert 'token' in data


def test_recover_unknown_user(client: Client):
    response = client.post_json('/auth/recover', {'username': 'nobody'}, check=False)
    assert response.status_code == 403


def test_recover_no_body(client: Client):
    response = client.post_json('/auth/recover', None, check=False)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Password reset
# ---------------------------------------------------------------------------

def test_reset_password_success(client: Client, given: Given):
    given.a_user_with_email(username='resetme')
    recover_resp = client.post_json('/auth/recover', {'username': 'resetme'})
    token = recover_resp.get_json()['token']
    response = client.post_json('/auth/reset', {
        'username': 'resetme',
        'token': token,
        'password': 'newpassword',
        'password_repeat': 'newpassword',
    })
    assert response.status_code == 200
    assert 'message' in response.get_json()


def test_reset_password_invalid_token(client: Client, given: Given):
    given.a_user_with_email(username='resetbadtoken')
    response = client.post_json('/auth/reset', {
        'username': 'resetbadtoken',
        'token': 'bogustoken',
        'password': 'newpassword',
        'password_repeat': 'newpassword',
    }, check=False)
    assert response.status_code == 401


def test_reset_password_mismatch(client: Client, given: Given):
    given.a_user_with_email(username='resetmismatch')
    recover_resp = client.post_json('/auth/recover', {'username': 'resetmismatch'})
    token = recover_resp.get_json()['token']
    response = client.post_json('/auth/reset', {
        'username': 'resetmismatch',
        'token': token,
        'password': 'newpassword',
        'password_repeat': 'different',
    }, check=False)
    assert response.status_code == 400


def test_reset_password_too_short(client: Client, given: Given):
    given.a_user_with_email(username='resetshort')
    recover_resp = client.post_json('/auth/recover', {'username': 'resetshort'})
    token = recover_resp.get_json()['token']
    response = client.post_json('/auth/reset', {
        'username': 'resetshort',
        'token': token,
        'password': 'abc',
        'password_repeat': 'abc',
    }, check=False)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Change password
# ---------------------------------------------------------------------------

def test_change_password_success(client: Client, given: Given):
    user = given.logged_in_as_new_teacher()
    response = client.post_json('/auth/change_password', {
        'old_password': user['password'],
        'new-password': 'newpassword123',
        'password_repeat': 'newpassword123',
    })
    assert response.status_code == 200
    assert 'message' in response.get_json()


def test_change_password_wrong_old(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/auth/change_password', {
        'old_password': 'wrongpassword',
        'new-password': 'newpassword123',
        'password_repeat': 'newpassword123',
    }, check=False)
    assert response.status_code == 403


def test_change_password_too_short(client: Client, given: Given):
    user = given.logged_in_as_new_teacher()
    response = client.post_json('/auth/change_password', {
        'old_password': user['password'],
        'new-password': 'abc',
        'password_repeat': 'abc',
    }, check=False)
    assert response.status_code == 400


def test_change_password_requires_login(client: Client):
    response = client.post_json('/auth/change_password', {
        'old_password': 'x',
        'new-password': 'y',
        'password_repeat': 'y',
    }, check=False)
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Turn into teacher
# ---------------------------------------------------------------------------

def test_turn_into_teacher(client: Client, given: Given):
    given.logged_in_as_new_student()
    response = client.post_json('/auth/turn-into-teacher', {})
    assert response.status_code == 200
    assert 'message' in response.get_json()
