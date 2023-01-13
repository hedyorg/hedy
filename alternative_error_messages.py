# coding=utf-8

from flask import (g, session)
from hedy_content import ALTERNATIVE_ERROR_LANGUAGES
from website.auth import (current_user)
from utils import ColoredConsole as clog

def is_available():
    user = current_user()
    is_test_group = user.get('test_group')
    
    lang = session.get('lang')
    is_supported_lang = lang in ALTERNATIVE_ERROR_LANGUAGES

    return is_test_group and is_supported_lang
