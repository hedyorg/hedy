import functools
import base64
import boto3
import copy
import numbers
from abc import ABCMeta
import os
import logging
from config import config
from . import querylog
from dataclasses import dataclass
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
import json
import threading
from typing import List, Optional


class TableStorage(metaclass=ABCMeta):
    def get_item(self, table_name, key): ...

    # The 'sort_key' argument for query and query_index is used to indicate that one of the keys is a sort_key
    # This is now needed because we can query by index sort key too. Still hacky hacky :).
    def query(self, table_name, key, sort_key, reverse, limit, pagination_token): ...
    def query_index(self, table_name, index_name, keys, sort_key, reverse=False, limit=None, pagination_token=None): ...
    def put(self, table_name, key, data): ...
    def update(self, table_name, key, updates): ...
    def delete(self, table_name, key): ...
    def item_count(self, table_name): ...
    def scan(self, table_name, limit, pagination_token): ...


@dataclass
class IndexKey:
    partition_key: str
    sort_key: str = None


@dataclass
class ResultPage:
    """A page of results, as returned by get_many().

    If the field `next_page_token` has a non-`None` value,
    there is more data to retrieve.

    Implements the iterator protocol, so can be used in a `for`
    loop. To convert it to a `list`, write:

        result_list = list(table.get_many(...))
    """
    records: List[dict]
    next_page_token: Optional[str]

    @property
    def has_next_page(self):
        return bool(self.next_page_token)

    def __iter__(self):
        return iter(self.records)

    def __getitem__(self, i):
        return self.records[i]

    def __len__(self):
        return len(self.records)

    def __nonzero__(self):
        return bool(self.records)
    __bool__ = __nonzero__


