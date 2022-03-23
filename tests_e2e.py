# *** NATIVE DEPENDENCIES ***
import os
import collections
import random
import json
import re
import urllib.parse
from http.cookies import SimpleCookie

# *** LIBRARIES ***
import unittest
import requests

# *** HEDY RESOURCES ***
import utils
from config import config as CONFIG

# *** GLOBAL VARIABLES ***

HOST = os.getenv('ENDPOINT', 'http://localhost:' + str(CONFIG['port']) + '/')
if not HOST.endswith('/'): HOST += '/'

# This dict has global scope and holds all created users and their still current sessions (as cookies), for convenient reuse wherever needed
USERS = {}

# *** HELPERS ***

def request(method, path, headers={}, body='', cookies=None):

    if method not in['get', 'post', 'put', 'delete']:
        raise Exception('request - Invalid method: ' + str(method))

    # We pass the X-Testing header to let the server know that this is a request coming from an E2E test, thus no transactional emails should be sent.
    headers['X-Testing'] = '1'

    # If sending an object as body, stringify it and set the proper content-type header
    if isinstance(body, dict):
        headers['content-type'] = 'application/json'
        body = json.dumps(body)

    start = utils.timems()

    response = getattr(requests, method)(HOST + path, headers=headers, data=body, cookies=cookies)

    # Remember all cookies in the cookie jar
    if cookies is not None:
        cookies.update(response.cookies)

    ret = {'time': utils.timems() - start}

    if response.history and response.history[0]:
        # This code branch will be executed if there is a redirect
        ret['code']    = response.history[0].status_code
        ret['headers'] = response.history[0].headers
        if getattr(response.history[0], '_content'):
            # We can assume that bodies returned from redirected responses are always plain text, since no JSON endpoint in the server is reachable through a redirect.
            ret['body'] = getattr(response.history[0], '_content').decode('utf-8')
    else:
        ret['code']    = response.status_code
        ret['headers'] = response.headers
        if 'Content-Type' in response.headers and response.headers['Content-Type'] == 'application/json':
            ret['body'] = response.json()
        else:
            ret['body'] = response.text

    return ret

class AuthHelper(unittest.TestCase):
    def setUp(self):
        """SetUp gets called on a fresh instance of this object, before each test.

        We have a collection of users in the USER global array. However, we store
        the cookies for individual users, so that cookies from different sessions don't
        interfere with each other (i.e., every user must login again in each test).
        """
        self.user_cookies = collections.defaultdict(requests.cookies.RequestsCookieJar)
        self.user = None

    @property
    def username(self):
        return self.user['username'] if self.user else None

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
        body = {'username': username, 'email': username + '@hedy.com', 'mail_repeat': username + '@hedy.com',
                'language': 'nl', 'keyword_language': 'en', 'agree_terms': True, 'password': 'foobar', 'password_repeat': 'foobar'}
        response = request('post', 'auth/signup', {}, body, cookies=self.user_cookies[username])

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

    def get_any_logged_user(self):
        # If there's no logged in user, we login the user
        user = self.get_any_user()
        return self.login_user(user['username'])

    def login_user(self, username):
        """Login another user. Does not BECOME that user for all subsequent request."""
        self.assert_user_exists(username)
        user = USERS[username]
        request('post', 'auth/login', {}, {'username': user['username'], 'password': user['password']}, cookies=self.user_cookies[username])
        return user

    def given_specific_user_is_logged_in(self, username):
        """Become this specific user for all subsequent calls."""
        self.user = self.login_user(username)

    def get_hedy_cookie(self, cookie_string):
        cookie = SimpleCookie()
        cookie.load(cookie_string)

        for key, cookie in cookie.items():
            if key == CONFIG['session']['cookie_name']:
                return cookie

    def given_fresh_user_is_logged_in(self):
        username = self.make_username()
        self.user = self.login_user(username)

    def make_current_user_teacher(self):
        """Mark the current user as teacher.

        Need to log in again to refresh the session.
        """
        self.post_data('admin/markAsTeacher', {'username': self.username, 'is_teacher': True})
        return self.login_user(self.username)

    def given_user_is_logged_in(self):
        self.user = self.get_any_logged_user()

    def given_teacher_is_logged_in(self):
        self.given_user_is_logged_in()
        self.make_current_user_teacher()

    def given_fresh_teacher_is_logged_in(self):
        self.given_fresh_user_is_logged_in()
        self.make_current_user_teacher()

    def given_any_user(self):
        self.user = self.get_any_user()

    def switch_user(self, user):
        self.user = self.login_user(user['username'])

    def post_data(self, path, body, expect_http_code=200, no_cookie=False, return_headers=False, put_data=False):
        cookies = self.user_cookies[self.username] if self.username and not no_cookie else None

        method = 'put' if put_data else 'post'
        response = request(method, path, body=body, cookies=cookies)
        self.assertEqual(response['code'], expect_http_code, f'While {method}ing {body} to {path} (user: {self.username})')

        return response['headers'] if return_headers else response['body']

    def delete_data(self, path, expect_http_code=200, no_cookie=False, return_headers=False):
        cookies = self.user_cookies[self.username] if self.username and not no_cookie else None

        method = 'delete'
        response = request(method, path, cookies=cookies)
        self.assertEqual(response['code'], expect_http_code,
                         f'While {method}ing {path} (user: {self.username})')

        return response['headers'] if return_headers else response['body']

    def get_data(self, path, expect_http_code=200, no_cookie=False, return_headers=False):
        cookies = self.user_cookies[self.username] if self.username and not no_cookie else None
        response = request('get', path, body='', cookies=cookies)

        self.assertEqual(response['code'], expect_http_code, f'While reading {path} (user: {self.username})')

        return response['headers'] if return_headers else response['body']

    def destroy_current_user(self):
        assert self.username is not None
        self.post_data('auth/destroy', '')
        # Remove any records of this user
        USERS.pop(self.username)

