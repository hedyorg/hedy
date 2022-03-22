import contextlib
import datetime
import time
import functools
import os
import re
import string
import random
import uuid

from flask_babel import gettext
from ruamel import yaml
from website import querylog
import commonmark
commonmark_parser = commonmark.Parser()
commonmark_renderer = commonmark.HtmlRenderer()
from bs4 import BeautifulSoup
from flask_helpers import render_template
from flask import g, session, request

IS_WINDOWS = os.name == 'nt'

class Timer:
  """A quick and dirty timer."""
  def __init__(self, name):
    self.name = name

  def __enter__(self):
    self.start = time.time()

  def __exit__(self, type, value, tb):
    delta = time.time() - self.start
    print(f'{self.name}: {delta}s')


def timer(fn):
  """Decoractor for fn."""
  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    with Timer(fn.__name__):
      return fn(*args, **kwargs)
  return wrapper


def timems():
    """Return the UNIX timestamp in milliseconds.

    You only need to use this function if you are doing performance-sensitive
    timing. Otherwise, `times` (which returns second-resolution) is probably
    a better choice.
    """
    return int(round(time.time() * 1000))

def times():
    """Return the UNIX timestamp in seconds.

    If you need to store a date/time in the database, prefer this function.
    """
    return int(round(time.time()))




DEBUG_MODE = False

def is_debug_mode():
    """Return whether or not we're in debug mode.

    We do more expensive things that are better for development in debug mode.
    """
    return DEBUG_MODE


def set_debug_mode(debug_mode):
    """Switch debug mode to given value."""
    global DEBUG_MODE
    DEBUG_MODE = debug_mode


def load_yaml_rt(filename):
    """Load YAML with the round trip loader."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.round_trip_load(f, preserve_quotes=True)
    except IOError:
        return {}


def dump_yaml_rt(data):
    """Dump round-tripped YAML."""
    return yaml.round_trip_dump(data, indent=4, width=999)

def slash_join(*args):
    ret =[]
    for arg in args:
        if not arg: continue

        if ret and not ret[-1].endswith('/'):
            ret.append('/')
        ret.append(arg.lstrip('/') if ret else arg)
    return ''.join(ret)

def is_testing_request(request):
    return bool('X-Testing' in request.headers and request.headers['X-Testing'])

def extract_bcrypt_rounds(hash):
    return int(re.match(r'\$2b\$\d+', hash)[0].replace('$2b$', ''))

def isoformat(timestamp):
    """Turn a timestamp into an ISO formatted string."""
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    return dt.isoformat() + 'Z'


def is_production():
    """Whether we are serving production traffic."""
    return os.getenv('IS_PRODUCTION', '') != ''


def is_heroku():
    """Whether we are running on Heroku.

    Only use this flag if you are making a decision that really has to do with
    Heroku-based hosting or not.

    If you are trying to make a decision whether something needs to be done
    "for real" or not, prefer using:

    - `is_production()` to see if we're serving customer traffic and trying to
      optimize for safety and speed.
    - `is_debug_mode()` to see if we're on a developer machine and we're trying
      to optimize for developer productivity.

    """
    return os.getenv('DYNO', '') != ''


def version():
    """Get the version from the Heroku environment variables."""
    if not is_heroku():
        return 'DEV'

    vrz = os.getenv('HEROKU_RELEASE_CREATED_AT')
    the_date = datetime.date.fromisoformat(vrz[:10]) if vrz else datetime.date.today()

    commit = os.getenv('HEROKU_SLUG_COMMIT', '????')[0:6]
    return the_date.strftime('%b %d') + f'({commit})'

def valid_email(s):
    return bool(re.match(r'^(([a-zA-Z0-9_+\.\-]+)@([\da-zA-Z\.\-]+)\.([a-zA-Z\.]{2,6})\s*)$', s))


@contextlib.contextmanager
def atomic_write_file(filename, mode='wb'):
    """Write to a filename atomically.

    First write to a unique tempfile, then rename the tempfile into
    place. Use as a context manager:

        with atomic_write_file('file.txt') as f:
            f.write('hello')

    THIS WON'T WORK ON WINDOWS -- atomic file renames don't overwrite
    on Windows. We now just swallow the exception, someone else already wrote the file?)
    """

    tmp_file = f'{filename}.{os.getpid()}'
    with open(tmp_file, mode) as f:
        yield f

    try:
        os.rename(tmp_file, filename)
    except IOError:
        pass
        
# This function takes a date in milliseconds from the Unix epoch and transforms it into a printable date
# It operates by converting the date to a string, removing its last 3 digits, converting it back to an int
# and then invoking the `isoformat` date function on it
def mstoisostring(date):
    unix_ts = date / 1000
    dt = datetime.datetime.fromtimestamp(unix_ts)
    return datetime.datetime.fromtimestamp(int(str(date)[:-3])).isoformat()

def datetotimeordate(date):
    return date.replace("T", " ")

# https://stackoverflow.com/a/2257449
def random_id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# This function takes a Markdown string and returns a list with each of the HTML elements obtained
# by rendering the Markdown into HTML.
def markdown_to_html_tags(markdown):
    _html = commonmark_renderer.render(commonmark_parser.parse(markdown))
    soup = BeautifulSoup(_html, 'html.parser')
    return soup.find_all()


def error_page(error=404, page_error=None, ui_message=None, menu=True, iframe=None):
    if error not in [403, 404, 500]:
        error = 404
    default = gettext(u'default_404')
    if error == 403:
        default = gettext(u'default_403')
    elif error == 500:
        default = gettext(u'default_500')
    return render_template("error-page.html", menu=menu, error=error, iframe=iframe,
                           page_error=page_error or ui_message or '', default=default), error


def session_id():
    """Returns or sets the current session ID."""
    if 'session_id' not in session:
        if os.getenv('IS_TEST_ENV') and 'X-session_id' in request.headers:
            session['session_id'] = request.headers['X-session_id']
        else:
            session['session_id'] = uuid.uuid4().hex
    return session['session_id']
