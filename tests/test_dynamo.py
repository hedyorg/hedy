import contextlib
import os
import unittest
from unittest import mock

from website import dynamo


class Helpers:
    def __init__(self):
        # Necessary to make pylint happy
        self.table = None

    def insert(self, *rows):
        for row in rows:
            self.table.create(row)

    def insert_sample_data(self):
        self.insert(
            dict(id='key', sort=1, x=1, y=1, m=9),
            dict(id='key', sort=2, x=1, y=3, m=9),
            dict(id='key', sort=3, x=1, y=2, m=8))

    def get_pages(self, key, **kwargs):
        ret = []

        p = self.table.get_many(key, **kwargs)
        while True:
            if p.records:
                ret.append(p.records)

            if not p.next_page_token:
                break
            p = self.table.get_many(key, **kwargs, pagination_token=p.next_page_token)
        return ret


class TestDynamoAbstraction(unittest.TestCase):
    def setUp(self):
        self.table = dynamo.Table(dynamo.MemoryStorage(), 'table', 'id')

    def test_set_manipulation(self):
        """Test that adding to a set and removing from a set works."""
        self.table.create(dict(
            id='key',
            values=set(['a', 'b', 'c']),
        ))

        self.table.update(dict(id='key'), dict(
            values=dynamo.DynamoAddToStringSet('x', 'y'),
        ))

        final = self.table.get(dict(id='key'))
        self.assertEqual(final['values'], set(['a', 'b', 'c', 'x', 'y']))

        self.table.update(dict(id='key'), dict(
            values=dynamo.DynamoRemoveFromStringSet('b', 'c'),
        ))

        final = self.table.get(dict(id='key'))
        self.assertEqual(final['values'], set(['a', 'x', 'y']))

    def test_cannot_set_manipulate_lists(self):
        """Test that if a value originally got created as a 'list', we cannot
        use set manipulation on it.

        This also doesn't work in Real DynamoDB, our in-memory API shouldn't make
        this appear to work.
        """
        self.table.create(dict(
            id='key',
            values=['a', 'b', 'c'],  # List instead of set
        ))

        with self.assertRaises(TypeError):
            self.table.update(dict(id='key'), dict(
                values=dynamo.DynamoAddToStringSet('x', 'y'),
            ))

    def test_sets_are_serialized_properly(self):
        """Test that adding to a set and removing from a set works."""
        with with_clean_file('test.json'):
            table = dynamo.Table(dynamo.MemoryStorage('test.json'), 'table', 'id')
            table.create(dict(
                id='key',
                values=set(['a', 'b', 'c']),
            ))

            table = dynamo.Table(dynamo.MemoryStorage('test.json'), 'table', 'id')
            final = table.get(dict(id='key'))
            self.assertEqual(final['values'], set(['a', 'b', 'c']))


class TestSortKeysInMemory(unittest.TestCase):
    """Test that the operations work on an in-memory table with a sort key."""

    def setUp(self):
        self.table = dynamo.Table(
            dynamo.MemoryStorage(),
            'table',
            partition_key='id',
            sort_key='sort')

    def test_put_and_get(self):
        self.table.create(dict(
            id='key',
            sort='sort',
            value='V',
        ))

        ret = self.table.get(dict(id='key', sort='sort'))
        self.assertEqual(ret['value'], 'V')

    def test_put_and_get_many(self):
        # Insert in reverse order
        self.table.create(dict(id='key', sort='b', value='B'))
        self.table.create(dict(id='key', sort='a', value='A'))

        # Get them back in the right order
        ret = list(self.table.get_many(dict(id='key')))
        self.assertEqual(ret, [
            dict(id='key', sort='a', value='A'),
            dict(id='key', sort='b', value='B'),
        ])

    def test_updates(self):
        # Two updates to a record with a sort key
        self.table.update(dict(id='key', sort='s'), dict(x='x'))
        self.table.update(dict(id='key', sort='s'), dict(y='y'))

        ret = self.table.get(dict(id='key', sort='s'))
        self.assertEqual(ret, dict(id='key', sort='s', x='x', y='y'))


