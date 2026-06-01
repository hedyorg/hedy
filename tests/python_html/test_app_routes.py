"""Tests for main app.py routes and functions."""
import json
import uuid
import pytest
import app as hedy_app
from tests.python_html.fixtures.flask import Client


@pytest.fixture()
def client(app):
    return Client(app.test_client())


def assert_html_response(response):
    assert response.status_code == 200
    assert response.mimetype == 'text/html'
    assert response.get_data(as_text=True).strip() != ''


def last_template_context(template_variables):
    assert template_variables
    return template_variables[-1]


class TestMainPageRoute:
    """Test the main landing page route."""

    def test_main_page_loads(self, client, template_variables):
        """Test GET /."""
        response = client.get('/')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'start'
        assert context['page_title'] == 'Hedy - Textual programming made easy'

    def test_main_page_with_locale(self, client, template_variables):
        """Test main page with locale parameter."""
        response = client.get('/?language=nl')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'start'
        assert context['page_title'] == 'Hedy - Een graduele programmeertaal'


class TestHedyEditorRoute:
    """Test the Hedy code editor route."""

    def test_hedy_level_1(self, client, template_variables):
        """Test GET /hedy/1 (level 1 editor)."""
        response = client.get('/hedy/1')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'hedy'
        assert context['level'] == 1

    def test_hedy_level_with_adventure(self, client, template_variables):
        """Test GET /hedy/1 with adventure parameter."""
        response = client.get('/hedy/1?adventure=intro')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'hedy'
        assert context['javascript_page_options']['page'] == 'code'

    def test_hedy_level_high_returns_no_such_level_message(self, client):
        """Test out-of-range level returns a meaningful 404 page."""
        response = client.get('/hedy/25', check=False)
        assert response.status_code == 404
        assert response.mimetype == 'text/html'
        body = response.get_data(as_text=True)
        assert body.strip() != ''
        assert '<html' in body.lower()


class TestAuthRoutes:
    """Test authentication-related routes."""

    def test_programs_api_save_requires_login(self, client):
        """Saving a program via /programs/ requires authentication."""
        response = client.post_json(
            '/programs/',
            {'code': 'print Hello', 'name': 'My Program', 'level': 1},
            check=False,
        )
        assert response.status_code == 401

    def test_get_program_no_auth(self, client):
        """Test retrieving a program without authentication."""
        response = client.get('/get_saved_program/test', check=False)
        assert response.status_code == 404

    def test_programs_api_delete_requires_login(self, client):
        """Deleting a program via /programs/delete/ requires authentication."""
        response = client.post_json('/programs/delete/', {'id': 'someid'}, check=False)
        assert response.status_code == 401


class TestHeadersAndErrorHandling:
    """Test error handling and header validation."""

    def test_nonexistent_page(self, client):
        """Test accessing a non-existent page."""
        response = client.get('/nonexistent_page', check=False)
        assert response.status_code == 404
        assert response.mimetype == 'text/html'
        assert response.get_data(as_text=True).strip() != ''

    def test_static_css(self, client):
        """Test accessing static CSS files."""
        response = client.get('/static/css/definitely-missing.css', check=False)
        assert response.status_code == 404
        assert response.get_data(as_text=True).strip() != ''

    def test_static_js(self, client):
        """Test accessing static JS files."""
        response = client.get('/static/js/definitely-missing.js', check=False)
        assert response.status_code == 404
        assert response.get_data(as_text=True).strip() != ''

    def test_update_yaml_endpoint_removed_returns_404(self, client):
        """The legacy update_yaml route was removed and should not be routable."""
        response = client.post('/update_yaml', data={'file': 'foo.yaml'}, check=False)
        assert response.status_code in (404, 405)


class TestPublicPages:
    """Test public-facing pages."""

    def test_privacy_page(self, client, template_variables):
        """Test GET /privacy."""
        response = client.get('/privacy')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['page_title']
        assert 'content' in context

    def test_about_page(self, client):
        """Test GET /about."""
        response = client.get('/about', check=False)
        assert response.status_code == 404

    def test_join_page(self, client, template_variables):
        """Test GET /join."""
        response = client.get('/join')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'join'
        assert context['content']


