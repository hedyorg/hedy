"""Tests for publicly accessible pages and API endpoints."""
import pytest

from .fixtures.flask import Client
from .fixtures.given import Given


def assert_html_response(response):
    assert response.status_code == 200
    assert response.mimetype == 'text/html'
    assert response.get_data(as_text=True).strip() != ''


def assert_json_response(response):
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    return data


def last_template_context(template_variables):
    assert template_variables
    return template_variables[-1]


# ---------------------------------------------------------------------------
# Hedy code editor pages
# ---------------------------------------------------------------------------

def test_hedy_page_default_level(client: Client, template_variables):
    response = client.get('/hedy')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['current_page'] == 'hedy'
    assert context['level'] == 1
    assert context['javascript_page_options']['page'] == 'code'


def test_hedy_page_level_1(client: Client, template_variables):
    response = client.get('/hedy/1')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['level_nr'] == '1'
    assert context['current_page'] == 'hedy'


def test_hedy_page_level_2(client: Client, template_variables):
    response = client.get('/hedy/2')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['level'] == 2
    assert context['initial_adventure']


def test_hedy_page_invalid_level(client: Client):
    response = client.get('/hedy/999', check=False)
    assert response.status_code == 404


def test_hour_of_code_page(client: Client, template_variables):
    response = client.get('/hour-of-code')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['current_page'] == 'Hour of Code'
    assert context['HOC_tracking_pixel'] is True


def test_hour_of_code_with_level(client: Client):
    response = client.get('/hour-of-code/1', check=False)
    assert response.status_code == 308


# ---------------------------------------------------------------------------
# Cheatsheet
# ---------------------------------------------------------------------------

def test_cheatsheet_default_level(client: Client, template_variables):
    response = client.get('/cheatsheet/')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['level'] == 1
    assert context['commands']


def test_cheatsheet_level_1(client: Client, template_variables):
    response = client.get('/cheatsheet/1')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['level'] == 1
    assert context['commands']


def test_cheatsheet_invalid_level(client: Client):
    response = client.get('/cheatsheet/999', check=False)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Version page
# ---------------------------------------------------------------------------

def test_version_page(client: Client, template_variables):
    response = client.get('/version')
    assert response.status_code == 200
    assert response.get_data(as_text=True).strip() != ''
    context = last_template_context(template_variables)
    assert 'app_name' in context
    assert 'commit' in context


# ---------------------------------------------------------------------------
# Parse endpoint
# ---------------------------------------------------------------------------

def test_parse_valid_code(client: Client):
    response = client.post_json('/parse', {
        'code': 'print Hello world',
        'level': 1,
        'is_debug': False,
        'raw': False,
    })
    data = assert_json_response(response)
    assert 'Code' in data
    assert isinstance(data['Code'], str)
    assert data['Code'].strip() != ''


def test_parse_code_with_error(client: Client):
    # Invalid Hedy code returns 200 with an 'Error' field in the JSON
    response = client.post_json('/parse', {
        'code': 'this is not valid hedy code at all!',
        'level': 1,
        'is_debug': False,
        'raw': False,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'Error' in data


def test_parse_missing_code_field(client: Client):
    response = client.post_json('/parse', {
        'level': 1,
        'is_debug': False,
        'raw': False,
    }, check=False)
    assert response.status_code == 400


def test_parse_missing_level_field(client: Client):
    response = client.post_json('/parse', {
        'code': 'print Hello',
        'is_debug': False,
        'raw': False,
    }, check=False)
    assert response.status_code == 400


def test_parse_missing_is_debug_field(client: Client):
    response = client.post_json('/parse', {
        'code': 'print Hello',
        'level': 1,
        'raw': False,
    }, check=False)
    assert response.status_code == 400


def test_parse_missing_raw_field(client: Client):
    response = client.post_json('/parse', {
        'code': 'print Hello',
        'level': 1,
        'is_debug': False,
    }, check=False)
    assert response.status_code == 400


def test_parse_with_explicit_lang(client: Client):
    response = client.post_json('/parse', {
        'code': 'print Hello',
        'level': 1,
        'is_debug': False,
        'raw': False,
        'lang': 'en',
    })
    data = assert_json_response(response)
    assert 'Code' in data


def test_parse_higher_level_code(client: Client):
    response = client.post_json('/parse', {
        'code': 'name = ask What is your name?\nprint Hello name',
        'level': 3,
        'is_debug': False,
        'raw': False,
    })
    data = assert_json_response(response)
    assert 'Code' in data or 'Error' in data
    if 'Error' in data:
        assert 'Location' in data


# ---------------------------------------------------------------------------
# Change language
# ---------------------------------------------------------------------------

def test_change_language(client: Client):
    response = client.post_json('/change_language', {'lang': 'nl'})
    data = assert_json_response(response)
    assert data.get('success') == 204


def test_change_language_to_english(client: Client):
    response = client.post_json('/change_language', {'lang': 'en'})
    data = assert_json_response(response)
    assert data.get('success') == 204


# ---------------------------------------------------------------------------
# Auth page routes (unauthenticated)
# ---------------------------------------------------------------------------

def test_signup_page(client: Client, template_variables):
    response = client.get('/signup')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['page_title']
    assert context['current_page'] == 'login'


def test_login_page(client: Client, template_variables):
    response = client.get('/login')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['page_title']
    assert context['current_page'] == 'login'


def test_recover_page(client: Client, template_variables):
    response = client.get('/recover')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['page_title']
    assert context['current_page'] == 'login'


def test_signup_page_redirects_when_logged_in(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.get('/signup', check=False)
    # Should redirect to /my-profile
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/my-profile')


def test_login_page_redirects_when_logged_in(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.get('/login', check=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/my-profile')


def test_recover_page_redirects_when_logged_in(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.get('/recover', check=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/my-profile')


# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------

def test_main_page(client: Client, template_variables):
    response = client.get('/')
    assert_html_response(response)
    context = last_template_context(template_variables)
    assert context['current_page'] == 'start'
    assert context['content']


# ---------------------------------------------------------------------------
# Programs page (requires login)
# ---------------------------------------------------------------------------

def test_programs_page_requires_login(client: Client):
    response = client.get('/programs', check=False)
    # Should redirect to login
    assert response.status_code == 302


def test_programs_page_logged_in(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.get('/programs')
    assert_html_response(response)