class TestQueryInMemory(unittest.TestCase, Helpers):
    """Test that the query work on an in-memory table."""

    def setUp(self):
        self.table = dynamo.Table(
            dynamo.MemoryStorage(),
            'table',
            partition_key='id',
            sort_key='sort',
            indexed_fields=[
                dynamo.IndexKey(
                    'x',
                    'y'),
                dynamo.IndexKey('m')])

    def test_query(self):
        self.table.create({'id': 'key', 'sort': 1, 'm': 'val'})
        self.table.create({'id': 'key', 'sort': 2, 'm': 'another'})

        ret = list(self.table.get_many({'id': 'key'}))

        self.assertEqual(ret, [
            {'id': 'key', 'sort': 1, 'm': 'val'},
            {'id': 'key', 'sort': 2, 'm': 'another'}
        ])

    def test_between_query(self):
        self.table.create({'id': 'key', 'sort': 1, 'x': 'x'})
        self.table.create({'id': 'key', 'sort': 2, 'x': 'y'})
        self.table.create({'id': 'key', 'sort': 3, 'x': 'z'})

        ret = list(self.table.get_many({
            'id': 'key',
            'sort': dynamo.Between(2, 5),
        }))
        self.assertEqual(ret, [
            {'id': 'key', 'sort': 2, 'x': 'y'},
            {'id': 'key', 'sort': 3, 'x': 'z'},
        ])

    def test_query_index(self):
        self.table.create({'id': 'key', 'sort': 1, 'm': 'val'})
        self.table.create({'id': 'key', 'sort': 2, 'm': 'another'})

        ret = list(self.table.get_many({'m': 'val'}))

        self.assertEqual(ret, [
            {'id': 'key', 'sort': 1, 'm': 'val'}
        ])

    def test_query_index_with_partition_key(self):
        self.table.create({'id': 'key', 'sort': 1, 'x': 'val', 'y': 0})
        self.table.create({'id': 'key', 'sort': 2, 'x': 'val', 'y': 1})
        self.table.create({'id': 'key', 'sort': 3, 'x': 'val', 'y': 1})
        self.table.create({'id': 'key', 'sort': 4, 'x': 'another_val', 'y': 2})

        ret = list(self.table.get_many({'x': 'val'}))

        self.assertEqual(ret, [
            {'id': 'key', 'sort': 1, 'x': 'val', 'y': 0},
            {'id': 'key', 'sort': 2, 'x': 'val', 'y': 1},
            {'id': 'key', 'sort': 3, 'x': 'val', 'y': 1}
        ])

    def test_query_index_with_partition_sort_key(self):
        self.table.create({'id': 'key', 'sort': 1, 'x': 'val', 'y': 0})
        self.table.create({'id': 'key', 'sort': 2, 'x': 'val', 'y': 1})
        self.table.create({'id': 'key', 'sort': 3, 'x': 'val', 'y': 1})
        self.table.create({'id': 'key', 'sort': 4, 'x': 'another_val', 'y': 2})

        ret = list(self.table.get_many({'x': 'val', 'y': 1}))

        self.assertEqual(ret, [
            {'id': 'key', 'sort': 2, 'x': 'val', 'y': 1},
            {'id': 'key', 'sort': 3, 'x': 'val', 'y': 1}
        ])

    def test_query_index_sort_key_between(self):
        self.table.create({'id': 'key', 'sort': 1, 'x': 'val', 'y': 1})
        self.table.create({'id': 'key', 'sort': 2, 'x': 'val', 'y': 3})
        self.table.create({'id': 'key', 'sort': 3, 'x': 'val', 'y': 6})

        ret = list(self.table.get_many({
            'x': 'val',
            'y': dynamo.Between(2, 5),
        }))
        self.assertEqual(ret, [
            {'id': 'key', 'sort': 2, 'x': 'val', 'y': 3}
        ])

    def test_paginated_query(self):
        self.insert_sample_data()
        pages = self.get_pages({'id': 'key'}, limit=1)

        self.assertEqual(pages, [
            [dict(id='key', sort=1, x=1, y=1, m=9)],
            [dict(id='key', sort=2, x=1, y=3, m=9)],
            [dict(id='key', sort=3, x=1, y=2, m=8)],
        ])

    def test_paginated_query_reverse(self):
        self.insert_sample_data()
        pages = self.get_pages({'id': 'key'}, limit=1, reverse=True)

        self.assertEqual(pages, [
            [dict(id='key', sort=3, x=1, y=2, m=8)],
            [dict(id='key', sort=2, x=1, y=3, m=9)],
            [dict(id='key', sort=1, x=1, y=1, m=9)],
        ])

    def test_paginated_query_on_sortkey_index(self):
        self.insert_sample_data()
        pages = self.get_pages({'x': 1}, limit=1)

        self.assertEqual(pages, [
            [dict(id='key', sort=1, x=1, y=1, m=9)],
            [dict(id='key', sort=3, x=1, y=2, m=8)],
            [dict(id='key', sort=2, x=1, y=3, m=9)],
        ])

    def test_paginated_query_on_sortkey_index_reverse(self):
        self.insert_sample_data()
        pages = self.get_pages({'x': 1}, limit=1, reverse=True)

        self.assertEqual(pages, [
            [dict(id='key', sort=2, x=1, y=3, m=9)],
            [dict(id='key', sort=3, x=1, y=2, m=8)],
            [dict(id='key', sort=1, x=1, y=1, m=9)],
        ])

    def test_paginated_query_on_partitionkey_index(self):
        self.insert_sample_data()
        pages = self.get_pages({'m': 9}, limit=1)

        self.assertEqual(pages, [
            [dict(id='key', sort=1, x=1, y=1, m=9)],
            [dict(id='key', sort=2, x=1, y=3, m=9)],
        ])

    def test_paginated_query_on_partitionkey_index_reverse(self):
        self.insert_sample_data()
        pages = self.get_pages({'m': 9}, limit=1, reverse=True)

        self.assertEqual(pages, [
            [dict(id='key', sort=2, x=1, y=3, m=9)],
            [dict(id='key', sort=1, x=1, y=1, m=9)],
        ])

    def test_paginated_scan(self):
        self.insert(
            dict(id='key', sort=1, y=1),
            dict(id='key', sort=2, y=3),
            dict(id='key', sort=3, y=6))

        ret = self.table.scan(limit=1)
        self.assertEqual(ret[0], {'id': 'key', 'sort': 1, 'y': 1})

        ret = self.table.scan(limit=1, pagination_token=ret.next_page_token)
        self.assertEqual(ret[0], {'id': 'key', 'sort': 2, 'y': 3})

        ret = self.table.scan(limit=1, pagination_token=ret.next_page_token)
        self.assertEqual(ret[0], {'id': 'key', 'sort': 3, 'y': 6})

        self.assertIsNone(ret.next_page_token)


