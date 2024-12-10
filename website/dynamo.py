import base64
import copy
import functools
import json
import logging
import math
import numbers
import os
import threading
import time
import random
import datetime
import collections
import re
from abc import ABCMeta
from dataclasses import dataclass
from typing import List, Optional

import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

from config import config

from . import querylog

logger = logging.getLogger(__name__)


class TableStorage(metaclass=ABCMeta):
    def get_item(self, table_name, key):
        ...

    def batch_get_item(self, table_name, keys_map, table_key_names):
        ...

    # The 'sort_key' argument for query and query_index is used to indicate that one of the keys is a sort_key
    # This is now needed because we can query by index sort key too. Still hacky hacky :).
    def query(self, table_name, key, sort_key, reverse, limit, pagination_token, filter=None):
        ...

    def query_index(self, table_name, index_name, keys, sort_key, reverse=False,
                    limit=None, pagination_token=None, keys_only=None, table_key_names=None,
                    filter=None):
        ...

    def put(self, table_name, key, data):
        """Put the given data under the given key.

        Does not need to return anything.
        """
        ...

    def update(self, table_name, key, updates):
        """Update the given record, identified by a key, with updates.

        Must return the updated state of the record.
        """
        ...

    def delete(self, table_name, key):
        ...

    def item_count(self, table_name):
        ...

    def scan(self, table_name, limit, pagination_token):
        ...


class KeySchema:
    """The schema of a table key.

    Consists of a partition key and optionally a sort key.
    """

    def __init__(self, partition_key, sort_key=None):
        self.partition_key = partition_key
        self.sort_key = sort_key
        self.is_compound = sort_key is not None

        # Both names in an array
        self.key_names = [self.partition_key] + ([self.sort_key] if self.sort_key else [])

    def matches(self, key):
        """Whether the given key matches the current schema.

        There must be exactly one value which is the partition key,
        or exactly two values which are the partition and sort keys.
        """
        names = tuple(key.keys())
        if len(names) == 1:
            return self.partition_key == names[0]
        if len(names) == 2:
            return ((self.partition_key == names[0] and self.sort_key == names[1])
                    or (self.partition_key == names[1] and self.sort_key == names[0]))
        return False

    def contains_both_keys(self, data):
        """Return whether all keys in are in the data."""
        return (self.partition_key in data and
                (not self.sort_key or self.sort_key in data))

    def extract(self, data):
        ret = {}
        if self.partition_key not in data:
            raise ValueError(f"Partition key '{self.partition_key}' missing from data: {data}")
        ret[self.partition_key] = data[self.partition_key]

        if self.sort_key:
            if self.sort_key not in data:
                raise ValueError(f"Sort key '{self.sort_key}' missing from data: {data}")
            ret[self.sort_key] = data[self.sort_key]
        return ret

    def to_string(self, opt=False):
        if self.sort_key and opt:
            return f'({self.partition_key}[, {self.sort_key}])'
        if self.sort_key and not opt:
            return f'({self.partition_key}, {self.sort_key})'
        return f'({self.partition_key})'

    def __repr__(self):
        return f'KeySchema({repr(self.partition_key)}, {repr(self.sort_key)})'

    def __str__(self):
        return self.to_string()


class Index:
    """A DynamoDB index.

    The name of the index will be assumed to be '{partition_key}-{sort_key}-index', if not given.

    Specify if the index is a keys-only index. If not, is is expected to have all fields.
    """

    def __init__(self, partition_key: str, sort_key: str = None, index_name: str = None, keys_only: bool = False):
        self.key_schema = KeySchema(partition_key, sort_key)
        self.index_name = index_name
        self.keys_only = keys_only
        if not self.index_name:
            self.index_name = '-'.join([partition_key] + ([sort_key] if sort_key else [])) + '-index'


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
    prev_page_token: Optional[str] = None
    next_page_token: Optional[str] = None

    # Holds a reference to a PaginationKey object, which can be used to calculate
    # pagination keys for arbitrary elements from the result set if desired.
    #
    # This object may not always be present; it mostly exists for `get_page()` to
    # be able to use the same pagination key as expected by `get_many()`.
    pagination_key: Optional['PaginationKey'] = None

    @property
    def has_next_page(self):
        return bool(self.next_page_token)

    @property
    def has_prev_page(self):
        return bool(self.prev_page_token)

    def __iter__(self):
        return iter(self.records)

    def __getitem__(self, i):
        return self.records[i]

    def __len__(self):
        return len(self.records)

    def __nonzero__(self):
        return bool(self.records)

    __bool__ = __nonzero__


class Cancel(metaclass=ABCMeta):
    """Contract for cancellation tokens."""
    @staticmethod
    def after_timeout(duration):
        return TimeoutCancellation(datetime.datetime.now() + duration)

    @staticmethod
    def after_seconds(seconds):
        return TimeoutCancellation(datetime.datetime.now() + datetime.timedelta(seconds=seconds))

    @staticmethod
    def never():
        return CallableCancellation(lambda: False)

    @staticmethod
    def immediate():
        return CallableCancellation(lambda: True)

    def is_cancelled(self):
        ...


class TimeoutCancellation(Cancel):
    """Cancellation token for a timeout."""

    def __init__(self, deadline):
        self.deadline = deadline

    def is_cancelled(self):
        return datetime.datetime.now() >= self.deadline


class CallableCancellation(Cancel):
    """Use a callable as a cancellation token."""

    def __init__(self, cb):
        self.cb = cb

    def is_cancelled(self):
        return self.cb()


