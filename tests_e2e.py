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
    def makeUsername():
        # We create usernames with a random component so that if a test fails, we don't have to do a cleaning of the DB so that the test suite can run again
        # This also allows us to run concurrent tests without having username conflicts.
        username = 'user' + str(random.randint(10000, 100000))
        return username

    # If user with `username` exists, return it. Otherwise, create it.
    @staticmethod
    def assertUserExists(username):
        if not isinstance(username, str):
            raise Exception('AuthHelper.assertUserExists - Invalid username: ' + str(username))

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
    def getAnyUser():
        if len(USERS.keys()) > 0:
            return USERS[next(iter(USERS))]
        return AuthHelper.assertUserExists(AuthHelper.makeUsername())

    # Returns the first logged in user, if any; otherwise, logs in a user; if no user exists, creates and then logs in the user.
    @staticmethod
    def getAnyLoggedUser():
        for user in USERS:
            if 'cookie' in user:
                return user

        # If there's no logged in user, we login the user
        user = AuthHelper.getAnyUser()
        return AuthHelper.loginUser(user['username'])

    @staticmethod
    def loginUser(username):
        user = USERS[username]
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']})
        cookie = AuthHelper.getHedyCookie(response['headers']['Set-Cookie'])

        # The cookie value must be set to `hedy={{SESSION}};` so that it can be used as a Cookie header in subsequent requests
        USERS[user['username']]['cookie'] = CONFIG['session']['cookie_name'] + '=' + cookie.value + ';'
        return user

    @staticmethod
    def assertUserIsLogged(username):
        AuthHelper.assertUserExists(username)
        return AuthHelper.loginUser(username)

    @staticmethod
    def getHedyCookie(cookieString):
        cookie = SimpleCookie()
        cookie.load(cookieString)

        for key, cookie in cookie.items():
            if key == CONFIG['session']['cookie_name']:
                return cookie

# *** TESTS ***

