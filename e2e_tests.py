import requests
import json
import random
from utils import timems
import urllib.parse
from config import config
import sys
import threading
import re

# USAGE: python e2e_tests.py [CONCURRENT_TESTS] [alpha|test]
# Concurrent tests are a way to stress test an environment
# When no environment is specified, the tests are run against localhost

import argparse
args = argparse.ArgumentParser ()
args.add_argument ('--concurrent', help='how many tests to run at the same time (stress testing), default is 1', type=int)
args.add_argument ('--host', help='Host against which to run the tests (optional), default is localhost')
args.add_argument ('--endpoint', help='Endpoint against which to run the tests (optional, by default \'--host\' is used)')
args = args.parse_args ()

host = 'http://localhost:' + str (config ['port']) + '/'
hosts = {'alpha': 'https://hedy-alpha.herokuapp.com/', 'test': 'https://hedy-test.herokuapp.com/'}

if args.endpoint:
  host = args.endpoint

elif args.host:
    if not args.host in hosts:
        raise Exception ('No such host')
    host = hosts [sys.argv [2]]

# test structure: [tag, method, path, headers, body, code, after_test_function]
def request (state, test, counter, username):

    start = timems ()

    if isinstance (threading.current_thread (), threading._MainThread):
        print ('Start #' + str (counter) + ': ' + test [0])

    # If path, headers or body are functions, invoke them passing them the current state
    if callable(test[2]):
        test[2] = test[2] (state)

    if callable (test[3]):
        test[3] = test[3] (state)

    if callable(test[4]):
        test[4] = test[4] (state)

    # If no explicit cookie passed, use the one from the state
    if not 'cookie' in test [3] and 'cookie' in state ['headers']:
        test [3] ['cookie'] = state ['headers'] ['cookie']

    if isinstance(test[4], dict):
        test[3] ['content-type'] = 'application/json'
        test[4] = json.dumps (test [4])

    # We pass the X-Testing header to let the server know that this is a request coming from an E2E test, thus no transactional emails should be sent.
    test [3] ['X-Testing'] = '1'

    r = getattr (requests, test [1]) (host + test [2], headers=test[3], data=test[4])

    if 'Content-Type' in r.headers and r.headers ['Content-Type'] == 'application/json':
        body = r.json ()
    else:
        body = r.text

    if r.history and r.history [0]:
        # This will be the case if there's a redirect
        code = r.history [0].status_code
        headers = r.history [0].headers
        if getattr (r.history [0], '_content'):
            body = getattr (r.history [0], '_content').decode ('utf-8')
    else:
        code = r.status_code

    output = {
        'code':    code,
        'headers': r.headers,
        'body':    body
    }

    if (code != test[5]):
        print (output)
        raise Exception ('A test failed!')

    if len (test) == 7:
        test [6] (state, output, username)

    if isinstance (threading.current_thread (), threading._MainThread):
        print ('Done  #' + str (counter) + ': ' + test [0] + ' - ' + str (r.status_code) + ' (' + str (timems () - start) + 'ms)')

    return output

def run_suite (suite):
    # We use a random username so that if a test fails, we don't have to do a cleaning of the DB so that the test suite can run again
    # This also allows us to run concurrent tests without having username conflicts.
    username = 'user' + str (random.randint (10000, 100000))
    tests = suite (username)
    state = {'headers': {}}
    t0 = timems ()

    if not isinstance (tests, list):
        return print ('Invalid test suite, must be a list.')
    counter = 1

    def run_test (test, counter):
        result = request (state, test, counter, username)

    for test in tests:
        # If test is nested, run a nested loop
        if not (isinstance (test[0], str)):
            for subtest in test:
                run_test (subtest, counter)
                counter += 1
        else:
           run_test (test, counter)
           counter += 1

    if isinstance (threading.current_thread (), threading._MainThread):
        print ('Test suite successful! (' + str (timems () - t0) + 'ms)')
    else:
        return timems () - t0

