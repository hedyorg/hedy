import dataclasses
import json

from markupsafe import Markup

from . import querylog

import flask
from flask_babel import force_locale, gettext
from flask.json.provider import JSONProvider
from jinja2 import Undefined


@querylog.timed
def render_template(filename, **kwargs):
    """A copy of Flask's render_template that is timed, and also validated."""
    rendered = flask.render_template(filename, **kwargs)

    # Late imports because of circular dependencies. Don't care to figure this out right now.
    from utils import is_debug_mode
    if is_debug_mode():
        from website.html_validation import validate_output_html
        validate_output_html(rendered)
    return rendered


def proper_json_dumps(x, **kwargs):
    """Properly convert the input to JSON that deals with a bunch of edge cases.

    This function will account for:

    - None: by default would translate to 'null', but 'undefined' (missing) is
      much more generally useful.
    - Undefined: will treat Jinja's 'Undefined' value as a 'None'
    - Dataclasses: will serialize data classes as their fields.
    """
    return json.dumps(x, cls=EnhancedJSONEncoder, **kwargs)


def proper_tojson(x):
    """A version of 'tojson' that uses the conversions we want."""
    return proper_json_dumps(x)


def gettext_with_fallback(x):
    if flask.session:
        locale = flask.session['lang']
    else:
        locale = 'en'
    res = gettext(x)
    if locale != 'en' and res == x:
        with force_locale('en'):
            res = gettext(x)
    return Markup(res)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return strip_nones(dataclasses.asdict(o))
        if isinstance(o, Undefined):
            return None
        return super().default(strip_nones(o))


def strip_nones(x):
    if isinstance(x, dict):
        return {k: v for k, v in x.items() if v is not None and not isinstance(v, Undefined)}
    return x


class JinjaCompatibleJsonProvider(JSONProvider):
    """A JSON provider for Flask 2.3+ that removes Nones and Jinja Undefineds."""

    def dumps(self, obj, **kwargs):
        return proper_json_dumps(obj, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)
