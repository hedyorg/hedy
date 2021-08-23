import functools
import boto3
from abc import ABCMeta
import os
import logging
from config import config
from . import querylog
from dataclasses import dataclass
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
import json
import threading


class TableStorage(metaclass=ABCMeta):
    def get_item(self, table_name, key): ...
    def query(self, table_name, key, reverse=False): ...
    def query_index(self, table_name, index_name, key, reverse=False): ...
    def put(self, table_name, key, data): ...
    def update(self, table_name, key, updates): ...
    def delete(self, table_name, key): ...
    def item_count(self, table_name): ...
    def scan(self, table_name): ...


class Table:
    """Dynamo table access

    Transparently handles indexes, and doesn't support sort keys yet.
    """
    def __init__(self, storage: TableStorage, table_name, partition_key, indexed_fields=None):
        self.storage = storage
        self.table_name = table_name
        self.partition_key = partition_key
        self.indexed_fields = indexed_fields or []

    @querylog.timed_as('db_get')
    def get(self, key):
        """Gets an item by key from the database.

        The key must be a dict with a single entry which references the
        partition key or an index key.
        """
        querylog.log_counter(f'db_get:{self.table_name}')
        lookup = self._determine_lookup(key)
        if isinstance(lookup, TableLookup):
            return self.storage.get_item(lookup.table_name, key)
        if isinstance(lookup, IndexLookup):
            return first_or_none(self.storage.query_index(lookup.table_name, lookup.index_name, key))
        assert False

    @querylog.timed_as('db_get_many')
    def get_many(self, key, reverse=True):
        """Gets a list of items by key from the database.

        The key must be a dict with a single entry which references the
        partition key or an index key.

        get_many is a paged operation, and will return to a maximum size of data.
        """
        querylog.log_counter(f'db_get_many:{self.table_name}')

        lookup = self._determine_lookup(key)
        if isinstance(lookup, TableLookup):
            items = self.storage.query(lookup.table_name, key, reverse=reverse)
        elif isinstance(lookup, IndexLookup):
            items = self.storage.query_index(lookup.table_name, lookup.index_name, key, reverse=reverse)
        else:
            assert False
        querylog.log_counter('db_get_many_items', len(items))
        return items

    @querylog.timed_as('db_create')
    def create(self, data):
        """Put a single complete record into the database."""
        assert(self.partition_key in data)

        querylog.log_counter(f'db_create:{self.table_name}')
        self.storage.put(self.table_name, self._extract_key(data), data)

    @querylog.timed_as('db_update')
    def update(self, key, updates):
        """Update select fields of a given record.

        The values of data can be plain data, or an instance of
        one of the subclasses of DynamoUpdate which represent
        updates that aren't representable as plain values.
        """
        querylog.log_counter(f'db_update:{self.table_name}')

        return self.storage.update(self.table_name, key, updates)

    @querylog.timed_as('db_del')
    def delete(self, key):
        """Delete an item by primary key.

        Returns the delete item.
        """
        querylog.log_counter('db_del:' + self.table_name)
        return self.storage.delete(self.table_name, key)

    @querylog.timed_as('db_del_many')
    def del_many (self, key):
        """Delete all items matching a key.

        DynamoDB does not support this operation natively, so we have to turn
        it into a fetch+batch delete (and since our N is small, we do
        repeated "single" deletes instead of doing a proper batch delete).
        """
        querylog.log_counter('db_del_many:' + self.table_name)

        # The result of get_many is paged, so we might need to do this more than once.
        to_delete = self.get_many(key)
        while to_delete:
            for item in to_delete:
                key = self._extract_key(item)
                self.delete(key)
            to_delete = self.get_many(key)

    @querylog.timed_as('db_scan')
    def scan(self):
        """Reads the entire table into memory."""
        querylog.log_counter('db_scan:' + self.table_name)
        return self.storage.scan (self.table_name)


    @querylog.timed_as('db_describe')
    def item_count(self):
        querylog.log_counter('db_describe:' + self.table_name)
        return self.storage.item_count(self.table_name)

    def _determine_lookup(self, key_data):
        keys = list(key_data.keys())
        if len(keys) != 1:
            raise RuntimeError('Only supporting 1 (partition) key for now')
        key_field = keys[0]
        if key_field == self.partition_key:
            return TableLookup(self.table_name)
        if key_field in self.indexed_fields:
            return IndexLookup(self.table_name, f'{key_field}-index')
        raise RuntimeError(f'Field not indexed: {key_field}')

    def _extract_key(self, data):
        """
        Extract the key data out of plain data.
        """
        if self.partition_key not in data:
            raise RuntimeError(f'Partition key {self.partition_key} missing from data: {data}')
        key_value = data.get(self.partition_key)
        return { self.partition_key: key_value }