def invalidMap (tag, method, path, bodies):
    output = []
    counter = 1
    for body in bodies:
        output.append (['invalid ' + tag + ' #' + str (counter), method, path, {}, body, 400])
        counter += 1
    return output

# We define after_test_functions here because multiline lambdas are not supported by python
def setSentCookies (state, response, username):
    if 'Set-Cookie' in response ['headers']:
        state ['headers'] ['cookie'] = response ['headers'] ['Set-Cookie']

def successfulSignup (state, response, username):
    if not 'token' in response ['body']:
        raise Exception ('No token present')
    state ['token'] = response ['body'] ['token']
    setSentCookies (state, response, username)

def successfulSignupTeacher (state, response, username):
    state ['teacher-session'] = response ['headers'] ['Set-Cookie']
    setSentCookies (state, response, username)

def successfulSignupStudent (state, response, username):
    state ['student-session'] = response ['headers'] ['Set-Cookie']

def getProfile1 (state, response, username):
    profile = response ['body']
    if profile ['username'] != username:
        raise Exception ('Invalid username (getProfile1)')
    if profile ['email'] != username + '@e2e-testing.com':
        raise Exception ('Invalid username (getProfile1)')
    if not profile ['session_expires_at']:
        raise Exception ('No session_expires_at (getProfile1)')
    expire = profile ['session_expires_at'] - config ['session'] ['session_length'] * 60 * 1000 - timems ()
    if expire > 0:
        raise Exception ('Invalid session_expires_at (getProfile1), too large')
    # We give the server up to 2s to respond to the query
    if expire < -2000:
        raise Exception ('Invalid session_expires_at (getProfile1), too small')

def getProfile2 (state, response, username):
    profile = response ['body']
    if profile ['country'] != 'NL':
        raise Exception ('Invalid country (getProfile2)')
    if profile ['email'] != username + '@e2e-testing2.com':
        raise Exception ('Invalid country (getProfile2)')
    if not 'verification_pending' in profile or profile ['verification_pending'] != True:
        raise Exception ('Invalid verification_pending (getProfile2)')

def getProfile3 (state, response, username):
    profile = response ['body']
    if 'verification_pending' in profile:
        raise Exception ('Invalid verification_pending (getProfile3)')

def getProfile4 (state, response, username):
    profile = response ['body']
    if not 'verification_pending' in profile or profile ['verification_pending'] != True:
        raise Exception ('Invalid verification_pending (getProfile4)')
    if not 'prog_experience' in profile or profile ['prog_experience'] != 'yes':
        raise Exception ('Invalid prog_experience (getProfile4)')
    if not 'experience_languages' in profile or not isinstance(profile ['experience_languages'], list) or len (profile ['experience_languages']) != 1 or profile ['experience_languages'] [0] != 'python':
        raise Exception ('Invalid experience_languages (getProfile4)')

def getProfile5 (state, response, username):
    profile = response ['body']
    if not 'prog_experience' in profile or profile ['prog_experience'] != 'no':
        raise Exception ('Invalid prog_experience (getProfile5)')
    if not 'experience_languages' in profile or not isinstance(profile ['experience_languages'], list) or len (profile ['experience_languages']) != 2 or profile ['experience_languages'] [0] not in ['scratch', 'other_text'] or profile ['experience_languages'] [1] not in ['scratch', 'other_text']:
        raise Exception ('Invalid experience_languages (getProfile5)')

def emailChange (state, response, username):
    if not isinstance (response ['body'] ['token'], str):
        raise Exception ('Invalid country (emailChange)')
    if response ['body'] ['username'] != username:
        raise Exception ('Invalid username (emailChange)')
    state ['token2'] = response ['body'] ['token']

def recoverPassword (state, response, username):
    if not 'token' in response ['body']:
        raise Exception ('No token present')
    state ['token'] = response ['body'] ['token']

