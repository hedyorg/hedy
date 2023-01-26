from random import random as random

from flask import session
from hedy_content import ALTERNATIVE_ERROR_LANGUAGES
from website.auth import current_user, update_test_group_in_session
# from utils import ColoredConsole as clog

PERCENTAGE_IN_TEST_GROUP = 1/3  # One third of the users should be in the test group


def is_available():
    # get test_group field from session user
    is_test_group = current_user().get('test_group')

    lang = session.get('lang')

    return is_test_group and is_supported_lang(lang)


def is_supported_lang(lang):
    return lang in ALTERNATIVE_ERROR_LANGUAGES


def select_users_test_group():
    lang = session.get('lang')
    if is_supported_lang(lang):
        if random() < PERCENTAGE_IN_TEST_GROUP:
            return True
    return False

# Creation of test_group entry if it doesn't exist in session or db


def update_users_test_group(db):
    user = current_user()
    # Check if there is a logged-in user
    if user['username']:
        # Check if test_group field exists or is filled properly in session
        if not session.get('test_group'):
            test_group = db.test_group_by_username(user['username'])
            # Double check if test_group field also doesn't exist in db entry
            if test_group is None:
                test_group = select_users_test_group()
                db.add_test_group_to_username(user['username'], test_group)
            # Anyway update session user now with test_group field
            update_test_group_in_session(test_group)
