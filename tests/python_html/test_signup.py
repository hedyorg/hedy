"""Tests for the POST /auth/signup endpoint.

Complements the basic signup tests in test_auth.py with detailed coverage of:
  - response shape
  - username/email normalisation
  - every validation branch in validate_signup_data() and signup()
  - all optional fields (heard_about, gender, country, birth_year, …)
  - duplicate-detection edge cases
  - malformed request bodies
"""
import datetime
import uuid

import pytest

from .fixtures.flask import Client
from .fixtures.given import Given


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def signup_body(**overrides):
    """Return a minimal valid signup payload with globally-unique identifiers."""
    unique = uuid.uuid4().hex[:8]
    body = {
        'username': f'su_{unique}',
        'email': f'su_{unique}@example.com',
        'password': 'password123',
        'password_repeat': 'password123',
        'language': 'en',
        'agree_terms': 'yes',
        'keyword_language': 'en',
    }
    body.update(overrides)
    return body


# ---------------------------------------------------------------------------
# Response shape
# ---------------------------------------------------------------------------

def test_signup_response_contains_username_and_token(client: Client):
    """A successful signup response contains 'username' and 'token' keys."""
    data = client.post_json('/auth/signup', signup_body()).get_json()
    assert 'username' in data
    assert 'token' in data


# ---------------------------------------------------------------------------
# Username normalisation
# ---------------------------------------------------------------------------

def test_signup_username_is_stored_lowercase(client: Client):
    """Input usernames are converted to lowercase before storage."""
    unique = uuid.uuid4().hex[:6]
    username = f'MixedCaseUser{unique}'
    body = signup_body(username=username)
    data = client.post_json('/auth/signup', body).get_json()
    assert data['username'] == username.lower()


def test_signup_username_leading_trailing_spaces_stripped(client: Client):
    """Leading/trailing whitespace in the username is stripped."""
    unique = uuid.uuid4().hex[:6]
    username = f'spacey{unique}'
    body = signup_body(username=f'  {username}  ')
    data = client.post_json('/auth/signup', body).get_json()
    assert data['username'] == username


def test_signup_user_can_login_after_signup(client: Client):
    """After signing up the user can log in with the same credentials."""
    body = signup_body()
    client.post_json('/auth/signup', body)
    login = client.post_json('/auth/login', {
        'username': body['username'],
        'password': body['password'],
    })
    assert login.status_code == 200
    assert isinstance(login.get_json(), dict)


# ---------------------------------------------------------------------------
# Username validation – validate_signup_data()
# ---------------------------------------------------------------------------

def test_signup_username_with_at_sign_rejected(client: Client):
    """Usernames containing '@' are rejected (reserved for e-mails)."""
    response = client.post_json('/auth/signup', signup_body(username='user@domain'), check=False)
    assert response.status_code == 400


def test_signup_username_with_colon_rejected(client: Client):
    """Usernames containing ':' are rejected."""
    response = client.post_json('/auth/signup', signup_body(username='user:name'), check=False)
    assert response.status_code == 400


def test_signup_username_two_chars_rejected(client: Client):
    """Usernames shorter than 3 characters are rejected."""
    response = client.post_json('/auth/signup', signup_body(username='ab'), check=False)
    assert response.status_code == 400


def test_signup_username_exactly_three_chars_accepted(client: Client):
    """A 3-character username sits on the boundary and must be accepted."""
    short = uuid.uuid4().hex[:3]
    response = client.post_json('/auth/signup', signup_body(username=short))
    assert 'token' in response.get_json()


def test_signup_missing_username_rejected(client: Client):
    """Requests that omit the username field are rejected."""
    body = {k: v for k, v in signup_body().items() if k != 'username'}
    response = client.post_json('/auth/signup', body, check=False)
    assert response.status_code == 400


def test_signup_whitespace_only_username_rejected(client: Client):
    """A username that is all whitespace is stripped to empty and rejected as too short."""
    response = client.post_json('/auth/signup', signup_body(username='   '), check=False)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# E-mail validation
# ---------------------------------------------------------------------------

def test_signup_email_without_at_sign_rejected(client: Client):
    """An e-mail address that does not contain '@' is rejected."""
    response = client.post_json('/auth/signup', signup_body(email='notanemail'), check=False)
    assert response.status_code == 400


def test_signup_missing_email_rejected(client: Client):
    """Requests that omit the email field are rejected."""
    body = {k: v for k, v in signup_body().items() if k != 'email'}
    response = client.post_json('/auth/signup', body, check=False)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------

def test_signup_password_five_chars_rejected(client: Client):
    """Passwords shorter than 6 characters are rejected."""
    response = client.post_json(
        '/auth/signup',
        signup_body(password='12345', password_repeat='12345'),
        check=False,
    )
    assert response.status_code == 400


def test_signup_missing_password_rejected(client: Client):
    """Requests that omit both password fields are rejected."""
    body = {k: v for k, v in signup_body().items() if k not in ('password', 'password_repeat')}
    response = client.post_json('/auth/signup', body, check=False)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# keyword_language validation
# ---------------------------------------------------------------------------

