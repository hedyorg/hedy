# *** NATIVE DEPENDENCIES ***
import threading
import random
import json
import re
import urllib.parse
from http.cookies import SimpleCookie

# *** LIBRARIES ***
import pytest
import unittest
import requests

# *** HEDY RESOURCES ***
import utils
from config import config as CONFIG

# *** GLOBAL VARIABLES ***

HOST = 'http://localhost:' + str(CONFIG['port']) + '/'
# This dict has global scope and holds all created users and their still current sessions (as cookies), for convenient reuse wherever needed
USERS = {}

# *** HELPERS ***

def request(method, path, headers={}, body='', user=None):

    if method not in['get', 'post', 'put', 'delete']:
        raise Exception('request - Invalid method: ' + str(method))

    # We pass the X-Testing header to let the server know that this is a request coming from an E2E test, thus no transactional emails should be sent.
    headers['X-Testing'] = '1'

    # If sending an object as body, stringify it and set the proper content-type header
    if isinstance(body, dict):
        headers['content-type'] = 'application/json'
        body = json.dumps(body)

    start = utils.timems()

    cookies = None
    if user:
        if not 'cookies' in user:
            user['cookies'] = requests.cookies.RequestsCookieJar()
        cookies = user['cookies']

    request = getattr(requests, method)(HOST + path, headers=headers, data=body, cookies=cookies)

    # Remember all cookies in the cookie jar
    if user:
        user['cookies'].update(request.cookies)

    response = {'time': utils.timems() - start}

    if request.history and request.history[0]:
        # This code branch will be executed if there is a redirect
        response['code']    = request.history[0].status_code
        response['headers'] = request.history[0].headers
        if getattr(request.history[0], '_content'):
            # We can assume that bodies returned from redirected responses are always plain text, since no JSON endpoint in the server is reachable through a redirect.
            response['body'] = getattr(request.history[0], '_content').decode('utf-8')
    else:
        response['code']    = request.status_code
        response['headers'] = request.headers
        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
            response['body'] = request.json()
        else:
            response['body'] = request.text

    return response

class AuthHelper(unittest.TestCase):
    def make_username(self):
        # We create usernames with a random component so that if a test fails, we don't have to do a cleaning of the DB so that the test suite can run again
        # This also allows us to run concurrent tests without having username conflicts.
        username = 'user' + str(random.randint(10000, 100000))
        return username

    # If user with `username` exists, return it. Otherwise, create it.
    def assert_user_exists(self, username):
        if not isinstance(username, str):
            raise Exception('AuthHelper.assert_user_exists - Invalid username: ' + str(username))

        if username in USERS:
            return USERS[username]
        body = {'username': username, 'email': username + '@hedy.com', 'password': 'foobar'}
        response = request('post', 'auth/signup', {}, body, user=body)

        # It might sometimes happen that by the time we attempted to create the user, another test did it already.
        # In this case, we get a 403. We invoke the function recursively.
        if response['code'] == 403:
            return self.assert_user_exists(username)

        # Store the user & also the verify token for use in upcoming tests
        USERS[username] = body

        USERS[username]['verify_token'] = response['body']['token']
        return USERS[username]

    # Returns the first created user, if any; otherwise, creates one.
    def get_any_user(self):
        if len(USERS.keys()) > 0:
            return USERS[next(iter(USERS))]
        return self.assert_user_exists(self.make_username())

    # Returns the first logged in user, if any; otherwise, logs in a user; if no user exists, creates and then logs in the user.
    def get_any_logged_user(self):
        for user in USERS:
            if 'cookies' in user:
                return user

        # If there's no logged in user, we login the user
        user = self.get_any_user()
        return self.login_user(user['username'])

    def login_user(self, username):
        user = USERS[username]
        if 'cookies' in user:
            return user
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']}, user=user)
        return user

    def assert_user_is_logged(self, username):
        self.assert_user_exists(username)
        return self.login_user(username)

    def get_hedy_cookie(self, cookie_string):
        cookie = SimpleCookie()
        cookie.load(cookie_string)

        for key, cookie in cookie.items():
            if key == CONFIG['session']['cookie_name']:
                return cookie

    def given_fresh_user_is_logged_in(self):
        username = self.make_username()
        self.user = self.assert_user_is_logged(username)
        self.username = username

    def given_user_is_logged_in(self):
        self.user = self.get_any_logged_user()
        self.username = self.user['username']

    def given_any_user(self):
        self.user = self.get_any_user()
        self.username = self.user['username']

    def switch_user(self, user):
        self.user = user
        self.username = self.user['username']

    def post_data(self, path, body, expect_http_code=200, no_cookie=False, return_headers=False, put_data=False):
        user = None
        if hasattr (self, 'user') and not no_cookie:
            user = self.user

        response = request('put' if put_data else 'post', path, body=body, user=user)
        self.assertEqual(response['code'], expect_http_code)
        if return_headers:
            return response['headers']
        else:
            return response['body']

    def get_data(self, path, expect_http_code=200, no_cookie=False, return_headers=False):
        user = None
        if hasattr (self, 'user') and not no_cookie:
            user = self.user

        response = request('get', path, body='', user=user)
        self.assertEqual(response['code'], expect_http_code)
        if return_headers:
            return response['headers']
        else:
            return response['body']

