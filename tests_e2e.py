# *** NATIVE DEPENDENCIES ***
import threading
import random
import json
import urllib.parse

# *** LIBRARIES ***
import pytest
import unittest
import requests

# *** HEDY RESOURCES ***
import utils
from config import config as CONFIG

# *** GLOBAL VARIABLES ***

HOST = 'http://localhost:' + str (CONFIG ['port']) + '/'
# This dict has global scope and holds all created users and their still current sessions (as cookies), for convenient reuse wherever needed
USERS = {}

# *** HELPERS ***

def request (method, path, headers={}, body=''):

    if method not in ['get', 'post', 'put', 'delete']:
        raise Exception ('request - Invalid method: ' + str (method))

    # We pass the X-Testing header to let the server know that this is a request coming from an E2E test, thus no transactional emails should be sent.
    headers ['X-Testing'] = '1'

    # If sending an object as body, stringify it and set the proper content-type header
    if isinstance (body, dict):
        headers ['content-type'] = 'application/json'
        body = json.dumps (body)

    start = utils.timems ()

    request = getattr (requests, method) (HOST + path, headers=headers, data=body)

    response = {'time': utils.timems () - start}

    if request.history and request.history [0]:
        # This code branch will be executed if there is a redirect
        response ['code']    = request.history [0].status_code
        response ['headers'] = request.history [0].headers
        if getattr (request.history [0], '_content'):
            # We can assume that bodies returned from redirected responses are always plain text, since no JSON endpoint in the server is reachable through a redirect.
            response ['body'] = getattr (request.history [0], '_content').decode ('utf-8')
    else:
        response ['code']    = request.status_code
        response ['headers'] = request.headers
        if 'Content-Type' in request.headers and request.headers ['Content-Type'] == 'application/json':
            response ['body'] = request.json ()
        else:
            response ['body'] = request.text

    return response

def makeUsername ():
    # We create usernames with a random component so that if a test fails, we don't have to do a cleaning of the DB so that the test suite can run again
    # This also allows us to run concurrent tests without having username conflicts.
    username = 'user' + str (random.randint (10000, 100000))
    return username

class AuthHelper ():
    def assertUserExists (username):
        if not isinstance (username, str):
            raise Exception ('AuthHelper.assertUserExists - Invalid username: ' + str (username))

        if username in USERS:
            return USERS [username]
        body = {'username': username, 'email': username + '@hedy.com', 'password': 'foobar'}
        response = request ('post', 'auth/signup', {}, body)

        # Store the user & also the verify token for use in upcoming tests
        USERS [username] = body
        USERS [username] ['token'] = response ['body'] ['token']
        return USERS [username]

# *** TESTS ***

class TestSignup (unittest.TestCase):
    def test_InvalidSignups (self):
        username = makeUsername ()
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
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'prog_experience': [2]},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'prog_experience': 'foo'},
            {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'experience_languages': 'python'}
        ]
        for invalid_body in invalid_bodies:
            response = request ('post', 'auth/signup', {}, invalid_body)
            self.assertEqual (response ['code'], 400)

    def test_ValidSignup (self):
        username = makeUsername ()
        body = {'username': username, 'email': username + '@hedy.com', 'password': 'foobar'}

        response = request ('post', 'auth/signup', {}, body)
        self.assertEqual (response ['code'], 200)
        self.assertIsInstance (response ['body'], dict)
        self.assertIsInstance (response ['body'] ['token'], str)

        # Store the user for use in upcoming tests
        USERS [username] = body
        USERS [username] ['token'] = response ['body'] ['token']

class TestLogin (unittest.TestCase):
    def test_InvalidLogins (self):
        username = makeUsername ()
        invalid_bodies = [
            '',
            [],
            {},
            {'username': 1},
            {'username': 'user@me'},
            {'username:': 'user: me'}
        ]
        for invalid_body in invalid_bodies:
            response = request ('post', 'auth/login', {}, invalid_body)
            self.assertEqual (response ['code'], 400)

    def test_LoginVerifyFlow (self):
        username = makeUsername () if len (USERS.keys ()) == 0 else next (iter (USERS))
        # We create a new user to ensure that the verification flow hasn't been done by the user yet
        user = AuthHelper.assertUserExists (username)

        invalid_verifications = [
            # Missing username & missing token
            {'username': username},
            {'token': user ['token']},
        ]

        for invalid_verification in invalid_verifications:
            response = request ('get', 'auth/verify?' + urllib.parse.urlencode (invalid_verification))
            self.assertEqual (response ['code'], 400)

        incorrect_verifications = [
            # Invalid username & invalid token
            {'username': 'foobar', 'token': user ['token']},
            # Invalid username & invalid token
            {'username': username, 'token': 'foobar'}
        ]

        for incorrect_verification in incorrect_verifications:
            response = request ('get', 'auth/verify?' + urllib.parse.urlencode (incorrect_verification))
            self.assertEqual (response ['code'], 403)

        response = request ('get', 'auth/verify?' + urllib.parse.urlencode ({'username': username, 'token': user ['token']}))
        self.assertEqual (response ['code'], 302)
        self.assertEqual (response ['headers'] ['location'], HOST)

        # Attempt verification again, operation should be idempotent
        response = request ('get', 'auth/verify?' + urllib.parse.urlencode ({'username': username, 'token': user ['token']}))
        self.assertEqual (response ['code'], 302)
        self.assertEqual (response ['headers'] ['location'], HOST)

# Notes/TODO
# pytest doesn't seem to run subclasses, so my idea of auth to contain both signup & login didn't work