class Table:
    """Dynamo table access

    Transparently handles indexes, and doesn't support sort keys yet.

    Parameters:
        - partition_key: the partition key for the table.
        - indexes: a list of fields that have a GSI on them.
          Each individual index must be named '{field}-index', and each must
          project the full set of attributes. Indexes can have a partition and their
          own sort keys.
        - sort_key: a field that is the sort key for the table.
        - Types: a dictionary of field name to type object, to validate fields against.
          Does not have to be exhaustive, but it must include all the indexed fields.
          You can use: str, list, bool, bytes, int, float, numbers.Number, dict, list,
          string_set, number_set, binary_set (last 3 declared in this module).
    """
    key_schema: KeySchema
    storage: TableStorage
    indexes: List[Index]

    def __init__(self, storage: TableStorage, table_name, partition_key, types=None, sort_key=None, indexes: Optional[List[Index]] = None):
        self.key_schema = KeySchema(partition_key, sort_key)
        self.storage = storage
        self.table_name = table_name
        self.indexes: List[Index] = indexes or []
        self.indexed_fields = set()
        if types is not None:
            self.types = Validator.ensure_all(types)
        else:
            self.types = None

        all_schemas = [self.key_schema] + [i.key_schema for i in self.indexes]
        for schema in all_schemas:
            for field in schema.key_names:
                self.indexed_fields.add(field)

        # Check to make sure the indexes have unique partition keys. We do this to unambiguously
        # check which index to use for a given query.
        self._validate_indexes_unambiguous()

        # Check to make sure all indexed fields have a declared type
        if self.types:
            if undeclared := [f for f in self.indexed_fields if f not in self.types]:
                raise ValueError(f'Declare the type of these fields which are used as keys: {", ".join(undeclared)}')

    @querylog.timed_as("db_get")
    def get(self, key):
        """Gets an item by key from the database.

        The key must be a dict with a single entry which references the
        partition key or an index key.
        """
        querylog.log_counter(f"db_get:{self.table_name}")
        lookup = self._determine_lookup(key, many=False)
        if isinstance(lookup, TableLookup):
            return self.storage.get_item(lookup.table_name, lookup.key)
        if isinstance(lookup, IndexLookup):
            pagination_key = PaginationKey.from_index(lookup.key.keys(), lookup.sort_key, self.key_schema)
            return first_or_none(
                self.storage.query_index(
                    lookup.table_name, lookup.index_name, lookup.key, sort_key=lookup.sort_key, limit=1,
                    keys_only=lookup.keys_only, table_key_names=self.key_schema.key_names,
                    pagination_key=pagination_key,
                )[0]
            )
        assert False

    @querylog.timed_as("db_batch_get")
    def batch_get(self, keys):
        """Return a number of items by (primary+sort) key from the database.

        The 'keys' argument can be one of 3 different types. Depending on the type
        of the input, a different output will be returned. The supported types are:

        - Input: a list of database keys
          Example Input: `[{ 'id': 'a' }, { 'id': 'b' }]`
          Response: a list with the actual records
          Example Output: `[{ 'id': 'a', 'field': 'b', 'more': 'c', ... }, ...]`.

        - Input: a dictionary, mapping some chosen identifier to a database (dictionary) key.
          Example Input: `{ 'record1': { 'id': 'a' }, 'record2': { 'id': 'b' }`
          Response: a dictionary with the same keys and the actual records as values.
          Example Output: `{ 'record1': { 'id': 'a', 'field': 'b', 'more': 'c', ... }, ... }`.

        - Input: a ResultPage obtained from `get_many()`.
          Response: behaves like the "list" input case, but returns a `ResultPage` with
          the `prev_page_token` and `next_page_token` fields populated.

        Each key must be a dict with a single entry which references the
        partition key. This is currently not supporting index lookups.
        """
        querylog.log_counter(f"db_batch_get:{self.table_name}")
        input_is_dict = isinstance(keys, dict)

        # We normalize to a dict here, then maybe pull it out again to a list later
        keys_dict = keys if input_is_dict else {f'k{i}': k for i, k in enumerate(keys)}

        # We only try a table lookup
        non_matching_keys = [k for k in keys_dict.values() if not self.key_schema.contains_both_keys(k)]
        if non_matching_keys:
            raise ValueError(f'batch_get keys must contain {self.key_schema}, found: {non_matching_keys}')

        resp_dict = self.storage.batch_get_item(
            self.table_name,
            {k: self.key_schema.extract(l) for k, l in keys_dict.items()},
            table_key_names=self.key_schema.key_names)

        if input_is_dict:
            return {k: resp_dict.get(k) for k in keys.keys()}
        else:
            items = [resp_dict.get(f'k{i}') for i in range(len(keys))]
            if isinstance(keys, ResultPage):
                return ResultPage(items, keys.prev_page_token, keys.next_page_token)
            return items

    @querylog.timed_as("db_get_many")
    def get_many(self, key, reverse=False, limit=None, pagination_token=None, filter=None, server_side_filter=None):
        """Gets a list of items by key from the database.

        The key must be a dict with a single entry which references the
        partition key or an index key.

        `get_many` reads up to 1MB of data from the database, or a maximum of
        `limit` records, whichever one is hit first.

        'server_side_filter' can be used to filter down the max 1MB of data read
        from the database, to avoid sending useless bytes over the internet.

        The result object will have `next_page_token` and `prev_page_token` members
        which can be used to paginate through the result set.

        # On filtering

        - 'server_side_filter' is a dictionary of values that will be applied
          server-side after reading. The values should be either literal
          strings, ints or bools that are compared to the values in the database
          literally, or instances of subclasses of `DynamoCondition`.
        - The response may contain less than `limit` rows if
          'server_side_filter' is used. The response may contain 0 rows, yet still
          have a next page, if all rows read from disk are filtered out.
        - Filtering saves bytes sent over the wire, but still costs time and
          money, and may lead in receiving nearly no records. It is still
          important to pick a good key/index to read. Filters will not magically
          make a table scan efficient!

        'filter' is also accepted as a deprecated spelling of
        'server_side_filter' (but 'server_side_filter' is preferred for
        consistency with 'get_page').
        """
        querylog.log_counter(f"db_get_many:{self.table_name}")

        if filter is not None and server_side_filter is not None:
            raise ValueError("Only one of 'filter' and 'server_side_filter' may be specified")
        server_side_filter = server_side_filter or filter

        inverse_page, pagination_token = decode_page_token(pagination_token)
        if inverse_page:
            reverse = not reverse

        lookup = self._determine_lookup(key, many=True)
        if isinstance(lookup, TableLookup):
            validate_filter_nonkey_columns(server_side_filter, self.key_schema)

            pagination_key = PaginationKey.from_table(self.key_schema)
            items, next_page_token = self.storage.query(
                lookup.table_name,
                lookup.key,
                sort_key=self.key_schema.sort_key,
                reverse=reverse,
                limit=limit + 1 if limit else None,
                pagination_key=pagination_key,
                pagination_token=pagination_token,
                filter=server_side_filter
            )
        elif isinstance(lookup, IndexLookup):
            validate_filter_nonkey_columns(server_side_filter, lookup.key_schema)

            pagination_key = PaginationKey.from_index(lookup.key.keys(), lookup.sort_key, self.key_schema)
            items, next_page_token = self.storage.query_index(
                lookup.table_name,
                lookup.index_name,
                lookup.key,
                sort_key=lookup.sort_key,
                reverse=reverse,
                limit=limit + 1 if limit else None,
                pagination_key=pagination_key,
                pagination_token=pagination_token,
                keys_only=lookup.keys_only,
                table_key_names=self.key_schema.key_names,
                filter=server_side_filter,
            )
        else:
            assert False
        querylog.log_counter(f"db_get_many_items:{self.table_name}", len(items))

        # If we had a limit, we added 1 to it just to see if we didn't accidentally fetch exactly
        # as many items as the database had available. Slice back to the exactly requested amount.
        if limit and len(items) > limit:
            items = items[:limit]
            next_page_token = pagination_key.extract_dict(items[-1])
        prev_page_token = pagination_key.extract_dict(items[0]) if items and pagination_token else None

        # If we fetched a "previous page", we did a query using reverse=True. reverse again to get
        # the items back in the original order, and swap the prev and next page tokens.
        if inverse_page:
            items.reverse()
            next_page_token, prev_page_token = prev_page_token, next_page_token

        return ResultPage(
            items,
            encode_page_token(prev_page_token, True),
            encode_page_token(next_page_token, False),
            pagination_key=pagination_key)

    def get_page(self, key, limit, reverse=False, pagination_token=None, server_side_filter=None,
                 client_side_filter=None, timeout=5, fetch_factor=1.0):
        """Like `get_many()`, but may do multiple calls to the server to try and fill up the page to 'limit'.

        `get_many()` does one call, and may return up to 'limit' items. If that happens, `get_page()`
        will continue to make calls to fetch more items in order to return exactly 'limit' items,
        or the timeout is hit.

        'server_side_filter' is a dictionary with a set of values that will be applied as a server-side
        filter. The values should be either literal strings, ints or bools that are compared to the
        values in the database literally, or instances of subclasses of `DynamoCondition`.

        'client_side_filter' should be either a dictionary of values, or a
        callable (function) that will be called for every row. If it is a
        dictionary, the values in the dictionary must match the values in the
        records; if it is a callable, it will be invoked for every row and the
        callable should return True or False to indicate whether that row should
        be included.

        'fetch_factor' controls how many items are fetched per batch in order to try and fill
        'limit' items. Combination with an estimate of how many rows would be
        rejected due to filtering, this can be used to reduce the amount of individual queries
        necessary in order to come up with a given set of items (reducing latency slightly).
        Ignore this if you are unsure about the right value to use.

        # On server side filtering

        - 'server_side_filter' is a dictionary of values that will be applied
          server-side after reading. The values should be either literal
          strings, ints or bools that are compared to the values in the database
          literally, or instances of subclasses of `DynamoCondition`.
        - The response may contain less than `limit` rows if
          'server_side_filter' is used. The response may contain 0 rows, yet still
          have a next page, if all rows read from disk are filtered out.
        - Filtering saves bytes sent over the wire, but still costs time and
          money, and may lead in receiving nearly no records. It is still
          important to pick a good key/index to read. Filters will not magically
          make a table scan efficient!
        """
        if limit <= 0:
            raise ValueError('limit must be positive')
        items = []
        cancel = Cancel.after_seconds(timeout) if not isinstance(timeout, Cancel) else timeout
        predicate = make_predicate(client_side_filter)

        batch_size = math.ceil(limit * max(1.0, fetch_factor))

        # We need to know if we're doing a prevpage query or not.
        inverse_page, initial_pagination_token = decode_page_token(pagination_token)

        curr_pagination_token = pagination_token
        dropped_remaining_in_this_page = False
        first_page = None
        while len(items) < limit:
            space_remaining = limit - len(items)

            page = self.get_many(key, reverse=reverse, limit=batch_size,
                                 pagination_token=curr_pagination_token, filter=server_side_filter)
            if not first_page:
                first_page = page
            selected_in_this_page = [row for row in page if predicate(row)]

            if inverse_page:
                # They're already in the right order, but they need to go in the right place as well
                items = selected_in_this_page[-space_remaining:] + items
            else:  # Forward
                items.extend(selected_in_this_page[:space_remaining])
            dropped_remaining_in_this_page = len(selected_in_this_page) > space_remaining

            curr_pagination_token = page.next_page_token if not inverse_page else page.prev_page_token
            if not curr_pagination_token or cancel.is_cancelled():
                break

        if inverse_page:
            if dropped_remaining_in_this_page:
                prev_page_token = page.pagination_key.extract_dict(items[0])
            else:
                # Need to decode because it will be re-encoded below
                prev_page_token = decode_page_token(page.prev_page_token)[1] if page.prev_page_token else None

            # The last element of the first page marks our next_page_token. If this page is empty for
            # some reason, we just pretend that the initial pagination token is our forward pagination token.
            # Not entirely correct (we'll drop 1 element) but at least it gets us back into the flow.
            next_page_token = page.pagination_key.extract_dict(
                first_page[-1]) if first_page else initial_pagination_token
        else:
            if dropped_remaining_in_this_page:
                next_page_token = page.pagination_key.extract_dict(items[-1])
            else:
                # Need to decode because it will be re-encoded below
                next_page_token = decode_page_token(page.next_page_token)[1] if page.next_page_token else None

            # The first element of the first page marks our prev_page_token
            prev_page_token = page.pagination_key.extract_dict(
                first_page[0]) if first_page and pagination_token else None

        return ResultPage(
            items,
            encode_page_token(prev_page_token, True),
            encode_page_token(next_page_token, False))

    def get_all(self, key, reverse=False, batch_size=None):
        """Return an iterator that will iterate over all elements in the table matching the query.

        Iterating over all elements can take a long time, make sure you have a timeout in the loop
        somewhere!"""
        return GetManyIterator(self, key, reverse=reverse, batch_size=batch_size)

    @querylog.timed_as("db_create")
    def create(self, data):
        """Put a single complete record into the database."""
        if not self.key_schema.contains_both_keys(data):
            raise ValueError(f"Expecting fields {self.key_schema} in create() call, got: {data}")
        self._validate_indexable_fields(data, False)
        self._validate_types(data, full=True)

        querylog.log_counter(f"db_create:{self.table_name}")
        self.storage.put(self.table_name, self.key_schema.extract(data), data)
        return data

    def put(self, data):
        """An alias for 'create', if calling create reads uncomfortably."""
        return self.create(data)

    @querylog.timed_as("db_update")
    def update(self, key, updates):
        """Update select fields of a given record.

        The values of data can be plain data, or an instance of
        one of the subclasses of DynamoUpdate which represent
        updates that aren't representable as plain values.
        """
        querylog.log_counter(f"db_update:{self.table_name}")
        self._validate_indexable_fields(updates, True)
        self._validate_key(key)
        self._validate_types(updates, full=False)

        updating_keys = set(updates.keys()) & set(self.key_schema.key_names)
        if updating_keys:
            raise RuntimeError(' '.join([
                'update() may not include a key field in the \'updates\' field',
                f'({updating_keys} may not be part of {updates};',
                'did you accidentally pass an entire record to update()?)']))

        return self.storage.update(self.table_name, key, updates)

    @querylog.timed_as("db_del")
    def delete(self, key):
        """Delete an item by primary key.

        Returns the delete item.
        """
        querylog.log_counter("db_del:" + self.table_name)
        self._validate_key(key)

        return self.storage.delete(self.table_name, key)

    @querylog.timed_as("db_del_many")
    def del_many(self, key):
        """Delete all items matching a key.

        DynamoDB does not support this operation natively, so we have to turn
        it into a fetch+batch delete (and since our N is small, we do
        repeated "single" deletes instead of doing a proper batch delete).
        """
        querylog.log_counter("db_del_many:" + self.table_name)

        # The result of get_many is paged, so we might need to do this more than once.
        to_delete = self.get_many(key)
        backoff = ExponentialBackoff()
        while to_delete:
            for item in to_delete:
                key = self.key_schema.extract(item)
                self.delete(key)
            to_delete = self.get_many(key)
            backoff.sleep_when(to_delete)

    @querylog.timed_as("db_scan")
    def scan(self, limit=None, pagination_token=None):
        """Reads the entire table into memory.

        If 'limit' is given, there looks to be a desire to do proper pagination.
        To make the 'next_page_token' behavior more nicely for user code, we
        query 1 record more than expected, and use that to make sure we don't
        return a 'next_page_token' if the page would have been empty anyway.
        """
        querylog.log_counter("db_scan:" + self.table_name)
        pagination_key = PaginationKey.from_table(self.key_schema)
        inverse_page, pagination_token = decode_page_token(pagination_token)
        if inverse_page:
            raise ValueError('Scanning in reverse is not possible')

        items, next_page_token = self.storage.scan(
            self.table_name,
            limit=limit + 1 if limit else None,
            pagination_token=pagination_token,
            pagination_key=pagination_key,
        )

        if limit:
            # Set the next_page_token only if we retrieved N+1 items (there is an actual next page).
            has_more_items = len(items) > limit
            items = items[:limit]
            next_page_token = pagination_key.extract_dict(items[-1]) if has_more_items else None

        return ResultPage(items,
                          next_page_token=encode_page_token(next_page_token, False),
                          pagination_key=pagination_key)

    @querylog.timed_as("db_describe")
    def item_count(self):
        querylog.log_counter("db_describe:" + self.table_name)
        return self.storage.item_count(self.table_name)

    def _determine_lookup(self, key_data, many):
        """Given the key data, determine where we should perform the lookup.

        This can be either on the main table, or on one of the indexes.

        If the key data contains both a partition key and sort key, the table or
        index is identified unambiguously since the combination of (PK, SK) must
        be unique.

        If the key data contains only a partition key, we do the following:

        - If the PK matches the PK of the table, we do a table lookup.
        - If the PK matches a single index, we do a lookup in that index.
        - If the PK matches multiple indexes, we raise an error. The lookup
          needs to be disambiguated by adding a sort key with a `UseThisIndex`
          field.
        """
        if any(not v for v in key_data.values()):
            raise ValueError(f"Key data cannot have empty values: {key_data}")

        # We do a regular table lookup if both the table partition and sort keys occur in the given key.
        if self.key_schema.matches(key_data):
            # Sanity check that if we expect to query 1 element from the table, we must pass a sort key if defined
            if not many and not self.key_schema.contains_both_keys(key_data):
                raise ValueError(
                    f"Looking up one value, but missing sort key: {self.key_schema.sort_key} in {key_data}")

            return TableLookup(self.table_name, key_data)

        potential_indexes = [index for index in self.indexes if index.key_schema.matches(key_data)]

        data_keys = tuple(key_data.keys())

        if not potential_indexes:
            schemas = [self.key_schema] + [i.key_schema for i in self.indexes]
            str_schemas = ', '.join(s.to_string(opt=True) for s in schemas)
            raise ValueError(
                f"Table {self.table_name} can be queried using one of {str_schemas}. Got {data_keys}")

        if len(potential_indexes) == 1:
            index = potential_indexes[0]
            return IndexLookup(self.table_name, index.index_name, key_data,
                               index.key_schema.sort_key, keys_only=index.keys_only, key_schema=index.key_schema)

        # More than one index. This can only happen if a user passed a PK that is used
        # in multiple indexes. Frame a helpful error message.
        sort_keys = [i.key_schema.sort_key for i in potential_indexes]
        raise ValueError(
            f'Table {self.table_name} has multiple indexes with partition key \'{data_keys[0]}\'. Include one of these sort keys in your query {sort_keys} with a value of UseThisIndex() to indicate which index you want to query')

    def _validate_key(self, key):
        if not self.key_schema.contains_both_keys(key):
            raise ValueError(f"key fields incorrect: {key} not containing {self.key_schema}")
        if any(not v for v in key.values()):
            raise ValueError(f"key fields cannot be empty: {key}")

    def _validate_indexable_fields(self, data, for_update):
        """Check that all fields that have [index] keys on them in this data are either strings, ints or binaries.

        We can't validate whether the Dynamo index is properly defined, but at
        least we can catch some assumptions locally.
        """
        for field in self.indexed_fields:
            value = data.get(field)
            if value is None:
                continue

            if for_update and isinstance(value, DynamoUpdate):
                continue
            if isinstance(value, str) or isinstance(value, numbers.Number) or isinstance(value, bytes):
                continue

            raise ValueError('Trying to insert %r into table %s, but %s is a Partition or Sort Key of the table itself '
                             ' or an index, so must be of type string, number or binary.'
                             % ({field: value}, self.table_name, field))

    def _validate_types(self, data, full):
        """Validate the types in the record according to the 'self.types' map.

        If 'full=True' we will use the declared keys as a basis (making sure
        the record is complete). If full=False, we only use the given keys,
        making sure the updates are valid.
        """
        if self.types is None:
            return

        keys_to_validate = self.types.keys() if full else data.keys()

        for field in keys_to_validate:
            validator = self.types.get(field)
            if not validator:
                continue

            value = data.get(field)
            if not validate_value_against_validator(value, validator):
                raise ValueError(f'In {data}, value of {field} should be {validator} (got {value})')

    def _validate_indexes_unambiguous(self):
        """From a list of Index objects, make sure there are no duplicate sets of the same PK and SK.

        Also, there must not be an index with a PK that is a subset of an existing combination
        of PK and SK, because we wouldn't be able to disambiguate between them.
        """
        seen = set()
        pk_of_compound = set()

        # Add the table schema to begin with (we need to disambiguate with the table as well)
        seen.add(tuple(self.key_schema.key_names))
        if self.key_schema.is_compound:
            pk_of_compound.add(self.key_schema.partition_key)

        for index in self.indexes:
            key_names = tuple(index.key_schema.key_names)
            if key_names in seen:
                raise ValueError(f'Table {self.table_name}: multiple indexes with the same key: {key_names}')

            seen.add(key_names)
            if index.key_schema.is_compound:
                pk_of_compound.add(index.key_schema.partition_key)

        for index in self.indexes:
            if not index.key_schema.is_compound and index.key_schema.partition_key in pk_of_compound:
                raise ValueError(
                    f'Table {self.table_name}: PK-only index is a subset of a compound index: {index.key_schema}')


