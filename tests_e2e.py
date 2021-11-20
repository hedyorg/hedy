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

class AuthHelper():
    @staticmethod
    def make_username():
        # We create usernames with a random component so that if a test fails, we don't have to do a cleaning of the DB so that the test suite can run again
        # This also allows us to run concurrent tests without having username conflicts.
        username = 'user' + str(random.randint(10000, 100000))
        return username

    # If user with `username` exists, return it. Otherwise, create it.
    @staticmethod
    def assert_user_exists(username):
        if not isinstance(username, str):
            raise Exception('AuthHelper.assert_user_exists - Invalid username: ' + str(username))

        if username in USERS:
            return USERS[username]
        body = {'username': username, 'email': username + '@hedy.com', 'password': 'foobar'}
        response = request('post', 'auth/signup', {}, body)

        # Store the user & also the verify token for use in upcoming tests
        USERS[username] = body
        USERS[username]['verify_token'] = response['body']['token']
        return USERS[username]

    # Returns the first created user, if any; otherwise, creates one.
    @staticmethod
    def get_any_user():
        if len(USERS.keys()) > 0:
            return USERS[next(iter(USERS))]
        return AuthHelper.assert_user_exists(AuthHelper.make_username())

    # Returns the first logged in user, if any; otherwise, logs in a user; if no user exists, creates and then logs in the user.
    @staticmethod
    def get_any_logged_user():
        for user in USERS:
            if 'cookie' in user:
                return user

        # If there's no logged in user, we login the user
        user = AuthHelper.get_any_user()
        return AuthHelper.login_user(user['username'])

    @staticmethod
    def login_user(username):
        user = USERS[username]
        if 'cookie' in user:
            return user
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']})
        cookie = AuthHelper.get_hedy_cookie(response['headers']['Set-Cookie'])

        # The cookie value must be set to `hedy={{SESSION}};` so that it can be used as a Cookie header in subsequent requests
        USERS[user['username']]['cookie'] = CONFIG['session']['cookie_name'] + '=' + cookie.value + ';'
        return user

    @staticmethod
    def assert_user_is_logged(username):
        AuthHelper.assert_user_exists(username)
        return AuthHelper.login_user(username)

    @staticmethod
    def get_hedy_cookie(cookie_string):
        cookie = SimpleCookie()
        cookie.load(cookie_string)

        for key, cookie in cookie.items():
            if key == CONFIG['session']['cookie_name']:
                return cookie

# *** TESTS ***