class Table:
    """Dynamo table access

    Transparently handles indexes, and doesn't support sort keys yet.

    Parameters:
        - partition_key: the partition key for the table.
        - indexed_fields: a list of fields that have a (global) index on them.
          Each individual index must be named '{field}-index', and each must
          project the full set of attributes. Indexes can have a partition and their
          own sort keys.
        - sort_key: a field that is the sort key for the table.
    """
    def __init__(self, storage: TableStorage, table_name, partition_key, sort_key=None, indexed_fields=None):
        self.storage = storage
        self.table_name = table_name
        self.partition_key = partition_key
        self.sort_key = sort_key
        self.indexed_fields = indexed_fields or []

    @querylog.timed_as('db_get')
    def get(self, key, sort_key=None):
        """Gets an item by key from the database.

        The key must be a dict with a single entry which references the
        partition key or an index key.
        """
        querylog.log_counter(f'db_get:{self.table_name}')
        lookup = self._determine_lookup(key, many=False)
        if isinstance(lookup, TableLookup):
            return self.storage.get_item(lookup.table_name, lookup.key)
        if isinstance(lookup, IndexLookup):
            return first_or_none(
                self.storage.query_index(lookup.table_name, lookup.index_name, lookup.key, sort_key=lookup.sort_key, limit=1)[0]
            )
        assert False

    @querylog.timed_as('db_get_many')
    def get_many(self, key, sort_key=None, reverse=False, limit=None, pagination_token=None):
        """Gets a list of items by key from the database.

        The key must be a dict with a single entry which references the
        partition key or an index key.

        sort_key is a string - the name of the sort_key

        `get_many` reads up to 1MB of data from the database, or a maximum of `limit`
        records, whichever one is hit first.
        """
        querylog.log_counter(f'db_get_many:{self.table_name}')

        lookup = self._determine_lookup(key, many=True)
        if isinstance(lookup, TableLookup):
            items, next_page_token = self.storage.query(lookup.table_name, lookup.key,
                sort_key=self.sort_key,
                reverse=reverse,
                limit=limit,
                pagination_token=decode_page_token(pagination_token))
        elif isinstance(lookup, IndexLookup):
            items, next_page_token = self.storage.query_index(lookup.table_name, lookup.index_name, lookup.key,
                sort_key=lookup.sort_key,
                reverse=reverse,
                limit=limit,
                pagination_token=decode_page_token(pagination_token))
        else:
            assert False
        querylog.log_counter('db_get_many_items', len(items))
        return ResultPage(items, encode_page_token(next_page_token))

    @querylog.timed_as('db_create')
    def create(self, data):
        """Put a single complete record into the database."""
        if self.partition_key not in data:
            raise ValueError(f"Expecting '{self.partition_key}' field in create() call, got: {data}")
        if self.sort_key and self.sort_key not in data:
            raise ValueError(f"Expecting '{self.sort_key}' field in create() call, got: {data}")

        querylog.log_counter(f'db_create:{self.table_name}')
        self.storage.put(self.table_name, self._extract_key(data), data)

    def put(self, data):
        """An alias for 'create', if calling create reads uncomfortably."""
        return self.create(data)

    @querylog.timed_as('db_update')
    def update(self, key, updates):
        """Update select fields of a given record.

        The values of data can be plain data, or an instance of
        one of the subclasses of DynamoUpdate which represent
        updates that aren't representable as plain values.
        """
        querylog.log_counter(f'db_update:{self.table_name}')
        self._validate_key(key)

        return self.storage.update(self.table_name, key, updates)

    @querylog.timed_as('db_del')
    def delete(self, key):
        """Delete an item by primary key.

        Returns the delete item.
        """
        querylog.log_counter('db_del:' + self.table_name)
        self._validate_key(key)

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
    def scan(self, limit=None, pagination_token=None):
        """Reads the entire table into memory."""
        querylog.log_counter('db_scan:' + self.table_name)
        items, next_page_token = self.storage.scan(self.table_name, limit=limit, pagination_token=decode_page_token(pagination_token))
        return ResultPage(items, encode_page_token(next_page_token))

    @querylog.timed_as('db_describe')
    def item_count(self):
        querylog.log_counter('db_describe:' + self.table_name)
        return self.storage.item_count(self.table_name)

    def _determine_lookup(self, key_data, many):
        if any(not v for v in key_data.values()):
            raise ValueError(f'Key data cannot have empty values: {key_data}')

        keys = set(key_data.keys())
        table_keys = self._key_names()
        one_key = list(keys)[0]

        # We do a regular table lookup if both the table partition and sort keys occur in the given key.
        if keys == table_keys:
            return TableLookup(self.table_name, key_data)

        # We do an index table lookup if the partition (and possibly the sort key) of an index occur in the given key.
        for index in self.indexed_fields:
            index_key_names = [x for x in [index.partition_key, index.sort_key] if x is not None]
            if keys == set(index_key_names) or one_key == index.partition_key:
                return IndexLookup(
                    self.table_name,
                    f'{"-".join(index_key_names)}-index',
                    key_data,
                    index.sort_key)

        if len(keys) != 1:
            raise RuntimeError(f'Getting key data: {key_data}, but expecting: {table_keys}')

        # If the one key matches the partition key, it must be because we also have a
        # sort key, but that's allowed because we are looking for 'many' records.
        if one_key == self.partition_key:
            if not many:
                raise RuntimeError(f'Looking up one value, but missing sort key: {self.sort_key} in {key_data}')
            return TableLookup(self.table_name, key_data)

        raise RuntimeError(f'Field not partition key or index: {one_key}')

    def _extract_key(self, data):
        """
        Extract the key data out of plain data.
        """
        if self.partition_key not in data:
            raise RuntimeError(f"Partition key '{self.partition_key}' missing from data: {data}")
        if self.sort_key and self.sort_key not in data:
            raise RuntimeError(f"Sort key '{self.sort_key}' missing from data: {data}")

        return { k: data[k] for k in self._key_names() }

    def _key_names(self):
        return set(x for x in [self.partition_key, self.sort_key] if x is not None)

    def _validate_key(self, key):
        if key.keys() != self._key_names():
            raise RuntimeError(f'key fields incorrect: {key} != {self._key_names()}')
        if any(not v for v in key.values()):
            raise RuntimeError(f'key fields cannot be empty: {key}')

DDB_SERIALIZER = TypeSerializer()
DDB_DESERIALIZER = TypeDeserializer()