def validate_value_against_validator(value, validator: 'Validator'):
    """Validate a value against a validator.

    A validator can be a built-in class representing a type, like 'str'
    or 'int'.
    """
    if isinstance(value, DynamoUpdate):
        return value.validate_against_type(validator)
    else:
        return validator.is_valid(value)


def validate_filter_nonkey_columns(server_side_filter, key_schema):
    """Check that there are no filters that match columns in the key schema."""
    for column in server_side_filter or {}:
        if column in key_schema.key_names:
            raise ValueError(f'Do not use server_side_filter on "{column}", use a key lookup instead.')


DDB_SERIALIZER = TypeSerializer()
DDB_DESERIALIZER = TypeDeserializer()


class AwsDynamoStorage(TableStorage):
    @staticmethod
    def from_env():
        # If we have AWS credentials, use the real DynamoDB
        if os.getenv("AWS_ACCESS_KEY_ID"):
            db = boto3.client("dynamodb", region_name=config["dynamodb"]["region"])
            db_prefix = os.getenv("AWS_DYNAMODB_TABLE_PREFIX", "")
            return AwsDynamoStorage(db, db_prefix)
        return None

    def __init__(self, db, db_prefix):
        self.db = db
        self.db_prefix = db_prefix

    def get_item(self, table_name, key):
        result = self.db.get_item(TableName=make_table_name(self.db_prefix, table_name), Key=self._encode(key))
        return self._decode(result.get("Item", None))

    def batch_get_item(self, table_name, keys_map, table_key_names):
        # Do a batch query to DynamoDB. Handle that DDB will do at most 100 items by chunking.
        real_table_name = make_table_name(self.db_prefix, table_name)

        def immutable_key(record):
            # Extract the key fields from the record and make them suitable for indexing a dict
            return frozenset({k: record[k] for k in table_key_names}.items())

        # The input may have duplicates, but DynamoDB no likey
        key_to_ids = collections.defaultdict(list)
        to_query = []
        for id, key in keys_map.items():
            imkey = immutable_key(key)
            if imkey not in key_to_ids:
                to_query.append(self._encode(key))
            key_to_ids[imkey].append(id)

        ret = {}
        next_query = []

        def fill_er_up():
            # Fill up next_query (from to_query) until it has at most 100 items
            to_eat = min(100 - len(next_query), len(to_query))
            next_query.extend(to_query[:to_eat])
            to_query[:to_eat] = []

        fill_er_up()
        backoff = ExponentialBackoff()
        while next_query:
            result = self.db.batch_get_item(
                RequestItems={real_table_name: {'Keys': next_query}}
            )
            for row in result.get('Responses', {}).get(real_table_name, []):
                record = self._decode(row)
                for id in key_to_ids[immutable_key(record)]:
                    ret[id] = record

            # The DB may not have done everything (we might have gotten throttled). If so, sleep.
            next_query = result.get('UnprocessedKeys', {}).get(real_table_name, {}).get('Keys', [])
            backoff.sleep_when(to_query)
            fill_er_up()

        return ret

    def query(self, table_name, key, sort_key, reverse, limit, pagination_token, pagination_key, filter=None):
        key_expression, attr_values, attr_names = self._prep_query_data(key, sort_key)

        if filter:
            filter_expression, filter_values, filter_names = self._prep_query_data(filter, is_key_expression=False)
        else:
            filter_expression, filter_values, filter_names = None, None, None

        result = self.db.query(
            **notnone(
                TableName=make_table_name(self.db_prefix, table_name),
                # Key & Filter
                KeyConditionExpression=key_expression,
                FilterExpression=filter_expression,
                ExpressionAttributeValues=merge_dicts(attr_values, filter_values),
                ExpressionAttributeNames=merge_dicts(attr_names, filter_names),
                # Paging
                ScanIndexForward=not reverse,
                Limit=limit,
                ExclusiveStartKey=self._encode(pagination_token) if pagination_token else None,
            )
        )

        if result.get('Count') and result.get('ScannedCount') and filter:
            querylog.log_counter('dropped_by_filter', int(result['ScannedCount']) - int(result['Count']))

        items = [self._decode(x) for x in result.get("Items", [])]
        next_page_token = self._decode(result.get("LastEvaluatedKey", None))
        return items, next_page_token

    def query_index(self, table_name, index_name, keys, sort_key, reverse=False, limit=None, pagination_token=None,
                    pagination_key=None, keys_only=None, table_key_names=None, filter=None):
        # keys_only is ignored here -- that's only necessary for the in-memory implementation.
        # In an actual DDB table, that's an attribute of the index itself

        key_expression, attr_values, attr_names = self._prep_query_data(keys, sort_key)
        if filter:
            filter_expression, filter_values, filter_names = self._prep_query_data(filter, is_key_expression=False)
        else:
            filter_expression, filter_values, filter_names = None, None, None

        result = self.db.query(
            **notnone(
                TableName=make_table_name(self.db_prefix, table_name),
                IndexName=index_name,
                # Key & Filter
                KeyConditionExpression=key_expression,
                FilterExpression=filter_expression,
                ExpressionAttributeValues=merge_dicts(attr_values, filter_values),
                ExpressionAttributeNames=merge_dicts(attr_names, filter_names),
                # Paging
                ScanIndexForward=not reverse,
                Limit=limit,
                ExclusiveStartKey=self._encode(pagination_token) if pagination_token else None,
            )
        )

        if result.get('Count') and result.get('ScannedCount') and filter:
            querylog.log_counter('dropped_by_filter', int(result['ScannedCount']) - int(result['Count']))

        items = [self._decode(x) for x in result.get("Items", [])]
        next_page_token = (
            self._decode(result.get("LastEvaluatedKey", None)) if result.get("LastEvaluatedKey", None) else None
        )
        return items, next_page_token

    def _prep_query_data(self, key, sort_key=None, is_key_expression=True):
        """Build a DynamoDB condition expression from a dictionary mapping fields to values.

        The values may be literals, in which case we will render an `=` condition,
        or it may be a `DynamoCondition` subclass for more complex conditions.

        Field names are escaped in order to make them not conflict with
        built-in words.

        Returns a triple of (expression, values, names):

        - expression: a string containing placeholders like `#myfield = :myfield`.
        - names: a dict mapping `#myfield` placeholders to `my-field` field names.
        - values: a dict mapping `:myfield` placeholders to their serialized values.
        """
        conditions = DynamoCondition.make_conditions(key)
        if is_key_expression:
            validate_only_sort_key(conditions, sort_key)

        escaped_names = {k: slugify(k) for k in conditions.keys()}

        key_expression = " AND ".join(cond.to_dynamo_expression(escaped_names[field])
                                      for field, cond in conditions.items())

        attr_values = {}
        for field, cond in conditions.items():
            attr_values.update(cond.to_dynamo_values(escaped_names[field]))

        attr_names = {f'#{e}': k for k, e in escaped_names.items()}
        return key_expression, attr_values, attr_names

    def put(self, table_name, _key, data):
        self.db.put_item(TableName=make_table_name(self.db_prefix, table_name), Item=self._encode(data))

    def update(self, table_name, key, updates):
        value_updates = {k: v for k, v in updates.items() if not isinstance(v, DynamoUpdate)}
        special_updates = {k: v.to_dynamo() for k, v in updates.items() if isinstance(v, DynamoUpdate)}

        response = self.db.update_item(
            TableName=make_table_name(self.db_prefix, table_name),
            Key=self._encode(key),
            AttributeUpdates={
                **self._encode_updates(value_updates),
                **special_updates,
            },
            # Return the full new item after update
            ReturnValues='ALL_NEW',
        )
        return self._decode(response.get('Attributes', {}))

    def delete(self, table_name, key):
        return self.db.delete_item(TableName=make_table_name(self.db_prefix, table_name), Key=self._encode(key))

    def item_count(self, table_name):
        result = self.db.describe_table(TableName=make_table_name(self.db_prefix, table_name))
        return result["Table"]["ItemCount"]

    def scan(self, table_name, limit, pagination_token, pagination_key):
        result = self.db.scan(
            **notnone(
                TableName=make_table_name(self.db_prefix, table_name),
                Limit=limit,
                ExclusiveStartKey=self._encode(pagination_token) if pagination_token else None,
            )
        )
        items = [self._decode(x) for x in result.get("Items", [])]
        next_page_token = (
            self._decode(result.get("LastEvaluatedKey", None)) if result.get("LastEvaluatedKey", None) else None
        )
        return items, next_page_token

    def _encode(self, data):
        return {k: DDB_SERIALIZER.serialize(v) for k, v in data.items()}

    def _encode_updates(self, data):
        def encode_update(value):
            # None is special, we use it to remove a field from a record
            if value is None:
                return {"Action": "DELETE"}
            else:
                return {"Value": DDB_SERIALIZER.serialize(value)}

        return {k: encode_update(v) for k, v in data.items()}

    def _decode(self, data):
        if data is None:
            return None

        return {k: replace_decimals(DDB_DESERIALIZER.deserialize(v)) for k, v in data.items()}


