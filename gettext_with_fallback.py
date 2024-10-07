from flask import session
from flask_babel import gettext, force_locale


def gettext_with_fallback(x):
    locale = session['lang']
    res = gettext(x)
    if locale != 'en' and res == x:
        with force_locale('en'):
            res = gettext(x)
    return res


# Explicitly substitute the flask_babel function gettext with our own implementation that
# adds a fallback language. Note that we need to monkey-patch instead of use the gettext_with_fallback
# directly because the extract function requires us to use gettext with literal strings.
gettext = gettext_with_fallback