def checkMainSessionVars (state, response, username):
    if not 'session_id' in response ['body'] ['session']:
        raise Exception ('No session_id set')
    if not 'proxy_enabled' in response ['body']:
        raise Exception ('No proxy_enabled variable set')
    state ['session_id'] = response ['body'] ['session'] ['session_id']
    state ['proxy_enabled'] = response ['body'] ['proxy_enabled']
    setSentCookies (state, response, username)

def checkTestSessionVars (state, response, username):
    # If proxying to test is disabled, there is nothing to do.
    if not state ['proxy_enabled']:
        return
    if not 'session_id' in response ['body'] ['session']:
        raise Exception ('No session_id set')
    if not 'test_session' in response ['body'] ['session']:
        raise Exception ('No test_session set')
    if response ['body'] ['session'] ['session_id'] != state ['session_id']:
        raise Exception ('session_id from main not passed to test')
    state ['test_session'] = response ['body'] ['session'] ['test_session']
    setSentCookies (state, response, username)

def checkMainSessionVarsAgain (state, response, username):
    if not 'session_id' in response ['body'] ['session']:
        raise Exception ('No session_id set')
    if response ['body'] ['session'] ['session_id'] != state ['session_id']:
        raise Exception ('session_id from main not maintained after proxying to test')
    # If proxying to test is disabled, there is nothing else to do.
    if not state ['proxy_enabled']:
        return
    if not 'test_session' in response ['body'] ['session']:
        raise Exception ('No test_session set')
    if response ['body'] ['session'] ['test_session'] != state ['test_session']:
        raise Exception ('test_session not received by main')

def retrieveProgramsBefore (state, response, username):
    if not isinstance (response ['body'], dict):
        raise Exception ('Invalid response body')
    if not 'programs' in response ['body'] or not isinstance (response ['body'] ['programs'], list):
        raise Exception ('Invalid programs list')
    if len (response ['body'] ['programs']) != 0:
        raise Exception ('Programs list should be empty')

def retrieveProgramsAfter (state, response, username):
    if not isinstance (response ['body'], dict):
        raise Exception ('Invalid response body')
    if not 'programs' in response ['body'] or not isinstance (response ['body'] ['programs'], list):
        raise Exception ('Invalid programs list')
    if len (response ['body'] ['programs']) != 1:
        raise Exception ('Programs list should contain one program')
    program = response ['body'] ['programs'] [0]
    state ['program'] = program
    if not isinstance (program, dict):
        raise Exception ('Invalid program type')
    if not 'code' in program or program ['code'] != 'print Hello world':
        raise Exception ('Invalid program.code')
    if not 'level' in program or program ['level'] != 1:
        raise Exception ('Invalid program.level')

def getTeacherClasses1 (state, response, username):
    if not isinstance (response ['body'], list):
        raise Exception ('Classes should be a list')
    if len (response ['body']) != 0:
        raise Exception ('Classes should be empty')

def getTeacherClasses2 (state, response, username):
    if len (response ['body']) != 1:
        raise Exception ('Classes should contain one class')
    Class = response ['body'] [0]
    if not isinstance (Class.get ('date'), int):
        raise Exception ('Class should contain date')
    if not isinstance (Class.get ('id'), str):
        raise Exception ('Class should contain id')
    if not isinstance (Class.get ('link'), str):
        raise Exception ('Class should contain link')
    if Class.get ('name') != 'class1':
        raise Exception ('Invalid class name')
    if not isinstance (Class.get ('students'), list):
        raise Exception ('Class should contain a list of students')
    if len (Class.get ('students')) != 0:
        raise Exception ('Student list should be empty')
    if Class.get ('teacher') != 'teacher-' + username:
        raise Exception ('Invalid teacher')

    state ['classes'] = response ['body']

def getClass1 (state, response, username):
    Class = response ['body']
    if not isinstance (Class, dict):
        raise Exception ('Invalid response body')
    if not isinstance (Class.get ('link'), str):
        raise Exception ('Class should contain link')
    if not isinstance (Class.get ('id'), str):
        raise Exception ('Class should contain id')
    if Class.get ('name') != 'class1':
        raise Exception ('Invalid class name')
    if not isinstance (Class.get ('students'), list):
        raise Exception ('Class should contain a list of students')
    if len (Class.get ('students')) != 0:
        raise Exception ('Student list should be empty')