class TestLanguageRoutes:
    """Test language switching and locale handling."""

    def test_switch_language_nl(self, client):
        """Test switching to Dutch language."""
        response = client.get('/nl', check=False)
        assert response.status_code == 404

    def test_switch_language_en(self, client):
        """Test switching to English language."""
        response = client.get('/en', check=False)
        assert response.status_code == 404


class TestLevelRoutes:
    """Test level-specific routes."""

    def test_level_1(self, client, template_variables):
        """Test GET /1 (level 1)."""
        response = client.get('/1', check=False)
        assert response.status_code == 404

    def test_level_5(self, client, template_variables):
        """Test GET /5 (level 5)."""
        response = client.get('/5', check=False)
        assert response.status_code == 404

    def test_level_out_of_range(self, client):
        """Test accessing an out-of-range level."""
        response = client.get('/999', check=False)
        assert response.status_code == 404


class TestAjaxRoutes:
    """Test AJAX endpoints."""

    def test_translate_keywords_missing_fields_returns_400(self, client):
        """translate_keywords returns 400 for malformed request data."""
        response = client.post(
            '/translate_keywords',
            data=json.dumps({'keywords': ['print'], 'lang': 'nl'}),
            content_type='application/json',
            check=False,
        )
        assert response.status_code == 400
        assert response.get_data(as_text=True).strip() != ''

class TestErrorTracking:
    """Test error logging and tracking endpoints."""

    def test_error_list_route(self, client):
        """Test accessing error list (may not exist in all configs)."""
        response = client.get('/list', check=False)
        assert response.status_code == 404

    def test_programs_api_delete_missing_id_returns_400(self, client, given):
        """Deleting a program without id returns validation error."""
        given.logged_in_as_new_teacher()
        response = client.post_json('/programs/delete/', {}, check=False)
        assert response.status_code == 400


