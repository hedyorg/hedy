import unittest

from hedy import is_quoted, find_unquoted_segments
from parameterized import parameterized


class TestHedy(unittest.TestCase):
    @parameterized.expand([
        '',
        ' ',
        '"',
        "'",
        'Words',
        '"OpenDouble',
        'CloseDouble"',
        "'OpenSingle",
        "CloseSingle'",
        "'Middle'Single",
        '"Middle"Double',
        '»Resersed«',
        '\'Mismatch single and double"',
        '«Mismatch french and cyrillic“'
    ])
    def test_not_is_quoted(self, s):
        result = is_quoted(s)
        self.assertFalse(result)

    @parameterized.expand([
        "''",
        '""',
        "‘’",
        '„“',
        '«»',
        "'single'",
        '"double"',
        "‘correctly quoted’",
        '„cyrillic quoted“',
        '«correctly quoted»',
    ])
    def test_is_quoted(self, s):
        result = is_quoted(s)
        self.assertTrue(result)

    @parameterized.expand([
        ('', ''),
        ('""', ''),
        ("‘correctly quoted’", ''),
        ('"no closing quote', '"no closing quote'),
        ('no opening quote"', 'no opening quote"'),
        ("'single' 5", ' 5'),
        ('5 \\ 5 "double"', '5 \\ 5 '),
        ("'quoted' unquoted «quoted»", ' unquoted '),
        ("un'quoted'quot«quoted»ed", 'unquoted'),
        ("'quoted' unquoted «quoted» this is not", ' unquoted  this is not'),
        ("'quoted' unquoted «quoted» this is not \"again", ' unquoted  this is not \"again')
    ])
    def test_find_unquoted_segments(self, s, expected):
        result = find_unquoted_segments(s)
        self.assertEqual(expected, result)