def getTeacherClasses3 (state, response, username):
    Class = response ['body'] [0]
    if Class.get ('name') != 'class_renamed':
        raise Exception ('Invalid class name')

def getClass2 (state, response, username):
    Class = response ['body']
    if Class.get ('name') != 'class_renamed':
        raise Exception ('Invalid class name')

def redirectAfterJoin1 (state, response, username):
    if not re.search ('http://localhost:\d\d\d\d/my-profile', response ['body']):
        raise Exception ('Invalid redirect')

def createPublicProgram (state, response, username):
    state ['public_program'] = response ['body'] ['id']

def getStudentClasses1 (state, response, username):
    classes = response ['body'].get ('student_classes')
    if not isinstance (classes, list):
        raise Exception ('Invalid classes list')
    if len (classes) != 1:
        raise Exception ('Class list should contain one item')
    Class = classes [0]
    if not isinstance (Class, dict):
        raise Exception ('Invalid class')
    if Class ['id'] != state ['classes'] [0] ['id']:
        raise Exception ('Invalid class id')
    if Class ['name'] != 'class_renamed':
        raise Exception ('Invalid class name')
    if len (Class.keys ()) != 2:
        raise Exception ('Too many fields contained in class')

def getClass3 (state, response, username):
    students = response ['body'].get ('students')
    if len (students) != 1:
        raise Exception ('Student list should contain one student')
    student = students [0]
    state ['student'] = student
    if student.get ('highest_level') != 0:
        raise Exception ('student.highest_level should be 0')
    if student.get ('programs') != 0:
        raise Exception ('student.programs should be 0')
    if student.get ('latest_shared') != None:
        raise Exception ('student.latest_shared should be None')
    if not isinstance (student.get ('last_login'), str):
        raise Exception ('student.last_login should be a string')
    if student.get ('username') != 'student-' + username:
        raise Exception ('Invalid student username')

def getClass4 (state, response, username):
    student = response ['body'].get ('students') [0]
    if student.get ('highest_level') != 1:
        raise Exception ('student.highest_level should be 0')
    if student.get ('programs') != 2:
        raise Exception ('student.programs should be 2')
    if not isinstance (student.get ('latest_shared'), dict):
        raise Exception ('student.latest_shared should be a list')
    if student.get ('latest_shared').get ('name') != 'Public program 1':
        raise Exception ('student.latest_shared.name should be "Public program 1"')
    link = student.get ('latest_shared').get ('link')
    if not re.search ('http://localhost:\d\d\d\d/hedy/' + state ['public_program'] + '/view', link):
        raise Exception ('Invalid student.latest_shared.link ' + link + ', expecting', 'http://localhost:\d\d\d\d/hedy/' + state ['public_program'] + '/view')

def getTeacherClasses4 (state, response, username):
    Class = response ['body'] [0]
    if len (Class.get ('students')) != 1:
        raise Exception ('Student list should contain a student id')
    if Class.get ('students') [0] != 'student-' + username:
        raise Exception ('Invalid student username')

def getStudentClasses2 (state, response, username):
    classes = response ['body'].get ('student_classes')
    if not isinstance (classes, list):
        raise Exception ('Invalid classes list')
    if len (classes) != 0:
        raise Exception ('Class list should be empty')

def checkJoinLink (state, response, username):
    if not re.search ('http://localhost:\d\d\d\d/class/' + state ['classes'] [0] ['id'] + '/prejoin/' + state ['classes'] [0] ['link'], response ['body']):
        raise Exception ('Invalid redirect')

