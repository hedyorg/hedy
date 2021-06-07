from website import ab_proxying
import unittest

class TestAbTesting(unittest.TestCase):
  def test_extract_cookies(self):
    set_cookie = 'session=eyJzZXNzaW9uX2lkIjoiODgwOGMxMjIxMmVmNGM5NjkzNTFhMWYxYzEyNGExNjUiLCJ2YWx1ZSI6IjEyMyJ9.YLOIMA.b71v_iV4DgyniHlpuyzdVJBkM5M; Secure; HttpOnly; Path=/; SameSite=Lax'
    session = ab_proxying.extract_session_from_cookie(set_cookie, 'TheSecret')
    self.assertEqual(session, {
      'session_id': '8808c12212ef4c969351a1f1c124a165',
      'value': '123',
    })

  def test_extract_cookies_with_invalid_secret(self):
    """Test that we successfully decode the cookies, even if the secret key is wrong."""
    set_cookie = 'session=eyJzZXNzaW9uX2lkIjoiODgwOGMxMjIxMmVmNGM5NjkzNTFhMWYxYzEyNGExNjUiLCJ2YWx1ZSI6IjEyMyJ9.YLOIMA.b71v_iV4DgyniHlpuyzdVJBkM5M; Secure; HttpOnly; Path=/; SameSite=Lax'
    session = ab_proxying.extract_session_from_cookie(set_cookie, 'Banana')
    self.assertEqual(session, {
      'session_id': '8808c12212ef4c969351a1f1c124a165',
      'value': '123',
    })