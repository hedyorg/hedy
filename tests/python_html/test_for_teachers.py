"""Tests for the for_teachers.py endpoints."""
import uuid
import pytest
from flask import g, session

from tests.python_html.fixtures.flask import Client
from tests.python_html.fixtures.given import Given
import website_content as hedy_content
from website import for_teachers as for_teachers_module


def _unique_username(prefix='stu'):
    """Return a username unique to this test run."""
    return f'{prefix}{uuid.uuid4().hex[:8]}'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _init_class_customizations(client, class_id):
    """Trigger customization migration for a class by visiting the customize-level page.

    This is required before calling endpoints that read customizations["sorted_adventures"].
    """
    client.get(f'/for-teachers/redesign/class/{class_id}/customize-level/1')


def _unwrap_route(method):
    """Unwrap auth/route decorators so internals can be unit-tested directly."""
    fn = method
    while hasattr(fn, '__wrapped__'):
        fn = fn.__wrapped__
    return fn


def _set_en_locale():
    """Set a stable request locale/session used by direct internal method tests."""
    g.lang = 'en'
    g.keyword_lang = 'en'
    session['lang'] = 'en'


def _clear_session(client):
    """Clear the current client session."""
    with client.client.session_transaction() as sess:
        sess.clear()


def assert_useful_response(response):
    assert response.status_code == 200
    if response.is_json:
        assert response.get_json() is not None
    else:
        assert response.get_data(as_text=True).strip() != ''


# ---------------------------------------------------------------------------
# Public pages (no authentication required)
# ---------------------------------------------------------------------------

class TestPublicPages:
    def test_public_pages(self, client, template_variables):
        cases = [
            ('/for-teachers/workbooks/1', 200),
            ('/for-teachers/workbooks/999', 404),
            ('/for-teachers/workbooks/notanumber', 404),
            ('/for-teachers/manual', 200),
            ('/for-teachers/manual/intro', 308),
            ('/for-teachers/manual/this_does_not_exist', 200),
        ]
        for url, expected in cases:
            response = client.get(url, check=False)
            assert response.status_code == expected
            if response.status_code == 200:
                context = template_variables[-1]
                assert context['current_page'] == 'teacher-manual'
                if url.startswith('/for-teachers/workbooks/'):
                    assert context['page_title']
                    assert context['workbook']
                else:
                    assert context['section_title']
                    assert context['section_key'] in ('intro', 'this_does_not_exist')


# ---------------------------------------------------------------------------
# Authentication enforcement on teacher-only pages
# ---------------------------------------------------------------------------

class TestAuthEnforcement:
    def test_teacher_only_pages(self, client, given):
        cases = [
            ('anon', 'get', '/for-teachers/', 401),
            ('anon', 'get', '/for-teachers/class/all', 401),
            ('anon', 'get', '/for-teachers/class/new', 401),
            ('student', 'get', '/for-teachers/', 401),
            ('teacher', 'get', '/for-teachers/', 200),
            ('teacher', 'get', '/for-teachers/class/all', 200),
            ('teacher', 'get', '/for-teachers/class/new', 200),
        ]
        for actor, method, path, expected in cases:
            _clear_session(client)
            if actor == 'student':
                given.logged_in_as_new_student()
            elif actor == 'teacher':
                given.logged_in_as_new_teacher()
            response = getattr(client, method)(path, check=False)
            assert response.status_code == expected


# ---------------------------------------------------------------------------
# GET /for-teachers/class/<class_id>  (returns JSON in testing mode)
# ---------------------------------------------------------------------------

class TestGetClass:
    def test_get_class_variants(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])

        response = client.get(f'/for-teachers/class/{cls["id"]}')
        assert_useful_response(response)
        body = response.get_json()
        assert body['id'] == cls['id']
        assert body['name'] == cls['name']
        assert body['link'] == cls['link']
        assert 'students' in body

        anon_client = client.__class__(client.client.application.test_client())
        response = anon_client.get(f'/for-teachers/class/{cls["id"]}', check=False)
        assert response.status_code == 401

        _clear_session(client)
        given.logged_in_as_new_student()
        response = client.get(f'/for-teachers/class/{cls["id"]}', check=False)
        assert response.status_code == 401

        _clear_session(client)
        given.logged_in_as_new_teacher()
        response = client.get('/for-teachers/class/doesnotexist', check=False)
        assert response.status_code == 404

        response = client.get(f'/for-teachers/class/{cls["id"]}', check=False)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /for-teachers/class/<class_id>
# ---------------------------------------------------------------------------

