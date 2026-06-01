"""Tests for the programs API endpoints (/programs/*)."""
import pytest

from .fixtures.flask import Client
from .fixtures.given import Given


def test_list_programs_empty(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.get('/programs/list')
    data = response.get_json()
    assert 'programs' in data
    assert data['programs'] == []


def test_list_programs_with_entries(client: Client, given: Given):
    user = given.logged_in_as_new_teacher()
    given.some_saved_program(user['username'])
    given.some_saved_program(user['username'])
    response = client.get('/programs/list')
    data = response.get_json()
    assert len(data['programs']) == 2


def test_list_programs_requires_login(client: Client):
    response = client.get('/programs/list', check=False)
    assert response.status_code == 401


def test_save_program(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/', {
        'code': 'print Hello world',
        'name': 'My Program',
        'level': 1,
        'adventure_name': 'default',
    })
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == 'My Program'


def test_save_program_missing_code(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/', {
        'name': 'My Program',
        'level': 1,
    }, check=False)
    assert response.status_code == 400


def test_save_program_missing_name(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/', {
        'code': 'print Hello',
        'level': 1,
    }, check=False)
    assert response.status_code == 400


def test_save_program_missing_level(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'My Program',
    }, check=False)
    assert response.status_code == 400


def test_save_program_with_adventure_name(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'Adventure Program',
        'level': 1,
        'adventure_name': 'default',
    })
    data = response.get_json()
    assert 'id' in data


def test_save_program_requires_login(client: Client):
    response = client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'My Program',
        'level': 1,
    }, check=False)
    assert response.status_code == 401


def test_delete_program(client: Client, given: Given):
    user = given.logged_in_as_new_teacher()
    program = given.some_saved_program(user['username'])
    response = client.post_json('/programs/delete/', {'id': program['id']})
    data = response.get_json()
    assert 'message' in data


def test_delete_program_not_found(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/delete/', {'id': 'nonexistent-id'}, check=False)
    assert response.status_code == 404


def test_delete_program_missing_id(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/delete/', {}, check=False)
    assert response.status_code == 400


def test_delete_program_not_yours(client: Client, given: Given):
    owner = given.a_teacher_account(username='owner')
    program = given.some_saved_program(owner['username'])
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/delete/', {'id': program['id']}, check=False)
    assert response.status_code == 404


def test_delete_program_requires_login(client: Client):
    response = client.post_json('/programs/delete/', {'id': 'someid'}, check=False)
    assert response.status_code == 401


def test_duplicate_check_not_a_duplicate(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/duplicate-check', {'name': 'unique name'})
    data = response.get_json()
    assert data['duplicate'] is False


def test_duplicate_check_is_a_duplicate(client: Client, given: Given):
    user = given.logged_in_as_new_teacher()
    given.some_saved_program(user['username'], name='My Program')
    response = client.post_json('/programs/duplicate-check', {'name': 'My Program'})
    data = response.get_json()
    assert data['duplicate'] is True


def test_duplicate_check_missing_name(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/duplicate-check', {}, check=False)
    assert response.status_code == 400


def test_duplicate_check_not_logged_in(client: Client):
    response = client.post_json('/programs/duplicate-check', {'name': 'some name'}, check=False)
    assert response.status_code == 403


def test_save_then_list_program(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'Saved Program',
        'level': 2,
        'adventure_name': 'default',
    })
    response = client.get('/programs/list')
    programs = response.get_json()['programs']
    assert any(p['name'] == 'Saved Program' for p in programs)


def test_save_and_delete_program(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    save_resp = client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'To Delete',
        'level': 1,
        'adventure_name': 'default',
    })
    program_id = save_resp.get_json()['id']
    client.post_json('/programs/delete/', {'id': program_id})
    programs = client.get('/programs/list').get_json()['programs']
    assert not any(p['id'] == program_id for p in programs)
