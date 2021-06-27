import contextlib
import datetime
import time
from config import config
import pickle
import boto3
import functools
import os
import re
from ruamel import yaml
from website import querylog


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


def type_check (val, Type):
    if Type == 'dict':
        return isinstance (val, dict)
    if Type == 'list':
        return isinstance (val, list)
    if Type == 'str':
        return isinstance (val, str)
    if Type == 'int':
        return isinstance (val, int)
    if Type == 'tuple':
        return isinstance (val, tuple)
    if Type == 'fun':
        return callable (val)
    if Type == 'bool':
        return type (val) == bool

def object_check (obj, key, Type):
    if not type_check (obj, 'dict') or not key in obj:
        return False
    return type_check (obj [key], Type)

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
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
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


# *** DYNAMO DB ***

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html

db = boto3.client ('dynamodb', region_name = config ['dynamodb'] ['region'], aws_access_key_id = os.getenv ('AWS_DYNAMODB_ACCESS_KEY'), aws_secret_access_key = os.getenv ('AWS_DYNAMODB_SECRET_KEY'))
db_prefix = os.getenv ('AWS_DYNAMODB_TABLE_PREFIX')

# Encode a dict so that it has the format expected by DynamoDB
def db_encode (data):
    # update is a boolean flag which we use to detect whether we should format the payload for update_item
    processed_data = {}
    for key in data:
        if type_check (data [key], 'str'):
            processed_data [key] = {'S': data [key]}
        elif type_check (data [key], 'int'):
            # Note we convert the value into a string
            processed_data [key] = {'N': str (data [key])}
        elif data [key] == None:
            processed_data [key] = {'NULL': True}
        else:
            raise ValueError ('Unsupported type passed to db_put')
    return processed_data

# Encode a dict so that it has the format expected by DynamoDB
def db_encode_updates (data):
    processed_data = {}
    for key in data:
        if type_check (data [key], 'str'):
            processed_data [key] = {'Value': {'S': data [key]}}
        elif type_check (data [key], 'int'):
            # Note we convert the value into a string
            processed_data [key] = {'Value': {'N': str (data [key])}}
        elif data [key] == None:
            processed_data [key] = {'Action': 'DELETE'}
        else:
            raise ValueError ('Unsupported type passed to db_put')
    return processed_data

# Decode data in DynamoDB format to a plain dict
def db_decode (data):
    processed_data = {}
    for key in data:
        if 'S' in data [key]:
            processed_data [key] = data [key] ['S']
        elif 'N' in data [key]:
            processed_data [key] = int (data [key] ['N'])
        elif 'NULL' in data [key]:
            processed_data [key] = None
        else:
            raise ValueError ('Unsupported type passed to db_put')
    return processed_data

db_main_indexes = {
   'users': 'username',
   'tokens': 'id',
   'programs': 'id'
}

# This function takes a dict `data` and returns a new dict with only the key/value for the index key for the table.
# If remove is truthy, then the index key is removed instead, leaving the rest of the keys intact.
def db_key (table, data, remove=False):
    processed_data = {}
    if remove:
        for key in data:
            if key != db_main_indexes [table]:
                processed_data [key] = data [key]
    else:
        processed_data [db_main_indexes [table]] = data [db_main_indexes [table]]
    return processed_data

# Gets an item by index from the database. If not_primary is truthy, the search is done by a field that should be set as a secondary index.
@querylog.timed
def db_get (table, data, not_primary=False):
    querylog.log_counter('db_get:' + table)
    # If we're querying by something else than the primary key of the table, we assume that data contains only one field, that on which we want to search. We also require that field to have an index.
    if not_primary:
        field = list (data.keys ()) [0]
        result = db.query (TableName = db_prefix + '-' + table, IndexName = field + '-index', KeyConditionExpression = field + ' = :value', ExpressionAttributeValues = {':value': {'S': data [field]}})
        if len (result ['Items']):
            return db_decode (result ['Items'] [0])
        else:
            return None
    else:
        result = db.get_item (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)))
        if 'Item' not in result:
            return None
        return db_decode (result ['Item'])

# Gets an item by index from the database. If not_primary is truthy, the search is done by a field that should be set as a secondary index.
@querylog.timed
def db_get_many (table, data, not_primary=False):
    querylog.log_counter('db_get_many:' + table)
    if not_primary:
        field = list (data.keys ()) [0]
        # We use ScanIndexForward = False to get the latest items from the Programs table
        result = db.query (TableName = db_prefix + '-' + table, IndexName = field + '-index', KeyConditionExpression = field + ' = :value', ExpressionAttributeValues = {':value': {'S': data [field]}}, ScanIndexForward = False)
    else:
        result = db.query (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)))
    data = []
    querylog.log_counter('db_get_many_items', len(result['Items']))
    for item in result ['Items']:
        data.append (db_decode (item))
    return data

# Creates an item.
@querylog.timed
def db_create (table, data):
    querylog.log_counter('db_create:' + table)
    return db.put_item (TableName = db_prefix + '-' + table, Item = db_encode (data))

# Updates an item by primary key.
@querylog.timed
def db_update (table, data):
    querylog.log_counter('db_update:' + table)
    return db.update_item (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)), AttributeUpdates = db_encode_updates (db_key (table, data, True)))

# Deletes an item by primary key.
@querylog.timed
def db_del (table, data):
    querylog.log_counter('db_del:' + table)
    return db.delete_item (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)))

# Deletes multiple items.
@querylog.timed
def db_del_many (table, data, not_primary=False):
    querylog.log_counter('db_del_many:' + table)
    # We define a recursive function in case the number of results is very large and cannot be returned with a single call to db_get_many.
    def batch ():
        to_delete = db_get_many (table, data, not_primary)
        if len (to_delete) == 0:
            return
        for item in to_delete:
            db_del (table, db_key (table, item))
        batch ()
    batch ()

# Searches for items.
@querylog.timed
def db_scan (table):
    querylog.log_counter('db_scan:' + table)
    result = db.scan (TableName = db_prefix + '-' + table)
    output = []
    querylog.log_counter('db_scan_items', len(result['Items']))
    for item in result ['Items']:
        output.append (db_decode (item))
    return output

@querylog.timed
def db_describe (table):
    querylog.log_counter('db_describe:' + table)
    return db.describe_table (TableName = db_prefix + '-' + table)


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
