# https://werkzeug.palletsprojects.com/en/stable/test/
from .fixtures.given import Given
from .fixtures.flask import Client


def test_programs_page_loads_with_lots_of_programs(client: Client, given: Given):
    """Smoke test of the programs page, if there are enough programs for pagination."""
    # GIVEN
    user = given.logged_in_as_new_student()
    for _ in range(20):
        given.some_saved_program(user['username'])

    # WHEN
    client.get('/programs')

    # THEN - it succeeds


def test_list_programs_requires_login_returns_401(client: Client):
    response = client.get('/programs/list', check=False)
    assert response.status_code == 401


def test_list_programs_returns_saved_programs(client: Client, given: Given):
    user = given.logged_in_as_new_teacher()
    given.some_saved_program(user['username'])
    given.some_saved_program(user['username'])
    response = client.get('/programs/list')
    assert len(response.get_json()['programs']) == 2


def test_save_program_requires_login_returns_401(client: Client):
    response = client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'My Program',
        'level': 1,
    }, check=False)
    assert response.status_code == 401


def test_save_program_invalid_program_id_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'My Program',
        'level': 1,
        'program_id': 123,
        'adventure_name': 'default',
    }, check=False)
    assert response.status_code == 400


def test_save_program_invalid_shared_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'My Program',
        'level': 1,
        'shared': 'yes',
        'adventure_name': 'default',
    }, check=False)
    assert response.status_code == 400


def test_save_program_invalid_adventure_name_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/', {
        'code': 'print Hello',
        'name': 'My Program',
        'level': 1,
        'adventure_name': 1,
    }, check=False)
    assert response.status_code == 400


def test_delete_program_invalid_id_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/delete/', {'id': 123}, check=False)
    assert response.status_code == 400


def test_delete_program_requires_login_returns_401(client: Client):
    response = client.post_json('/programs/delete/', {'id': 'someid'}, check=False)
    assert response.status_code == 401


def test_duplicate_check_invalid_body_type_returns_400(client: Client):
    response = client.post('/programs/duplicate-check', data='[]', content_type='application/json', check=False)
    assert response.status_code == 400


def test_duplicate_check_not_logged_in_returns_403(client: Client):
    response = client.post_json('/programs/duplicate-check', {'name': 'some name'}, check=False)
    assert response.status_code == 403


def test_share_program_missing_program_returns_404(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post('/programs/share/missing-program', check=False)
    assert response.status_code == 404


def test_share_program_not_yours_returns_404(client: Client, given: Given):
    owner = given.a_teacher_account(username='shareowner')
    program = given.some_saved_program(owner['username'])
    given.logged_in_as_new_teacher()
    response = client.post(f"/programs/share/{program['id']}", check=False)
    assert response.status_code == 404


def test_submit_program_requires_login_returns_401(client: Client):
    response = client.post_json('/programs/submit', {'id': 'someid'}, check=False)
    assert response.status_code == 401


def test_submit_program_invalid_id_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/submit', {'id': 123}, check=False)
    assert response.status_code == 400


def test_submit_program_not_yours_returns_400(client: Client, given: Given):
    owner = given.a_teacher_account(username='submitowner')
    program = given.some_saved_program(owner['username'])
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/submit', {'id': program['id']}, check=False)
    assert response.status_code == 400


def test_unsubmit_program_requires_teacher_returns_401(client: Client, given: Given):
    given.logged_in_as_new_student()
    response = client.post_json('/programs/unsubmit', {'id': 'someid'}, check=False)
    assert response.status_code == 401


def test_set_favourite_program_invalid_set_type_returns_400(client: Client, given: Given):
    user = given.logged_in_as_new_teacher()
    program = given.some_saved_program(user['username'])
    response = client.post_json('/programs/set_favourite', {'id': program['id'], 'set': 'yes'}, check=False)
    assert response.status_code == 400


def test_set_favourite_program_not_yours_returns_400(client: Client, given: Given):
    owner = given.a_teacher_account(username='favouriteowner')
    program = given.some_saved_program(owner['username'])
    given.logged_in_as_new_teacher()
    response = client.post_json('/programs/set_favourite', {'id': program['id'], 'set': True}, check=False)
    assert response.status_code == 400