# *** TESTS ***

class TestPages(AuthHelper):
    def test_get_main_page(self):
        # WHEN attempting to get the main page
        # THEN receive an OK response code from the server
        self.get_data('/')

    def test_get_code_page(self):
        # WHEN attempting to get the code page
        # THEN receive an OK response code from the server
        self.get_data('/hedy')

    def test_get_explore_page(self):
        # WHEN attempting to get the explore page
        # THEN receive an OK response code from the server
        self.given_fresh_user_is_logged_in()
        self.get_data('/explore')

    def test_get_learn_more_page(self):
        # WHEN attempting to get the learn-more page
        # THEN receive an OK response code from the server
        self.get_data('/learn-more')

    def test_get_login_page(self):
        # WHEN attempting to get the login page
        # THEN receive an OK response code from the server
        self.get_data('/login')

    def test_get_signup_page(self):
        # WHEN attempting to get the signup page
        # THEN receive an OK response code from the server
        self.get_data('/signup')

    def test_get_recover_page(self):
        # WHEN attempting to get the signup page
        # THEN receive an OK response code from the server
        self.get_data('/recover')

    def test_get_programs_page(self):
        # WHEN attempting to get the programs page
        # THEN receive an OK response code from the server
        self.given_fresh_user_is_logged_in()
        self.get_data('/programs')

    def test_get_achievements_page(self):
        # WHEN attempting to get the achievements page
        # THEN receive an OK response code from the server
        self.given_fresh_user_is_logged_in()
        self.get_data('/my-achievements')

    def test_get_profile_page(self):
        # WHEN attempting to get the profile page
        # THEN receive an OK response code from the server
        self.given_fresh_user_is_logged_in()
        self.get_data('/my-profile')

    def test_get_landing_page(self):
        # WHEN attempting to get the landing page
        # THEN receive an OK response code from the server
        self.given_fresh_user_is_logged_in()
        self.get_data('/landing-page')

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
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'language': 123},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'language': True},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'prog_experience': [2]},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'prog_experience': 'foo'},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'experience_languages': 'python'}
        ]
        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/signup', invalid_body, expect_http_code=400)

    def test_signup(self):
        # GIVEN a valid username and signup body
        username = self.make_username()
        user = {'username': username, 'email': username + '@hedy.com', 'mail_repeat': username + '@hedy.com',
                'password': 'foobar', 'password_repeat': 'foobar', 'language': 'nl', 'keyword_language': 'en', 'agree_terms': True}

        # WHEN signing up a new user
        # THEN receive an OK response code from the server
        body = self.post_data('auth/signup', user)

        # THEN receive a body containing a token
        self.assertIsInstance(body, dict)
        self.assertIsInstance(body['token'], str)

        # FINALLY Store the user and its token for upcoming tests
        user['verify_token'] = body['token']
        USERS[username] = user

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
        # THEN receive a redirect from the server taking us to `/landing-page`
        headers = self.get_data('auth/verify?' + urllib.parse.urlencode({'username': self.username, 'token': self.user['verify_token']}), expect_http_code=302, return_headers=True)
        self.assertEqual(headers['location'], HOST + 'landing-page')

        # WHEN attepting to verify the user again (the operation should be idempotent)
        # THEN (again) receive a redirect from the server taking us to `/landing-page`
        headers = self.get_data('auth/verify?' + urllib.parse.urlencode({'username': self.username, 'token': self.user['verify_token']}), expect_http_code=302, return_headers=True)
        self.assertEqual(headers['location'], HOST + 'landing-page')

        # WHEN retrieving profile to see that the user is no longer marked with `verification_pending`
        self.given_specific_user_is_logged_in(self.username)
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
        self.destroy_current_user()

        # WHEN retrieving the profile of the user
        # THEN receive a forbidden response code from the server
        self.get_data('profile', expect_http_code=403)

    def test_invalid_change_password(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN attempting change password with invalid bodies
        invalid_bodies = [
            '',
            [],
            {},
            {'old_password': 123456},
            {'old_password': 'pass1'},
            {'old_password': 'pass1', 'password': 123456},
            {'old_password': 'pass1', 'password': 'short'},
            {'old_password': 'pass1', 'password': 123456, 'password_repeat': 'panda'},
            {'old_password': 'pass1', 'password_repeat': 'panda'},
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/change_password', invalid_body, expect_http_code=400)

        # WHEN attempting to change password without sending the correct old password
        # THEN receive an invalid response code from the server
        body = {'old_password': 'pass1', 'password': '123456', 'password_repeat': '123456'}
        self.post_data('auth/change_password', body, expect_http_code=403)

    def test_change_password(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN attempting to change the user's password
        new_password = 'pas1234'
        # THEN receive an OK response code from the server
        self.post_data('auth/change_password', {'old_password': self.user['password'],
                                                'password': 'pas1234', 'password_repeat': 'pas1234'})

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
            {'gender': 0},
            {'gender': 'a'},
            {'language': True},
            {'language': 123},
            {'keyword_language': True},
            {'keyword_language': 123},
        ]

        for invalid_body in invalid_bodies:
            # Create a valid body that we overwrite with invalid values
            if isinstance(invalid_body, dict):
                body = {
                    'email': self.user['email'],
                    'language': self.user['language'],
                    'keyword_language': self.user['keyword_language']
                }
                body.update(invalid_body)
                invalid_body = body
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
           'gender': 'o'
        }

        body = {
            'email': self.user['email'],
            'language': self.user['language'],
            'keyword_language': self.user['keyword_language']
        }
        for key in profile_changes:
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
        body = self.post_data('profile', {'email': new_email, 'language': self.user['language'], 'keyword_language': self.user['keyword_language']})

        # THEN confirm that the server replies with an email verification token
        self.assertIsInstance(body['token'], str)

        # FINALLY update the email & email verification token on user
        self.user['email'] = new_email
        self.user['verify_token'] = body['token']

    def test_invalid_change_language(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN trying to update the profile with an invalid language
        body = {
            'email': self.user['email'],
            'language': 'abc',
            'keyword_language': self.user['keyword_language']
        }
        # THEN receive an invalid response code from the server
        self.post_data('profile', body, expect_http_code=400)

    def test_valid_change_language(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN trying to update the profile with a valid language
        body = {
            'email': self.user['email'],
            'language': 'nl',
            'keyword_language': 'nl'
        }
        # THEN receive a valid response code from the server
        self.post_data('profile', body, expect_http_code=200)

        # WHEN trying to retrieve the current profile
        profile = self.get_data('profile')
        # THEN verify that the language is successfully changed
        self.assertEqual(profile['language'], body['language'])

    def test_invalid_keyword_language(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN trying to update the profile with an invalid keyword language
        invalid_keyword_language = [
            'nl',
            123,
            'panda'
        ]

        body = {
            'email': self.user['email'],
            'language': 'en'
        }
        for invalid_lang in invalid_keyword_language:
            body['keyword_language'] = invalid_lang
            # THEN receive an invalid response code from the server
            self.post_data('profile', body, expect_http_code=400)

    def test_valid_keyword_language(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # WHEN trying to update the profile with a valid keyword language
        body = {
            'email': self.user['email'],
            'language': 'nl',
            'keyword_language': 'nl'
        }
        # THEN receive a valid response code from the server
        self.post_data('profile', body, expect_http_code=200)

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
            {'username': 'foobar', 'token': 'some', 'password': 'short'},
            {'username': 'foobar', 'token': 'some', 'password': 'short', 'password_repeat': 123},
            {'username': 'foobar', 'token': 'some', 'password_repeat': 'panda123'}
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/reset', invalid_body, expect_http_code=400)

        # WHEN attempting a password reset with an invalid token
        # THEN receive a forbidden response code from the server
        self.post_data('auth/reset', {'username': self.username, 'password': '123456',
                                      'password_repeat': '123456', 'token': 'foobar'}, expect_http_code=403)

    def test_reset_password(self):
        # GIVEN an existing user
        self.given_any_user()

        # WHEN attempting a password reset with a valid username & token combination
        new_password = 'pas1234'
        recover_token = self.post_data('auth/recover', {'username': self.username})['token']
        # THEN receive an OK response code from the server
        self.post_data('auth/reset', {'username': self.username, 'password': new_password,
                                      'password_repeat': new_password, 'token': recover_token})

        # WHEN attempting a login with the new password
        # THEN receive an OK response code from the server
        self.post_data('auth/login', {'username': self.username, 'password': new_password})

        # FINALLY update user's password and attempt login with new password
        self.user['password'] = new_password

    def test_invalid_public_profile(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # Create a program -> make sure it is not public
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}
        program_id = self.post_data('programs', program)['id']

        # WHEN attempting to create a public profile with invalid bodies
        invalid_bodies = [
            '',
            [],
            {},
            {'image': 123456},
            {'image': '123'},
            {'image': '123', 'personal_text': 123},
            {'image': '123', 'personal_text': 123},
            {'image': '123', 'personal_text': 123, 'favourite_program': 123},
            {'image': '123', 'personal_text': 'Welcome to my profile!', 'favourite_program': 123},
            {'image': '5', 'personal_text': 'Welcome to my profile!', 'favourite_program': 123},
            {'image': '5', 'personal_text': 'Welcome to my profile!', 'favourite_program': "abcdefghi"},
            {'image': '5', 'personal_text': 'Welcome to my profile!', 'favourite_program': program_id},
        ]
        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('auth/public_profile', invalid_body, expect_http_code=400)

    def test_public_profile_without_favourite(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        public_profile = {'image': '9', 'personal_text': 'welcome to my profile!'}

        # WHEN creating a new public profile
        # THEN receive an OK response code from the server
        self.post_data('auth/public_profile', public_profile, expect_http_code=200)

    def test_public_profile_with_favourite(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        # Create a program that is public -> can be set as favourite on the public profile
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': True}
        program_id = self.post_data('programs', program)['id']

        public_profile = {'image': '9', 'personal_text': 'welcome to my profile!', 'favourite_program': program_id}

        # WHEN creating a new public profile with favourite program
        # THEN receive an OK response code from the server
        self.post_data('auth/public_profile', public_profile, expect_http_code=200)

    def test_destroy_public_profile(self):
        # GIVEN a logged in user
        self.given_user_is_logged_in()

        public_profile = {'image': '9', 'personal_text': 'welcome to my profile!'}

        # WHEN creating a new public profile with favourite program
        # THEN receive an OK response code from the server
        self.post_data('auth/public_profile', public_profile, expect_http_code=200)

        # WHEN destroying the public profile
        # THEN receive an OK response from the server
        self.post_data('auth/destroy_public', public_profile, expect_http_code=200)


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
        self.post_data('programs', {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}, expect_http_code=403, no_cookie=True)

    def test_create_program(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has no programs yet)
        self.given_fresh_user_is_logged_in()

        # WHEN submitting a valid program
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}
        # THEN receive an OK response code from the server
        program = self.post_data('programs', program)
        # THEN verify that the returned program has both a name and an id
        self.assertIsInstance(program, dict)
        self.assertIsInstance(program['id'], str)
        self.assertIsInstance(program['name'], str)

        # WHEN retrieving programs after saving a program
        saved_programs = self.get_data('programs_list')['programs']
        print(saved_programs)

        # THEN verify that the program we just saved is in the list
        self.assertEqual(len(saved_programs), 1)
        saved_program = saved_programs[0]
        for key in program:
            # WHEN we create a program an achievement is achieved, being in the response but not the saved_program
            if key != "achievements" and key != "message":
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
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}
        program_id = self.post_data('programs', program)['id']

        # WHEN making a program public
        # THEN receive an OK response code from the server
        self.post_data('programs/share', {'id': program_id, 'public': True,})

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
        self.get_data('hedy/1/' + program_id, expect_http_code=200)

    def test_valid_make_program_private(self):
        # GIVEN a logged in user with at least one public program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}
        program_id = self.post_data('programs', program)['id']
        self.post_data('programs/share', {'id': program_id, 'public': True})

        # WHEN making a program private
        # THEN receive an OK response code from the server
        self.post_data('programs/share', {'id': program_id, 'public': False})

        saved_programs = self.get_data('programs_list')['programs']
        for program in saved_programs:
            if program['id'] != program_id:
                continue
            # THEN the program must have a '0' value for Public
            self.assertEqual('public', 0)

        # GIVEN another user
        self.given_fresh_user_is_logged_in()
        # WHEN requesting a public program
        # THEN receive a not found response code from the server
        self.get_data('hedy/1/' + program_id, expect_http_code=404)

    def test_invalid_delete_program(self):
        # GIVEN a logged in user with at least one program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}
        self.post_data('programs', program)['id']
        program_id = '123456'

        # WHEN deleting a program that does not exist
        # THEN receive a not found response code from the server
        self.post_data('programs/delete/', {'id': program_id}, expect_http_code=404)

    def test_valid_delete_program(self):
        # GIVEN a logged in user with at least one program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}
        program_id = self.post_data('programs', program)['id']

        # WHEN deleting a program
        # THEN receive an OK response code from the server
        headers = self.post_data('programs/delete/', {'id': program_id}, return_headers=True)

        saved_programs = self.get_data('programs_list')['programs']
        for program in saved_programs:
            # THEN the program should not be any longer in the list of programs
            self.assertNotEqual(program['id'], program_id)

    def test_destroy_account_with_programs(self):
        # GIVEN a logged in user with at least one program
        self.given_user_is_logged_in()
        program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}
        program_id = self.post_data('programs', program)['id']

        # WHEN deleting the user account
        # THEN receive an OK response code from the server
        self.destroy_current_user()


class TestClasses(AuthHelper):
    def test_invalid_create_class(self):
        # GIVEN a new user
        # (we create a new user to ensure that the user has no teacher permissions yet)
        self.given_fresh_user_is_logged_in()

        # WHEN creating a class without teacher permissions
        # THEN receive a forbidden response code from the server
        self.post_data('class', {'name': 'class1'}, expect_http_code=403)

        # WHEN marking the user as teacher
        self.make_current_user_teacher()

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
        self.given_fresh_teacher_is_logged_in()

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
        Class = self.get_data('for-teachers/class/' + Class['id'])

        # THEN validate the fields of the class
        self.assertIsInstance(Class, dict)
        self.assertIsInstance(Class['id'], str)
        self.assertIsInstance(Class['link'], str)
        self.assertEqual(Class['name'], 'class1')
        self.assertIsInstance(Class['students'], list)
        self.assertEqual(len(Class['students']), 0)

    def test_invalid_update_class(self):
        # GIVEN a user with teacher permissions and a class
        self.given_teacher_is_logged_in()
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
        self.given_teacher_is_logged_in()
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # WHEN attempting to update a class
        # THEN receive an OK status code from the server
        self.post_data('class/' + Class['id'], {'name': 'class2'}, put_data=True)

        # WHEN retrieving the class
        # THEN receive an OK response code from the server
        Class = self.get_data('for-teachers/class/' + Class['id'])

        # THEN the name of the class should be updated
        self.assertEqual(Class['name'], 'class2')

    def test_join_class(self):
        # GIVEN a teacher
        self.given_teacher_is_logged_in()

        # GIVEN a class
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # WHEN attempting to join a class without being logged in
        # THEN receive a forbidden status code from the server
        self.post_data('class/join', {'id': Class['id']}, no_cookie=True, expect_http_code=403)

        # GIVEN a student (user without teacher permissions)
        self.given_fresh_user_is_logged_in()
        student = self.user

        # WHEN retrieving the short link of a class
        # THEN receive a redirect to `class/ID/join/LINK`
        body = self.get_data('hedy/l/' + Class['link'], expect_http_code=302)
        if not re.search(HOST + 'class/' + Class['id'] + '/prejoin/' + Class['link'], body):
            raise Exception('Invalid or missing redirect link')

        # WHEN joining a class
        # THEN we receive a 200 code
        body = self.post_data('class/join', {'id': Class['id']}, expect_http_code=200)

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
        # GIVEN a teacher (no classes yet)
        self.given_fresh_teacher_is_logged_in()
        teacher = self.user
        # GIVEN a class
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # GIVEN a student (user without teacher permissions) that has joined the class
        self.given_fresh_user_is_logged_in()
        student = self.user
        self.post_data('class/join', {'id': Class['id']}, expect_http_code=200)

        # GIVEN the aforementioned teacher
        self.switch_user(teacher)

        # WHEN retrieving the class with a student in it
        Class_data = self.get_data('for-teachers/class/' + Class['id'])
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
        # GIVEN a teacher (no classes yet)
        self.given_fresh_teacher_is_logged_in()
        teacher = self.user
        # GIVEN a class
        self.post_data('class', {'name': 'class1'})
        Class = self.get_data('classes') [0]

        # GIVEN a student (user without teacher permissions) that has joined the class and has a public program
        self.given_fresh_user_is_logged_in()
        student = self.user
        self.post_data('class/join', {'id': Class['id']}, expect_http_code=200)
        # GIVEN a student with two programs, one public and one private
        public_program = {'code': 'hello world', 'name': 'program 1', 'level': 1, 'shared': False}
        public_program_id = self.post_data('programs', public_program)['id']
        self.post_data('programs/share', {'id': public_program_id, 'public': True})
        private_program = {'code': 'hello world', 'name': 'program 2', 'level': 2, 'shared': False}
        private_program_id = self.post_data('programs', private_program)['id']

        # GIVEN the aforementioned teacher
        self.switch_user(teacher)

        # WHEN retrieving the class with a student in it
        Class_data = self.get_data('for-teachers/class/' + Class['id'])
        # THEN the class should contain a student with valid fields
        self.assertEqual(len(Class_data['students']), 1)


class TestCustomizeClasses(AuthHelper):
    def test_not_allowed_customization(self):
        # GIVEN a new user without teacher permissions
        self.given_fresh_user_is_logged_in()

        # We create a fake class_id as the access should be denied before checking if the class exists
        class_id = "123"

        # WHEN customizing a class without being a teacher
        # THEN receive a forbidden response code from the server
        self.post_data('for-teachers/customize-class/' + class_id, {}, expect_http_code=403)

    def test_invalid_customization(self):
        # GIVEN a user with teacher permissions
        # (we create a new user to ensure that the user has no classes yet)
        self.given_fresh_teacher_is_logged_in()

        # WHEN creating a class
        # THEN receive an OK response code with the server
        # AND retrieve the class_id from the first class of your classes
        self.post_data('class', {'name': 'class1'})
        class_id = self.get_data('classes')[0].get('id')

        # WHEN attempting to create an invalid customization
        invalid_bodies = [
            '',
            [],
            {},
            {'levels': 1},
            {'levels': [1, 2, 3]},
            {'levels': [1, 2, 3], 'adventures': []},
            {'levels': [1, 2, 3], 'adventures': {}},
            {'levels': [1, 2, 3], 'adventures': {}, 'opening_dates': {}},
            {'levels': [1, 2, 3], 'adventures': {}, 'opening_dates': {}, 'teacher_adventures': []}
        ]

        for invalid_body in invalid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('for-teachers/customize-class/' + class_id, invalid_body, expect_http_code=400)

        # WHEN customizing a class that doesn't exist
        # THEN receive a not found response code from the server
        self.post_data('for-teachers/customize-class/123' + class_id, {}, expect_http_code=404)

    def test_valid_customization(self):
        # GIVEN a user with teacher permissions
        # (we create a new user to ensure that the user has no classes yet)
        self.given_fresh_teacher_is_logged_in()

        # WHEN creating a class
        # THEN receive an OK response code with the server
        # AND retrieve the class_id from the first class of your classes
        self.post_data('class', {'name': 'class1'})
        class_id = self.get_data('classes')[0].get('id')

        valid_bodies = [
            {'levels': [], 'adventures': {}, 'opening_dates': {}, 'teacher_adventures': [], 'other_settings': []},
            {'levels': ['1'], 'adventures': {'story': ['1']}, 'opening_dates': {'1': '2022-03-16'}, 'teacher_adventures': [], 'other_settings': []},
            {'levels': ['1', '2', '3'], 'opening_dates': {'1': '', '2': '', '3': ''},
             'adventures': {'story': [], 'parrot': [], 'songs': [], 'turtle': [], 'dishes': [], 'dice': [], 'rock': [],
                            'calculator': [], 'restaurant': [], 'fortune': [], 'haunted': [], 'piggybank': [],
                            'quizmaster': [], 'language': [], 'next': [], 'end': []}, 'teacher_adventures': [],
             'other_settings': []},
            {'levels': ['1', '2', '3'], 'opening_dates': {'1': '', '2': '', '3': ''},
             'adventures': {'story': ['1', '2', '3'], 'parrot': ['1', '2', '3'], 'songs': [], 'turtle': ['1', '2', '3'],
                            'dishes': ['3'], 'dice': ['3'], 'rock': ['1', '2', '3'], 'calculator': [],
                            'restaurant': ['1', '2', '3'], 'fortune': ['1', '3'], 'haunted': ['1', '2', '3'],
                            'piggybank': [], 'quizmaster': [], 'language': [], 'next': ['1', '2', '3'],
                            'end': ['1', '2', '3']}, 'teacher_adventures': [],
             'other_settings': ['developers_mode', 'hide_cheatsheet']}
        ]

        for valid_body in valid_bodies:
            # THEN receive an invalid response code from the server
            self.post_data('for-teachers/customize-class/' + class_id, valid_body, expect_http_code=200)

    def test_remove_customization(self):
        # GIVEN a user with teacher permissions
        # (we create a new user to ensure that the user has no classes yet)
        self.given_fresh_teacher_is_logged_in()

        # WHEN creating a class
        # THEN receive an OK response code with the server
        # AND retrieve the class_id from the first class of your classes
        self.post_data('class', {'name': 'class1'})
        class_id = self.get_data('classes')[0].get('id')

        # WHEN creating class customizations
        # THEN receive an OK response code with the server
        body = {'levels': [], 'adventures': {}, 'opening_dates': {}, 'teacher_adventures': [], 'other_settings': []}
        self.post_data('for-teachers/customize-class/' + class_id, body, expect_http_code=200)

        # WHEN deleting class customizations
        # THEN receive an OK response code with the server
        self.delete_data('for-teachers/customize-class/' + class_id, expect_http_code=200)


class TestCustomAdventures(AuthHelper):
    def test_not_allowed_create_adventure(self):
        # GIVEN a new user without teacher permissions
        self.given_fresh_user_is_logged_in()

        # WHEN trying to create a custom adventure
        # THEN receive a forbidden response code from the server
        self.post_data('for-teachers/create_adventure', {}, expect_http_code=403)

    def test_invalid_create_adventure(self):
        # GIVEN a new teacher
        self.given_fresh_teacher_is_logged_in()

        # WHEN attempting to create an invalid adventure
        invalid_bodies = [
            '',
            [],
            {},
            {'name': 123}
        ]

        for invalid_body in invalid_bodies:
            self.post_data('for-teachers/create_adventure', invalid_body, expect_http_code=400)

        # WHEN attempting to create an adventure that already exists
        # THEN receive an 400 error from the server
        self.post_data('for-teachers/create_adventure', {'name': 'test_adventure'}, expect_http_code=200)
        self.post_data('for-teachers/create_adventure', {'name': 'test_adventure'}, expect_http_code=400)

    def test_create_adventure(self):
        # GIVEN a new teacher
        self.given_fresh_teacher_is_logged_in()

        # WHEN attempting to create a valid adventure
        # THEN receive an OK response with the server
        self.post_data('for-teachers/create_adventure', {'name': 'test_adventure'}, expect_http_code=200)

    def test_invalid_view_adventure(self):
        # GIVEN a new user
        self.given_fresh_user_is_logged_in()

        # WHEN attempting to view a custom adventure
        # THEN receive a 403 error from the server
        self.get_data('for-teachers/customize-adventure/view/123', expect_http_code=403)

        # GIVEN a new teacher
        self.given_fresh_teacher_is_logged_in()

        # WHEN attempting to view a custom adventure that doesn't exist
        # THEN receive a 404 error from the server
        self.get_data('for-teachers/customize-adventure/view/123', expect_http_code=404)

    def test_valid_view_adventure(self):
        # GIVEN a new teacher
        self.given_fresh_teacher_is_logged_in()

        # WHEN attempting to create a valid adventure
        # THEN receive an OK response with the server
        adventure_id = self.post_data('for-teachers/create_adventure', {'name': 'test_adventure'}, expect_http_code=200).get("id")

        # WHEN attempting to view the adventure using the id from the returned body
        # THEN receive an OK response with the server
        self.get_data('for-teachers/customize-adventure/view/' + adventure_id)

    def test_invalid_update_adventure(self):
        # GIVEN a new teacher
        self.given_fresh_teacher_is_logged_in()

        # WHEN attempting to create a valid adventure
        # THEN receive an OK response with the server
        adventure_id = self.post_data('for-teachers/create_adventure', {'name': 'test_adventure'}, expect_http_code=200).get("id")

        # WHEN attempting to updating an adventure with invalid data
        invalid_bodies = [
            '',
            [],
            {},
            {'id': 123},
            {'id': 123, 'name': 123},
            {'id': '123', 'name': 123},
            {'id': '123', 'name': 123, 'level': 5},
            {'id': '123', 'name': 123, 'level': 5, 'content': 123},
            {'id': adventure_id, 'name': 'panda', 'level': '5', 'content': 'too short!'},
            {'id': adventure_id, 'name': 'panda', 'level': '5', 'content': 'This is just long enough!', 'public': 'panda'},
        ]

        # THEN receive a 400 error from the server
        for invalid_body in invalid_bodies:
            self.post_data('for-teachers/customize-adventure', invalid_body, expect_http_code=400)

        # WHEN attempting to update a non-existing adventure
        # THEN receive a 404 error from the server
        body = {'id': '123', 'name': 'panda', 'level': '5', 'content': 'This is just long enough!', 'public': True}
        self.post_data('for-teachers/customize-adventure', body, expect_http_code=404)

    def test_valid_update_adventure(self):
        # GIVEN a new teacher
        self.given_fresh_teacher_is_logged_in()

        # WHEN attempting to create a valid adventure
        # THEN receive an OK response from the server
        adventure_id = self.post_data('for-teachers/create_adventure', {'name': 'test_adventure'}, expect_http_code=200).get("id")

        # WHEN attempting to update an adventure with a valid body
        # THEN receive an OK response from the server
        body = {'id': adventure_id, 'name': 'test_adventure', 'level': '5', 'content': 'This is just long enough!', 'public': True}
        self.post_data('for-teachers/customize-adventure', body, expect_http_code=200)

    def test_destroy_adventure(self):
        # GIVEN a user with teacher permissions
        # (we create a new user to ensure that the user has no classes yet)
        self.given_fresh_teacher_is_logged_in()

        # WHEN attempting to create a valid adventure
        # THEN receive an OK response from the server
        body = self.post_data('for-teachers/create_adventure', {'name': 'test_adventure'}, expect_http_code=200)

        # WHEN attempting to remove the adventure
        # THEN receive an OK response from the server
        self.delete_data('for-teachers/customize-adventure/' + body.get('id', ""), expect_http_code=200)

# *** CLEANUP OF USERS CREATED DURING THE TESTS ***

def tearDownModule ():
    auth_helper = AuthHelper()
    auth_helper.setUp()
    for username in USERS.copy():
        auth_helper.given_specific_user_is_logged_in(username)
        auth_helper.destroy_current_user()