class TestDeleteClass:
    def test_delete_class_variants(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.delete(f'/for-teachers/class/{cls["id"]}')
        assert_useful_response(response)

        _clear_session(client)
        given.logged_in_as_new_teacher()
        response = client.delete('/for-teachers/class/doesnotexist', check=False)
        assert response.status_code == 404

        owner = given.a_teacher_account()
        cls = given.a_class(owner['username'])
        _clear_session(client)
        given.logged_in_as_new_teacher()
        response = client.delete(f'/for-teachers/class/{cls["id"]}', check=False)
        assert response.status_code == 401

        _clear_session(client)
        response = client.delete(f'/for-teachers/class/{cls["id"]}', check=False)
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /for-teachers/class/<class_id>/archive
# ---------------------------------------------------------------------------

class TestArchiveClass:
    def test_archive_class_variants(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post(f'/for-teachers/class/{cls["id"]}/archive')
        assert_useful_response(response)

        _clear_session(client)
        given.logged_in_as_new_teacher()
        response = client.post('/for-teachers/class/doesnotexist/archive', check=False)
        assert response.status_code == 404

        owner = given.a_teacher_account()
        cls = given.a_class(owner['username'])
        _clear_session(client)
        given.logged_in_as_new_teacher()
        response = client.post(f'/for-teachers/class/{cls["id"]}/archive', check=False)
        assert response.status_code == 401

        _clear_session(client)
        response = client.post(f'/for-teachers/class/{cls["id"]}/archive', check=False)
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /for-teachers/class/<class_id>/unarchive
# ---------------------------------------------------------------------------

class TestUnarchiveClass:
    def test_unarchive_class_variants(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        client.post(f'/for-teachers/class/{cls["id"]}/archive')
        response = client.post(f'/for-teachers/class/{cls["id"]}/unarchive')
        assert_useful_response(response)

        owner = given.a_teacher_account()
        cls = given.a_class(owner['username'])
        _clear_session(client)
        given.logged_in_as_new_teacher()
        response = client.post(f'/for-teachers/class/{cls["id"]}/unarchive', check=False)
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /for-teachers/redesign/class/<class_id>  (view-class)
# ---------------------------------------------------------------------------

class TestRedesignClassPages:
    def test_redesign_class_pages_variants(self, client: Client, given: Given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        cases = [
            (f'/for-teachers/redesign/class/{cls["id"]}', 200),
            (f'/for-teachers/redesign/class/{cls["id"]}/manage', 200),
            (f'/for-teachers/redesign/class/{cls["id"]}/configure', 200),
            (f'/for-teachers/redesign/class/{cls["id"]}/grade', 200),
            (f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1', 200),
            (f'/for-teachers/redesign/class/{cls["id"]}/customize-level/9999', 404),
        ]
        for url, expected in cases:
            response = client.get(url, check=False)
            assert response.status_code == expected

        owner = given.a_teacher_account()
        cls = given.a_class(owner['username'])
        _clear_session(client)
        given.logged_in_as_new_teacher()
        response = client.get(f'/for-teachers/redesign/class/{cls["id"]}', check=False)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /for-teachers/customize-levels/<class_id>
# ---------------------------------------------------------------------------

class TestCustomizeLevels:
    def test_customize_levels_variants(self, client, given):
        _clear_session(client)
        teacher = given.a_teacher_account()
        cls = given.a_class(teacher['username'])
        response = client.post_json(
            f'/for-teachers/customize-levels/{cls["id"]}',
            {'levels': ['1']},
            check=False
        )
        assert response.status_code == 401

        teacher = given.a_user_with_email()
        given.logged_in_as(teacher)
        cls = given.a_class(teacher['username'])
        _init_class_customizations(client, cls['id'])
        response = client.post_json(
            f'/for-teachers/customize-levels/{cls["id"]}',
            {'levels': ['1', '2', '3']}
        )
        assert_useful_response(response)
        assert 'success' in response.get_json()

        for body, expected in [(['1', '2'], 400), ({'levels': 'notalist'}, 400)]:
            response = client.post_json(f'/for-teachers/customize-levels/{cls["id"]}', body, check=False)
            assert response.status_code == expected


# ---------------------------------------------------------------------------
# POST /for-teachers/customize-class/<class_id>  (update_customizations)
# ---------------------------------------------------------------------------

class TestUpdateCustomizations:
    def test_update_customizations_variants(self, client, given):
        _clear_session(client)
        teacher = given.a_teacher_account()
        cls = given.a_class(teacher['username'])
        response = client.post_json(
            f'/for-teachers/customize-class/{cls["id"]}',
            {'levels': ['1'], 'other_settings': [], 'opening_dates': {}, 'level_thresholds': {}},
            check=False
        )
        assert response.status_code == 401

        teacher = given.a_user_with_email()
        given.logged_in_as(teacher)
        cls = given.a_class(teacher['username'])
        _init_class_customizations(client, cls['id'])
        response = client.post_json(
            f'/for-teachers/customize-class/{cls["id"]}',
            {
                'levels': ['1', '2'],
                'other_settings': [],
                'opening_dates': {},
                'level_thresholds': {},
            }
        )
        assert_useful_response(response)
        assert 'success' in response.get_json()

        response = client.post_json(
            f'/for-teachers/customize-class/{cls["id"]}',
            ['1', '2'],
            check=False
        )
        assert response.status_code == 400

        _clear_session(client)
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.get(f'/for-teachers/customize-class/{cls["id"]}')
        assert_useful_response(response)


# ---------------------------------------------------------------------------
# POST /for-teachers/redesign/class/<class_id>/manage/invite  (invite_users)
# ---------------------------------------------------------------------------

class TestInviteUsers:
    def test_invite_existing_student_succeeds(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        student = given.a_student_account()
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/manage/invite',
            data={'usernames': student['username']},
        )
        assert_useful_response(response)

    def test_invite_without_usernames_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/manage/invite',
            data={},
            check=False
        )
        assert response.status_code == 400

    def test_invite_anonymous_returns_401(self, client, given):
        teacher = given.a_teacher_account()
        cls = given.a_class(teacher['username'])
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/manage/invite',
            data={'usernames': 'someuser'},
            check=False
        )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /for-teachers/redesign/class/<class_id>/configure/invite
# ---------------------------------------------------------------------------

class TestInviteSecondTeacher:
    def test_invite_second_teacher_succeeds(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        second_teacher = given.a_teacher_account()
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/configure/invite',
            data={'usernames': second_teacher['username']},
        )
        assert_useful_response(response)

    def test_invite_second_teacher_without_usernames_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/configure/invite',
            data={},
            check=False
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# POST /for-teachers/create-accounts  (store_accounts)
# ---------------------------------------------------------------------------

class TestCreateAccounts:
    def test_create_accounts_with_auto_password_returns_accounts(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        u1, u2 = _unique_username(), _unique_username()
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': True,
                'accounts': f'{u1}\n{u2}',
            }
        )
        assert_useful_response(response)
        body = response.get_json()
        assert 'accounts' in body
        usernames = [a['username'] for a in body['accounts']]
        assert u1 in usernames
        assert u2 in usernames

    def test_create_accounts_with_passwords_returns_accounts(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        u1, u2 = _unique_username(), _unique_username()
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': False,
                'accounts': f'{u1};password1\n{u2};password2',
            }
        )
        assert_useful_response(response)
        body = response.get_json()
        assert 'accounts' in body
        assert len(body['accounts']) == 2

    def test_create_accounts_too_many_lines_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        prefix = uuid.uuid4().hex[:6]
        accounts_str = '\n'.join(f'stu{prefix}{i:03d}' for i in range(101))
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': True,
                'accounts': accounts_str,
            },
            check=False
        )
        assert response.status_code == 400

    def test_create_accounts_duplicate_usernames_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        u = _unique_username()
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': True,
                'accounts': f'{u}\n{u}',
            },
            check=False
        )
        assert response.status_code == 400

    def test_create_accounts_username_too_short_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': True,
                'accounts': 'ab',  # < 3 chars, always fails regardless of DB state
            },
            check=False
        )
        assert response.status_code == 400

    def test_create_accounts_invalid_class_returns_404(self, client, given):
        given.logged_in_as_new_teacher()
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': 'nonexistentclassid',
                'generate_passwords': True,
                'accounts': _unique_username(),
            },
            check=False
        )
        assert response.status_code == 404

    def test_create_accounts_not_dict_returns_400(self, client, given):
        given.logged_in_as_new_teacher()
        response = client.post_json(
            '/for-teachers/create-accounts',
            ['not', 'a', 'dict'],
            check=False
        )
        assert response.status_code == 400

    def test_create_accounts_anonymous_returns_401(self, client, given):
        teacher = given.a_teacher_account()
        cls = given.a_class(teacher['username'])
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': True,
                'accounts': _unique_username(),
            },
            check=False
        )
        assert response.status_code == 401

    def test_create_accounts_generate_passwords_username_with_separator_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': True,
                'accounts': 'bad;user',
            },
            check=False,
        )
        assert response.status_code == 400

    def test_create_accounts_generate_passwords_invalid_symbol_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': True,
                'accounts': 'bad@user',
            },
            check=False,
        )
        assert response.status_code == 400

    def test_create_accounts_manual_passwords_missing_separator_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': False,
                'accounts': 'noseparatorline',
            },
            check=False,
        )
        assert response.status_code == 400

    def test_create_accounts_manual_password_too_short_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post_json(
            '/for-teachers/create-accounts',
            {
                'class': cls['id'],
                'generate_passwords': False,
                'accounts': f'{_unique_username()};123',
            },
            check=False,
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# Teacher adventures (customize-adventure)
# ---------------------------------------------------------------------------

class TestCustomizeAdventure:
    def _valid_adventure_body(self, user, adventure_id):
        return {
            'id': adventure_id,
            'name': 'My Test Adventure',
            'levels': ['1'],
            'content': 'This is an adventure with more than twenty characters of content here.',
            'public': False,
            'language': 'en',
            'classes': [],
        }

    def test_create_and_get_adventure_page(self, client, given):
        given.logged_in_as_new_teacher()
        # The GET redirects to /customize-adventure/<id>?new_adventure=1 then renders 200.
        response = client.get('/for-teachers/customize-adventure', check=False)
        assert response.status_code == 302

    def test_update_adventure_success(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        adventure = given.some_saved_adventure(teacher['username'])
        body = self._valid_adventure_body(teacher, adventure['id'])
        response = client.post_json('/for-teachers/customize-adventure', body)
        assert_useful_response(response)
        resp_body = response.get_json()
        assert 'success' in resp_body

    def test_update_adventure_content_too_short_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        adventure = given.some_saved_adventure(teacher['username'])
        body = self._valid_adventure_body(teacher, adventure['id'])
        body['content'] = 'too short'  # < 20 chars
        response = client.post_json('/for-teachers/customize-adventure', body, check=False)
        assert response.status_code == 400

    def test_update_adventure_missing_levels_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        adventure = given.some_saved_adventure(teacher['username'])
        body = self._valid_adventure_body(teacher, adventure['id'])
        body['levels'] = []  # empty list → invalid
        response = client.post_json('/for-teachers/customize-adventure', body, check=False)
        assert response.status_code == 400

    def test_update_adventure_owned_by_other_teacher_returns_401(self, client, given):
        owner = given.a_teacher_account()
        adventure = given.some_saved_adventure(owner['username'])
        given.logged_in_as_new_teacher()  # different teacher
        body = self._valid_adventure_body(owner, adventure['id'])
        body['id'] = adventure['id']
        response = client.post_json('/for-teachers/customize-adventure', body, check=False)
        assert response.status_code == 401

    def test_update_adventure_anonymous_returns_401(self, client, given):
        teacher = given.a_teacher_account()
        adventure = given.some_saved_adventure(teacher['username'])
        body = self._valid_adventure_body(teacher, adventure['id'])
        response = client.post_json('/for-teachers/customize-adventure', body, check=False)
        assert response.status_code == 401

    def test_delete_adventure_success(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        adventure = given.some_saved_adventure(teacher['username'])
        response = client.delete(f'/for-teachers/customize-adventure/{adventure["id"]}')
        assert_useful_response(response)

    def test_delete_adventure_nonexistent_returns_404(self, client, given):
        given.logged_in_as_new_teacher()
        response = client.delete('/for-teachers/customize-adventure/doesnotexist', check=False)
        assert response.status_code == 404

    def test_delete_adventure_owned_by_other_teacher_returns_401(self, client, given):
        owner = given.a_teacher_account()
        adventure = given.some_saved_adventure(owner['username'])
        given.logged_in_as_new_teacher()  # different teacher
        response = client.delete(f'/for-teachers/customize-adventure/{adventure["id"]}', check=False)
        assert response.status_code == 401

    def test_delete_adventure_anonymous_returns_401(self, client, given):
        teacher = given.a_teacher_account()
        adventure = given.some_saved_adventure(teacher['username'])
        response = client.delete(f'/for-teachers/customize-adventure/{adventure["id"]}', check=False)
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# Additional route coverage for for_teachers.py
# ---------------------------------------------------------------------------

class TestAdditionalForTeachersCoverage:
    def test_for_teachers_redesign_page_teacher_returns_200(self, client, given, template_variables):
        given.logged_in_as_new_teacher()
        response = client.get('/for-teachers/redesign')
        assert_useful_response(response)
        context = template_variables[-1]
        assert context['current_page'] == 'for-teachers'
        assert context['javascript_page_options']['page'] == 'for-teachers'

    def test_for_teachers_redesign_page_anonymous_returns_401(self, client):
        response = client.get('/for-teachers/redesign', check=False)
        assert response.status_code == 401

    def test_grade_filter_sort_returns_200(self, client, given, template_variables):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.get(
            f'/for-teachers/redesign/class/{cls["id"]}/grade/filter_sort'
            '?filter_level=all&filter_student=all&filter_adventure=all&student=ascendent'
        )
        assert_useful_response(response)
        context = template_variables[-1]
        assert context['class_id'] == cls['id']
        assert context['class_info']['id'] == cls['id']
        assert 'student_adventures' in context

    def test_manage_filter_sort_returns_200(self, client, given, template_variables):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.get(
            f'/for-teachers/redesign/class/{cls["id"]}/manage/filter_sort?student=ascendent&timestamp=descendent'
        )
        assert_useful_response(response)
        context = template_variables[-1]
        assert context['class_info']['id'] == cls['id']
        assert 'students' in context

    def test_configure_class_returns_200_for_owner(self, client, given, template_variables):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.get(f'/for-teachers/redesign/class/{cls["id"]}/configure')
        assert_useful_response(response)
        context = template_variables[-1]
        assert context['class_info']['id'] == cls['id']
        assert context['javascript_page_options']['page'] == 'configure-class'

    def test_customize_level_availability_invalid_level_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/9999/availability',
            data={'enabled': 'true'},
            check=False,
        )
        assert response.status_code == 400

    def test_add_adventure_customize_level_missing_adventure_id_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/add-adventure',
            data={},
            check=False,
        )
        assert response.status_code == 400

    def test_remove_adventure_customize_level_missing_adventure_id_returns_400(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/remove-adventure',
            check=False,
        )
        assert response.status_code == 400

    def test_sort_adventures_customize_level_returns_200(self, client, given):
        teacher = given.a_user_with_email()
        given.logged_in_as(teacher)
        cls = given.a_class(teacher['username'])
        response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/sort-adventures',
            data={'adventure': []},
        )
        assert_useful_response(response)

    def test_remove_all_adventures_modal_returns_200(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.get(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/remove-all-adventures-modal'
        )
        assert_useful_response(response)

    def test_create_accounts_page_get_returns_200(self, client, given, template_variables):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        response = client.get(f'/for-teachers/create-accounts/{cls["id"]}')
        assert_useful_response(response)
        context = template_variables[-1]
        assert context['current_class']['id'] == cls['id']
        assert context['javascript_page_options']['page'] == 'create-accounts'

    def test_create_accounts_page_get_wrong_teacher_returns_401(self, client, given):
        owner = given.a_teacher_account()
        cls = given.a_class(owner['username'])
        given.logged_in_as_new_teacher()
        response = client.get(f'/for-teachers/create-accounts/{cls["id"]}', check=False)
        assert response.status_code == 401

    def test_parse_preview_adventure_success(self, client):
        response = client.post_json('/for-teachers/preview-adventure', {'code': 'print hello'})
        assert_useful_response(response)
        assert 'code' in response.get_json()

    def test_parse_preview_adventure_invalid_format_returns_400(self, client):
        response = client.post_json('/for-teachers/preview-adventure', {'code': '{'}, check=False)
        assert response.status_code == 400

    def test_clear_preview_class_redirects(self, client):
        response = client.get('/for-teachers/clear-preview-class', check=False)
        assert response.status_code == 302

    def test_create_adventure_without_class_returns_200(self, client, given):
        given.logged_in_as_new_teacher()
        response = client.post('/for-teachers/create-adventure/', check=False)
        assert_useful_response(response)
        assert response.data

    def test_create_adventure_with_class_and_level_returns_200(self, client, given):
        teacher = given.a_user_with_email()
        given.logged_in_as(teacher)
        cls = given.a_class(teacher['username'])
        response = client.post(f'/for-teachers/create-adventure/{cls["id"]}/1', check=False)
        assert_useful_response(response)
        assert response.data

    def test_customize_level_availability_enable_and_disable(self, client, given):
        teacher = given.a_user_with_email()
        given.logged_in_as(teacher)
        cls = given.a_class(teacher['username'])
        _init_class_customizations(client, cls['id'])

        enable_response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/availability',
            data={'enabled': 'true'},
        )
        assert_useful_response(enable_response)

        disable_response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/availability',
            data={'enabled': 'false'},
        )
        assert_useful_response(disable_response)

    def test_add_restore_remove_sort_adventures_customize_level_valid_paths(self, client, given):
        teacher = given.a_user_with_email()
        given.logged_in_as(teacher)
        cls = given.a_class(teacher['username'])
        _init_class_customizations(client, cls['id'])

        teacher_adventure = given.some_saved_adventure(teacher['username'], level='1')

        add_response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/add-adventure',
            data={'adventure_id': teacher_adventure['id']},
        )
        assert_useful_response(add_response)

        restore_response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/restore-default-adventures',
        )
        assert_useful_response(restore_response)

        default_adv = hedy_content.adventures_order_per_level()[1][0]
        remove_response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/remove-adventure?adventure_id={default_adv}',
        )
        assert_useful_response(remove_response)

        sort_response = client.post(
            f'/for-teachers/redesign/class/{cls["id"]}/customize-level/1/sort-adventures',
            data={'adventure': [default_adv]},
        )
        assert_useful_response(sort_response)