# *** TESTS ***

class TestPages(AuthHelper):
    def test_get_main_page(self):
        # WHEN attempting to get the main page
        # THEN receive an OK response code from the server
        self.get_data('/')

    def test_get_admin_page(self):
        # WHEN attempting to get the admin page
        # THEN receive an OK response code from the server
        # (Note: this only happens in a dev environment)
        self.get_data('/admin')

class TestSessionVariables(AuthHelper):
    def test_get_session_variables(self):
        # WHEN getting session variables from the main environment
        body = self.get_data('/session_main')

        # THEN the body should contain a `session` with `session_id` and a `proxy_enabled` field
        self.assertIn('session', body)
        self.assertIn('session_id', body['session'])
        self.assertIn('proxy_enabled', body)

        session = body['session']
        proxy_enabled = body['proxy_enabled']

        # WHEN getting session variables from the test environment
        test_body = self.get_data('/session_test')
        if not proxy_enabled:
            # If proxying to test is disabled, there is nothing else to test.
            return

        # THEN the body should contain a `session` with `session_id` and a `test_session` field
        self.assertIn('session', test_body)
        self.assertIn('session_id', test_body['session'])
        self.assertIn('test_session', test_body['session'])
        self.assertEquals(test_body['session']['session_id'], session['id'])

        # WHEN getting session variables from the main environment
        body = self.get_data('/session_main')
        # THEN the body should have a session with a session_id that is still the same and a `test_session` field as well
        self.assertEqual(body['session']['session_id'], session['id'])
        self.assertEqual(body['session']['test_session'], test_body['session']['session_id'])

