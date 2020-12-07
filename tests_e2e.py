import requests
import json
import random
from utils import type_check, timems

# TODO: unhardcode port
host = 'http://localhost:5000/'

t0 = timems ()

state = {'headers': {}}

# test structure: tag method path headers body code
def request(test, counter):

    start = timems ()

    print ('Start #' + str (counter) + ': ' + test [0])

    # If no explicit cookie passed, use the one from the state
    if not 'cookie' in test [3] and 'cookie' in state ['headers']:
        test [3] ['cookie'] = state ['headers'] ['cookie']

    if type_check (test[4], 'dict'):
        test[3] ['content-type'] = 'application/json'
        test[4] = json.dumps (test [4])
    r = getattr (requests, test [1])(host + test [2], headers=test[3], data=test[4])

    if 'Content-Type' in r.headers and r.headers ['Content-Type'] == 'application/json':
        body = r.json ()
    else:
        body = r.text

    if len (test) == 7:
        test [6] (state, {
            'code':    r.status_code,
            'headers': r.headers,
            'body':    body
        })
    print ('Done  #' + str (counter) + ': ' + test [0] + ' - ' + str (r.status_code) + ' (' + str (timems () - start) + 'ms)')
    return {
        'code':    r.status_code,
        'headers': r.headers,
        'body':    body
    }

def run_suite(tests):
    if not type_check(tests, 'list'):
        return print ('Invalid test suite, must be a list.')
    counter = 1

    def run_test(test, counter):
        result = request(test, counter)
        if (result ['code'] != test[5]):
            print (result)
            raise Exception ('A test failed!')

    for test in tests:
        # If test is nested, run a nested loop
        if not (type_check(test[0], 'str')):
            for subtest in test:
                run_test(subtest, counter)
                counter += 1
        else:
           run_test(test, counter)
           counter += 1

    print ('Test suite successful! (' + str (timems () - t0) + 'ms)')

def invalidMap(tag, method, path, bodies):
    output = []
    counter = 1
    for body in bodies:
        output.append (['invalid ' + tag + ' #' + str (counter), method, path, {}, body, 400])
        counter += 1
    return output

# We use a random username so that if a test fails, we don't have to do a cleaning of the DB so that the test suite can run again
username = str (random.randint (10000, 100000))

# We define apres functions here because multiline lambdas are not supported by python
def successfulLogin(state, response):
    state ['headers'] ['cookie'] = response ['headers'] ['Set-Cookie']

def getProfile1(state, response):
    profile = response ['body']
    if response ['body'] ['username'] != username:
        raise Exception ('Invalid username (getProfile1)')
    if response ['body'] ['email'] != username + '@domain.com':
        raise Exception ('Invalid username (getProfile1)')

def getProfile2(state, response):
    profile = response ['body']
    if response ['body'] ['country'] != 'NL':
        raise Exception ('Invalid country (getProfile1)')
    if response ['body'] ['email'] != username + '@domain2.com':
        raise Exception ('Invalid country (getProfile1)')

suite = [
    ['get root', 'get', '/', {}, '', 200],
    invalidMap ('signup', 'post', '/auth/signup', ['', [], {}, {'username': 1}, {'username': 'user@me'}, {'username:': 'user: me'}, {'username': username}, {'username': username, 'password': 1}, {'username': username, 'password': 'foo'}, {'username': username, 'password': 'foobar'}, {'username': username, 'password': 'foobar', 'email': 'me@something'}]),
    ['valid signup', 'post', '/auth/signup', {}, {'username': username, 'password': 'foobar', 'email': username + '@domain.com'}, 200],
    invalidMap ('login', 'post', '/auth/login', ['', [], {}, {'username': 1}, {'username': 'user@me'}, {'username:': 'user: me'}]),
    ['valid login, invalid credentials', 'post', '/auth/login', {}, {'username': username, 'password': 'password'}, 403],
    ['valid login', 'post', '/auth/login', {}, {'username': username, 'password': 'foobar'}, 200, successfulLogin],
    ['change password', 'post', '/auth/changePassword', {}, {'oldPassword': 'foobar', 'newPassword': 'foobar2'}, 200],
    ['invalid login after password change', 'post', '/auth/login', {}, {'username': username, 'password': 'foobar'}, 403],
    ['valid login after password change', 'post', '/auth/login', {}, {'username': username, 'password': 'foobar2'}, 200, successfulLogin],
    ['logout', 'post', '/auth/logout', {}, {}, 200],
    ['check that session is no longer valid', 'get', '/profile', {}, '', 403],
    ['login again', 'post', '/auth/login', {}, {'username': username, 'password': 'foobar2'}, 200, successfulLogin],
    ['get profile before profile update', 'get', '/profile', {}, {}, 200, getProfile1],
    ['change profile', 'post', '/profile', {}, {'email': username + '@domain2.com', 'country': 'NL'}, 200],
    ['get profile before profile update', 'get', '/profile', {}, {}, 200, getProfile2],
    ['destroy account', 'post', '/auth/destroy', {}, {}, 200]
]

run_suite (suite)