class PaginationKey:
    """The fields that are involved in pagination for a table or index.

    A pagination key in Dynamo is a dictionary involving the keys of the "last
    evaluated item" in a result set; by passing it to a query, the query will
    continue up *just after* that element.

    This holds an ordered list of the partition and sort keys, in the order
    `[index_pk, index_sk, table_pk, table_sk]` (duplicates and unused keys
    will be removed).

    This class is used for 2 purposes:

    1. To extract pagination keys (dicts) from DynamoDB records: the prev_page_token
       will be extracted from first element in a page, and the next_page_token
       will be extracted from the last element in a page.
    2. To extract key values in an ordered list from in-memory database records.
       By extracting the values in order into a Python list, we can use the `<`
       operation to compare elements. This is used for the in-memory implementation
       of pagination.
    """
    @staticmethod
    def from_table(table_key_schema: KeySchema):
        return PaginationKey(table_key_schema.key_names)

    @staticmethod
    def from_index(index_key_names, index_sort_key_name, table_key_schema: KeySchema):
        keys = [q for q in index_key_names if q != index_sort_key_name]
        if index_sort_key_name is not None:
            keys.append(index_sort_key_name)
        for t in table_key_schema.key_names:
            if t not in keys:
                keys.append(t)
        return PaginationKey(keys)

    def __init__(self, key_names):
        self.key_names = key_names

    def extract_ordered(self, row):
        """Extract all fields in the key from a row, returning them ordered."""
        return [row[k] for k in self.key_names]

    def extract_dict(self, row):
        """Extract all fields in the key from a row, returning them as a dict."""
        return {k: row[k] for k in self.key_names}


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
                with open(filename, "r", encoding="utf-8") as f:
                    self.tables = json.load(f, object_hook=CustomEncoder.decode_object)
            except IOError:
                pass
            except json.decoder.JSONDecodeError as e:
                logger.warning(
                    f"Error loading {filename}. The next write operation \
                        will overwrite the database with a clean copy: {e}"
                )

    # NOTE: on purpose not @synchronized here
    def get_item(self, table_name, key):
        items, _ = self.query(table_name, key, sort_key=None, reverse=False, limit=None, pagination_token=None)
        return first_or_none(items)

    def batch_get_item(self, table_name, keys_map, table_key_names):
        # The in-memory implementation is lovely and trivial
        return {k: self.get_item(table_name, key) for k, key in keys_map.items()}

    @lock.synchronized
    def query(self, table_name, key, sort_key, reverse, limit, pagination_token, filter=None, pagination_key=None):
        key_conditions = DynamoCondition.make_conditions(key)
        validate_only_sort_key(key_conditions, sort_key)

        filter_conditions = DynamoCondition.make_conditions(filter or {})

        records = self.tables.get(table_name, [])
        filtered = [r for r in records if self._query_matches(r, key_conditions)]

        if sort_key:
            filtered.sort(key=lambda x: x[sort_key])

        if reverse:
            filtered.reverse()

        ordered_pagination_token = pagination_key.extract_ordered(pagination_token) if pagination_token else None

        def before_pagination_token(row):
            candidate = pagination_key.extract_ordered(row)
            if reverse:
                return candidate >= ordered_pagination_token
            else:
                return candidate <= ordered_pagination_token

        while ordered_pagination_token and filtered and before_pagination_token(filtered[0]):
            filtered.pop(0)

        next_page_key = None
        # DynamoDB will return a 'next_page_key' if there are exactly as many items in the table as requested
        if limit and limit <= len(filtered):
            filtered = filtered[:limit]
            next_page_key = pagination_key.extract_dict(filtered[-1])

        # Do a final filtering to mimic DynamoDB FilterExpression
        return copy.deepcopy([record
                              for record in filtered
                              if self._query_matches(record, filter_conditions)
                              ]), next_page_key

    # NOTE: on purpose not @synchronized here
    def query_index(self, table_name, index_name, keys, sort_key, reverse=False, limit=None, pagination_token=None,
                    pagination_key=None, keys_only=None, table_key_names=None, query_index=None, filter=None):
        """Query an index.

        - keys: the key values. May or may not contain the sort key, but it must at least contain the partition key.
        - sort_key: the field name of the sort key.
        - table_key_names: the keys in the table key, in order [partition, sort].
        """
        records, next_page_token = self.query(
            table_name, keys,
            sort_key=sort_key,
            reverse=reverse,
            limit=limit,
            pagination_key=pagination_key,
            pagination_token=pagination_token,
            filter=filter,
        )

        if not keys_only:
            return records, next_page_token

        # In a keys_only index, we retain all fields that are in either a table or index key
        # If keys_only, we project down to the index + table keys
        # In a REAL dynamo table, the index just wouldn't have more data. The in-memory table has everything,
        # so we need to drop some data so programmers don't accidentally rely on it.
        keys_to_retain = set(list(keys.keys()) + ([sort_key] if sort_key else []) + table_key_names)
        return [{key: record[key] for key in keys_to_retain} for record in records], next_page_token

    @lock.synchronized
    def put(self, table_name, key, data):
        records = self.tables.setdefault(table_name, [])
        index = self._find_index(records, key)
        if index is None:
            records.append(copy.deepcopy(data))
        else:
            records[index] = copy.deepcopy(data)
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
                        raise TypeError(f"Expected a set in {name}, got: {existing}")
                    record[name] = existing | set(update.elements)
                elif isinstance(update, DynamoRemoveFromStringSet):
                    existing = record.get(name, set())
                    if not isinstance(existing, set):
                        raise TypeError(f"Expected a set in {name}, got: {existing}")
                    record[name] = existing - set(update.elements)
                elif isinstance(update, DynamoAddToList):
                    existing = record.get(name, [])
                    if not isinstance(existing, list):
                        raise TypeError(f"Expected a list in {name}, got: {existing}")
                    record[name] = existing + list(update.elements)
                elif isinstance(update, DynamoAddToNumberSet):
                    existing = record.get(name, set())
                    if not isinstance(existing, set):
                        raise TypeError(f"Expected a set in {name}, got: {existing}")
                    record[name] = existing | set(update.elements)
                else:
                    raise RuntimeError(f"Unsupported update type for in-memory database: {update}")
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
    def scan(self, table_name, limit, pagination_token, pagination_key):
        items = self.tables.get(table_name, [])[:]

        ordered_pagination_token = pagination_key.extract_ordered(pagination_token) if pagination_token else None

        def before_pagination_token(row):
            candidate = pagination_key.extract_ordered(row)
            return candidate <= ordered_pagination_token

        while ordered_pagination_token and items and before_pagination_token(items[0]):
            items.pop(0)

        next_page_key = None
        # DynamoDB will return a 'next_page_key' if there are exactly as many items in the table as requested
        if limit and limit <= len(items):
            items = items[:limit]
            next_page_key = pagination_key.extract_dict(items[-1])

        items = copy.deepcopy(items)
        return items, next_page_key

    def _find_index(self, records, key):
        for i, v in enumerate(records):
            if self._eq_matches(v, key):
                return i
        return None

    def _eq_matches(self, record, key):
        return all(record.get(k) == v for k, v in key.items())

    def _query_matches(self, record, conds):
        return all(cond.matches(record.get(k)) for k, cond in conds.items())

    def _flush(self):
        if self.filename:
            try:
                with open(self.filename, "w", encoding="utf-8") as f:
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
    keys_only: bool
    key_schema: KeySchema


