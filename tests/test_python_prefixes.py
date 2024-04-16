import pytest

from prefixes.normal import convert_numerals

convert_numerals_test_data = [
    ('Latin', None, ''),
    ('Latin', '', ''),
    ('Latin', 1234567890, 1234567890),
    ('Latin', '١٢٣٤٥٦٧٨٩٠', 1234567890),
    ('Arabic', 1234567890, '١٢٣٤٥٦٧٨٩٠'),
    ('Latin', 1234567890.0987654321, 1234567890.0987654321),
    ('Latin', '١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤', 1234567890.0987654321),
    ('Arabic', 1234567890.0987654321, '١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤'),
    ('Latin', -1234567890, -1234567890),
    ('Latin', '-١٢٣٤٥٦٧٨٩٠', -1234567890),
    ('Arabic', -1234567890, '-١٢٣٤٥٦٧٨٩٠'),
    ('Latin', -1234567890.0987654321, -1234567890.0987654321),
    ('Latin', '-١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤', -1234567890.0987654321),
    ('Arabic', -1234567890.0987654321, '-١٢٣٤٥٦٧٨٩٠.٠٩٨٧٦٥٤'),
    ('Latin', '1 Thing, this is 1 arbitrary string', '1 Thing, this is 1 arbitrary string'),
    ('Arabic', '1 Thing, this is 1 arbitrary string', '1 Thing, this is 1 arbitrary string'),
]


@pytest.mark.parametrize("alphabet, number, expected", convert_numerals_test_data)
def test_convert_numerals(alphabet, number, expected):
    assert convert_numerals(alphabet, number) == expected
