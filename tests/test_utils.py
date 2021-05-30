import unittest
import utils
import bcrypt

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

  def test_extract_cookies(self):
    set_cookie = 'session=eyJzZXNzaW9uX2lkIjoiODgwOGMxMjIxMmVmNGM5NjkzNTFhMWYxYzEyNGExNjUiLCJ2YWx1ZSI6IjEyMyJ9.YLOIMA.b71v_iV4DgyniHlpuyzdVJBkM5M; Secure; HttpOnly; Path=/; SameSite=Lax'
    session = utils.extract_session_from_cookie(set_cookie, 'TheSecret')
    self.assertEqual(session, {
      'session_id': '8808c12212ef4c969351a1f1c124a165',
      'value': '123',
    })

  def test_extract_cookies_with_invalid_secret(self):
    """Test that we successfully decode the cookies, even if the secret key is wrong."""
    set_cookie = 'session=eyJzZXNzaW9uX2lkIjoiODgwOGMxMjIxMmVmNGM5NjkzNTFhMWYxYzEyNGExNjUiLCJ2YWx1ZSI6IjEyMyJ9.YLOIMA.b71v_iV4DgyniHlpuyzdVJBkM5M; Secure; HttpOnly; Path=/; SameSite=Lax'
    session = utils.extract_session_from_cookie(set_cookie, 'Banana')
    self.assertEqual(session, {
      'session_id': '8808c12212ef4c969351a1f1c124a165',
      'value': '123',
    })