import time
from config import config
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
from ruamel import yaml
import flask


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


def flask_in_debug_mode():
    """Whether or not Flask is in debug mode.

    We do more expensive things that are better for development in debug mode.
    """
    return flask.current_app.config['DEBUG']


YAML_CACHE = {}

def load_yaml(filename):
    """Load the given YAML file.

    The file load will be cached in production, but reloaded everytime in development mode.

    Whether we are running in production or not will be determined
    by the Flask config (FLASK_ENV).
    """
    # Bypass the cache in DEBUG mode for mucho iterating
    if not flask_in_debug_mode() and filename in YAML_CACHE:
        return YAML_CACHE[filename]
    try:
        with open (filename, 'r') as f:
            data = yaml.safe_load(f)
            YAML_CACHE[filename] = data
            return data
    except IOError:
        return {}


def load_yaml_rt(filename):
    """Load YAML with the round trip loader."""
    try:
        with open(filename, 'r') as f:
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
def db_encode (data, *args):
    # args may contain a boolean flag which we use to detect whether we should format the payload for update_item
    # when len (args) is truthy, we know we're dealing with update_item
    processed_data = {}
    for key in data:
        if type_check (data [key], 'str'):
            if len (args):
                processed_data [key] = {'Value': {'S': data [key]}}
            else:
                processed_data [key] = {'S': data [key]}
        elif type_check (data [key], 'int'):
            # Note we convert the value into a string
            if len (args):
                processed_data [key] = {'Value': {'N': str (data [key])}}
            else:
                processed_data [key] = {'N': str (data [key])}
        elif data [key] == None:
            if len (args):
                processed_data [key] = {'Action': 'DELETE'}
            else:
                processed_data [key] = {'NULL': True}
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

# This function takes a dict `data` and returns a new dict with only the key/value for the index key for the table.
# If *remove is truthy, then the index key is removed instead, leaving the rest of the keys intact.
def db_key (table, data, *remove):
    processed_data = {}
    if len (remove):
        for key in data:
            if table == 'users' and key == 'username':
                continue
            if (table == 'tokens' or table == 'programs') and key == 'id':
                continue
            processed_data [key] = data [key]
    else:
        if table == 'users':
            processed_data ['username'] = data ['username']
        if table == 'tokens' or table == 'programs':
            processed_data ['id'] = data ['id']
    return processed_data

# Gets an item by index from the database. If not_primary is truthy, the search is done by a field that should be set as a secondary index.
def db_get (table, data, *not_primary):
    # If we're querying by something else than the primary key of the table, we assume that data contains only one field, that on which we want to search. We also require that field to have an index.
    if len (not_primary):
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
def db_get_many (table, data, *not_primary):
    if len (not_primary):
        field = list (data.keys ()) [0]
        # We use ScanIndexForward = False to get the latest items from the Programs table
        result = db.query (TableName = db_prefix + '-' + table, IndexName = field + '-index', KeyConditionExpression = field + ' = :value', ExpressionAttributeValues = {':value': {'S': data [field]}}, ScanIndexForward = False)
    else:
        result = db.query (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)))
    data = []
    for item in result ['Items']:
        data.append (db_decode (item))
    return data

# Creates or updates an item by primary key.
def db_set (table, data):
    if db_get (table, data):
        result = db.update_item (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)), AttributeUpdates = db_encode (db_key (table, data, True), True))
    else:
        result = db.put_item (TableName = db_prefix + '-' + table, Item = db_encode (data))
    return result

# Deletes an item by primary key.
def db_del (table, data):
    return db.delete_item (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)))

# Deletes multiple items.
def db_del_many (table, data, *not_primary):
    # We define a recursive function in case the number of results is very large and cannot be returned with a single call to db_get_many.
    def batch ():
        to_delete = db_get_many (table, data, *not_primary)
        if len (to_delete) == 0:
            return
        for item in to_delete:
            db_del (table, db_key (table, item))
        batch ()
    batch ()

# Searches for items.
def db_scan (table):
    result = db.scan (TableName = db_prefix + '-' + table)
    output = []
    for item in result ['Items']:
        output.append (db_decode (item))
    return output

def db_describe (table):
    return db.describe_table (TableName = db_prefix + '-' + table)
