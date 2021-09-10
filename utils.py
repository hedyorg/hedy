import contextlib
import datetime
import time
import pickle
import functools
import os
import re
import string
import random
from ruamel import yaml
from website import querylog
import commonmark
commonmark_parser = commonmark.Parser ()
commonmark_renderer = commonmark.HtmlRenderer ()
from bs4 import BeautifulSoup

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



def timems ():
    return int (round (time.time () * 1000))

def times ():
    return int (round (time.time ()))




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


YAML_CACHE = {}

@querylog.timed
def load_yaml(filename):
    """Load the given YAML file.

    The file load will be cached in production, but reloaded everytime in
    development mode for much iterating. Because YAML loading is still
    somewhat slow, in production we'll have two levels of caching:

    - In-memory cache: each of the N processes on the box will only need to
      load the YAML file once (per restart).

    - On-disk pickle cache: "pickle" is a more efficient Python serialization
      format, and loads 400x quicker than YAML. We will prefer loading a pickle
      file to loading the source YAML file if possible. Hopefully only 1/N
      processes on the box will have to do the full load per deploy.

    We should be generating the pickled files at build time, but Heroku doesn't
    make it easy to have a build/deploy time... so for now let's just make sure
    we only do it once per box per deploy.
    """
    if is_debug_mode():
        return load_yaml_uncached(filename)

    # Production mode, check our two-level cache
    if filename not in YAML_CACHE:
        data = load_yaml_pickled(filename)
        YAML_CACHE[filename] = data
        return data
    else:
        return YAML_CACHE[filename]


def load_yaml_pickled(filename):
    # Let's not even attempt the pickling on Windows, because we have
    # no pattern to atomatically write the pickled result file.
    if IS_WINDOWS:
        return load_yaml_uncached(filename)

    pickle_file = f'{filename}.pickle'
    if not os.path.exists(pickle_file):
        data = load_yaml_uncached(filename)

        # Write a pickle file, first write to a tempfile then rename
        # into place because multiple processes might try to do this in parallel,
        # plus we only want `path.exists(pickle_file)` to return True once the
        # file is actually complete and readable.
        with atomic_write_file(pickle_file) as f:
            pickle.dump(data, f)

        return data
    else:
        with open(pickle_file, 'rb') as f:
            return pickle.load(f)


def load_yaml_uncached(filename):
    try:
        y = yaml.YAML(typ='safe', pure=True)
        with open(filename, 'r', encoding='utf-8') as f:
            return y.load(f)
    except IOError:
        return {}


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
    ret = []
    for arg in args:
        if not arg: continue

        if ret and not ret[-1].endswith('/'):
            ret.append('/')
        ret.append(arg.lstrip('/') if ret else arg)
    return ''.join(ret)

def is_testing_request(request):
    return bool ('X-Testing' in request.headers and request.headers ['X-Testing'])

def extract_bcrypt_rounds (hash):
    return int (re.match ('\$2b\$\d+', hash) [0].replace ('$2b$', ''))

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
    return the_date.strftime('%b %d') + f' ({commit})'

def valid_email(s):
    return bool (re.match ('^(([a-zA-Z0-9_+\.\-]+)@([\da-zA-Z\.\-]+)\.([a-zA-Z\.]{2,6})\s*)$', s))


@contextlib.contextmanager
def atomic_write_file(filename, mode='wb'):
    """Write to a filename atomically.

    First write to a unique tempfile, then rename the tempfile into
    place. Use as a context manager:

        with atomic_write_file('file.txt') as f:
            f.write('hello')

    THIS WON'T WORK ON WINDOWS -- atomic file renames don't overwrite
    on Windows. We could potentially do something else to make it work
    (just swallow the exception, someone else already wrote the file?)
    but for now we just don't support it.
    """
    if IS_WINDOWS:
        raise RuntimeError('Cannot use atomic_write_file() on Windows!')

    tmp_file = f'{filename}.{os.getpid()}'
    with open(tmp_file, mode) as f:
        yield f

    os.rename(tmp_file, filename)

# This function takes a date in milliseconds from the Unix epoch and transforms it into a printable date
# It operates by converting the date to a string, removing its last 3 digits, converting it back to an int
# and then invoking the `isoformat` date function on it
def mstoisostring(date):
    return datetime.datetime.fromtimestamp (int (str (date) [:-3])).isoformat ()

# https://stackoverflow.com/a/2257449
def random_id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join (random.choice (chars) for _ in range (size))

# This function takes a markdown string and returns a list with each of the HTML elements obtained
# by rendering the markdown into HTML.
def markdown_to_html_tags (markdown):
    _html = commonmark_renderer.render(commonmark_parser.parse (markdown))
    soup = BeautifulSoup(_html, 'html.parser')
    return soup.find_all ()