class AwsDynamoStorage(TableStorage):
    @staticmethod
    def from_env():
        # If we have AWS credentials, use the real DynamoDB
        if os.getenv('AWS_ACCESS_KEY_ID'):
            db = boto3.client ('dynamodb', region_name = config ['dynamodb'] ['region'])
            db_prefix = os.getenv ('AWS_DYNAMODB_TABLE_PREFIX', '')
            return AwsDynamoStorage(db, db_prefix)
        return None

    def __init__(self, db, db_prefix):
        self.db = db
        self.db_prefix = db_prefix

    def get_item(self, table_name, key):
        result = self.db.get_item(
            TableName=make_table_name(self.db_prefix, table_name),
            Key = self._encode(key))
        return self._decode(result.get('Item', None))

    def query(self, table_name, key, sort_key, reverse, limit, pagination_token):
        key_expression, attr_values, attr_names = self._prep_query_data(key, sort_key)
        result = self.db.query(**notnone(
            TableName=make_table_name(self.db_prefix, table_name),
            KeyConditionExpression=key_expression,
            ExpressionAttributeValues=attr_values,
            ScanIndexForward=not reverse,
            ExpressionAttributeNames=attr_names,
            Limit=limit,
            ExclusiveStartKey=self._encode(pagination_token) if pagination_token else None))

        items = [self._decode(x) for x in result.get('Items', [])]
        next_page_token = self._decode(result.get('LastEvaluatedKey', None)) if result.get('LastEvaluatedKey', None) else None
        return items, next_page_token

    def query_index(self, table_name, index_name, keys, sort_key, reverse=False, limit=None, pagination_token=None):
        key_expression, attr_values, attr_names = self._prep_query_data(keys, sort_key)

        result = self.db.query(**notnone(
            TableName=make_table_name(self.db_prefix, table_name),
            IndexName=index_name,
            KeyConditionExpression=key_expression,
            ExpressionAttributeValues=attr_values,
            ScanIndexForward=not reverse,
            ExpressionAttributeNames=attr_names,
            Limit=limit,
            ExclusiveStartKey=self._encode(pagination_token) if pagination_token else None))

        items = [self._decode(x) for x in result.get('Items', [])]
        next_page_token = self._decode(result.get('LastEvaluatedKey', None)) if result.get('LastEvaluatedKey', None) else None
        return items, next_page_token

    def _prep_query_data(self, key, sort_key=None):
        eq_conditions, special_conditions = DynamoCondition.partition(key)
        validate_only_sort_key(special_conditions, sort_key)

        # We must escape field names with a '#' because Dynamo is unhappy
        # with fields called 'level' etc: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html
        # This escapes too much, but at least it's easy.

        key_expression = ' AND '.join(
            [f'#{field} = :{field}' for field in eq_conditions.keys()] +
            [cond.to_dynamo_expression(field) for field, cond in special_conditions.items()])

        attr_values = {f':{field}': DDB_SERIALIZER.serialize(key[field]) for field in eq_conditions.keys()}
        for field, cond in special_conditions.items():
            attr_values.update(cond.to_dynamo_values(field))

        attr_names = {'#' + field: field for field in key.keys()}

        return key_expression, attr_values, attr_names

    def put(self, table_name, _key, data):
        return self.db.put_item(
            TableName=make_table_name(self.db_prefix, table_name),
            Item = self._encode(data))

    def update(self, table_name, key, updates):
        value_updates = {k: v for k, v in updates.items() if not isinstance(v, DynamoUpdate)}
        special_updates = {k: v.to_dynamo() for k, v in updates.items() if isinstance(v, DynamoUpdate)}

        return self.db.update_item(
            TableName=make_table_name(self.db_prefix, table_name),
            Key = self._encode(key),
            AttributeUpdates = {
                **self._encode_updates(value_updates),
                **special_updates,
            })

    def delete(self, table_name, key):
        return self.db.delete_item(
            TableName=make_table_name(self.db_prefix, table_name),
            Key = self._encode(key))

    def item_count(self, table_name):
        result = self.db.describe_table (
            TableName=make_table_name(self.db_prefix, table_name))
        return result['Table']['ItemCount']

    def scan(self, table_name, limit, pagination_token):
        result = self.db.scan(**notnone(
            TableName=make_table_name(self.db_prefix, table_name),
            Limit=limit,
            ExclusiveStartKey=self._encode(pagination_token) if pagination_token else None))
        items = [self._decode(x) for x in result.get('Items', [])]
        next_page_token = self._decode(result.get('LastEvaluatedKey', None)) if result.get('LastEvaluatedKey', None) else None
        return items, next_page_token

    def _encode (self, data):
        return {k: DDB_SERIALIZER.serialize(v) for k, v in data.items()}

    def _encode_updates (self, data):
        def encode_update(value):
            # None is special, we use it to remove a field from a record
            if value is None:
                return {'Action': 'DELETE'}
            else:
                return {'Value': DDB_SERIALIZER.serialize(value)}
        return {k: encode_update(v) for k, v in data.items()}

    def _decode (self, data):
        if data is None:
            return None

        return {k: replace_decimals(DDB_DESERIALIZER.deserialize(v)) for k, v in data.items()}


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
                with open(filename, 'r', encoding='utf-8') as f:
                    self.tables = json.load(f, object_hook=CustomEncoder.decode_object)
            except IOError:
                pass
            except json.decoder.JSONDecodeError as e:
                logging.warning(f'Error loading {filename}. The next write operation will overwrite the database with a clean copy: {e}')

    # NOTE: on purpose not @synchronized here
    def get_item(self, table_name, key):
        items, _ = self.query(table_name, key, sort_key=None, reverse=False, limit=None, pagination_token=None)
        return first_or_none(items)

    @lock.synchronized
    def query(self, table_name, key, sort_key, reverse, limit, pagination_token):
        eq_conditions, special_conditions = DynamoCondition.partition(key)
        validate_only_sort_key(special_conditions, sort_key)

        records = self.tables.get(table_name, [])
        filtered = [r for r in records if self._query_matches(r, eq_conditions, special_conditions)]

        if sort_key:
            filtered.sort(key=lambda x: x[sort_key])

        if reverse:
            filtered.reverse()

        # Pagination token
        def extract_key(i, record):
            ret = { k: record[k] for k in key.keys() }
            if sort_key is None:
                ret['offset'] = i
            else:
                ret[sort_key] = record[sort_key]
            return ret

        def orderable(key):
            partition_key = [k for k in key.keys() if k != sort_key][0]
            second_key = [k for k in key.keys() if k != partition_key][0]
            return (key[partition_key], key[second_key])

        def before_or_equal(key0, key1):
            k0 = orderable(key0)
            k1 = orderable(key1)
            return k0 <= k1 if not reverse or not sort_key else k1 <= k0

        with_keys = [(extract_key(i, r), r) for i, r in enumerate(filtered)]
        while pagination_token and with_keys and before_or_equal(with_keys[0][0], pagination_token):
            with_keys.pop(0)

        next_page_key = None
        if limit and limit < len(with_keys):
            with_keys = with_keys[:limit]
            next_page_key = with_keys[-1][0]

        return copy.copy([record for _, record in with_keys]), next_page_key

    # NOTE: on purpose not @synchronized here
    def query_index(self, table_name, index_name, keys, sort_key, reverse=False, limit=None, pagination_token=None):
        return self.query(table_name, keys, sort_key=sort_key, reverse=reverse, limit=limit, pagination_token=pagination_token)

    @lock.synchronized
    def put(self, table_name, key, data):
        records = self.tables.setdefault(table_name, [])
        index = self._find_index(records, key)
        if index is None:
            records.append(copy.copy(data))
        else:
            records[index] = copy.copy(data)
        self._flush()

    @lock.synchronized
    def update(self, table_name, key, updates):
        records = self.tables.setdefault(table_name, [])
        index = self._find_index(records, key)
        if index is None:
            records.append(key.copy())
            index = len(records) - 1

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
                elif isinstance(update, DynamoAddToList):
                    existing = record.get(name, [])
                    if not isinstance(existing, list):
                        raise TypeError(f'Expected a list in {name}, got: {existing}')
                    record[name] = existing + list(update.elements)
                elif isinstance(update, DynamoAddToNumberSet):
                    existing = record.get(name, set())
                    if not isinstance(existing, set):
                        raise TypeError(f'Expected a set in {name}, got: {existing}')
                    record[name] = existing | set(update.elements)
                else:
                    raise RuntimeError(f'Unsupported update type for in-memory database: {update}')
            elif update is None:
                if name in record:
                    del record[name]
            else:
                # Plain value update
                record[name] = update

        self._flush()
        return record.copy()

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
    def scan(self, table_name, limit, pagination_token):
        items = self.tables.get(table_name, [])[:]

        start_index = 0
        if pagination_token:
            start_index = pagination_token['offset']
            items = items[pagination_token['offset']:]

        next_page_token = None
        if limit and limit < len(items):
            next_page_token = {'offset': start_index + limit}
            items = items[:limit]

        items = copy.copy(items)
        return items, next_page_token

    def _find_index(self, records, key):
        for i, v in enumerate(records):
            if self._eq_matches(v, key):
                return i
        return None

    def _eq_matches(self, record, key):
        return all(record.get(k) == v for k, v in key.items())

    def _query_matches(self, record, eq, conds):
        return (all(record.get(k) == v for k, v in eq.items())
            and all(cond.matches(record.get(k)) for k, cond in conds.items()))

    def _flush(self):
        if self.filename:
            try:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    json.dump(self.tables, f, indent=2, cls=CustomEncoder)
            except IOError:
                pass

