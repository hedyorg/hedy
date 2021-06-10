from http.cookies import SimpleCookie
import hashlib
import re
import os
import logging

from flask import request, session, make_response
import requests
import flask.sessions
import itsdangerous

from .auth import current_user
import utils

class ABProxying:
    """Proxy some requests to another server."""
    def __init__(self, app, target_host, secret_key):
        self.target_host = target_host
        self.secret_key = secret_key

        app.before_request(self.before_request_proxy)

    def before_request_proxy(self):
        # If it is an auth route, we do not reverse proxy it to the PROXY_TO_TEST_HOST environment, with the exception of /auth/texts
        # We want to keep all cookie setting in the main environment, not the test one.
        if re.match ('.*/auth/.*', request.url) and not re.match ('.*/auth/texts', request.url):
            pass
        # This route is meant to return the session from the main environment, for testing purposes.
        elif re.match ('.*/session_main', request.url):
            pass
        # If we enter this block, we will reverse proxy the request to the PROXY_TO_TEST_HOST environment.
        # /session_test is meant to return the session from the test environment, for testing purposes.
        elif re.match ('.*/session_test', request.url) or redirect_ab (request):
            url = self.target_host + request.full_path
            logging.debug('Proxying %s %s %s to %s', request.method, request.url, dict (session), url)

            request_headers = {}
            for header in request.headers:
                if (header [0].lower () in ['host']):
                    continue
                request_headers [header [0]] = header [1]
            # In case the session_id is not yet set in the cookie, pass it in a special header
            request_headers ['X-session_id'] = session ['session_id']

            r = getattr (requests, request.method.lower ()) (url, headers=request_headers, data=request.data)

            response = make_response (r.content)
            for header in r.headers:
                # With great help from https://medium.com/customorchestrator/simple-reverse-proxy-server-using-flask-936087ce0afb
                if header.lower () in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']:
                    continue
                # Setting the session cookie returned by the test environment into the response won't work because it will be overwritten by Flask, so we need to read the cookie into the session so that then the session cookie can be updated by Flask
                if header.lower () == 'set-cookie':
                    proxied_session = extract_session_from_cookie (r.headers [header], self.secret_key)
                    for key in proxied_session:
                        session [key] = proxied_session [key]
                    continue
                response.headers [header] = r.headers [header]

            return response, r.status_code


def redirect_ab (request):
    # If this is a testing request, we return True
    if utils.is_testing_request (request):
        return True
    # If the user is logged in, we use their username as identifier, otherwise we use the session id
    user_identifier = current_user(request) ['username'] or str (session['session_id'])

    # This will send either % PROXY_TO_TEST_PROPORTION of the requests into redirect, or 50% if that variable is not specified.
    redirect_proportion = int (os.getenv ('PROXY_TO_TEST_PROPORTION', '50'))
    redirect_flag = (hash_user_or_session (user_identifier) % 100) < redirect_proportion
    return redirect_flag


def hash_user_or_session (string):
    hash = hashlib.md5 (string.encode ('utf-8')).hexdigest ()
    return int (hash, 16)


# Used by A/B testing to extract a session from a set-cookie header.
# The signature is ignored. The source of the session should be trusted.
def extract_session_from_cookie (cookie_header, secret_key):
    parsed_cookie = SimpleCookie (cookie_header)
    if not 'session' in parsed_cookie:
        return {}

    cookie_interface = flask.sessions.SecureCookieSessionInterface()

    # This code matches what Flask does for encoding
    serializer = itsdangerous.URLSafeTimedSerializer(
        secret_key,
        salt=cookie_interface.salt,
        serializer=cookie_interface.serializer,
        signer_kwargs=dict(
            key_derivation=cookie_interface.key_derivation,
            digest_method=cookie_interface.digest_method
       ))

    try:
        cookie_value = parsed_cookie['session'].value
        return serializer.loads(cookie_value)
    except itsdangerous.exc.BadSignature as e:
        # If the signature is wrong, we can still decode the cookie.
        # We try to do it properly with the actual key though, because exception
        # handling is slightly slow in Python and doing it successfully is therefore
        # faster.
        if e.payload is not None:
            try:
                return serializer.load_payload(e.payload)
            except itsdangerous.exc.BadData:
                pass
        return {}