class TestLegacyCustomizeClassFlows:
    def _set_class_session(self, client, class_id):
        with client.client.session_transaction() as sess:
            sess['class_id'] = class_id

    def test_get_customization_level_partial_returns_200(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])
        _init_class_customizations(client, cls['id'])
        self._set_class_session(client, cls['id'])
        response = client.get('/for-teachers/get-customization-level?level=1')
        assert_useful_response(response)

    def test_add_sort_remove_adventure_legacy_endpoints(self, client, given):
        teacher = given.a_user_with_email()
        given.logged_in_as(teacher)
        cls = given.a_class(teacher['username'])
        _init_class_customizations(client, cls['id'])
        self._set_class_session(client, cls['id'])

        default_adv = hedy_content.adventures_order_per_level()[1][0]

        add_response = client.post('/for-teachers/add-adventure/level/1',
                                   data={'adventure_id': default_adv}, check=False)
        assert add_response.status_code == 200

        sort_response = client.post('/for-teachers/sort-adventures?level=1', data={'adventure': [default_adv]})
        assert_useful_response(sort_response)

        remove_response = client.post(f'/for-teachers/remove-adventure?adventure_id={default_adv}&level=1', check=False)
        assert remove_response.status_code == 200

    def test_restore_customizations_and_adventures_endpoints(self, client, given):
        teacher = given.a_user_with_email()
        given.logged_in_as(teacher)
        cls = given.a_class(teacher['username'])
        _init_class_customizations(client, cls['id'])
        self._set_class_session(client, cls['id'])

        restore_custom = client.post('/for-teachers/restore-customizations?level=1')
        assert_useful_response(restore_custom)

        restore_level = client.post('/for-teachers/restore-adventures/level/1')
        assert_useful_response(restore_level)

        restore_modal = client.get('/for-teachers/restore-adventures-modal/level/1')
        assert_useful_response(restore_modal)

    def test_update_content_endpoints(self, client, given):
        teacher = given.logged_in_as_new_teacher()
        cls = given.a_class(teacher['username'])

        response_old = client.post(f'/for-teachers/update-content/{cls["id"]}')
        assert_useful_response(response_old)

        response_new = client.post(f'/for-teachers/redesign/update-content/{cls["id"]}')
        assert_useful_response(response_new)


