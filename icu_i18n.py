"""Enchance babel's gettext with ICU MessageFormat substitution
"""
# pylint: disable=no-member
import icu
from flask_babel import gettext as babel_gettext



def _keys_to_argnames(param_dict: dict):
    return list(map(str, param_dict.keys()))

def _vals_to_args(param_dict: dict):
    return list(map(icu.Formattable, param_dict.values()))


def icu_format(pattern: str, argdict = {}):
    """Replace ICU MessageFormat arguments in pattern"""
    argnames = _keys_to_argnames(argdict)
    args = _vals_to_args(argdict)
    return icu.MessageFormat(pattern).format(argnames, args)

def gettext(key: str, **kwargs):
    """Wraps Babel's gettext with MessageFormat argument substitution
        Use ICU pluralization instead of Babel's.
    """
    pattern = babel_gettext(key)
    return icu_format(pattern, kwargs)