class TestAuth(unittest.TestCase):
    def test_InvalidSignups(self):
        username = AuthHelper.makeUsername()
        invalid_bodies =[
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
            self.assertEqual(response['code'], 400)

    def test_Signup(self):
        username = AuthHelper.makeUsername()
        body = {'username': username, 'email': username + '@hedy.com', 'password': 'foobar'}

        response = request('post', 'auth/signup', {}, body)
        self.assertEqual(response['code'], 200)
        self.assertIsInstance(response['body'], dict)
        self.assertIsInstance(response['body']['token'], str)

        # Store the user for use in upcoming tests
        USERS[username] = body
        USERS[username]['verify_token'] = response['body']['token']

    def test_InvalidLogin(self):
        invalid_bodies =[
            '',
           [],
            {},
            {'username': 1},
            {'username': 'user@me'},
            {'username:': 'user: me'}
        ]
        for invalid_body in invalid_bodies:
            response = request('post', 'auth/login', {}, invalid_body)
            self.assertEqual(response['code'], 400)

    def test_Login(self):
        user = AuthHelper.getAnyUser()
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']})

        # Validate response
        self.assertEqual(response['code'], 200)

        # Validate cookie in response
        self.assertIsInstance(response['headers']['Set-Cookie'], str)
        hedyCookie = AuthHelper.getHedyCookie(response['headers']['Set-Cookie'])
        self.assertNotEqual(hedyCookie, None)
        self.assertEqual(hedyCookie['httponly'], True)
        self.assertEqual(hedyCookie['path'], '/')
        self.assertEqual(hedyCookie['samesite'], 'Lax,')

    def test_InvalidVerifyEmail(self):
        # We create a new user to ensure that the verification flow hasn't been done by the user yet
        username = AuthHelper.makeUsername()
        user = AuthHelper.assertUserExists(username)

        # Send malformed verifications
        invalid_verifications =[
            # Missing token
            {'username': username},
            # Missing username
            {'token': user['verify_token']},
        ]

        for invalid_verification in invalid_verifications:
            response = request('get', 'auth/verify?' + urllib.parse.urlencode(invalid_verification))
            self.assertEqual(response['code'], 400)

        # Send well-formed verifications with invalid values
        incorrect_verifications =[
            # Invalid username
            {'username': 'foobar', 'token': user['verify_token']},
            # Invalid token
            {'username': username, 'token': 'foobar'}
        ]

        for incorrect_verification in incorrect_verifications:
            response = request('get', 'auth/verify?' + urllib.parse.urlencode(incorrect_verification))
            self.assertEqual(response['code'], 403)

    def test_VerifyEmail(self):
        # We create a new user to ensure that the verification flow hasn't been done by the user yet
        username = AuthHelper.makeUsername()
        user = AuthHelper.assertUserExists(username)
        # Attempt verification, operation should be successful
        response = request('get', 'auth/verify?' + urllib.parse.urlencode({'username': username, 'token': user['verify_token']}))
        self.assertEqual(response['code'], 302)
        self.assertEqual(response['headers']['location'], HOST)

        # Attempt verification again, operation should be idempotent
        response = request('get', 'auth/verify?' + urllib.parse.urlencode({'username': username, 'token': user['verify_token']}))
        self.assertEqual(response['code'], 302)
        self.assertEqual(response['headers']['location'], HOST)

        # Remove token from user since it's already been used.
        USERS[user['username']].pop('verify_token')

        # Retrieve profile to see that the user is no longer marked with `verification_pending`
        AuthHelper.assertUserIsLogged (username)
        profile = request ('get', 'profile', {'cookie': user ['cookie']}, '') ['body']
        self.assertNotIn ('verification_pending', profile)

    def test_Logout(self):
        user = AuthHelper.getAnyLoggedUser()

        response = request('post', 'auth/logout', {'cookie': user['cookie']}, '')
        self.assertEqual(response['code'], 200)

        # Verify that cookie is no longer valid by retrieving profile, which requires login
        response = request('get', 'profile', {'cookie': user['cookie']}, '')
        self.assertEqual(response['code'], 403)

        # Remove cookie from user to avoid generating issues in subsequent tests
        USERS[user['username']].pop('cookie')

    def test_DestroyAccount(self):
        user = AuthHelper.getAnyLoggedUser()

        response = request('post', 'auth/destroy', {'cookie': user['cookie']}, '')
        self.assertEqual(response['code'], 200)

        # Verify that cookie is no longer valid by retrieving profile, which requires login
        response = request('get', 'profile', {'cookie': user['cookie']}, '')
        self.assertEqual(response['code'], 403)

        # Remove user to avoid generating issues in subsequent tests
        USERS.pop(user['username'])

    def test_InvalidChangePassword(self):
        user = AuthHelper.getAnyLoggedUser()

        # Send malformed payloads
        invalid_payloads =[
            '',
           [],
            {},
            {'old_password': 123456},
            {'old_password': 'pass1'},
            {'old_password': 'pass1', 'new_password': 123456},
            {'old_password': 'pass1', 'new_password': 'short'},
        ]

        for invalid_payload in invalid_payloads:
            response = request('post', 'auth/change_password', {'cookie': user['cookie']}, invalid_payload)
            self.assertEqual(response['code'], 400)

        # Attempt to change password without sending the correct old password
        response = request('post', 'auth/change_password', {'cookie': user['cookie']}, {'old_password': 'password', 'new_password': user['password'] + 'foo'})
        self.assertEqual(response['code'], 403)

    def test_ChangePassword(self):
        # GIVEN a logged in user
        user = AuthHelper.getAnyLoggedUser()
        new_password = 'pas1234'
        response = request('post', 'auth/change_password', {'cookie': user['cookie']}, {'old_password': user['password'], 'new_password': 'pas1234'})
        self.assertEqual(response['code'], 200)

        # WHEN attempting to login with old password
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']})

        # THEN
        self.assertEqual(response['code'], 403)

        # GIVEN the same user

        # WHEN attempting to login with new password
        response = request('post', 'auth/login', {}, {'username': user['username'], 'password': new_password})
        self.assertEqual(response['code'], 200)

        # THEN update password on user
        USERS[user['username']]['password'] = new_password

    def test_ProfileGet (self):
        # We create a new user to ensure that the user has a new profile
        user = AuthHelper.assertUserIsLogged (AuthHelper.makeUsername ())

        response = request ('get', 'profile', {'cookie': user ['cookie']}, '')
        self.assertEqual (response ['code'], 200)

        profile = response ['body']
        self.assertIsInstance (profile, dict)
        self.assertEqual (profile ['username'], user ['username']),
        self.assertEqual (profile ['email'],    user ['email']),
        self.assertEqual (profile ['verification_pending'], True)
        self.assertIsInstance (profile ['student_classes'], list)
        self.assertEqual (len (profile ['student_classes']), 0)
        self.assertIsInstance (profile ['session_expires_at'], int)

    def test_InvalidProfileModify (self):
        user = AuthHelper.getAnyLoggedUser ()

        # Send malformed payloads
        invalid_payloads = [
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

        for invalid_payload in invalid_payloads:
            response = request ('post', 'profile', {'cookie': user ['cookie']}, invalid_payload)
            self.assertEqual (response ['code'], 400)

    def test_ProfileModify (self):
        # We create a new user to ensure that the user has a new profile
        user = AuthHelper.assertUserIsLogged (AuthHelper.makeUsername ())

        profile_changes = {
           'birth_year': 1989,
           'country': 'NL',
           'gender': 'o',
           'prog_experience': 'yes',
           'experience_languages': ['python', 'other_block']
        }

        for key in profile_changes:
            body = {}
            body [key] = profile_changes [key]
            response = request ('post', 'profile', {'cookie': user ['cookie']}, body)
            self.assertEqual (response ['code'], 200)

            profile = request ('get', 'profile', {'cookie': user ['cookie']}, '') ['body']
            self.assertEqual (profile [key], profile_changes [key])

        # We check email change separately since it involves a flow with a token
        response = request ('post', 'profile', {'cookie': user ['cookie']}, {'email': user ['username'] + '@newhedy.com'})
        self.assertIsInstance (response ['body'] ['token'], str)

        # Update email & token on user
        USERS [user ['username']] ['email'] = user ['username'] + '@newhedy.com'
        USERS [user ['username']] ['verify_token'] = response ['body'] ['token']

    def test_InvalidRecoverPassword (self):
        user = AuthHelper.getAnyUser ()

        # Send malformed payloads
        invalid_payloads = [
            '',
            [],
            {},
            {'username': 1}
        ]

        for invalid_payload in invalid_payloads:
            response = request ('post', 'auth/recover', {}, invalid_payload)
            self.assertEqual (response ['code'], 400)

        # No such user
        response = request ('post', 'auth/recover', {}, {'username': AuthHelper.makeUsername ()})
        self.assertEqual (response ['code'], 403)

    def test_RecoverPassword (self):
        user = AuthHelper.getAnyUser ()

        response = request ('post', 'auth/recover', {}, {'username': user ['username']})
        self.assertEqual (response ['code'], 200)
        self.assertIsInstance (response ['body'] ['token'], str)

    def test_InvalidResetPassword (self):
        user = AuthHelper.getAnyUser ()

        # Send malformed payloads
        invalid_payloads = [
            '',
            [],
            {},
            {'username': 1},
            {'username': 'foobar', 'token': 1},
            {'username': 'foobar', 'token': 'some'},
            {'username': 'foobar', 'token': 'some', 'password': 1},
            {'username': 'foobar', 'token': 'some', 'password': 'short'}
        ]

        for invalid_payload in invalid_payloads:
            response = request ('post', 'auth/reset', {}, invalid_payload)
            self.assertEqual (response ['code'], 400)

        # No such token
        response = request ('post', 'auth/reset', {}, {'username': user ['username'], 'password': '123456', 'token': 'foobar'})
        self.assertEqual (response ['code'], 403)

    def test_ResetPassword (self):
        user = AuthHelper.getAnyUser ()

        recover_token = request ('post', 'auth/recover', {}, {'username': user ['username']}) ['body'] ['token']

        response = request ('post', 'auth/reset', {},   {'username': user ['username'], 'password': user ['password'] + '1', 'token': recover_token})
        self.assertEqual (response ['code'], 200)

        # Update user's password and attempt login with new password
        USERS [user ['username']] ['password'] = user ['password'] + '1'
        response = request ('post', 'auth/login', {}, {'username': user ['username'], 'password': user ['password']})
        self.assertEqual (response ['code'], 200)

class TestProgram(unittest.TestCase):
    def test_GetPrograms(self):
        user = AuthHelper.getAnyLoggedUser()

        # Get programs but without sending a cookie
        response = request('get', 'programs_list', {}, '')
        # Response should send a redirect to the login page
        self.assertEqual(response['code'], 403)

        # Get programs sending a cookie
        response = request('get', 'programs_list', {'cookie': user['cookie']}, '')
        # Response should be an object of the shape `{programs:[...]}`.
        self.assertEqual(response['code'], 200)
        self.assertIsInstance(response['body'], dict)
        self.assertIsInstance(response['body']['programs'], list)

    def test_InvalidCreateProgram(self):
        user = AuthHelper.getAnyLoggedUser()

        # Send malformed payloads
        invalid_payloads =[
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

        for invalid_payload in invalid_payloads:
            response = request('post', 'programs', {'cookie': user['cookie']}, invalid_payload)
            self.assertEqual(response['code'], 400)

    def test_CreateProgram(self):
        # We create a new user to ensure that the user has no programs
        user = AuthHelper.assertUserIsLogged(AuthHelper.makeUsername())

        program = {'code': 'hello world', 'name': 'program 1', 'level': 1}
        response = request('post', 'programs', {'cookie': user['cookie']}, program)
        self.assertEqual(response['code'], 200)

        # Get programs after saving program
        response = request('get', 'programs_list', {'cookie': user['cookie']}, '')
        saved_programs = response['body']['programs']
        self.assertEqual(len(saved_programs), 1)
        saved_program = saved_programs[0]
        for key in program:
            self.assertEqual(program[key], saved_program[key])

    # TODO: add further programs tests
