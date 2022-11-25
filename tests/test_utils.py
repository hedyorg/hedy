import unittest

import bcrypt

import utils


class TestUtils(unittest.TestCase):
    def test_slashjoin(self):
        self.assertEqual(
            'http://hedycode.com/banaan/xyz',
            utils.slash_join(
                'http://hedycode.com/',
                '/banaan',
                '',
                '/xyz'))
        self.assertEqual('/one/two', utils.slash_join('/one/two'))
        self.assertEqual('/one/two', utils.slash_join(None, '/one/two'))

    def test_extract_rounds(self):
        salt = bcrypt.gensalt(rounds=7).decode('utf-8')
        self.assertEqual(7, utils.extract_bcrypt_rounds(salt))

    def test_extract_default_rounds(self):
        salt = bcrypt.gensalt().decode('utf-8')
        self.assertEqual(12, utils.extract_bcrypt_rounds(salt))
