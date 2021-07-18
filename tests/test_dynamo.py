from website import dynamo
import unittest

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