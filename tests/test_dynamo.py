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


class TestDynamoAbstraction(unittest.TestCase, Helpers):
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

    def test_batch_get(self):
        self.insert(
            dict(id='k1', bla=1),
            dict(id='k2', bla=2),
            dict(id='k3', bla=3))

        # Test list API
        result = self.table.batch_get([
            dict(id='k1'),
            dict(id='oeps'),
            dict(id='k2'),
        ])

        self.assertEqual(result, [
            dict(id='k1', bla=1),
            None,
            dict(id='k2', bla=2),
        ])

        # Test dict API
        result = self.table.batch_get({
            'a': dict(id='k1'),
            'b': dict(id='k2'),
            'z': dict(id='oeps'),
        })

        self.assertEqual(result, {
            'a': dict(id='k1', bla=1),
            'b': dict(id='k2', bla=2),
            'z': None,
        })

    def test_no_memory_sharing_direct(self):
        """Ensure that changes to objects retrieved from the database do not leak into other operations."""
        self.table.put({'id': 'key', 'x': 1})

        # WHEN
        retrieved = self.table.get({'id': 'key'})
        retrieved['x'] = 666

        # THEN
        retrieved2 = self.table.get({'id': 'key'})
        self.assertEqual(retrieved2['x'], 1)

    def test_no_memory_sharing_sublists(self):
        """Ensure that changes to objects retrieved from the database do not leak into other operations."""
        # GIVEN
        self.table.put(dict(
            id='with_list',
            sublist=[1]
        ))

        # WHEN
        retrieved = self.table.get(dict(id='with_list'))
        retrieved['sublist'].append(2)

        # THEN
        retrieved2 = self.table.get(dict(id='with_list'))
        self.assertEqual(retrieved2['sublist'], [1])

    def test_no_memory_sharing_insert_direct(self):
        """Ensure that changes to objects we insert aren't accidentally seen by other viewers."""
        # GIVEN
        obj = dict(id='lookatme', x=0)

        # WHEN
        self.table.put(obj)
        obj['x'] = 1

        # THEN
        obj2 = self.table.get(dict(id='lookatme'))
        self.assertEqual(obj2['x'], 0)

    def test_no_memory_sharing_insert_sublist(self):
        """Ensure that changes to objects we insert aren't accidentally seen by other viewers."""
        # GIVEN
        obj = dict(id='lookatme', x=[0])

        # WHEN
        self.table.put(obj)
        obj['x'].append(1)

        # THEN
        obj2 = self.table.get(dict(id='lookatme'))
        self.assertEqual(obj2['x'], [0])


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
            indexes=[
                dynamo.Index(
                    'x',
                    'y'),
                dynamo.Index('m'),
                dynamo.Index('n', keys_only=True),
            ])

    def test_query(self):
        self.table.create({'id': 'key', 'sort': 1, 'm': 'val'})
        self.table.create({'id': 'key', 'sort': 2, 'm': 'another'})

        ret = list(self.table.get_many({'id': 'key'}))

        self.assertEqual(ret, [
            {'id': 'key', 'sort': 1, 'm': 'val'},
            {'id': 'key', 'sort': 2, 'm': 'another'}
        ])

    def test_cant_use_array_for_indexed_field(self):
        with self.assertRaises(ValueError):
            self.table.create({'id': 'key', 'sort': 1, 'm': [1, 2, 3]})

    def test_cant_use_array_for_partition(self):
        with self.assertRaises(ValueError):
            self.table.create({'id': [1, 2]})

    def test_query_with_filter(self):
        self.table.create({'id': 'key', 'sort': 1, 'm': 'val'})
        self.table.create({'id': 'key', 'sort': 2, 'm': 'another'})

        ret = list(self.table.get_many({'id': 'key'}, filter={'m': 'another'}))

        self.assertEqual(ret, [
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

    def test_no_superfluous_keys(self):
        with self.assertRaises(ValueError):
            self.table.get_many({'m': 'some_value', 'Z': 'some_other_value'})

    def test_query_index(self):
        self.table.create({'id': 'key', 'sort': 1, 'm': 'val'})
        self.table.create({'id': 'key', 'sort': 2, 'm': 'another'})

        ret = list(self.table.get_many({'m': 'val'}))

        self.assertEqual(ret, [
            {'id': 'key', 'sort': 1, 'm': 'val'}
        ])

    def test_query_index_with_filter(self):
        self.table.create({'id': 'key', 'sort': 1, 'm': 'val', 'p': 'p'})
        self.table.create({'id': 'key', 'sort': 3, 'm': 'val', 'p': 'p'})
        self.table.create({'id': 'key', 'sort': 2, 'm': 'another', 'q': 'q'})

        ret = list(self.table.get_many({'m': 'val'}, filter={'p': 'p'}))

        self.assertEqual(ret, [
            {'id': 'key', 'sort': 1, 'm': 'val', 'p': 'p'},
            {'id': 'key', 'sort': 3, 'm': 'val', 'p': 'p'},
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

    def test_keys_only_index(self):
        self.insert(
            dict(id='key', sort=1, n=1, other='1'),
            dict(id='key', sort=2, n=1, other='2'),
            dict(id='key', sort=3, n=1, other='3'))

        ret = self.table.get_many({'n': 1})

        # This is a keys_only index, so we expect to get { id, sort, n } back
        self.assertEqual(ret.records, [
            dict(id='key', sort=1, n=1),
            dict(id='key', sort=2, n=1),
            dict(id='key', sort=3, n=1),
        ])

    def test_get_many_iterator(self):
        N = 10

        for i in range(N):
            self.insert(
                dict(id='key', sort=i + 1))

        expected = [dict(id='key', sort=i + 1) for i in range(N)]

        # Query everything at once, using the Python iterator protocol
        self.assertEqual(list(dynamo.GetManyIterator(self.table, dict(id='key'))), expected)

        # Query paginated, using the Python iterator protocol
        self.assertEqual(list(dynamo.GetManyIterator(self.table, dict(id='key'), batch_size=3)), expected)

        # Reuse the client-side pager every time, using the Python iterator protocol
        ret = []
        token = None
        while True:
            many = dynamo.GetManyIterator(self.table, dict(id='key'), batch_size=3, pagination_token=token)
            ret.append(next(iter(many)))
            token = many.next_page_token
            if not token:
                break
        self.assertEqual(ret, expected)

        # Also test using the eof/current/advance protocol
        ret = []
        many = dynamo.GetManyIterator(self.table, dict(id='key'), batch_size=3, pagination_token=token)
        while many:
            ret.append(many.current)
            many.advance()
        self.assertEqual(ret, expected)


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
