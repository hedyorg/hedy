import unittest
import utils


class TestUtils(unittest.TestCase):
  def test_slashjoin(self):
    self.assertEqual('http://hedycode.com/banaan/xyz', utils.slash_join('http://hedycode.com/', '/banaan', '', '/xyz'))
    self.assertEqual('/one/two', utils.slash_join('/one/two'))
    self.assertEqual('/one/two', utils.slash_join(None, '/one/two'))