class TestForTeachersHelperMethods:
    class _FakeDB:
        def __init__(self):
            self.customizations = {}

        def get_class(self, class_id):
            return {'id': class_id, 'teacher': 'teacher1', 'name': 'Class 1', 'students': []}

        def get_teacher_adventures(self, _username):
            return [{'id': 'adv_teacher', 'name': 'Teacher Adventure', 'level': '1', 'levels': ['1']}]

        def get_second_teacher_adventures(self, _classes, _username):
            return []

        def get_class_customizations(self, class_id):
            return self.customizations.get(class_id)

        def update_class_customizations(self, customizations):
            self.customizations[customizations['id']] = customizations

        def get_teacher_classes(self, _username, _include_archived):
            return [
                {'id': 'c1', 'date': 0, 'teacher': 'teacher1', 'name': 'C1', 'archived': False},
                {'id': 'c2', 'date': 0, 'teacher': 'teacher1', 'name': 'C2', 'archived': True},
            ]

        def get_survey(self, survey_id):
            return None

        def store_survey(self, survey):
            self._survey = survey

        def add_survey_responses(self, _survey_id, _translate_db):
            return None

    class _FakeAuth:
        def logout(self):
            return None

    def _module(self):
        return for_teachers_module.ForTeachersModule(self._FakeDB(), self._FakeAuth())

    def test_split_teacher_classes_by_archive_state(self, app):
        classes = [
            {'id': 'a', 'date': 1700000000000, 'archived': False},
            {'id': 'b', 'date': 1700000000000, 'archived': True},
        ]
        with app.test_request_context('/'):
            active, archived = for_teachers_module.ForTeachersModule._split_teacher_classes_by_archive_state(classes)
        assert len(active) == 1
        assert len(archived) == 1

    def test_normalize_manage_class_sort_timestamp(self):
        mod = self._module()
        assert mod._normalize_manage_class_sort_timestamp(None) == float('-inf')
        assert isinstance(mod._normalize_manage_class_sort_timestamp(1), int)
        assert mod._normalize_manage_class_sort_timestamp(10_000_000_001) > 1

    def test_filter_and_sort_student_adventures(self):
        mod = self._module()
        data = {
            'x': {'student': 'alice', 'adventure_name': 'adv1', 'level': '1', 'name': 'A', 'timestamp': 1, 'ticked': False},
            'y': {'student': 'bob', 'adventure_name': 'adv2', 'level': '1', 'name': 'B', 'timestamp': 2, 'ticked': True},
        }
        filtered = mod.filter_student_adventures(data, 'alice', 'all')
        assert list(filtered.keys()) == ['x']
        sorted_data = mod.sort_student_adventures(data, {'student': True})
        assert list(sorted_data.keys())[0] in ('x', 'y')

    def test_extract_account_info(self):
        lines = ['user1;password1', 'invalidrow', 'user2;pass2']
        correct, incorrect = for_teachers_module.ForTeachersModule._extract_account_info(lines, ';')
        assert ('user1', 'password1') in correct
        assert 'invalidrow' in incorrect

    def test_has_placeholder_and_is_adventure_from_teacher(self):
        mod = self._module()
        assert mod.has_placeholder('print _') is True
        assert mod.has_placeholder('print 1') is False
        assert mod.is_adventure_from_teacher('adv1', [{'id': 'adv1'}]) is True
        assert mod.is_adventure_from_teacher('advX', [{'id': 'adv1'}]) is False

    def test_purge_customizations_removes_unknown_adventures(self):
        mod = self._module()
        sorted_adventures = {'1': [{'name': 'missing', 'from_teacher': False}, {'name': 'keep', 'from_teacher': False}]}
        mod.purge_customizations(sorted_adventures, {'keep': {}}, [{'id': 'teacher_keep'}])
        assert {'name': 'missing', 'from_teacher': False} not in sorted_adventures['1']

    def test_get_unused_adventures_returns_per_level_map(self, app):
        mod = self._module()
        adventures = {i: [] for i in range(1, 1 + hedy_content.MAX_LEVEL if hasattr(hedy_content, 'MAX_LEVEL') else 19)}
        # Use hedy max level from runtime constants used by module
        import hedy
        adventures = {i: [] for i in range(1, hedy.HEDY_MAX_LEVEL + 1)}
        with app.test_request_context('/'):
            g.lang = 'en'
            g.keyword_lang = 'en'
            names = {k: k for level in hedy_content.adventures_order_per_level().values() for k in level}
            available = mod.get_unused_adventures(adventures, [], names)
        assert 1 in available

    def test_get_class_info_creates_default_customizations(self, app):
        mod = self._module()
        user = {'username': 'teacher1'}
        with app.test_request_context('/'):
            g.lang = 'en'
            g.keyword_lang = 'en'
            customizations, adventures, adventure_names, available_adventures, min_level = mod.get_class_info(
                user, 'class123', migrate_customizations=True
            )
        assert customizations['id'] == 'class123'
        assert isinstance(adventures, dict)
        assert isinstance(adventure_names, dict)
        assert isinstance(available_adventures, dict)
        assert min_level >= 1

    def test_get_customizations_and_create_customizations_helpers(self):
        class Db:
            def __init__(self):
                self.c = {}

            def get_class_customizations(self, cid):
                return self.c.get(cid)

            def update_class_customizations(self, custom):
                self.c[custom['id']] = custom

        db = Db()
        custom = for_teachers_module.get_customizations(db, 'cid1')
        assert custom['id'] == 'cid1'
        custom2 = for_teachers_module._create_customizations(db, 'cid2', include_adventures=False)
        assert custom2['id'] == 'cid2'
        out = for_teachers_module._set_customizations_content_version(custom2, 'vX')
        assert out['content_version'] == 'vX'

    def test_render_why_class(self):
        text = for_teachers_module.render_why_class({'why_class': 'Class A', 'creator': 'teacher'})
        assert isinstance(text, str)