class TestAuth(AuthHelper):
    def test_invalid_signups(self):
        # GIVEN a valid username
        username = self.make_username()
        # WHEN attempting signups with invalid bodies
        invalid_bodies = [
            '',
            [],
            {},
            {'username': 1},
            {'username': 'user@me', 'password': 'foobar', 'email': 'a@a.com'},
            {'username:': 'user: me', 'password': 'foobar', 'email': 'a@a.co'},
            {'username': 't'},
            {'username': '    t    '},
            {'username': username},
            {'username': username, 'password': 1},
            {'username': username, 'password': 'foo'},
            {'username': username, 'password': 'foobar'},
            {'username': username, 'password': 'foobar', 'email': 'me@something'},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'prog_experience':[2]},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'prog_experience': 'foo'},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'experience_languages': 'python'}
        ]
        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/signup', invalid_body, expect_http_code=400)

    def test_signup(self):
        # GIVEN a valid username and signup body
        self.username = self.make_username()
        self.user = {'username': self.username, 'email': self.username + '@hedy.com', 'password': 'foobar'}

        # WHEN signing up a new user
        # THEN receive an OK response code from the server
        body = self.post_data('auth/signup', self.user)

        # THEN receive a body containing a token
        self.assertIsInstance(body, dict)
        self.assertIsInstance(body['token'], str)

        # FINALLY Store the user and its token for upcoming tests
        self.user['verify_token'] = body['token']
        USERS[self.username] = self.user

    def test_invalid_login(self):
        # WHEN attempting logins with invalid bodies
        invalid_bodies = [
            '',
            [],
            {},
            {'username': 1},
            {'username': 'user@me'},
            {'username:': 'user: me'}
        ]
        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/login', invalid_body, expect_http_code=400)

    def test_login(self):
        # GIVEN an existing user
        self.given_any_user()

        # WHEN logging in the user
        # THEN receive an OK response code from the server
        headers = self.post_data('auth/login', {'username': self.username, 'password': self.user['password']}, return_headers=True)

        # THEN validate the cookie sent in the response
        self.assertIsInstance(headers['Set-Cookie'], str)
        hedy_cookie = self.get_hedy_cookie(headers['Set-Cookie'])
        self.assertNotEqual(hedy_cookie, None)
        self.assertEqual(hedy_cookie['httponly'], True)
        self.assertEqual(hedy_cookie['path'], '/')
        self.assertEqual(hedy_cookie['samesite'], 'Lax,')

    def test_invalid_verify_email(self):
        # GIVEN a new user
        # (we create a new user to ensure that the verification flow hasn't been done for this user yet)
        self.given_fresh_user_is_logged_in()

        # WHEN submitting invalid verifications
        invalid_verifications = [
            # Missing token
            {'username': self.username},
            # Missing username
            {'token': self.user['verify_token']},
        ]

        for invalid_verification in invalid_verifications:
            # THEN receive an invalid response code from the server
            self.get_data('auth/verify?' + urllib.parse.urlencode(invalid_verification), expect_http_code=400)

        # WHEN submitting well-formed verifications with invalid values
        incorrect_verifications = [
            # Invalid username
            {'username': 'foobar', 'token': self.user['verify_token']},
            # Invalid token
            {'username': self.username, 'token': 'foobar'}
        ]

        for incorrect_verification in incorrect_verifications:
            # THEN receive a forbidden response code from the server
            self.get_data('auth/verify?' + urllib.parse.urlencode(incorrect_verification), expect_http_code=403)

    def test_verify_email(self):
        # GIVEN a new user
        # (we create a new user to ensure that the verification flow hasn't been done for this user yet)
        self.given_fresh_user_is_logged_in()

        # WHEN attepting to verify the user
        # THEN receive a redirect from the server taking us to `/`
        headers = self.get_data('auth/verify?' + urllib.parse.urlencode({'username': self.username, 'token': self.user['verify_token']}), expect_http_code=302, return_headers=True)
        self.assertEqual(headers['location'], HOST)

        # WHEN attepting to verify the user again (the operation should be idempotent)
        # THEN (again) receive a redirect from the server taking us to `/`
        headers = self.get_data('auth/verify?' + urllib.parse.urlencode({'username': self.username, 'token': self.user['verify_token']}), expect_http_code=302, return_headers=True)
        self.assertEqual(headers['location'], HOST)

        # WHEN retrieving profile to see that the user is no longer marked with `verification_pending`
        self.assert_user_is_logged(self.username)
        profile = self.get_data('profile')

        # THEN check that the `verification_pending` has been removed from the user profile
        self.assertNotIn('verification_pending', profile)

        # FINALLY remove token from user since it's already been used.
        self.user.pop('verify_token')

    def test_logout(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN logging out the user
        # THEN receive an OK response code from the server
        self.post_data('auth/logout', '')

        # WHEN retrieving the user profile with the same cookie
        # THEN receive a forbidden response code from the server
        self.get_data('profile', expect_http_code=403)

    def test_destroy_account(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN deleting the user account
        # THEN receive an OK response code from the server
        self.post_data('auth/destroy', '')

        # WHEN retrieving the profile of the user
        # THEN receive a forbidden response code from the server
        self.get_data('profile', expect_http_code=403)

        # FINALLY remove user since it has already been deleted in the server
        USERS.pop(self.username)

    def test_invalid_change_password(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN attempting signups with invalid bodies
        invalid_bodies = [
            '',
            [],
            {},
            {'old_password': 123456},
            {'old_password': 'pass1'},
            {'old_password': 'pass1', 'new_password': 123456},
            {'old_password': 'pass1', 'new_password': 'short'},
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/change_password', invalid_body, expect_http_code=400)

        # WHEN attempting to change password without sending the correct old password
        # THEN receive an invalid response code from the server
        self.post_data('auth/change_password', {'old_password': 'password', 'new_password': self.user['password'] + 'foo'}, expect_http_code=403)

    def test_change_password(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN attempting to change the user's password
        new_password = 'pas1234'
        # THEN receive an OK response code from the server
        self.post_data('auth/change_password', {'old_password': self.user['password'], 'new_password': 'pas1234'})

        # WHEN attempting to login with old password
        # THEN receive a forbidden response code from the server
        self.post_data('auth/login', {'username': self.username, 'password': self.user['password']}, expect_http_code=403)

        # GIVEN the same user

        # WHEN attempting to login with new password
        # THEN receive an OK response code from the server
        self.post_data('auth/login', {'username': self.username, 'password': new_password})

        # FINALLY update password on user
        self.user['password'] = new_password

    def test_profile_get(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has a clean profile)
        self.given_fresh_user_is_logged_in()

        # WHEN retrieving the user profile
        # THEN receive an OK response code from the server
        profile = self.get_data('profile')

        # THEN check that the fields returned by the server have the correct values
        self.assertIsInstance(profile, dict)
        self.assertEqual(profile['username'], self.username),
        self.assertEqual(profile['email'],    self.user['email']),
        self.assertEqual(profile['verification_pending'], True)
        self.assertIsInstance(profile['student_classes'], list)
        self.assertEqual(len(profile['student_classes']), 0)
        self.assertIsInstance(profile['session_expires_at'], int)

    def test_invalid_profile_modify(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN attempting profile modifications with invalid bodies
        invalid_bodies = [
            '',
            [],
            {'email': 'foobar'},
            {'birth_year': 'a'},
            {'birth_year': 20},
            {'country': 'Netherlands'},
            {'gender': 0},
            {'gender': 'a'},
            {'prog_experience': 1},
            {'prog_experience': 'foo'},
            {'prog_experience': True},
            {'experience_languages': 'python'},
            {'experience_languages': ['python', 'foo']}
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('profile', invalid_body, expect_http_code=400)

    def test_profile_modify(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has a clean profile)
        self.given_fresh_user_is_logged_in()

        # WHEN submitting valid profile changes
        profile_changes = {
           'birth_year': 1989,
           'country': 'NL',
           'gender': 'o',
           'prog_experience': 'yes',
           'experience_languages': ['python', 'other_block']
        }

        for key in profile_changes:
            body = {}
            body[key] = profile_changes[key]
            # THEN receive an OK response code from the server
            self.post_data('profile', body)

            # WHEN retrieving the profile
            profile = self.get_data('profile')
            # THEN confirm that our modification has been stored by the server and returned in the latest version of the profile
            self.assertEqual(profile[key], profile_changes[key])

        # WHEN updating the user's email
        # (we check email change separately since it involves a flow with a token)
        # THEN receive an OK response code from the server
        new_email = self.username + '@newhedy.com'
        body = self.post_data('profile', {'email': new_email})

        # THEN confirm that the server replies with an email verification token
        self.assertIsInstance(body['token'], str)

        # FINALLY update the email & email verification token on user
        self.user['email'] = new_email
        self.user['verify_token'] = body['token']

    def test_invalid_recover_password(self):
        # GIVEN an existing user
        self.given_any_user()

        # WHEN attempting a password recovery with invalid bodies
        invalid_bodies = [
            '',
            [],
            {},
            {'username': 1}
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/recover', invalid_body, expect_http_code=400)

        # WHEN attempting a password recovery with a non-existing username
        # THEN receive a forbidden response code from the server
        self.post_data('auth/recover', {'username': self.make_username()}, expect_http_code=403)

    def test_recover_password(self):
        # GIVEN an existing user
        self.given_any_user()

        # WHEN attempting a password recovery
        # THEN receive an OK response code from the server
        body = self.post_data('auth/recover', {'username': self.username})
        # THEN check that we have received a password recovery token from the server
        self.assertIsInstance(body['token'], str)

    def test_invalid_reset_password(self):
        # GIVEN an existing user
        self.given_any_user()

        # WHEN attempting a password reset with invalid bodies
        invalid_bodies = [
            '',
            [],
            {},
            {'username': 1},
            {'username': 'foobar', 'token': 1},
            {'username': 'foobar', 'token': 'some'},
            {'username': 'foobar', 'token': 'some', 'password': 1},
            {'username': 'foobar', 'token': 'some', 'password': 'short'}
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/reset', invalid_body, expect_http_code=400)

        # WHEN attempting a password reset with an invalid token
        # THEN receive a forbidden response code from the server
        self.post_data('auth/reset', {'username': self.username, 'password': '123456', 'token': 'foobar'}, expect_http_code=403)

    def test_reset_password(self):
        # GIVEN an existing user
        self.given_any_user()

        # WHEN attempting a password reset with a valid username & token combination
        new_password = 'pas1234'
        recover_token = self.post_data('auth/recover', {'username': self.username})['token']
        # THEN receive an OK response code from the server
        self.post_data('auth/reset', {'username': self.username, 'password': new_password, 'token': recover_token})

        # WHEN attempting a login with the new password
        # THEN receive an OK response code from the server
        self.post_data('auth/login', {'username': self.username, 'password': new_password})

        # FINALLY update user's password and attempt login with new password
        self.user['password'] = new_password

class TestProgram(AuthHelper):
    def test_invalid_get_programs(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN retrieving own programs but without sending a cookie
        # THEN receive a forbidden response code from the server
        self.get_data('programs_list', expect_http_code=403, no_cookie=True)

    def test_get_programs(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN retrieving own programs sending a cookie
        # THEN receive an OK response code from the server
        body = self.get_data('programs_list')

        # THEN verify that the server sent a body that is an object of the shape `{programs:[...]}`.
        self.assertIsInstance(body, dict)
        self.assertIsInstance(body['programs'], list)

    def test_invalid_create_program(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN attempting to create an invalid program
        invalid_bodies = [
            '',
            [],
            {},
            {'code': 1},
            {'code':['1']},
            {'code': 'hello world'},
            {'code': 'hello world', 'name': 1},
            {'code': 'hello world', 'name': 'program 1'},
            {'code': 'hello world', 'name': 'program 1', 'level': '1'},
            {'code': 'hello world', 'name': 'program 1', 'level': 1, 'adventure_name': 1},
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('programs', invalid_body, expect_http_code=400)

        # WHEN submitting a program without being logged in
        # THEN receive a forbidden response code from the server
        self.post_data('programs', {'code': 'hello world', 'name': 'program 1', 'level': 1}, expect_http_code=403, no_cookie=True)

    def test_create_program(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has no programs yet)
        self.given_fresh_user_is_logged_in()

        # WHEN submitting a valid program
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        # THEN receive an OK response code from the server
        program = self.post_data('programs', program)
        # THEN verify that the returned program has both a name and an id
        self.assertIsInstance(program, dict)
        self.assertIsInstance(program['id'], str)
        self.assertIsInstance(program['name'], str)

        # WHEN retrieving programs after saving a program
        saved_programs = self.get_data('programs_list')['programs']

        # THEN verify that the program we just saved is in the list
        self.assertEqual(len(saved_programs), 1)
        saved_program = saved_programs[0]
        for key in program:
            self.assertEqual(program[key], saved_program[key])

    def test_invalid_make_program_public(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN attempting to share a program with an invalid body
        invalid_bodies = [
            '',
            [],
            {},
            {'code': 1},
            {'code':['1']},
            {'code': 'hello world'},
            {'code': 'hello world', 'name': 1},
            {'code': 'hello world', 'name': 'program 1'},
            {'code': 'hello world', 'name': 'program 1', 'level': '1'},
            {'code': 'hello world', 'name': 'program 1', 'level': 1, 'adventure_name': 1},
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('programs/share', invalid_body, expect_http_code=400)

        # WHEN sharing a program without being logged in
        # THEN receive a forbidden response code from the server
        self.post_data('programs/share', {'id': '123456', 'public': True}, expect_http_code=403, no_cookie=True)

        # WHEN sharing a program that does not exist
        # THEN receive a not found response code from the server
        self.post_data('programs/share', {'id': '123456', 'public': True}, expect_http_code=404)

    def test_valid_make_program_public(self):
        # GIVEN a logged in user with at least one program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        program_id = self.post_data('programs', program)['id']

        # WHEN making a program public
        # THEN receive an OK response code from the server
        self.post_data('programs/share', {'id': program_id, 'public': True})

        saved_programs = self.get_data('programs_list')['programs']
        for program in saved_programs:
            if program['id'] != program_id:
                continue
            # THEN the program must have its `public` field enabled
            self.assertEqual(program['public'], 1)

        # GIVEN another user
        self.given_fresh_user_is_logged_in()
        # WHEN requesting a public program
        # THEN receive an OK response code from the server
        self.get_data('hedy/1/' + program_id)

    def test_valid_make_program_private(self):
        # GIVEN a logged in user with at least one public program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        program_id = self.post_data('programs', program)['id']
        self.post_data('programs/share', {'id': program_id, 'public': True})

        # WHEN making a program private
        # THEN receive an OK response code from the server
        self.post_data('programs/share', {'id': program_id, 'public': False})

        saved_programs = self.get_data('programs_list')['programs']
        for program in saved_programs:
            if program['id'] != program_id:
                continue
            # THEN the program must have no `public` field
            self.assertNotIn('public', program)

        # GIVEN another user
        self.given_fresh_user_is_logged_in()
        # WHEN requesting a public program
        # THEN receive a not found response code from the server
        self.get_data('hedy/1/' + program_id, expect_http_code=404)

    def test_invalid_delete_program(self):
        # GIVEN a logged in user with at least one program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        self.post_data('programs', program)['id']
        program_id = '123456'

        # WHEN deleting a program that does not exist
        # THEN receive a not ound response code from the server
        self.get_data('programs/delete/' + program_id, expect_http_code=404)

    def test_valid_delete_program(self):
        # GIVEN a logged in user with at least one program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        program_id = self.post_data('programs', program)['id']

        # WHEN deleting a program
        # THEN receive an OK response code from the server
        headers = self.get_data('programs/delete/' + program_id, expect_http_code=302, return_headers=True)
        # THEN verify that the header has a `location` header pointing to `/programs`
        self.assertEqual(headers['location'], HOST + 'programs')

        saved_programs = self.get_data('programs_list')['programs']
        for program in saved_programs:
            # THEN the program should not be any longer in the list of programs
            self.assertNotEqual(program['id'], program_id)

    def test_destroy_account_with_programs(self):
        # GIVEN a logged in user with at least one program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        program_id = self.post_data('programs', program)['id']

        # WHEN deleting the user account
        # THEN receive an OK response code from the server
        self.post_data('auth/destroy', '')

        # FINALLY remove user since it has already been deleted in the server
        USERS.pop(self.username)

class TestClasses(AuthHelper):
    def test_invalid_create_class(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has no teacher permissions yet)
        self.given_fresh_user_is_logged_in()

        # WHEN creating a class without teacher permissions
        # THEN receive a forbidden response code from the server
        self.post_data('class', {'name': 'class1'}, expect_http_code=403)

        # WHEN marking the user as teacher
        # THEN receive an OK response code from the server
        self.post_data('admin/markAsTeacher', {'username': self.username, 'is_teacher': True})

        # GIVEN a user with teacher permissions

        # WHEN attempting to create a class with an invalid body
        invalid_bodies = [
            '',
            [],
            {},
            {'name': 1},
            {'name': ['foobar']}
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('class', invalid_body, expect_http_code=400)

    def test_create_class(self):
        # GIVEN a user with teacher permissions
        # (we create a new user to ensure that the user has no classes yet)
        self.given_fresh_user_is_logged_in()
        self.post_data('admin/markAsTeacher', {'username': self.username, 'is_teacher': True})

        # WHEN retrieving the list of classes
        class_list = self.get_data('classes')

        # THEN receive a body containing an empty list
        self.assertIsInstance(class_list, list)
        self.assertEqual(len(class_list), 0)

        # WHEN creating a class
        # THEN receive an OK response code with the server
        self.post_data('class', {'name': 'class1'})

        # GIVEN a class already saved
        # WHEN retrieving the list of classes
        class_list = self.get_data('classes')
        # THEN receive a body containing an list with one element
        self.assertEqual(len(class_list), 1)

        # THEN validate the fields of the class
        Class = class_list[0]
        self.assertIsInstance(Class, dict)
        self.assertIsInstance(Class['id'], str)
        self.assertIsInstance(Class['date'], int)
        self.assertIsInstance(Class['link'], str)
        self.assertEqual(Class['name'], 'class1')
        self.assertIsInstance(Class['students'], list)
        self.assertEqual(len(Class['students']), 0)
        self.assertEqual(Class['teacher'], self.username)

        # WHEN retrieving the class
        # THEN receive an OK response code from the server
        Class = self.get_data('class/' + Class['id'])

        # THEN validate the fields of the class
        self.assertIsInstance(Class, dict)
        self.assertIsInstance(Class['id'], str)
        self.assertIsInstance(Class['link'], str)
        self.assertEqual(Class['name'], 'class1')
        self.assertIsInstance(Class['students'], list)
        self.assertEqual(len(Class['students']), 0)

    def test_invalid_update_class(self):
        # GIVEN a user with teacher permissions and a class
        self.given_user_is_logged_in()
        self.post_data('admin/markAsTeacher', {'username': self.username, 'is_teacher': True})
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # WHEN attempting to update a class with no cookie
        # THEN receive a forbidden status code from the server
        self.post_data('class/' + Class['id'], {'name': 'class2'}, expect_http_code=403, put_data=True, no_cookie=True)

        # WHEN attempting to update a class that does not exist
        # THEN receive a not found status code from the server
        self.post_data('class/foo', {'name': 'class2'}, expect_http_code=404, put_data=True)

        # WHEN attempting to update a class with an invalid body
        invalid_bodies = [
            '',
            [],
            {},
            {'name': 1},
            {'name': ['foobar']}
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('class/' + Class['id'], invalid_body, expect_http_code=400, put_data=True)

    def test_update_class(self):
        # GIVEN a user with teacher permissions and a class
        self.given_user_is_logged_in()
        self.post_data('admin/markAsTeacher', {'username': self.username, 'is_teacher': True})
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # WHEN attempting to update a class
        # THEN receive an OK status code from the server
        self.post_data('class/' + Class['id'], {'name': 'class2'}, put_data=True)

        # WHEN retrieving the class
        # THEN receive an OK response code from the server
        Class = self.get_data('class/' + Class['id'])

        # THEN the name of the class should be updated
        self.assertEqual(Class['name'], 'class2')

    def test_join_class(self):
        # GIVEN a teacher
        self.given_user_is_logged_in()
        teacher = self.user
        self.post_data('admin/markAsTeacher', {'username': self.username, 'is_teacher': True})
        # GIVEN a class
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # GIVEN a student (user without teacher permissions)
        self.given_fresh_user_is_logged_in()
        student = self.user

        # WHEN attempting to join a class without being logged in
        # THEN receive a forbidden status code from the server
        self.get_data('class/' + Class['id'] + '/join/' + Class['link'], no_cookie=True, expect_http_code=403)

        # WHEN retrieving the short link of a class
        # THEN receive a redirect to `class/ID/join/LINK`
        body = self.get_data('hedy/l/' + Class['link'], expect_http_code=302)
        if not re.search(HOST + 'class/' + Class['id'] + '/prejoin/' + Class['link'], body):
            raise Exception('Invalid or missing redirect link')

        # WHEN joining a class
        # THEN receive a redirect to `class/ID/join/LINK`
        body = self.get_data('class/' + Class['id'] + '/join/' + Class['link'], expect_http_code=302)
        if not re.search(HOST + 'my-profile', body):
            raise Exception('Invalid redirect')

        # WHEN joining a class again (idempotent call)
        # THEN receive a redirect to `class/ID/join/LINK`
        body = self.get_data('class/' + Class['id'] + '/join/' + Class['link'], expect_http_code=302)
        if not re.search(HOST + 'my-profile', body):
            raise Exception('Invalid redirect')

        # WHEN getting own profile after joining a class
        profile = self.get_data('profile')
        # THEN verify that the class is there and contains the right fields
        self.assertIsInstance(profile['student_classes'], list)
        self.assertEqual(len(profile['student_classes']), 1)
        student_class = profile['student_classes'][0]
        self.assertIsInstance(student_class, dict)
        self.assertEqual(student_class['id'], Class['id'])
        self.assertEqual(student_class['name'], Class['name'])

    def test_see_students_in_class(self):
        # GIVEN a teacher
        self.given_user_is_logged_in()
        teacher = self.user
        self.post_data('admin/markAsTeacher', {'username': self.username, 'is_teacher': True})
        # GIVEN a class
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # GIVEN a student (user without teacher permissions) that has joined the class
        self.given_fresh_user_is_logged_in()
        student = self.user
        self.get_data('class/' + Class['id'] + '/join/' + Class['link'], expect_http_code=302)

        # GIVEN the aforementioned teacher
        self.switch_user(teacher)

        # WHEN retrieving the class with a student in it
        Class_data = self.get_data('class/' + Class['id'])
        # THEN the class should contain a student with valid fields
        self.assertEqual(len(Class_data['students']), 1)
        class_student = Class_data['students'][0]
        self.assertEqual(class_student['highest_level'], 0)
        self.assertEqual(class_student['programs'], 0)
        self.assertEqual(class_student['latest_shared'], None)
        self.assertIsInstance(class_student['last_login'], str)
        self.assertEqual(class_student['username'], student['username'])

        # WHEN retrieving the student's programs
        # THEN receive an OK response code from the server
        body = self.get_data('programs?user=' + student['username'], expect_http_code=200)

    def test_see_students_with_programs_in_class(self):
        # GIVEN a teacher
        self.given_user_is_logged_in()
        teacher = self.user
        self.post_data('admin/markAsTeacher', {'username': self.username, 'is_teacher': True})
        # GIVEN a class
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # GIVEN a student (user without teacher permissions) that has joined the class and has a public program
        self.given_fresh_user_is_logged_in()
        student = self.user
        self.get_data('class/' + Class['id'] + '/join/' + Class['link'], expect_http_code=302)
        # GIVEN a student with two programs, one public and one private
        public_program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        public_program_id = self.post_data('programs', public_program)['id']
        self.post_data('programs/share', {'id': public_program_id, 'public': True})
        private_program = {'code': 'hello world', 'name': 'program 2', 'level': 2}
        private_program_id = self.post_data('programs', private_program)['id']

        # GIVEN the aforementioned teacher
        self.switch_user(teacher)

        # WHEN retrieving the class with a student in it
        Class_data = self.get_data('class/' + Class['id'])
        # THEN the class should contain a student with valid fields
        self.assertEqual(len(Class_data['students']), 1)


# *** CLEANUP OF USERS CREATED DURING THE TESTS ***

def tearDownModule ():
    auth_helper = AuthHelper()
    for username in USERS:
        auth_helper.assert_user_is_logged(username)
        request('post', 'auth/destroy', user=USERS[username])
