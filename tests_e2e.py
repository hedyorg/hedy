# *** NATIVE DEPENDENCIES ***
import threading
import random
import json
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
# This dict has global scope and holds all created users and their still current sessions(as cookies), for convenient reuse wherever needed
USERS = {}
# This dict is used to transmit data from test to test
STATE = {}

# *** HELPERS ***

def request(method, path, headers={}, body=''):

    if method not in['get', 'post', 'put', 'delete']:
        raise Exception('request - Invalid method: ' + str(method))

    # We pass the X-Testing header to let the server know that this is a request coming from an E2E test, thus no transactional emails should be sent.
    headers['X-Testing'] = '1'

    # If sending an object as body, stringify it and set the proper content-type header
    if isinstance(body, dict):
        headers['content-type'] = 'application/json'
        body = json.dumps(body)

    start = utils.timems()

    request = getattr(requests, method)(HOST + path, headers=headers, data=body)

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
        response = request('post', 'auth/signup', {}, body)

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
            if 'cookie' in user:
                return user

        # If there's no logged in user, we login the user
        user = self.get_any_user()
        return self.login_user(user['username'])

    def login_user(self, username):
        user = USERS[username]
        if 'cookie' in user:
            return user
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']})
        cookie = self.get_hedy_cookie(response['headers']['Set-Cookie'])

        # The cookie value must be set to `hedy={{SESSION}};` so that it can be used as a Cookie header in subsequent requests
        USERS[user['username']]['cookie'] = CONFIG['session']['cookie_name'] + '=' + cookie.value + ';'
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
        if 'cookie' in self.user:
            self.cookie = self.user['cookie']
        else:
            self.cookie = None

    def given_user_is_logged_in(self):
        self.user = self.get_any_logged_user()
        self.username = self.user['username']
        if 'cookie' in self.user:
            self.cookie = self.user['cookie']
        else:
            self.cookie = None

    def given_any_user(self):
        self.user = self.get_any_user()
        self.username = self.user['username']
        if 'cookie' in self.user:
            self.cookie = self.user['cookie']
        else:
            self.cookie = None

    def post_data(self, path, body, expect_http_code=200):
        headers = {}
        if hasattr(self, 'cookie') and self.cookie:
            headers['cookie'] = self.cookie

        response = request('post', path, headers, body)
        self.assertEqual(response['code'], expect_http_code)
        return response['body']

    def get_data(self, path, expect_http_code=200):
        headers = {}
        if hasattr(self, 'cookie') and self.cookie:
            headers['cookie'] = self.cookie

        response = request('get', path, headers, '')
        self.assertEqual(response['code'], expect_http_code)
        return response['body']

# *** TESTS ***

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
        # Note: we don't use self.post_data because we want to get the headers (rather than the body) in order to validate it
        response = request('post', 'auth/login', {}, {'username': self.username, 'password': self.user['password']})

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # THEN validate the cookie sent in the response
        self.assertIsInstance(response['headers']['Set-Cookie'], str)
        hedy_cookie = self.get_hedy_cookie(response['headers']['Set-Cookie'])
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
        # Note: we don't use self.get_data because we want to get the headers (rather than the body) in order to validate it
        response = request('get', 'auth/verify?' + urllib.parse.urlencode({'username': self.username, 'token': self.user['verify_token']}))

        # THEN receive a redirect from the server taking us to `/`
        self.assertEqual(response['code'], 302)
        self.assertEqual(response['headers']['location'], HOST)

        # WHEN attepting to verify the user again (the operation should be idempotent)
        # Note: we don't use self.get_data because we want to get the headers (rather than the body) in order to validate it
        response = request('get', 'auth/verify?' + urllib.parse.urlencode({'username': self.username, 'token': self.user['verify_token']}))

        # THEN (again) receive a redirect from the server taking us to `/`
        self.assertEqual(response['code'], 302)
        self.assertEqual(response['headers']['location'], HOST)

        # WHEN retrieving profile to see that the user is no longer marked with `verification_pending`
        self.assert_user_is_logged(self.username)
        profile = self.get_data('profile')

        # THEN check that the `verification_pending` has been removed from the user profile
        self.assertNotIn('verification_pending', profile)

        # FINALLY remove token from user since it's already been used.
        self.user.pop('cookie')

    def test_logout(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN logging out the user
        # THEN receive an OK response code from the server
        self.post_data('auth/logout', '')

        # WHEN retrieving the user profile with the same cookie
        # THEN receive a forbidden response code from the server
        self.get_data('profile', expect_http_code=403)

        # FINALLY remove the cookie from user since it has already been deleted in the server
        self.user.pop('cookie')

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
        self.given_user_is_logged_in()

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
    def test_get_programs(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN retrieving own programs but without sending a cookie
        # Note: we don't use self.get_data because we want to send no cookie in the headers
        response = request('get', 'programs_list', {}, '')

        # THEN receive a forbidden response code from the server
        self.assertEqual(response['code'], 403)

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

    def test_create_program(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has no programs yet)
        self.given_fresh_user_is_logged_in()

        # WHEN submitting a valid program
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        # THEN receive an OK response code from the server
        self.post_data('programs', program)

        # WHEN retrieving programs after saving a program
        saved_programs = self.get_data('programs_list')['programs']

        # THEN verify that the program we just saved is in the list
        self.assertEqual(len(saved_programs), 1)
        saved_program = saved_programs[0]
        for key in program:
            self.assertEqual(program[key], saved_program[key])

    # TODO: add further programs tests

# *** CLEANUP ***

# We delete all the test users we created during the tests.
# For this purpose, we use a pytest fixture. This requires us to use the `request` variable, without any possible renaming.
# For this reason, we must rename our `request` function to `Request` so it will be referenceable from within the fixture.
Request = request
@pytest.fixture(scope='session', autouse=True)
def DeleteAllTestUsers(request):
    def InnerFunction():
        auth_helper = AuthHelper()
        for username in USERS:
            auth_helper.assert_user_is_logged(username)
            Request('post', 'auth/destroy', {'cookie': USERS [username]['cookie']}, '')
    request.addfinalizer(InnerFunction)