class DynamoUpdate:
    def to_dynamo(self):
        raise NotImplementedError()

    def validate_against_type(self, validator):
        raise NotImplementedError()


class DynamoIncrement(DynamoUpdate):
    def __init__(self, delta=1):
        self.delta = delta

    def to_dynamo(self):
        return {
            "Action": "ADD",
            "Value": {"N": str(self.delta)},
        }

    def validate_against_type(self, validator):
        return validate_value_against_validator(self.delta, validator)

    def __repr__(self):
        return f'Inc({self.delta})'


class DynamoAddToStringSet(DynamoUpdate):
    """Add one or more elements to a string set."""

    def __init__(self, *elements):
        self.elements = elements

    def to_dynamo(self):
        return {
            "Action": "ADD",
            "Value": {"SS": list(self.elements)},
        }

    def validate_against_type(self, validator):
        # The validator should be SetOf(...)
        return validate_value_against_validator(set(self.elements), validator)

    def __repr__(self):
        return f'Add{self.elements}'


class DynamoAddToNumberSet(DynamoUpdate):
    """Add one or more elements to a number set."""

    def __init__(self, *elements):
        for el in elements:
            if not isinstance(el, numbers.Real):
                raise ValueError(f"Must be a number, got: {el}")
        self.elements = elements

    def to_dynamo(self):
        return {
            "Action": "ADD",
            "Value": {"NS": [str(x) for x in self.elements]},
        }

    def validate_against_type(self, validator):
        # The validator should be SetOf(...)
        return validate_value_against_validator(set(self.elements), validator)

    def __repr__(self):
        return f'Add{self.elements}'


