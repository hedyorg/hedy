from random import random as random

from flask import (g, session)
from hedy_content import ALTERNATIVE_ERROR_LANGUAGES
from website.auth import (current_user)
from utils import ColoredConsole as clog

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
