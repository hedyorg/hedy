from website import dynamo
import unittest
import os
import contextlib

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


class TestDynamoWithSortKeys(unittest.TestCase):
  """Test that the operations work on a table with a sort key."""
  def setUp(self):
    self.table = dynamo.Table(dynamo.MemoryStorage(), 'table', partition_key='id', sort_key='sort')

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
    ret = self.table.get_many(dict(id='key'))
    self.assertEqual(ret, [
      dict(id='key', sort='a', value='A'),
      dict(id='key', sort='b', value='B'),
    ])

  def test_updates(self):
    # Two updates to a record with a sort key
    self.table.update(dict(id='key', sort='s'), dict(x='x'))
    self.table.update(dict(id='key', sort='s'), dict(y='y'))

    print(self.table.storage.tables)

    ret = self.table.get(dict(id='key', sort='s'))
    self.assertEqual(ret, dict(id='key', sort='s', x='x', y='y'))

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