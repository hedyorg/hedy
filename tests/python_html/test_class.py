from .fixtures.given import Given
from .fixtures.flask import Client


def put_json(client: Client, endpoint: str, data, check=True):
    response = client.client.put(
        endpoint,
        json=data,
        headers={'X-Testing': '1'},
    )
    if check:
        assert 200 <= response.status_code < 300
    return response


def test_second_teacher_of_deleted_class(client: Client, given: Given):
    # GIVEN a class with a second teacher
    teacher = given.logged_in_as_new_teacher('teacher')
    second_teacher = given.a_teacher_account('second_teacher')
    cls = given.a_class(teacher['username'])
    given.assign_second_teacher(second_teacher['username'], cls['id'])

    # WHEN the owner teacher deletes the class
    client.delete(f'/class/{cls["id"]}')
    client.post('/auth/logout')

    # THEN the second teacher can access the /for-teachers page
    client.post_json('/auth/login', second_teacher)
    client.get('/for-teachers')


def test_create_class_requires_teacher_returns_401(client: Client, given: Given):
    given.logged_in_as_new_student()
    response = client.post_json('/class/', {'name': 'Science'}, check=False)
    assert response.status_code == 401


def test_create_class_invalid_body_type_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    response = client.post('/class/', data='[]', content_type='application/json', check=False)
    assert response.status_code == 400


def test_create_class_missing_name_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    response = client.post_json('/class/', {}, check=False)
    assert response.status_code == 400


def test_create_class_empty_name_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    response = client.post_json('/class/', {'name': ''}, check=False)
    assert response.status_code == 400