def test_signup_keyword_language_same_as_ui_language_accepted(client: Client):
    """keyword_language equal to the selected UI language (here 'nl') is valid."""
    response = client.post_json('/auth/signup', signup_body(language='nl', keyword_language='nl'))
    assert 'token' in response.get_json()


def test_signup_keyword_language_en_with_non_en_ui_language_accepted(client: Client):
    """keyword_language='en' is always valid regardless of the UI language."""
    response = client.post_json('/auth/signup', signup_body(language='nl', keyword_language='en'))
    assert 'token' in response.get_json()


def test_signup_keyword_language_mismatch_rejected(client: Client):
    """keyword_language that is neither 'en' nor the UI language is rejected."""
    response = client.post_json(
        '/auth/signup',
        signup_body(language='nl', keyword_language='fr'),
        check=False,
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Optional field: gender
# ---------------------------------------------------------------------------

def test_signup_gender_female_accepted(client: Client):
    response = client.post_json('/auth/signup', signup_body(gender='f'))
    assert 'token' in response.get_json()


def test_signup_gender_other_accepted(client: Client):
    response = client.post_json('/auth/signup', signup_body(gender='o'))
    assert 'token' in response.get_json()


# ---------------------------------------------------------------------------
# Optional field: birth_year
# ---------------------------------------------------------------------------

def test_signup_birth_year_non_integer_string_rejected(client: Client):
    """A birth_year that cannot be parsed as an integer is rejected."""
    response = client.post_json('/auth/signup', signup_body(birth_year='nineteen-ninety'), check=False)
    assert response.status_code == 400


def test_signup_birth_year_future_rejected(client: Client):
    """A birth year in the future is rejected."""
    response = client.post_json(
        '/auth/signup',
        signup_body(birth_year=datetime.datetime.now().year + 1),
        check=False,
    )
    assert response.status_code == 400


def test_signup_birth_year_current_year_accepted(client: Client):
    """A birth year equal to the current year is the upper boundary and must be accepted."""
    response = client.post_json('/auth/signup', signup_body(birth_year=datetime.datetime.now().year))
    assert 'token' in response.get_json()


# ---------------------------------------------------------------------------
# Optional field: country
# ---------------------------------------------------------------------------

def test_signup_valid_country_accepted(client: Client):
    """A valid ISO 3166-1 country code is accepted."""
    response = client.post_json('/auth/signup', signup_body(country='NL'))
    assert 'token' in response.get_json()


# ---------------------------------------------------------------------------
# Optional field: heard_about
# ---------------------------------------------------------------------------

def test_signup_heard_about_valid_list_accepted(client: Client):
    response = client.post_json(
        '/auth/signup',
        signup_body(heard_about=['social_media', 'from_another_teacher']),
    )
    assert 'token' in response.get_json()


def test_signup_heard_about_single_string_coerced_to_list(client: Client):
    """A single string for heard_about is coerced to a one-element list and accepted."""
    response = client.post_json('/auth/signup', signup_body(heard_about='social_media'))
    assert 'token' in response.get_json()


def test_signup_heard_about_invalid_value_rejected(client: Client):
    response = client.post_json(
        '/auth/signup',
        signup_body(heard_about=['unknown_source']),
        check=False,
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Optional field: prog_experience
# ---------------------------------------------------------------------------

def test_signup_prog_experience_no_accepted(client: Client):
    """prog_experience='no' is a valid value in addition to 'yes'."""
    response = client.post_json('/auth/signup', signup_body(prog_experience='no'))
    assert 'token' in response.get_json()


# ---------------------------------------------------------------------------
# Optional field: experience_languages
# ---------------------------------------------------------------------------

def test_signup_experience_languages_single_string_coerced(client: Client):
    """A single string for experience_languages is coerced to a list and accepted."""
    response = client.post_json('/auth/signup', signup_body(experience_languages='python'))
    assert 'token' in response.get_json()


def test_signup_experience_languages_multiple_accepted(client: Client):
    response = client.post_json('/auth/signup', signup_body(experience_languages=['python', 'scratch']))
    assert 'token' in response.get_json()


# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

def test_signup_duplicate_username_case_insensitive(client: Client, given: Given):
    """Duplicate username check is case-insensitive: 'DupUser' collides with 'dupuser'."""
    unique = uuid.uuid4().hex[:8]
    username = f'dup_{unique}'
    given.a_teacher_account(username=username)
    # Send the same name in a different case
    response = client.post_json('/auth/signup', signup_body(username=username.upper()), check=False)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Malformed request body
# ---------------------------------------------------------------------------

def test_signup_empty_json_object_rejected(client: Client):
    """An empty JSON object is missing all required fields and must be rejected."""
    response = client.post_json('/auth/signup', {}, check=False)
    assert response.status_code == 400


def test_signup_null_body_rejected(client: Client):
    """A JSON null body is not a dict and must be rejected."""
    response = client.post_json('/auth/signup', None, check=False)
    assert response.status_code == 400


def test_signup_array_body_rejected(client: Client):
    """A JSON array body is not a dict and must be rejected."""
    response = client.post_json('/auth/signup', ['not', 'a', 'dict'], check=False)
    assert response.status_code == 400