class TestParseEndpoint:
    """Test code parsing endpoints."""

    def test_parse_simple_code(self, client):
        """Test basic code parsing with a complete payload."""
        response = client.post(
            '/parse',
            data=json.dumps({'code': 'print Hello', 'level': 1, 'is_debug': False, 'raw': False}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert 'Code' in data

    def test_parse_by_id(self, client, given):
        """Test parsing code by ID."""
        # Create a program first and login as teacher
        teacher = given.logged_in_as_new_teacher()
        program = given.some_saved_program(teacher['username'], name='test_parse', code='print "hello"', level=1)

        response = client.post(
            '/parse-by-id',
            data=json.dumps({'id': program['id']}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 204

    def test_parse_by_id_not_logged_in_returns_401(self, client):
        """Test /parse-by-id returns 401 when user is not logged in."""
        response = client.post(
            '/parse-by-id',
            data=json.dumps({'id': 'program-id'}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 401

    def test_parse_by_id_invalid_body_type_returns_400(self, client, given):
        """Test /parse-by-id body validation for non-object JSON."""
        given.logged_in_as_new_teacher()
        response = client.post(
            '/parse-by-id',
            data=json.dumps(['not-an-object']),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 400

    def test_parse_by_id_missing_id_returns_400(self, client, given):
        """Test /parse-by-id validation when id is missing."""
        given.logged_in_as_new_teacher()
        response = client.post(
            '/parse-by-id',
            data=json.dumps({}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 400


class TestMachineAndMicrobitFiles:
    """Test machine and microbit file generation routes."""

    def test_generate_machine_files(self, client):
        """Test generating machine files."""
        # Test with minimal valid request
        response = client.post(
            '/generate_machine_files',
            data=json.dumps({'code': 'print "hello"', 'level': 1, 'lang': 'en'}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 200
        assert 'filename' in response.get_json()

    def test_generate_microbit_files(self, client):
        """Test generating microbit files."""
        # MICROBIT_FEATURE is false by default
        response = client.post(
            '/generate_microbit_files',
            data=json.dumps({'code': 'print "hello"', 'level': 1, 'lang': 'en'}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 403
        assert response.get_json()['message']

    def test_generate_microbit_files_feature_enabled_returns_200(self, client, monkeypatch):
        """When enabled, generate_microbit_files returns a success payload."""
        monkeypatch.setattr(hedy_app, 'MICROBIT_FEATURE', True)
        monkeypatch.setattr(hedy_app.hedy, 'transpile_and_return_python', lambda code, level: 'print("ok")')
        monkeypatch.setattr(hedy_app, 'save_transpiled_code_for_microbit', lambda transpiled: None)

        response = client.post(
            '/generate_microbit_files',
            data=json.dumps({'code': 'print "hello"', 'level': 1}),
            content_type='application/json',
            check=False,
        )
        assert response.status_code == 200
        body = response.get_json()
        assert body['microbit'] is True
        assert body['filename'] == 'Micro-bit.py'

    def test_download_microbit_files_feature_enabled_returns_200(self, client, monkeypatch):
        """When enabled, download_microbit_files responds successfully."""
        monkeypatch.setattr(hedy_app, 'MICROBIT_FEATURE', True)
        monkeypatch.setattr(hedy_app, 'flash_micro_bit', lambda: None)
        monkeypatch.setattr(
            hedy_app,
            'send_file',
            lambda *args, **kwargs: hedy_app.make_response({'download': 'ok'}, 200),
        )

        response = client.get('/download_microbit_files/', check=False)
        assert response.status_code == 200
        assert response.get_json()['download'] == 'ok'

    def test_download_microbit_files(self, client):
        """Test downloading microbit files."""
        response = client.get('/download_microbit_files/test', check=False)
        assert response.status_code == 404


class TestErrorReporting:
    """Test error reporting endpoints."""

    def test_report_error(self, client):
        """Test reporting a parse error."""
        response = client.post(
            '/report_error',
            data=json.dumps({'message': 'test error', 'level': 1}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'logged'

    def test_client_exception(self, client):
        """Test client-side exception reporting."""
        response = client.post(
            '/client_exception',
            data=json.dumps({'message': 'client error'}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 500
        assert response.get_data(as_text=True) == 'logged'


class TestVersion:
    """Test version endpoint."""

    def test_version_endpoint(self, client, template_variables):
        """Test GET /version."""
        response = client.get('/version', check=False)
        assert response.status_code == 200
        context = last_template_context(template_variables)
        assert 'app_name' in context
        assert 'commit' in context


class TestCommands:
    """Test command/keyword endpoints."""

    def test_commands_endpoint_renders_program_commands(self, client, given, template_variables):
        """Test /commands/<id> renders commands for a saved program."""
        teacher = given.logged_in_as_new_teacher()
        program = given.some_saved_program(teacher['username'], name='command_test', code='print hello', level=1)
        response = client.get(f'/commands/{program["id"]}')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['commands']


class TestProgramsListing:
    """Test programs listing endpoint."""

    def test_programs_list_not_logged_in_redirects(self, client):
        """Test /programs redirects when user is not logged in."""
        response = client.get('/programs', check=False)
        assert response.status_code == 302

    def test_programs_list(self, client, given):
        """Test /programs endpoint."""
        given.logged_in_as_new_teacher()
        response = client.get('/programs', check=False)
        assert response.status_code == 200

    def test_programs_with_offset(self, client, given):
        """Test /programs with offset parameter."""
        given.logged_in_as_new_teacher()
        response = client.get('/programs?offset=0&limit=5', check=False)
        assert response.status_code == 200


class TestHourOfCode:
    """Test Hour of Code routes."""

    def test_hour_of_code_default(self, client, template_variables):
        """Test /hour-of-code (default level)."""
        response = client.get('/hour-of-code')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'Hour of Code'
        assert context['level'] == 1

    def test_hour_of_code_level(self, client, template_variables):
        """Test /hour-of-code/<level>."""
        response = client.get('/hour-of-code/5')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['level'] == 5
        assert context['javascript_page_options']['page'] == 'code'

    def test_ontrack_default(self, client):
        """Test /ontrack (default level)."""
        response = client.get('/ontrack', check=False)
        assert response.status_code == 308

    def test_ontrack_with_level(self, client):
        """Test /ontrack/3."""
        response = client.get('/ontrack/3', check=False)
        assert response.status_code == 404

    def test_onlinemasters_default(self, client):
        """Test /onlinemasters (default level)."""
        response = client.get('/onlinemasters', check=False)
        assert response.status_code == 308

    def test_onlinemasters_with_level(self, client):
        """Test /onlinemasters/7."""
        response = client.get('/onlinemasters/7', check=False)
        assert response.status_code == 308


class TestHedyEditor:
    """Test Hedy editor routes with different variations."""

    def test_hedy_default(self, client, template_variables):
        """Test /hedy (default level 1)."""
        response = client.get('/hedy')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'hedy'
        assert context['level'] == 1

    def test_hedy_specific_level(self, client, template_variables):
        """Test /hedy with specific level."""
        response = client.get('/hedy/3')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'hedy'
        assert context['level'] == 3

    def test_hedy_with_program_id(self, client):
        """Test /hedy/<level>/<program_id>."""
        program_id = uuid.uuid4().hex
        response = client.get(f'/hedy/2/{program_id}', check=False)
        assert response.status_code == 404

    def test_hedy_view_redesign_not_logged_in_returns_401(self, client):
        """Test /hedy/<id>/view/redesign returns 401 when user is not logged in."""
        response = client.get('/hedy/invalid_id/view/redesign', check=False)
        assert response.status_code == 401

    def test_hedy_view_default(self, client, given):
        """Test viewing program in default view."""
        teacher = given.logged_in_as_new_teacher()
        program = given.some_saved_program(teacher['username'], name='view_test', code='print "hello"', level=1)
        response = client.get(f'/hedy/{program["id"]}/view', check=False)
        assert response.status_code == 200

    def test_hedy_view_redesign_default(self, client, given, template_variables):
        """Test viewing program in redesigned view."""
        teacher = given.logged_in_as_new_teacher()
        class_ = given.a_class(teacher['username'])
        given.db.add_student_to_class(class_['id'], teacher['username'])
        teacher_adventure = given.some_saved_adventure(teacher['username'], level='1')
        program = given.some_saved_program(
            teacher['username'],
            name='view_redesign_test',
            code='print "hello"',
            level=1,
            adventure_name=teacher_adventure['id'],
        )
        response = client.get(f'/hedy/{program["id"]}/view/redesign', check=False)
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['editor_readonly'] is True
        assert context['program']['id'] == program['id']
        assert context['javascript_page_options']['page'] == 'view-program'

    def test_hedy_view_not_logged_in_returns_401(self, client):
        """Test /hedy/<id>/view returns 401 when user is not logged in."""
        response = client.get('/hedy/invalid_id/view', check=False)
        assert response.status_code == 401

    def test_hedy_view_redesign_missing_program_logged_in_returns_404(self, client, given):
        """Test /hedy/<id>/view/redesign returns 404 for missing program when logged in."""
        given.logged_in_as_new_teacher()
        response = client.get('/hedy/invalid_id/view/redesign', check=False)
        assert response.status_code == 404

    def test_hedy_view_missing_program_logged_in_returns_404(self, client, given):
        """Test /hedy/<id>/view returns 404 for missing program when logged in."""
        given.logged_in_as_new_teacher()
        response = client.get('/hedy/invalid_id/view', check=False)
        assert response.status_code == 404

    def test_get_current_user_program_permissions_none_program_returns_none(self):
        """Guard against callers passing a missing program object."""
        assert hedy_app.get_current_user_program_permissions(None) is None


class TestAdventures:
    """Test adventure/exercise routes."""

    def test_adventure_with_teacher_created_adventure_renders(self, client, given, template_variables):
        """Teacher-created adventures can be rendered in the public adventure route."""
        teacher = given.logged_in_as_new_teacher()
        adventure = given.some_saved_adventure(teacher['username'], name='custom-adventure', level='2', levels=['2'])
        response = client.get(f'/adventure/{adventure["name"]}/2')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['specific_adventure'] is True
        assert context['level'] == 2
        assert context['initial_adventure'].name == adventure['name']
        assert context['initial_adventure'].save_name

    def test_adventure_default(self, client):
        """Test /adventure/<name>."""
        response = client.get('/adventure/intro', check=False)
        assert response.status_code == 404

    def test_adventure_with_level(self, client):
        """Test /adventure/<name>/<level>."""
        response = client.get('/adventure/intro/3', check=False)
        assert response.status_code == 404

    def test_adventure_with_mode(self, client):
        """Test /adventure/<name>/<level>/<mode>."""
        response = client.get('/adventure/intro/2/instructions', check=False)
        assert response.status_code == 404


class TestRenderCode:
    """Test code rendering endpoints."""

    def test_render_code_success_renders_editor_context(self, client, template_variables):
        """Valid render_code requests return the editor page with expected context."""
        response = client.get('/render_code/1/?code=print%20Hello')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['specific_adventure'] is True
        assert context['level'] == 1
        assert context['javascript_page_options']['page'] == 'view_adventure'

    def test_render_code(self, client):
        """Test /render_code/<level>/."""
        response = client.get('/render_code/1/', check=False)
        assert response.status_code == 400


class TestEmbedded:
    """Test embedded editor route."""

    def test_embedded_editor(self, client, template_variables):
        """Test /embedded/<level>."""
        response = client.get('/embedded/2')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['level'] == 2
        assert context['fullWidth'] is False
        assert context['javascript_page_options']['page'] == 'view-program'


class TestCheatsheet:
    """Test cheatsheet routes."""

    def test_cheatsheet_default(self, client, template_variables):
        """Test /cheatsheet/ (default level)."""
        response = client.get('/cheatsheet/')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['level'] == 1
        assert context['commands']

    def test_cheatsheet_level(self, client, template_variables):
        """Test /cheatsheet/<level>."""
        response = client.get('/cheatsheet/5')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['level'] == 5
        assert context['commands']


class TestSlides:
    """Test slides endpoint."""

    def test_slides_default(self, client):
        """Test /slides (default level)."""
        response = client.get('/slides')
        assert_html_response(response)

    def test_slides_with_level(self, client):
        """Test /slides/<level>."""
        response = client.get('/slides/4')
        assert_html_response(response)


class TestPublicPages2:
    """Additional public page tests."""

    def test_learn_more(self, client, template_variables):
        """Test /learn-more."""
        response = client.get('/learn-more')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'learn-more'
        assert context['content']

    def test_start_page(self, client, template_variables):
        """Test /start."""
        response = client.get('/start')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'start'
        assert context['content']

    def test_subscribe(self, client, template_variables):
        """Test /subscribe."""
        response = client.get('/subscribe')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'subscribe'

    def test_kerndoelen(self, client):
        """Test /kerndoelen."""
        response = client.get('/kerndoelen', check=False)
        assert response.status_code == 200

    def test_research(self, client):
        """Test /research/<filename>."""
        response = client.get('/research/test.pdf', check=False)
        assert response.status_code == 404

    def test_favicon(self, client):
        """Test /favicon.ico."""
        response = client.get('/favicon.ico', check=False)
        assert response.status_code == 404

    def test_index_html(self, client, template_variables):
        """Test /index.html."""
        response = client.get('/index.html')
        assert_html_response(response)
        context = last_template_context(template_variables)
        assert context['current_page'] == 'start'


class TestLanguageAndLocale:
    """Test language switching and locale handling."""

    def test_change_language_post(self, client):
        """Test changing language via POST."""
        response = client.post(
            '/change_language',
            data=json.dumps({'lang': 'nl'}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 200

    def test_translate_keywords(self, client):
        """Test /translate_keywords endpoint."""
        response = client.post(
            '/translate_keywords',
            data=json.dumps({'code': 'print hello', 'start_lang': 'en', 'goal_lang': 'nl', 'level': 1}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 200
        body = response.get_json()
        assert isinstance(body, dict)
        assert 'code' in body

    def test_main_page_with_different_locales(self, client):
        """Test main page with different languages."""
        for lang in ['en', 'nl', 'es', 'fr', 'de']:
            response = client.get(f'/?language={lang}', check=False)
            assert response.status_code == 200


class TestSessionAndLogging:
    """Test session and logging endpoints."""

    def test_query_logs_endpoint_valid_teacher_request_returns_200(self, client, given, monkeypatch):
        """Authorized teacher log queries with valid class/student filters succeed."""
        teacher = given.logged_in_as_new_teacher()
        student = given.a_student_account()
        class_ = given.a_class(teacher['username'])
        given.db.add_student_to_class(class_['id'], student['username'])

        monkeypatch.setattr(
            hedy_app.log_fetcher,
            'query',
            lambda body: ('exec-1', 'SUCCEEDED'),
        )

        response = client.post(
            '/logs/query',
            data=json.dumps({'class_id': class_['id'], 'username': student['username']}),
            content_type='application/json',
            check=False,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['query_execution_id'] == 'exec-1'
        assert data['query_status'] == 'SUCCEEDED'

    def test_logs_results_endpoint_teacher_returns_results(self, client, given, monkeypatch):
        """Authorized users can fetch query results payloads."""
        given.logged_in_as_new_teacher()

        monkeypatch.setattr(
            hedy_app.log_fetcher,
            'get_query_results',
            lambda execution_id, next_token: ([{'line': 1}], 'next-page-token'),
        )

        response = client.get('/logs/results?query_execution_id=exec-1', check=False)
        assert response.status_code == 200
        data = response.get_json()
        assert data['data'] == [{'line': 1}]
        assert data['next_token'] == 'next-page-token'

    def test_session_test_endpoint(self, client):
        """Test /session_test endpoint."""
        response = client.get('/session_test', check=False)
        assert response.status_code == 200

    def test_session_main_endpoint(self, client):
        """Test /session_main endpoint."""
        response = client.get('/session_main', check=False)
        assert response.status_code == 200

    def test_query_logs_endpoint_requires_class_and_username_for_teacher(self, client, given):
        """Test /logs/query returns 401 for teacher requests missing required fields."""
        given.logged_in_as_new_teacher()
        response = client.post(
            '/logs/query',
            data=json.dumps({}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 401

    def test_query_logs_endpoint_not_logged_in_returns_401(self, client):
        """Test /logs/query returns 401 when user is not logged in."""
        response = client.post(
            '/logs/query',
            data=json.dumps({}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 401

    def test_query_logs_endpoint_invalid_class_for_teacher_returns_401(self, client, given):
        """Test /logs/query returns 401 when teacher queries a class they don't own."""
        given.logged_in_as_new_teacher()
        response = client.post(
            '/logs/query',
            data=json.dumps({'class_id': 'missing-class-id', 'username': 'student1'}),
            content_type='application/json',
            check=False
        )
        assert response.status_code == 401

    def test_logs_results_endpoint_not_logged_in_returns_401(self, client):
        """Test /logs/results returns 401 when user is not logged in."""
        response = client.get('/logs/results', check=False)
        assert response.status_code == 401


class TestMyProfile:
    """Test my profile page."""

    def test_my_profile_not_logged_in_redirects(self, client):
        """Test /my-profile redirects when user is not logged in."""
        response = client.get('/my-profile', check=False)
        assert response.status_code == 302

    def test_my_profile_authenticated(self, client, given):
        """Test /my-profile with authentication."""
        given.logged_in_as_new_teacher()
        response = client.get('/my-profile', check=False)
        assert response.status_code == 200