class AwsDynamoStorage(TableStorage):
    SERIALIZER = TypeSerializer()
    DESERIALIZER = TypeDeserializer()

    @staticmethod
    def from_env():
        if is_dynamo_available():
            db = boto3.client ('dynamodb', region_name = config ['dynamodb'] ['region'], aws_access_key_id = os.getenv ('AWS_DYNAMODB_ACCESS_KEY'), aws_secret_access_key = os.getenv ('AWS_DYNAMODB_SECRET_KEY'))
            db_prefix = os.getenv ('AWS_DYNAMODB_TABLE_PREFIX', '')
            return AwsDynamoStorage(db, db_prefix)
        return None

    def __init__(self, db, db_prefix):
        self.db = db
        self.db_prefix = db_prefix

    def get_item(self, table_name, key):
        result = self.db.get_item(
            TableName=self.db_prefix + '-' + table_name,
            Key = self._encode(key))
        return self._decode(result.get('Item', None))

    def query(self, table_name, key, reverse=False):
        assert len(key.keys ()) == 1
        key_field = list (key.keys ()) [0]
        key_value = key [key_field]
        result = self.db.query(
            TableName=self.db_prefix + '-' + table_name,
            KeyConditionExpression = key_field + ' = :value',
            ExpressionAttributeValues = {':value': self.SERIALIZER.serialize (key_value)},
            ScanIndexForward = not reverse)
        return list(map(self._decode, result.get('Items', [])))

    def query_index(self, table_name, index_name, key, reverse=False):
        assert len(key) == 1
        key_field, key_value = list(key.items())[0]

        result = self.db.query(
            TableName = self.db_prefix + '-' + table_name,
            IndexName = index_name,
            KeyConditionExpression = key_field + ' = :value',
            ExpressionAttributeValues = {':value': {'S': key_value}},
            ScanIndexForward = not reverse)

        return list(map(self._decode, result.get('Items', [])))

    def put(self, table_name, _key, data):
        return self.db.put_item(
            TableName = self.db_prefix + '-' + table_name,
            Item = self._encode(data))

    def update(self, table_name, key, updates):
        value_updates = {k: v for k, v in updates.items() if not isinstance(v, DynamoUpdate)}
        special_updates = {k: v.to_dynamo() for k, v in updates.items() if isinstance(v, DynamoUpdate)}

        return self.db.update_item(
            TableName = self.db_prefix + '-' + table_name,
            Key = self._encode(key),
            AttributeUpdates = {
                **self._encode_updates(value_updates),
                **special_updates,
            })

    def delete(self, table_name, key):
        return self.db.delete_item(
            TableName = self.db_prefix + '-' + table_name,
            Key = self._encode(key))

    def item_count(self, table_name):
        return self.db.describe_table (TableName = self.db_prefix + '-' + table_name)['Table']['ItemCount']

    def scan(self, table_name):
        result = self.db.scan (TableName = self.db_prefix + '-' + table_name)
        return list(map(self._decode, result.get('Items', [])))

    def _encode (self, data):
        return {k: self.SERIALIZER.serialize(v) for k, v in data.items()}

    def _encode_updates (self, data):
        def encode_update(value):
            # None is special, we use it to remove a field from a record
            if value is None:
                return {'Action': 'DELETE'}
            else:
                return {'Value': self.SERIALIZER.serialize(value)}
        return {k: encode_update(v) for k, v in data.items()}

    def _decode (self, data):
        if data is None:
            return None

        return {k: replace_decimals(self.DESERIALIZER.deserialize(v)) for k, v in data.items()}


class Lock:
    def __init__(self):
        self.lock = threading.Lock()

    def synchronized(self, fn):
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            with self.lock:
                return fn(*args, **kwargs)
        return _wrapper

lock = Lock()