def suite (username):
    return [
        # Session variables
        ['get session vars from main', 'get', '/session_main', {}, {}, 200, checkMainSessionVars],
        ['get session vars from test', 'get', '/session_test', {}, {}, 200, checkTestSessionVars],
        ['get session vars from main again', 'get', '/session_main', {}, {}, 200, checkMainSessionVarsAgain],
        # Main page
        ['get root', 'get', '/', {}, '', 200],
        # Admin page
        ['get admin', 'get', '/admin', {}, {}, 200],
        # Auth: signup
        invalidMap ('signup', 'post', '/auth/signup', ['', [], {}, {'username': 1}, {'username': 'user@me', 'password': 'foobar', 'email': 'a@a.com'}, {'username:': 'user: me', 'password': 'foobar', 'email': 'a@a.co'}, {'username': 't'}, {'username': '    t    '}, {'username': username}, {'username': username, 'password': 1}, {'username': username, 'password': 'foo'}, {'username': username, 'password': 'foobar'}, {'username': username, 'password': 'foobar', 'email': 'me@something'}, {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'prog_experience': [2]}, {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'prog_experience': 'foo'}, {'username': username, 'password': 'foobar', 'email': 'me@something.com', 'experience_languages': 'python'}]),
        ['valid signup', 'post', '/auth/signup', {}, {'username': username, 'password': 'foobar', 'email': username + '@e2e-testing.com'}, 200, successfulSignup],
        invalidMap ('login', 'post', '/auth/login', ['', [], {}, {'username': 1}, {'username': 'user@me'}, {'username:': 'user: me'}]),
        # Auth: verify & login
        ['valid login, invalid credentials', 'post', '/auth/login', {}, {'username': username, 'password': 'password'}, 403],
        ['verify email (missing fields)', 'get', lambda state: '/auth/verify?' + urllib.parse.urlencode ({'username': 'foobar', 'token': state ['token']}), {}, '', 403],
        ['verify email (invalid username)', 'get', lambda state: '/auth/verify?' + urllib.parse.urlencode ({'username': 'foobar', 'token': state ['token']}), {}, '', 403],
        ['verify email (invalid token)', 'get', lambda state: '/auth/verify?' + urllib.parse.urlencode ({'username': username, 'token': 'foobar'}), {}, '', 403],
        ['verify email', 'get', lambda state: '/auth/verify?' + urllib.parse.urlencode ({'username': username, 'token': state ['token']}), {}, '', 302],
        ['valid login', 'post', '/auth/login', {}, {'username': username, 'password': 'foobar'}, 200, setSentCookies],
        invalidMap ('change password', 'post', '/auth/change_password', ['', [], {}, {'foo': 'bar'}, {'old_password': 1}, {'old_password': 'foobar'}, {'old_password': 'foobar', 'new_password': 1}, {'old_password': 'foobar', 'new_password': 'short'}]),
        ['change password', 'post', '/auth/change_password', {}, {'old_password': 'foobar', 'new_password': 'foobar2'}, 200],
        ['invalid login after password change', 'post', '/auth/login', {}, {'username': username, 'password': 'foobar'}, 403],
        ['valid login after password change', 'post', '/auth/login', {}, {'username': username + '@e2e-testing.com', 'password': 'foobar2'}, 200, setSentCookies],
        ['logout', 'post', '/auth/logout', {}, {}, 200],
        ['check that session is no longer valid', 'get', '/profile', {}, '', 403],
        ['login again', 'post', '/auth/login', {}, {'username': username, 'password': 'foobar2'}, 200, setSentCookies],
        invalidMap ('change password', 'post', '/auth/change_password', ['', [], {}, {'foo': 'bar'}, {'old_password': 1}, {'old_password': 'foobar'}, {'old_password': 'foobar', 'new_password': 1}]),
        # Auth: profile
        ['get profile before profile update', 'get', '/profile', {}, {}, 200, getProfile1],
        invalidMap ('update profile', 'post', '/profile', ['', [], {'email': 'foobar'}, {'birth_year': 'a'}, {'birth_year': 20}, {'country': 'Netherlands'}, {'gender': 0}, {'gender': 'a'}, {'prog_experience': 1}, {'prog_experience': 'foo'}, {'experience_languages': ['python', 'foo']}]),
        ['change profile with same email', 'post', '/profile', {}, {'email': username + '@e2e-testing.com', 'country': 'US'}, 200],
        ['change profile with different email', 'post', '/profile', {}, {'email': username + '@e2e-testing2.com', 'country': 'NL'}, 200, emailChange],
        ['get profile after profile update', 'get', '/profile', {}, {}, 200, getProfile2],
        ['verify email after email change', 'get', lambda state: '/auth/verify?' + urllib.parse.urlencode ({'username': username, 'token': state ['token2']}), {}, '', 302],
        # Auth: recover & reset
        ['get profile after email verification', 'get', '/profile', {}, {}, 200, getProfile3],
        invalidMap ('recover password', 'post', '/auth/recover', ['', [], {}, {'username': 1}]),
        ['recover password, invalid user', 'post', '/auth/recover', {}, {'username': 'nosuch'}, 403],
        ['recover password', 'post', '/auth/recover', {}, {'username': username}, 200, recoverPassword],
        invalidMap ('reset password', 'post', '/auth/reset', ['', [], {}, {'username': 1}, {'username': 'foobar', 'token': 1}, {'username': 'foobar', 'token': 'some'}, {'username': 'foobar', 'token': 'some', 'password': 1}, {'username': 'foobar', 'token': 'some', 'password': 'short'}]),
        ['reset password, invalid username', 'post', '/auth/reset', {}, lambda state: {'username': 'foobar', 'token': state ['token'], 'password': 'foobar'}, 403],
        ['reset password, invalid token', 'post', '/auth/reset', {}, lambda state: {'username': username, 'token': 'foobar', 'password': 'foobar'}, 403],
        ['reset password, invalid password', 'post', '/auth/reset', {}, lambda state: {'username': username, 'token': state ['token'], 'password': 'short'}, 400],
        ['reset password', 'post', '/auth/reset', {}, lambda state: {'username': username, 'token': state ['token'], 'password': 'foobar3'}, 200],
        ['login again after reset', 'post', '/auth/login', {}, {'username': username, 'password': 'foobar3'}, 200],
        # Programs
        ['retrieve programs before saving any', 'get', '/programs_list', {}, {}, 200, retrieveProgramsBefore],
        ['create program', 'post', '/programs', {}, {'code': 'print Hello world', 'name': 'Program 1', 'level': 1}, 200],
        ['retrieve programs after saving one', 'get', '/programs_list', {}, {}, 200, retrieveProgramsAfter],
        ['share program', 'post', '/programs/share', {}, lambda state: {'id': state ['program'] ['id'], 'public': True}, 200],
        ['unshare program', 'post', '/programs/share', {}, lambda state: {'id': state ['program'] ['id'], 'public': False}, 200],
        ['delete program', 'get', lambda state: '/programs/delete/' + state ['program'] ['id'], {}, {}, 302],
        ['retrieve programs after deleting saved program', 'get', '/programs_list', {}, {}, 200, retrieveProgramsBefore],
        ['create program before destroying account', 'post', '/programs', {}, {'code': 'print Hello world', 'name': 'Program 1', 'level': 1}, 200],
        ['destroy account', 'post', '/auth/destroy', {}, {}, 200],
        ['get programs without being logged in', 'get', '/programs', {}, {}, 302],
        # Auth: profile (programming experience)
        ['valid signup again', 'post', '/auth/signup', {}, {'username': username, 'password': 'foobar', 'email': username + '@e2e-testing.com', 'prog_experience': 'yes', 'experience_languages': ['python']}, 200, successfulSignup],
        ['get profile after recreating account', 'get', '/profile', {}, {}, 200, getProfile4],
        ['change profile with different programming experience', 'post', '/profile', {}, {'prog_experience': 'no', 'experience_languages': ['scratch', 'other_text']}, 200],
        ['get profile after updating experience', 'get', '/profile', {}, {}, 200, getProfile5],
        ['destroy account', 'post', '/auth/destroy', {}, {}, 200],
        # Classes
        ['valid signup as student', 'post', '/auth/signup', {}, {'username': 'student-' + username, 'password': 'foobar', 'email': 'student-' + username + '@e2e-testing.com'}, 200, successfulSignupStudent],
        ['valid signup as teacher', 'post', '/auth/signup', {}, {'username': 'teacher-' + username, 'password': 'foobar', 'email': 'teacher-' + username + '@e2e-testing.com'}, 200, successfulSignupTeacher],
        ['create class without being a teacher', 'post', '/class', {}, {'name': 'class1'}, 403],
        ['mark teacher user as teacher', 'post', '/admin/markAsTeacher', {}, {'username': 'teacher-' + username, 'is_teacher': True}, 200],
        ['get classes before creating a class', 'get', '/classes', {}, {}, 200, getTeacherClasses1],
        invalidMap ('create class', 'post', '/class', ['', [], {}, {'name': 1}, {'name': ['foobar']}]),
        ['create class', 'post', '/class', {}, {'name': 'class1'}, 200],
        ['get classes after creating a class', 'get', '/classes', {}, {}, 200, getTeacherClasses2],
        ['get empty class', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'], {}, {}, 200, getClass1],
        invalidMap ('update class', 'put', lambda state: '/class/' + state ['classes'] [0] ['id'], ['', [], {}, {'name': 1}, {'name': ['foobar']}]),
        ['update class', 'put', lambda state: '/class/' + state ['classes'] [0] ['id'], {}, {'name': 'class_renamed'}, 200],
        ['get classes after renaming a class', 'get', '/classes', {}, {}, 200, getTeacherClasses3],
        ['get renamed class', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'], {}, {}, 200, getClass2],
        ['join class as non-logged in user', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/join/' + state ['classes'] [0] ['link'], lambda state: {'cookie': 'foo'}, {}, 403],
        ['login as student', 'post', '/auth/login', {}, {'username': 'student-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['join class that does not exist', 'get', lambda state: '/class/foo' + '/join/' + state ['classes'] [0] ['link'], {}, {}, 404],
        ['join class with invalid link', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/join/' + 'foo', {}, {}, 404],
        ['test short class link', 'get', lambda state: '/hedy/l/' + state ['classes'] [0] ['link'], {}, {}, 302, checkJoinLink],
        ['join class', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/join/' + state ['classes'] [0] ['link'], {}, {}, 302, redirectAfterJoin1],
        ['join class again (idempotent call)', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/join/' + state ['classes'] [0] ['link'], {}, {}, 302, redirectAfterJoin1],
        ['get profile after joining class', 'get', '/profile', {}, {}, 200, getStudentClasses1],
        ['login as teacher', 'post', '/auth/login', {}, {'username': 'teacher-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['get class with a student', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'], {}, {}, 200, getClass3],
        ['get student programs', 'get', lambda state: '/programs?user=' + state ['student'] ['username'], {}, {}, 200],
        ['login as student', 'post', '/auth/login', {}, {'username': 'student-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['create public program (not shared yet)', 'post', '/programs', {}, {'code': 'print Hello world', 'name': 'Public program 1', 'level': 1}, 200, createPublicProgram],
        ['share public program', 'post', '/programs/share', {}, lambda state: {'id': state ['public_program'], 'public': True}, 200],
        ['create private program after public program', 'post', '/programs', {}, {'code': 'print Hello world', 'name': 'Private program 1', 'level': 1}, 200],
        ['login as teacher', 'post', '/auth/login', {}, {'username': 'teacher-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['get class with a student with a shared program', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'], {}, {}, 200, getClass4],
        ['get classes after student shared a program', 'get', '/classes', {}, {}, 200, getTeacherClasses4],
        ['remove non-existing student from class', 'delete', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/student/' + 'foo', {}, {}, 200],
        ['remove student from class', 'delete', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/student/' + 'student-' + username, {}, {}, 200],
        ['remove student from class again (idempotent call)', 'delete', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/student/' + 'student-' + username, {}, {}, 200],
        ['get class that is now again empty', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'], {}, {}, 200, getClass2],
        ['get student programs if student is no longer in teacher\'s class', 'get', lambda state: '/programs?user=' + state ['student'] ['username'], {}, {}, 403],
        ['login as student', 'post', '/auth/login', {}, {'username': 'student-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['get profile after being removed from class', 'get', '/profile', {}, {}, 200, getStudentClasses2],
        ['join class again', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/join/' + state ['classes'] [0] ['link'], {}, {}, 302, redirectAfterJoin1],
        ['login as teacher', 'post', '/auth/login', {}, {'username': 'teacher-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['delete class', 'delete', lambda state: '/class/' + state ['classes'] [0] ['id'], {}, {}, 200],
        ['check that short class link was deleted', 'get', lambda state: '/hedy/l/' + state ['classes'] [0] ['link'], {}, {}, 404],
        ['get classes after deleting the class', 'get', '/classes', {}, {}, 200, getTeacherClasses1],
        ['destroy teacher account', 'post', '/auth/destroy', {}, {}, 200],
        ['login as student', 'post', '/auth/login', {}, {'username': 'student-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['get profile after class being deleted', 'get', '/profile', {}, {}, 200, getStudentClasses2],
        ['destroy student account', 'post', '/auth/destroy', {}, {}, 200],
        ['valid signup as student', 'post', '/auth/signup', {}, {'username': 'student-' + username, 'password': 'foobar', 'email': 'student-' + username + '@e2e-testing.com'}, 200, successfulSignupStudent],
        ['valid signup as teacher', 'post', '/auth/signup', {}, {'username': 'teacher-' + username, 'password': 'foobar', 'email': 'teacher-' + username + '@e2e-testing.com'}, 200, successfulSignupTeacher],
        ['mark teacher user as teacher', 'post', '/admin/markAsTeacher', {}, {'username': 'teacher-' + username, 'is_teacher': True}, 200],
        ['login as teacher', 'post', '/auth/login', {}, {'username': 'teacher-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['create class', 'post', '/class', {}, {'name': 'class1'}, 200],
        ['get classes to set its id in the state', 'get', '/classes', {}, {}, 200, getTeacherClasses2],
        ['login as student', 'post', '/auth/login', {}, {'username': 'student-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['join class', 'get', lambda state: '/class/' + state ['classes'] [0] ['id'] + '/join/' + state ['classes'] [0] ['link'], {}, {}, 302, redirectAfterJoin1],
        ['destroy student account', 'post', '/auth/destroy', {}, {}, 200],
        ['login as teacher', 'post', '/auth/login', {}, {'username': 'teacher-' + username, 'password': 'foobar'}, 200, setSentCookies],
        ['get classes after student destroyed their account', 'get', '/classes', {}, {}, 200, getTeacherClasses2],
        ['destroy teacher account', 'post', '/auth/destroy', {}, {}, 200],
    ]

if not args.concurrent:
    run_suite (suite)
else:
    counter = 0
    threads = []
    results = []
    errors  = []

    def thread_function (counter):
        try:
            ms = run_suite (suite)
            print ('Finished concurrent test #' + str (counter))
            results.append (ms)
        except Exception as e:
            print ('Concurrent test #' + str (counter), "finished with error")
            errors.append (e)

    print ('Starting', args.concurrent, 'concurrent tests')
    while counter < args.concurrent:
        counter += 1
        thread = threading.Thread (target=thread_function, args=[counter])
        thread.start ()
        threads.append (thread)

    for thread in threads:
        # join waits until all threads are done
        thread.join ()
    print ('Done with', args.concurrent, 'concurrent tests,', len (results), 'OK,', len (errors), 'errors,', round (sum (results) / (len (results) * 1000), 2), 'seconds average')