class TestAuth(unittest.TestCase):
    def test_invalid_signups(self):
        # GIVEN a valid username
        username = AuthHelper.make_username()
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
            response = request('post', 'auth/signup', {}, invalid_body)
            # THEN receive an invalid response code from the server
            self.assertEqual(response['code'], 400)

    def test_signup(self):
        # GIVEN a valid username and signup body
        username = AuthHelper.make_username()
        body = {'username': username, 'email': username + '@hedy.com', 'password': 'foobar'}

        # WHEN signing up a new user
        response = request('post', 'auth/signup', {}, body)

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)
        # THEN receive a body containing a token
        self.assertIsInstance(response['body'], dict)
        self.assertIsInstance(response['body']['token'], str)

        # THEN Store the user and its token for upcoming tests
        USERS[username] = body
        USERS[username]['verify_token'] = response['body']['token']

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
            response = request('post', 'auth/login', {}, invalid_body)
            # THEN receive an invalid response code from the server
            self.assertEqual(response['code'], 400)

    def test_login(self):
        # GIVEN an existing user
        user = AuthHelper.get_any_user()

        # WHEN logging in the user
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']})

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # THEN validate the cookie sent in the response
        self.assertIsInstance(response['headers']['Set-Cookie'], str)
        hedy_cookie = AuthHelper.get_hedy_cookie(response['headers']['Set-Cookie'])
        self.assertNotEqual(hedy_cookie, None)
        self.assertEqual(hedy_cookie['httponly'], True)
        self.assertEqual(hedy_cookie['path'], '/')
        self.assertEqual(hedy_cookie['samesite'], 'Lax,')

    def test_invalid_verify_email(self):
        # GIVEN a new user
        # (we create a new user to ensure that the verification flow hasn't been done for this user yet)
        username = AuthHelper.make_username()
        user = AuthHelper.assert_user_exists(username)

        # WHEN submitting invalid verifications
        invalid_verifications = [
            # Missing token
            {'username': username},
            # Missing username
            {'token': user['verify_token']},
        ]

        for invalid_verification in invalid_verifications:
            response = request('get', 'auth/verify?' + urllib.parse.urlencode(invalid_verification))
            # THEN receive an invalid response code from the server
            self.assertEqual(response['code'], 400)

        # WHEN submitting well-formed verifications with invalid values
        incorrect_verifications = [
            # Invalid username
            {'username': 'foobar', 'token': user['verify_token']},
            # Invalid token
            {'username': username, 'token': 'foobar'}
        ]

        for incorrect_verification in incorrect_verifications:
            response = request('get', 'auth/verify?' + urllib.parse.urlencode(incorrect_verification))
            # THEN receive a forbidden response code from the server
            self.assertEqual(response['code'], 403)

    def test_verify_email(self):
        # GIVEN a new user
        # (we create a new user to ensure that the verification flow hasn't been done for this user yet)
        username = AuthHelper.make_username()
        user = AuthHelper.assert_user_exists(username)

        # WHEN attepting to verify the user
        response = request('get', 'auth/verify?' + urllib.parse.urlencode({'username': username, 'token': user['verify_token']}))

        # THEN receive a redirect from the server taking us to `/`
        self.assertEqual(response['code'], 302)
        self.assertEqual(response['headers']['location'], HOST)

        # WHEN attepting to verify the user again (the operation should be idempotent)
        response = request('get', 'auth/verify?' + urllib.parse.urlencode({'username': username, 'token': user['verify_token']}))

        # THEN (again) receive a redirect from the server taking us to `/`
        self.assertEqual(response['code'], 302)
        self.assertEqual(response['headers']['location'], HOST)

        # THEN remove token from user since it's already been used.
        USERS[user['username']].pop('verify_token')

        # WHEN retrieving profile to see that the user is no longer marked with `verification_pending`
        AuthHelper.assert_user_is_logged(username)
        profile = request('get', 'profile', {'cookie': user['cookie']}, '')['body']

        # THEN check that the `verification_pending` has been removed from the user profile
        self.assertNotIn('verification_pending', profile)

    def test_logout(self):
        # GIVEN a logged in user
        user = AuthHelper.get_any_logged_user()

        # WHEN logging out the user
        response = request('post', 'auth/logout', {'cookie': user['cookie']}, '')

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # WHEN retrieving the user profile with the same cookie
        response = request('get', 'profile', {'cookie': user['cookie']}, '')
        # THEN receive a forbidden response code from the server
        self.assertEqual(response['code'], 403)

        # THEN remove the cookie from user since it has already been deleted in the server
        USERS[user['username']].pop('cookie')

    def test_destroy_account(self):
        # GIVEN a logged in user
        user = AuthHelper.get_any_logged_user()

        # WHEN deleting the user account
        response = request('post', 'auth/destroy', {'cookie': user['cookie']}, '')
        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # WHEN retrieving the profile of the user
        response = request('get', 'profile', {'cookie': user['cookie']}, '')
        # THEN receive a forbidden response code from the server
        self.assertEqual(response['code'], 403)

        # THEN remove user since it has already been deleted in the server
        USERS.pop(user['username'])

    def test_invalid_change_password(self):
        # GIVEN a logged in user
        user = AuthHelper.get_any_logged_user()

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
            response = request('post', 'auth/change_password', {'cookie': user['cookie']}, invalid_body)
            # THEN receive an invalid response code from the server
            self.assertEqual(response['code'], 400)

        # WHEN attempting to change password without sending the correct old password
        response = request('post', 'auth/change_password', {'cookie': user['cookie']}, {'old_password': 'password', 'new_password': user['password'] + 'foo'})
        # THEN receive an invalid response code from the server
        self.assertEqual(response['code'], 403)

    def test_change_password(self):
        # GIVEN a logged in user
        user = AuthHelper.get_any_logged_user()

        # WHEN attempting to change the user's password
        new_password = 'pas1234'
        response = request('post', 'auth/change_password', {'cookie': user['cookie']}, {'old_password': user['password'], 'new_password': 'pas1234'})
        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # WHEN attempting to login with old password
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']})

        # THEN receive a forbidden response code from the server
        self.assertEqual(response['code'], 403)

        # GIVEN the same user

        # WHEN attempting to login with new password
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': new_password})

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # THEN update password on user
        USERS[user['username']]['password'] = new_password

    def test_profile_get(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has a clean profile)
        user = AuthHelper.assert_user_is_logged(AuthHelper.make_username())

        # WHEN retrieving the user profile
        response = request('get', 'profile', {'cookie': user['cookie']}, '')

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # THEN check that the fields returned by the server have the correct values
        profile = response['body']
        self.assertIsInstance(profile, dict)
        self.assertEqual(profile['username'], user['username']),
        self.assertEqual(profile['email'],    user['email']),
        self.assertEqual(profile['verification_pending'], True)
        self.assertIsInstance(profile['student_classes'], list)
        self.assertEqual(len(profile['student_classes']), 0)
        self.assertIsInstance(profile['session_expires_at'], int)

    def test_invalid_profile_modify(self):
        # GIVEN a logged in user
        user = AuthHelper.get_any_logged_user()

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
            response = request('post', 'profile', {'cookie': user['cookie']}, invalid_body)
            # THEN receive an invalid response code from the server
            self.assertEqual(response['code'], 400)

    def test_profile_modify(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has a clean profile)
        user = AuthHelper.assert_user_is_logged(AuthHelper.make_username())

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
            response = request('post', 'profile', {'cookie': user['cookie']}, body)
            # THEN receive an OK response code from the server
            self.assertEqual(response['code'], 200)

            # WHEN retrieving the profile
            profile = request('get', 'profile', {'cookie': user['cookie']}, '')['body']
            # THEN confirm that our modification has been stored by the server and returned in the latest version of the profile
            self.assertEqual(profile[key], profile_changes[key])

        # WHEN updating the user's email
        # (we check email change separately since it involves a flow with a token)
        response = request('post', 'profile', {'cookie': user['cookie']}, {'email': user['username'] + '@newhedy.com'})

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)
        # THEN confirm that the server replies with an email verification token
        self.assertIsInstance(response['body']['token'], str)

        # THEN update the email & email verification token on user
        USERS[user['username']]['email'] = user['username'] + '@newhedy.com'
        USERS[user['username']]['verify_token'] = response['body']['token']

    def test_invalid_recover_password(self):
        # GIVEN an existing user
        user = AuthHelper.get_any_user()

        # WHEN attempting a password recovery with invalid bodies
        invalid_bodies = [
            '',
            [],
            {},
            {'username': 1}
        ]

        for invalid_body in invalid_bodies:
            response = request('post', 'auth/recover', {}, invalid_body)
            # THEN receive an invalid response code from the server
            self.assertEqual(response['code'], 400)

        # WHEN attempting a password recovery with a non-existing username
        response = request('post', 'auth/recover', {}, {'username': AuthHelper.make_username()})
        # THEN receive a forbidden response code from the server
        self.assertEqual(response['code'], 403)

    def test_recover_password(self):
        # GIVEN an existing user
        user = AuthHelper.get_any_user()

        # WHEN attempting a password recovery
        response = request('post', 'auth/recover', {}, {'username': user['username']})
        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)
        # THEN check that we have received a password recovery token from the server
        self.assertIsInstance(response['body']['token'], str)

    def test_invalid_reset_password(self):
        # GIVEN an existing user
        user = AuthHelper.get_any_user()

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
            response = request('post', 'auth/reset', {}, invalid_body)
            # THEN receive an invalid response code from the server
            self.assertEqual(response['code'], 400)

        # WHEN attempting a password reset with an invalid token
        response = request('post', 'auth/reset', {}, {'username': user['username'], 'password': '123456', 'token': 'foobar'})
        # THEN receive a forbidden response code from the server
        self.assertEqual(response['code'], 403)

    def test_reset_password(self):
        # GIVEN an existing user
        user = AuthHelper.get_any_user()

        # WHEN attempting a password reset with a valid username & token combination
        new_password = 'pas1234'
        recover_token = request('post', 'auth/recover', {}, {'username': user['username']})['body']['token']
        response = request('post', 'auth/reset', {},   {'username': user['username'], 'password': new_password, 'token': recover_token})

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # WHEN attempting a login with the new password
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': new_password})
        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # THEN update user's password and attempt login with new password
        USERS [user['username']]['password'] = new_password