class MemoryStorage(TableStorage):
    def __init__(self, filename=None):
        # In-memory structure:
        #
        # { table_name -> [ {...record...}, {...record...} ] }
        #
        # Needs work done to support sort keys properly
        self.tables = {}
        self.filename = filename

        if filename:
            try:
                with open(filename, 'r') as f:
                    self.tables = json.load(f, object_hook=CustomEncoder.decode_object)
            except IOError:
                pass
            except json.decoder.JSONDecodeError as e:
                logging.warning(f'Error loading {filename}. The next write operation will overwrite the database with a clean copy: {e}')

    # NOTE: on purpose not @synchronized here
    def get_item(self, table_name, key):
        return first_or_none(self.query(table_name, key))

    @lock.synchronized
    def query(self, table_name, key, reverse=False):
        records = self.tables.get(table_name, [])
        filtered = [r for r in records if self._matches(r, key)]
        if reverse:
            filtered.reverse()
        return filtered

    # NOTE: on purpose not @synchronized here
    def query_index(self, table_name, index_name, key, reverse=False):
        return self.query(table_name, key, reverse=reverse)

    @lock.synchronized
    def put(self, table_name, key, data):
        records = self.tables.setdefault(table_name, [])
        index = self._find_index(records, key)
        if index is None:
            records.append(data)
        else:
            records[index] = data
        self._flush()

    @lock.synchronized
    def update(self, table_name, key, updates):
        records = self.tables.get(table_name, [])
        index = self._find_index(records, key)
        if index is None:
            return {}

        record = records[index]
        for name, update in updates.items():
            if isinstance(update, DynamoUpdate):
                if isinstance(update, DynamoIncrement):
                    record[name] = record.get(name, 0) + update.delta
                elif isinstance(update, DynamoAddToStringSet):
                    existing = record.get(name, set())
                    if not isinstance(existing, set):
                        raise TypeError(f'Expected a set in {name}, got: {existing}')
                    record[name] = existing | set(update.elements)
                elif isinstance(update, DynamoRemoveFromStringSet):
                    existing = record.get(name, set())
                    if not isinstance(existing, set):
                        raise TypeError(f'Expected a set in {name}, got: {existing}')
                    record[name] = existing - set(update.elements)
                else:
                    raise RuntimeError(f'Unsupported update type for in-memory database: {update}')
            elif update is None:
                if name in record:
                    del record[name]
            else:
                # Plain value update
                record[name] = update

        self._flush()
        return record

    @lock.synchronized
    def delete(self, table_name, key):
        records = self.tables.get(table_name, [])
        index = self._find_index(records, key)
        ret = None
        if index is not None:
            ret = records.pop(index)
            self._flush()
        return ret

    @lock.synchronized
    def item_count(self, table_name):
        return len(self.tables.get(table_name, []))

    @lock.synchronized
    def scan(self, table_name):
        return self.tables.get(table_name, [])

    def _find_index(self, records, key):
        for i, v in enumerate(records):
            if self._matches(v, key):
                return i
        return None

    def _matches(self, record, key):
        return all(record.get(k) == v for k, v in key.items())

    def _flush(self):
        if self.filename:
            try:
                with open(self.filename, 'w') as f:
                    json.dump(self.tables, f, indent=2, cls=CustomEncoder)
            except IOError:
                pass

def is_dynamo_available():
    return bool(os.getenv ('AWS_DYNAMODB_ACCESS_KEY'))


def first_or_none(xs):
    return xs[0] if xs else None

@dataclass
class TableLookup:
    table_name: str

@dataclass
class IndexLookup:
    table_name: str
    index_name: str


class DynamoUpdate:
    def to_dynamo(self):
        raise NotImplementedError()

class DynamoIncrement(DynamoUpdate):
    def __init__(self, delta=1):
        self.delta = delta

    def to_dynamo(self):
        return {
                'Action': 'ADD',
                'Value': { 'N': str(self.delta) },
            }

class DynamoAddToStringSet(DynamoUpdate):
    """Add one or more elements to a string set."""
    def __init__(self, *elements):
        self.elements = elements

    def to_dynamo(self):
        return {
                'Action': 'ADD',
                'Value': { 'SS': list(self.elements) },
            }


class DynamoRemoveFromStringSet(DynamoUpdate):
    """Remove one or more elements to a string set."""
    def __init__(self, *elements):
        self.elements = elements

    def to_dynamo(self):
        return {
                'Action': 'DELETE',
                'Value': { 'SS': list(self.elements) },
            }

def replace_decimals(obj):
    """
    Replace Decimals with native Python values.

    The default DynamoDB deserializer returns Decimals instead of ints,
    which we can't to-JSON. *sigh*.
    """
    import decimal

    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.iterkeys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


class CustomEncoder(json.JSONEncoder):
    """An encoder that serializes non-standard types like sets."""
    def default(self, obj):
        if isinstance(obj, set):
            return {"$type": "set", "elements": list(obj)}
        return json.JSONEncoder.default(self, obj)


    @staticmethod
    def decode_object(obj):
        """The decoding for the encoding above."""
        if obj.get('$type') == 'set':
            return set(obj['elements'])
        return obj
