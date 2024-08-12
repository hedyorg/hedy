import pytest

from prefixes.normal import localize, to_latin_numeral

localize_test_data = [
    # None and empty values
    (None, None, None, ''),
    (None, 'Latin', None, ''),
    ('', None, None, ''),
    ('', 'Latin', None, ''),

    # Boolean values
    (True, None, None, 'True'),
    (True, 'Latin', None, 'True'),
    (True, None, {True: 'yes', False: 'no'}, 'yes'),
    (False, None, None, 'False'),
    (False, 'Latin', None, 'False'),
    (False, None, {True: 'yes', False: 'no'}, 'no'),
    ('True', None, None, 'True'),
    ('True', None, {True: 'да', False: 'не'}, 'да'),
    ('False', None, None, 'False'),
    ('False', None, {True: 'да', False: 'не'}, 'не'),
    (True, None, 15, 'True'),  # bools is not a dictionary
    (True, None, {}, 'True'),  # bools is an empty dictionary
    (False, None, {'incorrect': 'dictionary', 'values': ''}, 'False'),  # bools does not have correct keys

    # Numbers
    (1234567890, None, None, 1234567890),
    (1234567890, 'Incorrect', None, 1234567890),  # non-existing numeral system
    (1234567890, '', None, 1234567890),  # empty string for numeral system
    (1234567890, {}, None, 1234567890),  # incorrect type of numeral system
    (1234567890, 'Latin', None, 1234567890),
    ('١٢٣٤٥٦٧٨٩٠', 'Latin', None, 1234567890),
    ('١٢٣٤٥٦٧٨٩٠', None, None, 1234567890),
    (1234567890, 'Arabic', None, '١٢٣٤٥٦٧٨٩٠'),
    (1234567890.0987654321, 'Latin', None, 1234567890.0987654321),
    ('١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤', 'Latin', None, 1234567890.0987654),
    (1234567890.0987654321, 'Arabic', None, '١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤'),
    (-1234567890, 'Latin', None, -1234567890),
    ('-١٢٣٤٥٦٧٨٩٠', 'Latin', None, -1234567890),
    (-1234567890, 'Arabic', None,  '-١٢٣٤٥٦٧٨٩٠'),
    (-1234567890.0987654321, 'Latin', None, -1234567890.0987654321),
    (-1234567890.0987654321, None, None, -1234567890.0987654321),
    ('-١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤', 'Latin', None, -1234567890.0987654),
    (-1234567890.0987654321, 'Arabic', None, '-١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤'),

    # Strings
    ('1 Thing, this is 1 arbitrary string', None, None, '1 Thing, this is 1 arbitrary string'),
    ('1 Thing, this is 1 arbitrary string', 'Arabic', None, '1 Thing, this is 1 arbitrary string'),
    ('1 Thing, this is 1 arbitrary string', 'Latin', {True: 'yes', False: 'no'}, '1 Thing, this is 1 arbitrary string'),
    ('This is ١', None, None, 'This is ١'),
    ('This is ١', 'Latin', None, 'This is ١'),
    ('This is ١', 'Arabic', None, 'This is ١'),
]

to_latin_numeral_test_data = [
    # None and empty values
    (None, ''),
    ('', ''),

    # Numbers
    (1234567890, '1234567890'),
    ('١٢٣٤٥٦٧٨٩٠', '1234567890'),
    (-1234567890, '-1234567890'),
    ('-七八', '-78'),
    ('-١٢٣٤٥٦٧٨٩٠', '-1234567890'),
    (1234567890.0987654, '1234567890.0987654'),
    ('١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤٣٢١', '1234567890.0987654321'),
    ('七.八', '7.8'),
    (-1234567890.0987654, '-1234567890.0987654'),
    ('-١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤٣٢١', '-1234567890.0987654321'),
    ('-七.八', '-7.8'),

    # Strings
    ('1 Thing, this is 1 arbitrary string', '1 Thing, this is 1 arbitrary string'),
    ('This is ١', 'This is 1'),
    ('八 languages', '8 languages'),
]


@pytest.mark.parametrize("value, num_sys, bools, expected", localize_test_data)
def test_localize(value, num_sys, bools, expected):
    assert localize(value, num_sys, bools) == expected


@pytest.mark.parametrize("value, expected", to_latin_numeral_test_data)
def test_to_latin_numeral(value, expected):
    assert to_latin_numeral(value) == expected