class TestProgram(unittest.TestCase):
    def test_get_programs(self):
        # GIVEN a logged in user
        user = AuthHelper.get_any_logged_user()

        # WHEN retrieving own programs but without sending a cookie
        response = request('get', 'programs_list', {}, '')
        # THEN receive a forbidden response code from the server
        self.assertEqual(response['code'], 403)

        # WHEN retrieving own programs sending a cookie
        response = request('get', 'programs_list', {'cookie': user['cookie']}, '')
        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)
        # THEN verify that the server sent a body that is an object of the shape `{programs:[...]}`.
        self.assertIsInstance(response['body'], dict)
        self.assertIsInstance(response['body']['programs'], list)

    def test_invalid_create_program(self):
        # GIVEN a logged in user
        user = AuthHelper.get_any_logged_user()

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
            response = request('post', 'programs', {'cookie': user['cookie']}, invalid_body)
            # THEN receive an invalid response code from the server
            self.assertEqual(response['code'], 400)

    def test_create_program(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has no programs yet)
        user = AuthHelper.assert_user_is_logged(AuthHelper.make_username())

        # WHEN submitting a valid program
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        response = request('post', 'programs', {'cookie': user['cookie']}, program)

        # THEN receive an OK response code from the server
        self.assertEqual(response['code'], 200)

        # WHEN retrieving programs after saving a program
        response = request('get', 'programs_list', {'cookie': user['cookie']}, '')

        # THEN verify that the program we just saved is in the list
        saved_programs = response['body']['programs']
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
        for username in USERS:
            AuthHelper.assert_user_is_logged(username)
            Request('post', 'auth/destroy', {'cookie': USERS [username]['cookie']}, '')
    request.addfinalizer(InnerFunction)