def first_or_none(xs):
    return xs[0] if xs else None

@dataclass
class TableLookup:
    table_name: str
    key: dict

@dataclass
class IndexLookup:
    table_name: str
    index_name: str
    key: dict
    sort_key: Optional[str]


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

class DynamoAddToNumberSet(DynamoUpdate):
    """Add one or more elements to a number set."""
    def __init__(self, *elements):
        for el in elements:
            if not isinstance(el, numbers.Real):
                raise ValueError(f'Must be a number, got: {el}')
        self.elements = elements

    def to_dynamo(self):
        return {
                'Action': 'ADD',
                'Value': { 'NS': [str(x) for x in self.elements] },
            }


class DynamoAddToList(DynamoUpdate):
    """Add one or more elements to a list."""
    def __init__(self, *elements):
        self.elements = elements

    def to_dynamo(self):
        return {
                'Action': 'ADD',
                'Value': { 'L': [DDB_SERIALIZER.serialize(x) for x in self.elements] },
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


class DynamoCondition:
    """Base class for Query conditions.

    These encode any type of comparison supported by Dynamo except equality.

    Conditions only apply to sort keys.
    """
    def to_dynamo_expression(self, _field_name):
        """Render expression part of Dynamo query."""
        raise NotImplementedError()

    def to_dynamo_values(self, _field_name):
        """Render values for the Dynamo expression."""
        raise NotImplementedError()

    def matches(self, value):
        """Whether or not the given value matches the condition (for in-memory db)."""
        raise NotImplementedError()

    @staticmethod
    def partition(key):
        """Partition a dictionary into 2 dictionaries.

        The first one will contain all elements for which the values are
        NOT of type DynamoCondition. The other one will contain all the elements
        for which the value ARE DynamoConditions.
        """
        eq_conditions = { k: v for k, v in key.items() if not isinstance(v, DynamoCondition) }
        special_conditions = { k: v for k, v in key.items() if isinstance(v, DynamoCondition) }

        return (eq_conditions, special_conditions)


class Between(DynamoCondition):
    """Assert that a value is between two other values."""

    def __init__(self, minval, maxval):
        self.minval = minval
        self.maxval = maxval

    def to_dynamo_expression(self, field_name):
        return f'#{field_name} BETWEEN :{field_name}_min AND :{field_name}_max'

    def to_dynamo_values(self, field_name):
        return {
            f':{field_name}_min': DDB_SERIALIZER.serialize(self.minval),
            f':{field_name}_max': DDB_SERIALIZER.serialize(self.maxval),
        }

    def matches(self, value):
        return self.minval <= value <= self.maxval


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
        for k in obj.keys():
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


def validate_only_sort_key(conds, sort_key):
    """Check that only the sort key is used in the given key conditions."""
    if sort_key and set(conds.keys()) - {sort_key}:
        raise RuntimeError(f'Conditions only allowed on sort key {sort_key}, got: {list(conds)}')


def encode_page_token(x):
    """Encode a compound key page token (dict) to a string."""
    if x is None: return None
    return base64.b64encode(json.dumps(x).encode('utf-8'))


def decode_page_token(x):
    """Decode string page token to compound key (dict)."""
    if x is None: return None
    return json.loads(base64.b64decode(x).decode('utf-8'))


def notnone(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def make_table_name(prefix, name):
    return f'{prefix}-{name}' if prefix else name