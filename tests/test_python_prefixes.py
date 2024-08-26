import pytest

from prefixes.normal import localize, to_latin_numeral, Value

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


@pytest.mark.parametrize("value, num_sys, bool_sys, expected", localize_test_data)
def test_localize(value, num_sys, bool_sys, expected):
    assert localize(value, num_sys, bool_sys) == expected


@pytest.mark.parametrize("value, expected", to_latin_numeral_test_data)
def test_to_latin_numeral(value, expected):
    assert to_latin_numeral(value) == expected


value_str_test_data = [
    (Value('hello Hedy'), 'hello Hedy'),
    (Value(1, num_sys='Latin'), '1'),
    (Value(True, bool_sys={True: 'yes', False: 'no'}), 'yes'),
    (Value(False, bool_sys={True: 'yes', False: 'no'}), 'no'),

    # TODO: before, lists were printed out by python, e.g. ['test', 1] and now they are printed as individual
    #  elements, e.g. [test, 1]. Should we wrap strings in lists in quotes for compatibility with the old way?
    #  For now, let's keep the values in lists just like they would be printed if not in a list.
    (Value([Value('hello Hedy')]), '[hello Hedy]'),
    (Value([Value('hello'), Value('Hedy')]), '[hello, Hedy]'),
    (Value([Value(1, num_sys='Latin')]), '[1]'),
    (Value([Value(False, bool_sys={True: 'yes', False: 'no'})]), '[no]'),
]


@pytest.mark.parametrize("value, expected", value_str_test_data)
def test_value(value, expected):
    result = value.__str__()
    assert result == expected
