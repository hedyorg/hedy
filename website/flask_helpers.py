import dataclasses
import json
import re

from markupsafe import Markup

from . import querylog

import flask
from flask_babel import force_locale, gettext
from flask.json.provider import JSONProvider
from jinja2 import Undefined


@querylog.timed
def render_template(filename, **kwargs):
    """A copy of Flask's render_template that is timed."""
    return flask.render_template(filename, **kwargs)


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
    result = gettext(x)
    is_valid_content, _ = validate_content(result)
    # If there is no translation or the translation has suspicious content, fetch the English content
    if locale != 'en' and (result == x or not is_valid_content):
        with force_locale('en'):
            result = gettext(x)
    # Regardless whether this is English or translated content, always show escaped html
    _, content = validate_content(result)
    return Markup(content)


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


whitelisted_links = {
    'OPEN_BUG_REPORT':
        "https://github.com/hedyorg/hedy/issues/new?assignees=&labels=&template=bug_report.md&title=%5BBUG%5D",
    'SLIDES_COM': 'https://slides.com',
    'TEACHERS_MANUAL': 'https://www.hedy.org/for-teachers/manual',
    'TEACHERS_MANUAL_FEATURES': 'https://hedy.org/for-teachers/manual/features',
    'TEACHERS_MANUAL_FOR_TEACHERS': 'https://hedy.org/for-teachers/manual/preparations#for-teachers',
    'FOR_TEACHERS': 'https://hedycode.com/for-teachers',
    'DISCORD_SERVER': 'https://discord.gg/8yY7dEme9r',
    'MAIL_TO_HELLO_HEDY': 'mailto: hello@hedy.org',
    'DISCORD_VIDEO': 'https://www.youtube.com/watch?v=Lyz_Lnd-_aI',
    'CUSTOMIZE_ADVENTURE': 'https://github.com/hedyorg/hedy/assets/80678586/df38cbb2-468e-4317-ac67-92eaf4212adc',
}

whitelisted_keys = {v for k in whitelisted_links.keys() for v in {f'#HREF_{k}#', f'#MD_{k}#', f'#SRC_{k}#'}}

whitelisted_html_tags = ['a', 'b', 'em', 'strong', 'img']


def validate_content(input_):
    """
    Validates that the input does not have suspicious HTML or markdown content. If there is no suspicious content,
    the function returns True and input in which the URL references are substitute with the actual whitelisted URLs.
    If there is suspicious content, the function returns False and the input where all special characters are escaped,
    so that the HTML or markdown appears as plain text. For example:
    - '<a #HREF_DISCORD_SERVER#>link</a>' returns (True, '<a href="https://discord.gg/8yY7dEme9r">link</a>')
    - '[link](#MD_SLIDES_COM#)' returns '[link](https://slides.com)'
    - '<a href="https://hedy.org">link</a>' is (False, '&lt;a href="https://discord.gg/8yY7dEme9r"&gt;link&lt;/a&gt;')
    """
    def escape_special_chars(i):
        return (i.replace('<', '&lt;').replace('>', '&gt;')
                .replace('[', '\\[').replace(']', '\\]')
                .replace('(', '\\(').replace(')', '\\)'))

    def replace_whitelisted_links(i):
        for key in whitelisted_keys:
            parts = key[1:-1].split('_')
            value = whitelisted_links['_'.join(parts[1:])]
            if parts[0] == 'HREF':
                replace_by = f'href="{value}"'
            elif parts[0] == 'SRC':
                replace_by = f'src={value}'
            else:
                replace_by = value
            i = i.replace(key, replace_by)
        return i

    def has_valid_ref(i, prefix=''):
        href_times = i.lower().count(prefix.lower())
        whitelist_keys_present = [link in i for link in whitelisted_keys if link.startswith(f'#{prefix.upper()}_')]
        return href_times == 1 and any(whitelist_keys_present)

    # If the content contains something which remotely reminds of an HTML or markdown comment, it is suspicious.
    if re.search(r'<!--', input_) or re.search(r'-->', input_) or re.search(r']:', input_):
        return False, escape_special_chars(input_)

    # Find all occurrences which look like an opening HTML tag
    matches = re.findall(r'<\s*[^/][^>]+', input_)
    for match in matches:
        # If an HTML tag is used then the tag must be the first non-empty string after the < symbol.
        # If the tag is not first? Then it is considered suspicious.
        tag = match[1:].strip().split(' ')[0]
        if tag not in whitelisted_html_tags:
            return False, escape_special_chars(input_)
        # If the tag is an anchor or an image, then the href and src must be a reference to a whitelisted URL
        if ((tag == 'a' and not has_valid_ref(match, 'href')) or
                (tag == 'img' and not has_valid_ref(match, 'src'))):
            return False, escape_special_chars(input_)

    # Find all occurrences which look like a Markdown link
    matches = re.findall(r']\([^)]+', input_)
    for match in matches:
        url = match[2:].strip()
        # The link must be a reference to a whitelisted URL
        if not url.startswith('#MD_') or url not in whitelisted_keys:
            return False, escape_special_chars(input_)

    # If no suspicious content is found, replace all URL references with the actual links
    return True, replace_whitelisted_links(input_)