class TestSortKeysAgainstAws(unittest.TestCase):
    """Test that the operations send out appropriate Dynamo requests."""

    def setUp(self):
        self.db = mock.Mock()
        self.table = dynamo.Table(
            dynamo.AwsDynamoStorage(
                self.db,
                ''),
            'table',
            partition_key='id',
            sort_key='sort')

        self.db.query.return_value = {'Items': []}

    def test_between_query(self):
        self.table.get_many({
            'id': 'key',
            'sort': dynamo.Between(2, 5),
        })
        self.db.query.assert_called_with(
            KeyConditionExpression='#id = :id AND #sort BETWEEN :sort_min AND :sort_max', ExpressionAttributeValues={
                ':id': {
                    'S': 'key'}, ':sort_min': {
                    'N': '2'}, ':sort_max': {
                    'N': '5'}}, ExpressionAttributeNames={
                        '#id': 'id', '#sort': 'sort'}, TableName=mock.ANY, ScanIndexForward=mock.ANY)


def try_to_delete(filename):
    if os.path.exists(filename):
        os.unlink(filename)


@contextlib.contextmanager
def with_clean_file(filename):
    """Remove file before starting, and after running.

    Intended for tempfiles used in tests.
    """
    try_to_delete(filename)
    try:
        yield
    finally:
        try_to_delete(filename)
