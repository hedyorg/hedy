from random import random as random

from flask import session
from hedy_content import ALTERNATIVE_ERROR_LANGUAGES
from website.auth import (current_user, remember_current_user)
# from utils import ColoredConsole as clog


def is_available():
    user = current_user()
    is_test_group = user.get('test_group')

    lang = session.get('lang')

    return is_test_group and is_supported_lang(lang)


def is_supported_lang(lang):
    return lang in ALTERNATIVE_ERROR_LANGUAGES


def select_users_test_group():
    lang = session.get('lang')
    if is_supported_lang(lang):
        if random() > 0.66:
            return True
    return False

# Creation of test_group field if it doesn't exist in session or db user


def update_users_test_group(db):
    user = current_user()
    # Check if there is a logged-in user
    if user['username']:
        # Check if test_group field exists or is filled properly
        if 'test_group' not in user.keys() or user.get('test_group') is None:
            db_user = db.user_by_username(user['username'])
            # Double check if test_group field also doesn't exist in db user
            if 'test_group' not in db_user.keys():
                test_group = select_users_test_group()
                db.update_user(user['username'], {'test_group': test_group})
            # Anyway update session user now with test_group field
            remember_current_user(db_user)
