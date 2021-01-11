import time
from config import config
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

def type_check (val, Type):
    if Type == 'dict':
        return isinstance(val, dict)
    if Type == 'list':
        return isinstance(val, list)
    if Type == 'str':
        return isinstance(val, str)
    if Type == 'int':
        return isinstance(val, int)
    if Type == 'fun':
        return callable(val)

def object_check (obj, key, Type):
  if not type_check (obj, 'dict') or not key in obj:
     return False
  return type_check (obj [key], Type)

def timems ():
    return int (round (time.time () * 1000))

def times ():
    return int (round (time.time ()))

# *** DYNAMO DB ***

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html

db = boto3.client ('dynamodb', region_name = config ['dynamodb'] ['region'], aws_access_key_id = os.getenv ('AWS_DYNAMODB_ACCESS_KEY'), aws_secret_access_key = os.getenv ('AWS_DYNAMODB_SECRET_KEY'))
db_prefix = os.getenv ('AWS_DYNAMODB_TABLE_PREFIX')

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

def db_decode (data):
    processed_data = {}
    for key in data:
        if 'S' in data [key]:
            processed_data [key] = data [key] ['S']
        elif 'N' in data [key]:
            processed_data [key] = int (data [key] ['N'])
        else:
            raise ValueError ('Unsupported type passed to db_put')
    return processed_data

def db_key (table, data, *remove):
    processed_data = {}
    if len (remove):
        for key in data:
            if table == 'users' and key == 'username':
                continue
            if table == 'tokens' and key == 'id':
                continue
            processed_data [key] = data [key]
    else:
        if table == 'users':
            processed_data ['username'] = data ['username']
        if table == 'tokens':
            processed_data ['id'] = data ['id']
    return processed_data

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

def db_set (table, data):
    if db_get (table, data):
        result = db.update_item (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)), AttributeUpdates = db_encode (db_key (table, data, True), True))
    else:
        result = db.put_item (TableName = db_prefix + '-' + table, Item = db_encode (data))
    return result

def db_del (table, data):
    return db.delete_item (TableName = db_prefix + '-' + table, Key = db_encode (db_key (table, data)))

def db_scan (table):
    result = db.scan (TableName = db_prefix + '-' + table)
    output = []
    for item in result ['Items']:
        output.append (db_decode (item))
    return output