def test_create_class_duplicate_name_returns_200(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    existing_class = given.a_class(teacher['username'])
    response = client.post_json('/class/', {'name': existing_class['name']}, check=False)
    assert response.status_code == 200
    assert response.get_data(as_text=True).strip() != ''


def test_create_class_redesign_invalid_creation_type_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    response = client.post_json('/class/redesign', {
        'name': 'Redesign Class',
        'creation_type': 123,
    }, check=False)
    assert response.status_code == 400


def test_create_class_redesign_invalid_body_type_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    response = client.post('/class/redesign', data='[]', content_type='application/json', check=False)
    assert response.status_code == 400


def test_create_class_redesign_missing_name_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    response = client.post_json('/class/redesign', {'creation_type': 'standard'}, check=False)
    assert response.status_code == 400


def test_update_class_missing_class_returns_404(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    response = put_json(client, '/class/missing-class', {'name': 'Renamed'}, check=False)
    assert response.status_code == 404


def test_update_class_invalid_body_type_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    existing_class = given.a_class(teacher['username'])
    response = client.client.put(
        f'/class/{existing_class["id"]}',
        data='[]',
        content_type='application/json',
        headers={'X-Testing': '1'},
    )
    assert response.status_code == 400


def test_update_class_missing_name_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    existing_class = given.a_class(teacher['username'])
    response = put_json(client, f'/class/{existing_class["id"]}', {}, check=False)
    assert response.status_code == 400


def test_update_class_empty_name_returns_400(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    existing_class = given.a_class(teacher['username'])
    response = put_json(client, f'/class/{existing_class["id"]}', {'name': ''}, check=False)
    assert response.status_code == 400


def test_update_class_duplicate_name_returns_200(client: Client, given: Given):
    teacher = given.a_user_with_email()
    given.logged_in_as(teacher)
    first_class = given.a_class(teacher['username'])
    second_class = given.a_class(teacher['username'])
    response = put_json(client, f'/class/{second_class["id"]}', {'name': first_class['name']}, check=False)
    assert response.status_code == 200
    assert response.get_data(as_text=True).strip() != ''


def test_join_class_id_second_teacher_invite_succeeds(client: Client, given: Given):
    owner = given.a_teacher_account('join_second_teacher_owner')
    existing_class = given.a_class(owner['username'])
    second_teacher = given.a_teacher_account('join_second_teacher_user')
    given.db.add_class_invite(second_teacher['username'], existing_class['id'], 'second_teacher', 'second_teacher')
    given.logged_in_as(second_teacher)
    with client.client.session_transaction() as sess:
        sess['messages'] = 1
    response = client.post(f'/class/join/{existing_class["id"]}', check=False)
    assert response.status_code == 302
    updated_class = given.db.get_class(existing_class['id'])
    assert any(t['username'] == second_teacher['username'] for t in updated_class.get('second_teachers', []))


def test_delete_class_requires_login_returns_401(client: Client, given: Given):
    teacher = given.a_teacher_account('owner_for_delete')
    existing_class = given.a_class(teacher['username'])
    response = client.delete(f'/class/{existing_class["id"]}', check=False)
    assert response.status_code == 401


def test_delete_class_missing_class_returns_404(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('delete_missing_teacher')
    response = client.delete('/class/missing-class', check=False)
    assert response.status_code == 404


def test_delete_class_not_owner_returns_401(client: Client, given: Given):
    owner = given.a_teacher_account('class_owner')
    existing_class = given.a_class(owner['username'])
    given.logged_in_as_new_teacher('other_teacher')
    response = client.delete(f'/class/{existing_class["id"]}', check=False)
    assert response.status_code == 401


def test_join_class_id_missing_class_returns_404(client: Client, given: Given):
    given.logged_in_as_new_student('joiner_missing')
    response = client.post('/class/join/missing-class', check=False)
    assert response.status_code == 404


def test_join_class_id_student_in_another_class_returns_400(client: Client, given: Given):
    owner = given.a_teacher_account('join_owner')
    existing_class = given.a_class(owner['username'])
    target_class = given.a_class(owner['username'])
    student = given.a_student_account('occupied_student')
    given.db.add_student_to_class(existing_class['id'], student['username'])
    given.db.add_class_invite(student['username'], target_class['id'], 'student', 'student')
    given.logged_in_as(student)
    response = client.post(f'/class/join/{target_class["id"]}', check=False)
    assert response.status_code == 400


def test_legacy_join_missing_class_returns_404(client: Client):
    response = client.post_json('/class/join', {'id': 'missing-class'}, check=False)
    assert response.status_code == 404


def test_legacy_join_not_logged_in_returns_403(client: Client, given: Given):
    owner = given.a_teacher_account('legacy_join_owner')
    existing_class = given.a_class(owner['username'])
    response = client.post_json('/class/join', {'id': existing_class['id']}, check=False)
    assert response.status_code == 403


def test_legacy_join_student_in_another_class_returns_400(client: Client, given: Given):
    owner = given.a_teacher_account('legacy_join_owner_two')
    existing_class = given.a_class(owner['username'])
    other_class = given.a_class(owner['username'])
    student = given.a_student_account('legacy_join_student')
    given.db.add_student_to_class(other_class['id'], student['username'])
    given.logged_in_as(student)
    response = client.post_json('/class/join', {'id': existing_class['id']}, check=False)
    assert response.status_code == 400


def test_legacy_join_succeeds_and_removes_invite(client: Client, given: Given):
    owner = given.a_teacher_account('legacy_join_success_owner')
    existing_class = given.a_class(owner['username'])
    student = given.a_student_account('legacy_join_success_student')
    given.db.add_class_invite(student['username'], existing_class['id'], 'student', 'student')
    given.logged_in_as(student)
    with client.client.session_transaction() as sess:
        sess['messages'] = 1
    response = client.post_json('/class/join', {'id': existing_class['id']}, check=False)
    assert response.status_code == 200
    assert given.db.get_user_class_invite(student['username'], existing_class['id']) is None
    assert existing_class['id'] in given.db.get_student_classes_ids(student['username'])


def test_leave_class_succeeds_for_teacher(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('leave_class_teacher')
    existing_class = given.a_class(teacher['username'])
    student = given.a_student_account('leave_class_student')
    given.db.add_student_to_class(existing_class['id'], student['username'])
    response = client.delete(f'/class/{existing_class["id"]}/student/{student["username"]}')
    assert response.status_code == 200
    assert existing_class['id'] not in given.db.get_student_classes_ids(student['username'])


def test_remove_second_teacher_succeeds_for_owner(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('remove_second_teacher_owner')
    second_teacher = given.a_teacher_account('remove_second_teacher_user')
    existing_class = given.a_class(teacher['username'])
    given.assign_second_teacher(second_teacher['username'], existing_class['id'])
    response = client.delete(f'/class/{existing_class["id"]}/second-teacher/{second_teacher["username"]}')
    assert response.status_code == 200
    updated_class = given.db.get_class(existing_class['id'])
    assert not any(t['username'] == second_teacher['username'] for t in updated_class.get('second_teachers', []))


def test_remove_second_teacher_not_owner_returns_400(client: Client, given: Given):
    owner = given.a_teacher_account('remove_second_teacher_not_owner_owner')
    second_teacher = given.a_teacher_account('remove_second_teacher_not_owner_user')
    existing_class = given.a_class(owner['username'])
    given.assign_second_teacher(second_teacher['username'], existing_class['id'])
    given.logged_in_as_new_teacher('different_teacher')
    response = client.delete(
        f'/class/{existing_class["id"]}/second-teacher/{second_teacher["username"]}',
        check=False,
    )
    assert response.status_code == 400


def test_get_classes_returns_owned_and_second_teacher_classes(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('classes_list_teacher')
    owned_class = given.a_class(teacher['username'])
    owner = given.a_teacher_account('classes_list_other_owner')
    second_teacher_class = given.a_class(owner['username'])
    given.assign_second_teacher(teacher['username'], second_teacher_class['id'])
    response = client.get('/classes')
    data = response.get_json()
    ids = {item['id'] for item in data}
    assert owned_class['id'] in ids
    assert second_teacher_class['id'] in ids


def test_duplicate_class_invalid_body_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher('duplicate_class_invalid_body_teacher')
    response = client.post('/duplicate_class', data='[]', content_type='application/json', check=False)
    assert response.status_code == 400


def test_duplicate_class_missing_class_returns_404(client: Client, given: Given):
    given.logged_in_as_new_teacher('duplicate_class_missing_teacher')
    response = client.post_json('/duplicate_class', {'id': 'missing-class', 'name': 'New Class'}, check=False)
    assert response.status_code == 404


def test_duplicate_class_duplicate_name_returns_400(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('duplicate_class_duplicate_teacher')
    source_class = given.a_class(teacher['username'])
    duplicate_name_class = given.a_class(teacher['username'])
    response = client.post_json('/duplicate_class', {
        'id': source_class['id'],
        'name': duplicate_name_class['name'],
    }, check=False)
    assert response.status_code == 400


def test_duplicate_class_copies_second_teacher_invites(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('duplicate_class_success_teacher')
    source_class = given.a_class(teacher['username'])
    second_teacher = given.a_teacher_account('duplicate_class_second_teacher')
    given.assign_second_teacher(second_teacher['username'], source_class['id'])
    response = client.post_json('/duplicate_class', {
        'id': source_class['id'],
        'name': 'Duplicated Class',
        'copy_second_teachers': True,
    })
    new_class_id = response.get_json()['id']
    assert given.db.get_user_class_invite(second_teacher['username'], new_class_id) is not None


def test_filter_usernames_empty_search_returns_200(client: Client, given: Given):
    given.logged_in_as_new_teacher('filter_usernames_empty_teacher')
    response = client.get('/search?search=&user_type=student')
    assert response.status_code == 200
    assert response.mimetype == 'text/html'


def test_filter_usernames_excludes_existing_students_invites_and_self(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('filter_usernames_teacher')
    existing_class = given.a_class(teacher['username'])
    included_student = given.a_student_account('filter_student_included')
    existing_student = given.a_student_account('filter_student_existing')
    invited_student = given.a_student_account('filter_student_invited')
    given.db.add_student_to_class(existing_class['id'], existing_student['username'])
    given.db.add_class_invite(invited_student['username'], existing_class['id'], 'student', 'student')
    response = client.get(
        f'/search?search=filter_student&user_type=student&class_id={existing_class["id"]}',
        check=False,
    )
    body = response.get_data(as_text=True)
    assert included_student['username'] in body
    assert existing_student['username'] not in body
    assert invited_student['username'] not in body
    assert teacher['username'] not in body


def test_invite_users_without_usernames_returns_400(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('invite_teacher')
    existing_class = given.a_class(teacher['username'])
    response = client.post(
        f'/invite?class_id={existing_class["id"]}&invite_as=student',
        data={},
        check=False,
    )
    assert response.status_code == 400


def test_invite_users_missing_class_returns_404(client: Client, given: Given):
    given.logged_in_as_new_teacher('invite_missing_teacher')
    student = given.a_student_account('invite_missing_student')
    response = client.post(
        '/invite?class_id=missing-class&invite_as=student',
        data={'usernames': student['username']},
        check=False,
    )
    assert response.status_code == 404


def test_invite_users_missing_class_id_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher('invite_missing_class_id_teacher')
    student = given.a_student_account('invite_missing_class_id_student')
    response = client.post(
        '/invite?invite_as=student',
        data={'usernames': student['username']},
        check=False,
    )
    assert response.status_code == 400


def test_invite_second_teacher_unknown_user_returns_400(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('owner_second_teacher')
    existing_class = given.a_class(teacher['username'])
    response = client.post_json('/invite-second-teacher', {
        'username': 'missing_teacher',
        'class_id': existing_class['id'],
    }, check=False)
    assert response.status_code == 400


def test_invite_second_teacher_invalid_body_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher('owner_invalid_second_teacher')
    response = client.post('/invite-second-teacher', data='[]', content_type='application/json', check=False)
    assert response.status_code == 400


def test_invite_second_teacher_existing_invite_returns_400(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('owner_with_invite')
    existing_class = given.a_class(teacher['username'])
    second_teacher = given.a_teacher_account('pending_second_teacher')
    given.db.add_class_invite(second_teacher['username'], existing_class['id'], 'second_teacher', 'second_teacher')
    response = client.post_json('/invite-second-teacher', {
        'username': second_teacher['username'],
        'class_id': existing_class['id'],
    }, check=False)
    assert response.status_code == 400


def test_invite_second_teacher_student_target_returns_400(client: Client, given: Given):
    teacher = given.logged_in_as_new_teacher('owner_student_target')
    existing_class = given.a_class(teacher['username'])
    student = given.a_student_account('not_a_teacher')
    response = client.post_json('/invite-second-teacher', {
        'username': student['username'],
        'class_id': existing_class['id'],
    }, check=False)
    assert response.status_code == 400


def test_invite_second_teacher_missing_class_returns_404(client: Client, given: Given):
    given.logged_in_as_new_teacher('owner_missing_class')
    second_teacher = given.a_teacher_account('teacher_for_missing_class')
    response = client.post_json('/invite-second-teacher', {
        'username': second_teacher['username'],
        'class_id': 'missing-class',
    }, check=False)
    assert response.status_code == 404


def test_remove_invite_requires_login_returns_401(client: Client, given: Given):
    response = client.post_json('/remove_student_invite', {
        'username': 'student',
        'class_id': 'some-class',
    }, check=False)
    assert response.status_code == 401


def test_remove_invite_invalid_body_type_returns_400(client: Client, given: Given):
    given.logged_in_as_new_teacher('remove_invalid_body_teacher')
    response = client.post('/remove_student_invite', data='[]', content_type='application/json', check=False)
    assert response.status_code == 400


def test_remove_invite_non_teacher_for_other_user_returns_401(client: Client, given: Given):
    teacher = given.a_teacher_account('remove_invite_owner')
    existing_class = given.a_class(teacher['username'])
    given.logged_in_as_new_student('remove_invite_student')
    response = client.post_json('/remove_student_invite', {
        'username': 'someone_else',
        'class_id': existing_class['id'],
    }, check=False)
    assert response.status_code == 401


def test_remove_invite_missing_class_returns_404(client: Client, given: Given):
    given.logged_in_as_new_teacher('remove_missing_teacher')
    response = client.post_json('/remove_student_invite', {
        'username': 'anyone',
        'class_id': 'missing-class',
    }, check=False)
    assert response.status_code == 404
