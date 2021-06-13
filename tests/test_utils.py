import unittest
import utils
import bcrypt
import time

class TestUtils(unittest.TestCase):
  def test_slashjoin(self):
    self.assertEqual('http://hedycode.com/banaan/xyz', utils.slash_join('http://hedycode.com/', '/banaan', '', '/xyz'))
    self.assertEqual('/one/two', utils.slash_join('/one/two'))
    self.assertEqual('/one/two', utils.slash_join(None, '/one/two'))

  def test_extract_rounds(self):
    salt = bcrypt.gensalt (rounds=7).decode ('utf-8')
    self.assertEqual(7, utils.extract_bcrypt_rounds(salt))

  def test_extract_default_rounds(self):
    salt = bcrypt.gensalt ().decode ('utf-8')
    self.assertEqual(12, utils.extract_bcrypt_rounds(salt))

  def test_load_yaml_speed(self):
    n = 50
    file = 'coursedata/adventures/hu.yaml'

    start = time.time()
    for _ in range(n):
      original_data = utils.load_yaml_uncached(file)
    original_seconds = time.time() - start

    start = time.time()
    for _ in range(n):
      cached_data = utils.load_yaml_pickled(file)
    cached_seconds = time.time() - start

    self.assertEqual(original_data, cached_data)
    print(f'YAML loading takes {original_seconds / n} seconds, unpickling takes {cached_seconds / n} ({original_seconds / cached_seconds}x faster)')