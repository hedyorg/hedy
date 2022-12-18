import unittest
from safe_format import safe_format


class TestSafeFormat(unittest.TestCase):
    def test_normal_operation(self):
        self.assertEqual(safe_format('a {b} c', b='b'), 'a b c')

    def test_missing_key(self):
        self.assertEqual(safe_format('a {b} c'), 'a {b} c')

    def test_superfluous_key(self):
        self.assertEqual(safe_format('a {b} c', bb='bb'), 'a {b} c')