class TestForTeachersHeavyInternalMethods:
    class _Result(list):
        next_page_token = None

    class _RichFakeDB:
        def __init__(self):
            self.class_id = 'cid'
            self.class_data = {
                'id': self.class_id,
                'name': 'Class One',
                'teacher': 'teacher1',
                'students': ['student1'],
                'link': 'abcde',
                'last_viewed_level': 1,
                'second_teachers': [],
            }
            self.program = {
                'id': 'prog1',
                'level': 1,
                'adventure_name': 'default',
                'is_modified': True,
                'submitted': True,
                'code': 'print 1',
                'date': 1700000000000,
                'name': 'Program 1',
                'public': True,
            }
            self.customizations = {
                self.class_id: {
                    'id': self.class_id,
                    'levels': [1],
                    'opening_dates': {},
                    'other_settings': [],
                    'level_thresholds': {},
                    'sorted_adventures': {'1': [{'name': 'default', 'from_teacher': False}]},
                    'dashboard_customization': {'selected_levels': [1]},
                }
            }
            self.student_adventures = {}
            self.adventures = {
                'adv1': {
                    'id': 'adv1',
                    'creator': 'teacher1',
                    'name': 'Adventure One',
                    'content': '<pre>print 1</pre>',
                    'level': 1,
                    'levels': ['1'],
                    'classes': ['cid'],
                    'tags': [],
                }
            }
            self.surveys = {}

        def get_class(self, class_id):
            return self.class_data if class_id == self.class_id else None

        def get_teacher_adventures(self, _username):
            return [{
                'id': 'tadv',
                'name': 'Teacher Adventure',
                'content': '<pre>print 1</pre>',
                'level': '1',
                'levels': ['1'],
                'date': 1700000000000,
                'creator': 'teacher1',
                'author': 'teacher1',
            }]

        def get_second_teacher_adventures(self, _classes, _username):
            return []

        def get_class_customizations(self, class_id):
            return self.customizations.get(class_id)

        def update_class_customizations(self, customizations):
            self.customizations[customizations['id']] = customizations

        def user_by_username(self, username):
            return {'username': username, 'last_login': 1700000000000}

        def get_quiz_stats(self, _students):
            return [{'level': 1, 'finished': True}]

        def last_level_programs_for_user(self, _student, _level):
            return {'prog1': dict(self.program)}

        def get_program_stats_per_level(self, _student, _level):
            return [{'successful_runs': 2, 'SomeException': 1}]

        def student_adventure_by_id(self, adventure_id):
            return self.student_adventures.get(adventure_id)

        def store_student_adventure(self, adventure):
            self.student_adventures[adventure['id']] = adventure
            return adventure

        def update_student_adventure(self, adventure_id, ticked):
            if adventure_id in self.student_adventures:
                self.student_adventures[adventure_id]['ticked'] = not ticked

        def last_programs_for_user_all_levels(self, _student):
            return {1: {'prog1': dict(self.program)}}

        def level_programs_for_user(self, _student, _level):
            return [dict(self.program)]

        def programs_for_user(self, _student):
            return [dict(self.program)]

        def filtered_programs_for_user(self, _from_user, **_kwargs):
            return TestForTeachersHeavyInternalMethods._Result([dict(self.program)])

        def get_public_profile_settings(self, _username):
            return {}

        def get_class_invites(self, class_id=None):
            return []

        def get_teacher_classes(self, _username, _include_archived):
            return [self.class_data]

        def get_adventure(self, adventure_id):
            return self.adventures.get(adventure_id)

        def update_adventure(self, adventure_id, adventure):
            current = dict(self.adventures.get(adventure_id, {}))
            current.update(adventure)
            current['id'] = adventure_id
            self.adventures[adventure_id] = current

        def read_tags(self, _tags):
            return []

        def update_tag(self, _tag_id, _tag):
            return None

        def delete_adventure(self, adventure_id):
            self.adventures.pop(adventure_id, None)

        def store_adventure(self, adventure):
            self.adventures[adventure['id']] = adventure
            return adventure

        def get_survey(self, survey_id):
            return self.surveys.get(survey_id)

        def store_survey(self, survey):
            self.surveys[survey['id']] = survey

        def add_survey_responses(self, _survey_id, _translate_db):
            return None

        def remove_user_class_invite(self, _student_id, _class_id):
            return None

        def remove_student_from_class(self, _class_id, student_id):
            if student_id in self.class_data['students']:
                self.class_data['students'].remove(student_id)

        def update_last_viewed_level_in_class(self, _class_id, _level):
            return None

    class _FakeAuth:
        def logout(self):
            return None

    def _module(self):
        return for_teachers_module.ForTeachersModule(self._RichFakeDB(), self._FakeAuth())

    @pytest.fixture()
    def mod(self):
        return self._module()

    def test_get_grid_info_and_build_student_adventures(self, app):
        mod = self._module()
        user = {'username': 'teacher1'}
        with app.test_request_context('/'):
            g.lang = 'en'
            g.keyword_lang = 'en'
            students, _class, class_adv, adv_names, student_adv, graph_students, students_info = mod.get_grid_info(
                user, 'cid', 1
            )
            built = mod.build_student_adventures(_class, user, [1])
        assert students == ['student1']
        assert _class['id'] == 'cid'
        assert isinstance(class_adv, dict)
        assert isinstance(adv_names, dict)
        assert isinstance(student_adv, dict)
        assert isinstance(graph_students, list)
        assert isinstance(students_info, dict)
        assert isinstance(built, dict)

    def test_build_student_adventures_executes_inner_program_path(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1'}

        monkeypatch.setattr(
            mod,
            'get_class_information',
            lambda _class, _user: (
                ['student1'],
                {'1': [{'name': 'Localized Default', 'id': 'default'}]},
                {'default': 'Localized Default'},
            ),
        )

        with app.test_request_context('/'):
            g.lang = 'en'
            g.keyword_lang = 'en'
            built = mod.build_student_adventures(mod.db.class_data, user, [1])

        assert isinstance(built, dict)
        assert built

    def test_check_adventure_and_change_checkbox(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1'}
        monkeypatch.setattr(for_teachers_module.jinja_partials, 'render_partial', lambda *args, **kwargs: {'ok': True})
        check_adventure = _unwrap_route(for_teachers_module.ForTeachersModule.check_adventure)
        change_checkbox = _unwrap_route(for_teachers_module.ForTeachersModule.change_checkbox)
        with app.test_request_context('/?level=1&student_name=student1&adventure_name=default&program_id=prog1'):
            _set_en_locale()
            response = check_adventure(mod, user)
        assert_useful_response(response)

        with app.test_request_context('/?level=1&student=student1&adventure=default'):
            _set_en_locale()
            result = change_checkbox(mod, user, 'cid')
        assert result == {'ok': True}

    def test_remove_student_modals_and_removal(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1', 'is_teacher': 1}
        monkeypatch.setattr(for_teachers_module, 'render_partial', lambda *args, **kwargs: {'ok': True})
        monkeypatch.setattr(for_teachers_module.jinja_partials, 'render_partial', lambda *args, **kwargs: {'ok': True})
        get_remove_modal = _unwrap_route(for_teachers_module.ForTeachersModule.get_remove_student_modal)
        get_remove_modal_redesign = _unwrap_route(
            for_teachers_module.ForTeachersModule.get_remove_student_modal_redesign)
        remove_redesign = _unwrap_route(for_teachers_module.ForTeachersModule.remove_student_from_class_redesign)
        with app.test_request_context('/?level=1'):
            _set_en_locale()
            session['class_id'] = 'cid'
            modal = get_remove_modal(mod, user, 'cid', 'student1')
        assert modal == {'ok': True}

        with app.test_request_context('/?is_invite=0'):
            _set_en_locale()
            modal2 = get_remove_modal_redesign(mod, user, 'cid', 'student1')
            table = remove_redesign(mod, user, 'cid', 'student1')
        assert modal2 == {'ok': True}
        assert table == {'ok': True}

    def test_show_students_programs_endpoints(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1'}
        monkeypatch.setattr(for_teachers_module.jinja_partials, 'render_partial', lambda *args, **kwargs: {'ok': True})
        perf_graph = _unwrap_route(for_teachers_module.ForTeachersModule.show_students_programs_performance_graph)
        show_programs = _unwrap_route(for_teachers_module.ForTeachersModule.show_students_programs)
        with app.test_request_context('/?usernames=student1&level=1'):
            _set_en_locale()
            r1 = perf_graph(mod, user)
        with app.test_request_context('/'):
            _set_en_locale()
            r2 = show_programs(mod, user, 'student1')
        assert r1 == {'ok': True}
        assert r2 == {'ok': True}

    def test_preview_class_as_teacher_redirects(self, app):
        mod = self._module()
        user = {'username': 'teacher1', 'is_teacher': 1}
        preview = _unwrap_route(for_teachers_module.ForTeachersModule.preview_class_as_teacher)
        with app.test_request_context('/?level=1'):
            _set_en_locale()
            response = preview(mod, user, 'cid')
        assert response.status_code == 302

    def test_is_program_modified_paths(self, app):
        mod = self._module()
        with app.test_request_context('/'):
            g.lang = 'en'
            g.keyword_lang = 'en'
            program_same = {
                'adventure_name': 'default',
                'level': 1,
                'code': 'print 1',
            }
            full_adventures = {
                'default': {
                    'levels': {
                        1: {'example_code': '```\nprint 1\n```'}
                    }
                }
            }
            same_result = mod.is_program_modified(program_same, full_adventures, [])

            program_changed = dict(program_same)
            program_changed['code'] = 'print 2'
            changed_result = mod.is_program_modified(program_changed, full_adventures, [])

        assert same_result is False
        assert changed_result is True

    def test_get_adventure_info_and_view_adventure(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1', 'is_teacher': 1}
        get_adv_info = _unwrap_route(for_teachers_module.ForTeachersModule.get_adventure_info)
        view_adv = _unwrap_route(for_teachers_module.ForTeachersModule.view_adventure)
        monkeypatch.setattr(for_teachers_module, 'render_template', lambda *args, **kwargs: {'ok': True})
        with app.test_request_context('/'):
            _set_en_locale()
            info = get_adv_info(mod, user, 'adv1')
            view = view_adv(mod, user, 'adv1')
        assert info == {'ok': True}
        assert view == {'ok': True}

    def test_get_adventure_info_not_found_returns_404(self, app):
        mod = self._module()
        user = {'username': 'teacher1', 'is_teacher': 1}
        get_adv_info = _unwrap_route(for_teachers_module.ForTeachersModule.get_adventure_info)
        with app.test_request_context('/'):
            _set_en_locale()
            response = get_adv_info(mod, user, 'missing')
        assert response[1] == 404

    def test_update_and_delete_adventure_internal_paths(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1', 'email': 'teacher@example.com'}
        update_adv = _unwrap_route(for_teachers_module.ForTeachersModule.update_adventure)
        delete_adv = _unwrap_route(for_teachers_module.ForTeachersModule.delete_adventure)
        monkeypatch.setattr(mod, 'add_adventure_to_class_level', lambda *args, **kwargs: None)
        monkeypatch.setattr(for_teachers_module, 'render_partial', lambda *args, **kwargs: {'ok': True})

        body = {
            'id': 'adv1',
            'name': 'Adventure One',
            'levels': ['1'],
            'content': 'This adventure content is long enough to pass validation.',
            'public': False,
            'language': 'en',
            'classes': ['cid'],
            'formatted_solution_code': 'print 1',
        }

        with app.test_request_context('/', json=body):
            _set_en_locale()
            update_response = update_adv(mod, user)
        assert_useful_response(update_response)

        with app.test_request_context('/'):
            _set_en_locale()
            delete_response = delete_adv(mod, user, 'adv1')
        assert delete_response == {'ok': True}

    def test_update_adventure_invalid_types_return_400(self, app):
        mod = self._module()
        update_adv = _unwrap_route(for_teachers_module.ForTeachersModule.update_adventure)
        user = {'username': 'teacher1'}

        invalid_cases = [
            {'id': 1, 'name': 'n', 'levels': ['1'], 'content': 'x' *
                30, 'public': False, 'language': 'en', 'classes': []},
            {'id': 'adv1', 'name': 1, 'levels': ['1'], 'content': 'x' *
                30, 'public': False, 'language': 'en', 'classes': []},
            {'id': 'adv1', 'name': 'n', 'levels': [], 'content': 'x' * 30, 'public': False, 'language': 'en', 'classes': []},
            {'id': 'adv1', 'name': 'n', 'levels': ['1'], 'content': 1,
                'public': False, 'language': 'en', 'classes': []},
            {'id': 'adv1', 'name': 'n', 'levels': ['1'], 'content': 'x' *
                30, 'public': 'no', 'language': 'en', 'classes': []},
        ]

        for body in invalid_cases:
            with app.test_request_context('/', json=body):
                _set_en_locale()
                response = update_adv(mod, user)
                assert response.status_code == 400

    def test_update_adventure_new_adventure_from_session_and_language_fallback(self, app, monkeypatch):
        mod = self._module()
        update_adv = _unwrap_route(for_teachers_module.ForTeachersModule.update_adventure)
        user = {'username': 'teacher1', 'email': 'teacher@example.com'}

        monkeypatch.setattr(mod, 'add_adventure_to_class_level', lambda *args, **kwargs: None)

        body = {
            'id': 'adv_new',
            'name': 'Adventure Session',
            'levels': ['1'],
            'content': 'This adventure content is long enough to pass validation.',
            'public': True,
            'language': 'zz',
            'classes': ['cid'],
            'formatted_solution_code': 'print 1',
        }

        with app.test_request_context('/', json=body):
            _set_en_locale()
            session['new_adventure'] = {
                'id': 'adv_new',
                'creator': 'teacher1',
                'classes': ['cid'],
                'levels': ['1'],
                'tags': [],
            }
            response = update_adv(mod, user)
        assert_useful_response(response)

    def test_get_adventure_info_invalid_adventure_id_types(self, app):
        mod = self._module()
        get_adv_info = _unwrap_route(for_teachers_module.ForTeachersModule.get_adventure_info)
        user = {'username': 'teacher1', 'is_teacher': 1}

        with app.test_request_context('/'):
            _set_en_locale()
            response_none = get_adv_info(mod, user, None)
            response_type = get_adv_info(mod, user, 123)

        assert response_none.status_code == 400
        assert response_type.status_code == 400

    def test_leave_class_and_change_dropdown_level(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1'}
        leave = _unwrap_route(for_teachers_module.ForTeachersModule.leave_class)
        change_level = _unwrap_route(for_teachers_module.ForTeachersModule.change_dropdown_level_class_overview)
        monkeypatch.setattr(for_teachers_module.jinja_partials, 'render_partial', lambda *args, **kwargs: {'ok': True})

        with app.test_request_context('/?level=1'):
            _set_en_locale()
            left = leave(mod, user, 'cid', 'student1')
        assert left == {'ok': True}

        with app.test_request_context('/?level=1'):
            _set_en_locale()
            changed = change_level(mod, user, 'cid')
        assert changed == {'ok': True}

    def test_public_programs_internal_success(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1'}
        public_programs = _unwrap_route(for_teachers_module.ForTeachersModule.public_programs)
        monkeypatch.setattr(for_teachers_module, 'render_template', lambda *args, **kwargs: {'ok': True})
        with app.test_request_context('/?level=1&filter=submitted'):
            _set_en_locale()
            session['class_id'] = 'cid'
            result = public_programs(mod, user, 'cid', 'student1')
        assert result == {'ok': True}

    def test_get_workbooks_covers_all_exercise_types(self, app, monkeypatch):
        mod = self._module()
        get_workbooks = _unwrap_route(for_teachers_module.ForTeachersModule.get_workbooks)

        class FakeWorkbooks:
            def get_workbook_for_level(self, level, lang):
                return {
                    'exercises': [
                        'new-page',
                        {'type': 'output', 'answer': 'a\nb'},
                        {'type': 'circle', 'goal': 'goal'},
                        {'type': 'input', 'answer': 'a\nb', 'output': 'o1\no2'},
                        {'type': 'MC-code'},
                        {'type': 'define', 'word': 'w', 'lines': '2'},
                        {'type': 'question', 'lines': '1'},
                    ]
                }

        monkeypatch.setitem(for_teachers_module.WORKBOOKS, 'en', FakeWorkbooks())
        monkeypatch.setattr(for_teachers_module, 'render_template', lambda *args, **kwargs: {'ok': True})

        with app.test_request_context('/'):
            _set_en_locale()
            result = get_workbooks(mod, '1')
        assert result == {'ok': True}

    def test_get_teacher_classes_after_class_update_retry_paths(self):
        mod = self._module()

        class RetryDB:
            def __init__(self):
                self.calls = 0

            def get_teacher_classes(self, username, include_archived):
                self.calls += 1
                if self.calls < 2:
                    return []
                return [{'id': 'cid', 'archived': True}]

        mod.db = RetryDB()
        classes = mod._get_teacher_classes_after_class_update(
            'teacher1',
            'cid',
            expected_archived=True,
            should_exist=True,
            max_retries=2,
            retry_delay_s=0,
        )
        assert classes

    def test_class_survey_and_load_survey(self, app, monkeypatch):
        mod = self._module()
        monkeypatch.setattr(for_teachers_module.utils, 'get_unanswered_questions',
                            lambda survey, questions: (questions, {'q': 'a'}))
        monkeypatch.setattr(for_teachers_module, 'render_partial', lambda *args, **kwargs: {'ok': True})
        with app.test_request_context('/'):
            _set_en_locale()
            survey = mod.class_survey('cid')
            rendered = mod.load_survey('cid')
        assert survey
        assert rendered == {'ok': True}

    def test_update_adventure_validation_edge_cases(self, app):
        mod = self._module()
        update_adv = _unwrap_route(for_teachers_module.ForTeachersModule.update_adventure)
        user = {'username': 'teacher1'}

        with app.test_request_context('/', json=['not-a-dict']):
            _set_en_locale()
            r1 = update_adv(mod, user)
        assert r1.status_code == 400

        bad = {
            'id': 'adv1',
            'name': 'Adventure One',
            'levels': ['1'],
            'content': 'This adventure content is long enough to pass validation.',
            'public': False,
            'language': 'xx',
            'classes': [],
            'formatted_content': 123,
        }
        with app.test_request_context('/', json=bad):
            _set_en_locale()
            r2 = update_adv(mod, user)
        assert r2.status_code == 400

    def test_add_adventure_to_class_level_add_and_remove(self, app, monkeypatch):
        mod = self._module()
        user = {'username': 'teacher1', 'email': 'teacher@example.com'}
        monkeypatch.setattr(for_teachers_module, 'add_class_customized_to_subscription', lambda _email: None)
        with app.test_request_context('/'):
            _set_en_locale()
            mod.add_adventure_to_class_level(user, 'cid', 'new_adv', '1', False)
            mod.add_adventure_to_class_level(user, 'cid', 'new_adv', '1', True)

        custom = mod.db.get_class_customizations('cid')
        assert isinstance(custom, dict)
