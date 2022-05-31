import contextlib
import datetime
import textwrap
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

# Define code that will be used if some turtle command is present
TURTLE_PREFIX_CODE = textwrap.dedent("""\
    # coding=utf8
    import random, time, turtle
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.left(90)
    t.pendown()
    t.speed(3)
    t.showturtle()
 """)

# Preamble that will be used for non-Turtle programs
# numerals list generated from: https://replit.com/@mevrHermans/multilangnumerals

NORMAL_PREFIX_CODE = textwrap.dedent("""\
    # coding=utf8
    import random, time
    global int_saver
    global convert_numerals # needed for recursion to work
    int_saver = int
    def int(s):
        if isinstance(s, str):
            numerals_dict = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '𑁦': '0', '𑁧': '1', '𑁨': '2', '𑁩': '3', '𑁪': '4', '𑁫': '5', '𑁬': '6', '𑁭': '7', '𑁮': '8', '𑁯': '9', '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9', '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4', '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9', '੦': '0', '੧': '1', '੨': '2', '੩': '3', '੪': '4', '੫': '5', '੬': '6', '੭': '7', '੮': '8', '੯': '9', '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9', '೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4', '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9', '୦': '0', '୧': '1', '୨': '2', '୩': '3', '୪': '4', '୫': '5', '୬': '6', '୭': '7', '୮': '8', '୯': '9', '൦': '0', '൧': '1', '൨': '2', '൩': '3', '൪': '4', '൫': '5', '൬': '6', '൭': '7', '൮': '8', '൯': '9', '௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9', '౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4', '౫': '5', '౬': '6', '౭': '7', '౮': '8', '౯': '9', '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4', '၅': '5', '၆': '6', '၇': '7', '၈': '8', '၉': '9', '༠': '0', '༡': '1', '༢': '2', '༣': '3', '༤': '4', '༥': '5', '༦': '6', '༧': '7', '༨': '8', '༩': '9', '᠐': '0', '᠑': '1', '᠒': '2', '᠓': '3', '᠔': '4', '᠕': '5', '᠖': '6', '᠗': '7', '᠘': '8', '᠙': '9', '០': '0', '១': '1', '២': '2', '៣': '3', '៤': '4', '៥': '5', '៦': '6', '៧': '7', '៨': '8', '៩': '9', '๐': '0', '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9', '໐': '0', '໑': '1', '໒': '2', '໓': '3', '໔': '4', '໕': '5', '໖': '6', '໗': '7', '໘': '8', '໙': '9', '꧐': '0', '꧑': '1', '꧒': '2', '꧓': '3', '꧔': '4', '꧕': '5', '꧖': '6', '꧗': '7', '꧘': '8', '꧙': '9', '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9', '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9', '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0'}
            latin_numerals = ''.join([numerals_dict.get(letter, letter) for letter in s])
            return int_saver(latin_numerals)
        return(int_saver(s))

    def convert_numerals(alphabet, number):
        numerals_dict_return = {
            'Latin': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            'Brahmi': ['𑁦', '𑁧', '𑁨', '𑁩', '𑁪', '𑁫', '𑁬', '𑁭', '𑁮', '𑁯'],
            'Devanagari': ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'],
            'Gujarati': ['૦', '૧', '૨', '૩', '૪', '૫', '૬', '૭', '૮', '૯'],
            'Gurmukhi': ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯'],
            'Bengali': ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'],
            'Kannada': ['೦', '೧', '೨', '೩', '೪', '೫', '೬', '೭', '೮', '೯'],
            'Odia': ['୦', '୧', '୨', '୩', '୪', '୫', '୬', '୭', '୮', '୯'],
            'Malayalam': ['൦', '൧', '൨', '൩', '൪', '൫', '൬', '൭', '൮', '൯'],
            'Tamil': ['௦', '௧', '௨', '௩', '௪', '௫', '௬', '௭', '௮', '௯'],
            'Telugu':['౦', '౧', '౨', '౩', '౪', '౫', '౬', '౭', '౮', '౯'],
            'Burmese':['၀', '၁', '၂', '၃', '၄', '၅', '၆', '၇', '၈', '၉'],
            'Tibetan':['༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩'],
            'Mongolian':['᠐', '᠑', '᠒', '᠓', '᠔', '᠕', '᠖', '᠗', '᠘', '᠙'],
            'Khmer':['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩'],
            'Thai':['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙'],
            'Lao':['໐', '໑', '໒', '໓', '໔', '໕', '໖', '໗', '໘', '໙'],
            'Javanese':['꧐', '꧑', '꧒', '꧓', '꧔', '꧕', '꧖', '꧗', '꧘', '꧙'],
            'Arabic':['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'],
            'Persian':['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'],
            'Urdu': ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
        }

        numerals_list = numerals_dict_return[alphabet]
        number=str(number)

        if number.isnumeric():
            number = int(number)
            numerals_list = numerals_dict_return[alphabet]
            if number <= 9:
                return numerals_list[number]
            else:
                last_digit = number // 10
                rest = number % 10
                return numerals_list[last_digit] + convert_numerals(alphabet, rest)
        else:
            return number
         """)

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
    return datetime.datetime.fromtimestamp(int(str(date)[:-3])).isoformat()

def stoisostring(date):
    return datetime.datetime.fromtimestamp(date)

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
    default = gettext('default_404')
    if error == 403:
        default = gettext('default_403')
    elif error == 500:
        default = gettext('default_500')
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