class DynamoAddToList(DynamoUpdate):
    """Add one or more elements to a list."""

    def __init__(self, *elements):
        self.elements = elements

    def validate_against_type(self, validator):
        # The validator should be ListOf(...)
        return validate_value_against_validator(list(self.elements), validator)

    def to_dynamo(self):
        return {
            "Action": "ADD",
            "Value": {"L": [DDB_SERIALIZER.serialize(x) for x in self.elements]},
        }

    def __repr__(self):
        return f'Add{self.elements}'


class DynamoRemoveFromStringSet(DynamoUpdate):
    """Remove one or more elements to a string set."""

    def __init__(self, *elements):
        self.elements = elements

    def to_dynamo(self):
        return {
            "Action": "DELETE",
            "Value": {"SS": list(self.elements)},
        }

    def validate_against_type(self, validator):
        # The validator should be SetOf(...)
        return validate_value_against_validator(set(self.elements), validator)

    def __repr__(self):
        return f'Remove{self.elements}'


class DynamoCondition:
    """Base class for Query conditions.

    These encode any type of comparison supported by Dynamo except equality.

    Conditions can be applied to sort keys for efficient lookup, or as a
    `server_side_filter` as a post-retrieval, pre-download filter. Queries will
    never fetch more than 1MB from disk, so your server-side filter should
    not filter out more than ~50% of the rows.

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
    def make_conditions(key):
        """Turn a dict of values into a dict of DynamoConditions.

        Non-DynamoConditions are returned into instances of Equals.
        """
        return {k: v if isinstance(v, DynamoCondition) else Equals(v) for k, v in key.items()}


class Equals(DynamoCondition):
    """Assert that a value is equal to another value.

    Conditions can be applied to sort keys for efficient lookup, or as a
    `server_side_filter` as a post-retrieval, pre-download filter. Queries will
    never fetch more than 1MB from disk, so your server-side filter should
    not filter out more than ~50% of the rows.
    """

    def __init__(self, value):
        self.value = value

    def to_dynamo_expression(self, field_name):
        return f"#{field_name} = :{field_name}"

    def to_dynamo_values(self, field_name):
        return {
            f':{field_name}': DDB_SERIALIZER.serialize(self.value),
        }

    def matches(self, value):
        return value == self.value


class Between(DynamoCondition):
    """Assert that a value is between two other values.

    Conditions can be applied to sort keys for efficient lookup, or as a
    `server_side_filter` as a post-retrieval, pre-download filter. Queries will
    never fetch more than 1MB from disk, so your server-side filter should
    not filter out more than ~50% of the rows.
    """

    def __init__(self, minval, maxval):
        self.minval = minval
        self.maxval = maxval

    def to_dynamo_expression(self, field_name):
        return f"#{field_name} BETWEEN :{field_name}_min AND :{field_name}_max"

    def to_dynamo_values(self, field_name):
        return {
            f":{field_name}_min": DDB_SERIALIZER.serialize(self.minval),
            f":{field_name}_max": DDB_SERIALIZER.serialize(self.maxval),
        }

    def matches(self, value):
        return self.minval <= value <= self.maxval


class BeginsWith(DynamoCondition):
    """Assert that a string begins with another string.

    Conditions can be applied to sort keys for efficient lookup, or as a
    `server_side_filter` as a post-retrieval, pre-download filter. Queries will
    never fetch more than 1MB from disk, so your server-side filter should
    not filter out more than ~50% of the rows.
    """

    def __init__(self, prefix):
        self.prefix = prefix

    def to_dynamo_expression(self, field_name):
        return f"begins_with(#{field_name}, :{field_name}_prefix)"

    def to_dynamo_values(self, field_name):
        return {
            f":{field_name}_prefix": DDB_SERIALIZER.serialize(self.prefix),
        }

    def matches(self, value):
        return isinstance(value, str) and value.startswith(self.prefix)


class UseThisIndex(DynamoCondition):
    """A dummy condition that always matches, and allows picking a specific index.

    If you have multiple indexes on the same primary key but with a different
    sort key, you need a way to disambiguate between those indexes. I.e. you add
    a field with a `UseThisIndex` to indicate which sort key you want to use.

    In practice, it looks like this:

        table.get_many({
            "pk": "some_value",
            "preferred_sortkey": UseThisIndex(),
        })
    """

    def __init__(self):
        pass

    def to_dynamo_expression(self, field_name):
        # Dynamo does not support the expression "true" :/
        return '1=1'

    def to_dynamo_values(self, field_name):
        return {}

    def matches(self, value):
        return True


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
        if obj.get("$type") == "set":
            return set(obj["elements"])
        return obj


def validate_only_sort_key(conds, sort_key):
    """Check that non-Equals conditions are only used on the sort key."""
    non_equals_fields = [k for k, v in conds.items() if not isinstance(v, Equals)]
    if sort_key and set(non_equals_fields) - {sort_key}:
        raise ValueError(f"Non-Equals conditions only allowed on sort key {sort_key}, got: {list(conds)}")


def encode_page_token(x, inverted):
    """Encode a compound key page token (dict) to a string.

    'inverted' indicates whether the page token goes in the other direction
    than the normally accepted query direction. If the query normally goes
    forward, a query with an inverted page token would go backwards; but if the
    query normally goes backwards (reverse=True), a query with an inverted page token
    would go forward.
    """
    if x is None:
        return None
    return ('-' if inverted else '') + base64.urlsafe_b64encode(json.dumps(x).encode("utf-8")).decode("ascii")


def decode_page_token(x):
    """Decode string page token to compound key (dict), and its inversion bit.

    'inverse' is not the same as 'reverse'. 'reverse' is the order the user wants
    the rows from Dynamo in. 'inverse' is whether the order we're currently querying in
    is the opposite of the desired 'reverse' order or not.
    """
    if x is None:
        return False, None
    inverted = False
    if x.startswith('-'):
        inverted = True
        x = x[1:]
    return inverted, json.loads(base64.urlsafe_b64decode(x.encode("ascii")).decode("utf-8"))


def notnone(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def make_table_name(prefix, name):
    return f"{prefix}-{name}" if prefix else name


class ExponentialBackoff:
    def __init__(self):
        self.time = 0.05

    @querylog.timed_as('db:sleep')
    def sleep(self):
        time.sleep(random.random() * self.time)
        self.time *= 2

    def sleep_when(self, condition):
        if condition:
            self.sleep()


class QueryIterator:
    """Iterate over a set of query results, keeping track of a database and client side
    pagination token at the same time.

    _do_fetch() should be overridden, and use self.pagination_token to
    paginate on the database.
    """

    def __init__(self, pagination_token=None):
        drop_initial = self._analyze_pagination_token(pagination_token)
        self.page = None
        self.have_eof = None

        # Eat records according to the amount we needed to drop
        i = 0
        while not self.eof and i < drop_initial:
            i += 1
            self.advance()

    def _fetch_next_page(self):
        self.i = 0
        self.page = self._do_fetch()
        if not isinstance(self.page, ResultPage):
            raise RuntimeError('_do_fetch must return a ResultPage')

        self.have_eof = len(self.page) == 0

    def _do_fetch(self):
        raise NotImplementedError('_do_fetch should be implemented')

    @property
    def eof(self):
        if self.have_eof:
            # This removes the need for fetches just to answer the EOF question
            return self.have_eof

        if self.page is None:
            self._fetch_next_page()

        # If we have a page, we're at eof if we're at the end of the last page
        return self.i >= len(self.page) and not self.page.next_page_token

    def advance(self):
        if self.page is None:
            self._fetch_next_page()
            return

        self.i += 1
        if self.i >= len(self.page) and self.page.next_page_token:
            self.pagination_token = self.page.next_page_token
            if self.pagination_token is None:
                self.have_eof = True

            # Reset self.page, so we don't retrieve the next page unnecessarily
            # but the next lookup will fetch it
            self.page = None

    @property
    def current(self):
        if self.page is None:
            self._fetch_next_page()
        if self.eof:
            raise RuntimeError('At eof')
        return self.page[self.i]

    def __iter__(self):
        return PythonQueryIterator(self)

    def __nonzero__(self):
        return not self.eof

    __bool__ = __nonzero__

    def _analyze_pagination_token(self, x):
        """Turn a pagination token into a DB part and a client part.

        Return the number part.
        """
        if not x:
            self.pagination_token = None
            return 0

        parts = x.split('@')
        self.pagination_token = parts[0] or None
        return int(parts[1])

    @property
    def next_page_token(self):
        if self.eof:
            return None
        return f'{self.pagination_token or ""}@{self.i}'


class PythonQueryIterator:
    """Implements the Python iterator protocol, which is slightly different
    from the Java (eof/current/advance) iterator protocol.
    """

    def __init__(self, iter):
        self.iter = iter

    def __next__(self):
        if self.iter.eof:
            raise StopIteration()
        ret = self.iter.current
        self.iter.advance()
        return ret


class GetManyIterator(QueryIterator):
    """Iterate over a set of query results, automatically proceeding to the next result page if necessary.

    Wrapper around query_many that automatically paginates.
    """

    def __init__(self, table, key, reverse=False, batch_size=None, pagination_token=None):
        self.table = table
        self.key = key
        self.reverse = reverse
        self.batch_size = batch_size
        super().__init__(pagination_token)

    def _do_fetch(self):
        return self.table.get_many(self.key,
                                   reverse=self.reverse,
                                   limit=self.batch_size,
                                   pagination_token=self.pagination_token)


class ScanIterator(QueryIterator):
    """Iterate over a table scan, automatically proceeding to the next result page if necessary.

    Wrapper around scan that automatically paginates.
    """

    def __init__(self, table, limit=None, pagination_token=None):
        self.table = table
        self.limit = limit
        super().__init__(pagination_token)

    def _do_fetch(self):
        return self.table.scan(limit=self.limit, pagination_token=self.pagination_token)


def merge_dicts(a, b):
    if not a:
        return b
    if not b:
        return a
    return dict(**a, **b)


def reverse_index(xs):
    """Transform a list of (key, value) into a dictionary of { value -> [key] }."""
    ret = collections.defaultdict(list)
    for key, value in xs:
        ret[value].append(key)
    return ret


def make_predicate(obj):
    if obj is None:
        return lambda row: True
    if callable(obj):
        return obj
    if isinstance(obj, dict):
        return lambda row: all(row.get(key) == value for key, value in obj.items())
    raise ValueError(f'Not a valid client_side_filter: {obj}')


class Validator(metaclass=ABCMeta):
    """Base class for validators.

    Subclasses should implement 'is_valid' and '__str__'.
    """

    @staticmethod
    def ensure(validator):
        """Turn the given value into a validator."""
        if validator is True:
            return Any()
        if isinstance(validator, Validator):
            return validator
        if type(validator) is type:
            return InstanceOf(validator)
        if callable(validator):
            return Predicate(validator)
        raise ValueError(f'Not sure how to treat {validator} as a validator')

    @staticmethod
    def ensure_all(validator_dict):
        if str in validator_dict.keys() and len(validator_dict.keys()) > 1:
            raise ValueError(f'If you specify str as part of the validation, you cant define more type checks.\
                              You dindt do that for {validator_dict}')
        type_dict = {}
        for k, v in validator_dict.items():
            if k is str:
                type_dict[Validator.ensure(k)] = Validator.ensure(v)
            elif isinstance(k, str):
                type_dict[k] = Validator.ensure(v)
            else:
                raise ValueError(f'Key values should be of type str or instances of string.\
                                 {k} does not comply with that')
        return type_dict

    def is_valid(self, value):
        ...

    def __str__(self):
        ...


class Any(Validator):
    """Validator which allows any type."""

    def is_valid(self, value):
        return True

    def __str__(self):
        return 'any value'


class InstanceOf(Validator):
    """Validator which checks if a value is an instance of a type."""

    def __init__(self, type):
        self.type = type

    def is_valid(self, value):
        return isinstance(value, self.type)

    def __str__(self):
        return f'instance of {self.type}'


class EitherOf(Validator):
    """Validator wihch checks if a value is instance of one of several types"""

    def __init__(self, *types):
        self.validators = [Validator.ensure(type) for type in types]

    def is_valid(self, value):
        return any(validator.is_valid(value) for validator in self.validators)

    def __str__(self):
        return f'matches one of {self.validators}'


class Predicate(Validator):
    """Validator which calls an arbitrary callback."""

    def __init__(self, fn):
        self.fn = fn

    def is_valid(self, value):
        return self.fn(value)

    def __str__(self):
        return f'matches {self.fn}'


class OptionalOf(Validator):
    """Validator which matches either None or an inner validator."""

    def __init__(self, inner):
        self.inner = Validator.ensure(inner)

    def is_valid(self, value):
        return value is None or self.inner.is_valid(value)

    def __str__(self):
        return f'optional {self.inner}'


class SetOf(Validator):
    """Validator which matches a set matching inner validators."""

    def __init__(self, inner):
        self.inner = Validator.ensure(inner)

    def is_valid(self, value):
        return isinstance(value, set) and all(self.inner.is_valid(x) for x in value)

    def __str__(self):
        return f'set of {self.inner}'


class ListOf(Validator):
    """Validator which matches a list matching inner validators."""

    def __init__(self, inner):
        self.inner = Validator.ensure(inner)

    def is_valid(self, value):
        return isinstance(value, list) and all(self.inner.is_valid(x) for x in value)

    def __str__(self):
        return f'list of {self.inner}'


class RecordOf(Validator):
    """Validator which matches a record with inner validators."""

    def __init__(self, inner):
        self.inner = Validator.ensure_all(inner)

    def is_valid(self, value):
        return (isinstance(value, dict)
                and all(validator.is_valid(value.get(key)) for key, validator in self.inner.items()))

    def __str__(self):
        return f'{self.inner}'


class DictOf(Validator):
    """ Validator wich matches dictionaries of any string to inner validators """

    def __init__(self, inner):
        self.inner = Validator.ensure_all(inner)

    def is_valid(self, value):
        if not isinstance(value, dict):
            return False
        first_type = list(self.inner.keys())[0]
        return all(first_type.is_valid(k) and self.inner.get(first_type).is_valid(v) for k, v in value.items())

    def __str__(self):
        return f'list of {self.inner}'


def slugify(x):
    """Strips special characters from Dynamo identifiers."""
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', x)
