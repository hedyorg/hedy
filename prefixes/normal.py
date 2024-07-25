# coding=utf8

import random  # noqa F401
import time  # noqa F401

try:
    import extensions  # noqa F401
except ModuleNotFoundError:
    # This is done because 'extensions' is not a python module but rather a Skulpt JS extension
    # These functions are defined in skulpt-stdlib-extensions.js
    # When running tests in test_python_prefixes it wil raise ModuleNotFoundError
    pass

global int_saver
int_saver = int


num_sys_to_digits_dict = {
    'Latin': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'Brahmi': ['𑁦', '𑁧', '𑁨', '𑁩', '𑁪', '𑁫', '𑁬', '𑁭', '𑁮', '𑁯'],
    'Devanagari': ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'],
    'Gujarati': ['૦', '૧', '૨', '૩', '૪', '૫', '૬', '૭', '૮', '૯'],
    'Gurmukhi': ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯'],
    'Bengali': ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'],
    'Kannada': ['೦', '೧', '೨', '೩', '೪', '೫', '೬', '೭', '೮', '೯'],
    'Odia': ['୦', '୧', '୨', '୩', '୪', '୫', '୬', '୭', '୮', '୯'],
    'Malayalam': ['൦', '൧', '൨', '൩', '൪', '൫', '൬', '൭', '൮', '൯'],
    'Tamil': ['௦', '௧', '௨', '௩', '௪', '௫', '௬', '௭', '௮', '௯'],
    'Telugu': ['౦', '౧', '౨', '౩', '౪', '౫', '౬', '౭', '౮', '౯'],
    'Burmese': ['၀', '၁', '၂', '၃', '၄', '၅', '၆', '၇', '၈', '၉'],
    'Tibetan': ['༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩'],
    'Mongolian': ['᠐', '᠑', '᠒', '᠓', '᠔', '᠕', '᠖', '᠗', '᠘', '᠙'],
    'Khmer': ['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩'],
    'Thai': ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙'],
    'Lao': ['໐', '໑', '໒', '໓', '໔', '໕', '໖', '໗', '໘', '໙'],
    'Javanese': ['꧐', '꧑', '꧒', '꧓', '꧔', '꧕', '꧖', '꧗', '꧘', '꧙'],
    'Arabic': ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'],
    'Persian': ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'],
    'Urdu': ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
}

digits_to_latin_dict = {
    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    '𑁦': '0', '𑁧': '1', '𑁨': '2', '𑁩': '3', '𑁪': '4', '𑁫': '5', '𑁬': '6', '𑁭': '7', '𑁮': '8', '𑁯': '9',
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
    '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4', '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9',
    '੦': '0', '੧': '1', '੨': '2', '੩': '3', '੪': '4', '੫': '5', '੬': '6', '੭': '7', '੮': '8', '੯': '9',
    '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9',
    '೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4', '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9',
    '୦': '0', '୧': '1', '୨': '2', '୩': '3', '୪': '4', '୫': '5', '୬': '6', '୭': '7', '୮': '8', '୯': '9',
    '൦': '0', '൧': '1', '൨': '2', '൩': '3', '൪': '4', '൫': '5', '൬': '6', '൭': '7', '൮': '8', '൯': '9',
    '௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9',
    '౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4', '౫': '5', '౬': '6', '౭': '7', '౮': '8', '౯': '9',
    '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4', '၅': '5', '၆': '6', '၇': '7', '၈': '8', '၉': '9',
    '༠': '0', '༡': '1', '༢': '2', '༣': '3', '༤': '4', '༥': '5', '༦': '6', '༧': '7', '༨': '8', '༩': '9',
    '᠐': '0', '᠑': '1', '᠒': '2', '᠓': '3', '᠔': '4', '᠕': '5', '᠖': '6', '᠗': '7', '᠘': '8', '᠙': '9',
    '០': '0', '១': '1', '២': '2', '៣': '3', '៤': '4', '៥': '5', '៦': '6', '៧': '7', '៨': '8', '៩': '9',
    '๐': '0', '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9',
    '໐': '0', '໑': '1', '໒': '2', '໓': '3', '໔': '4', '໕': '5', '໖': '6', '໗': '7', '໘': '8', '໙': '9',
    '꧐': '0', '꧑': '1', '꧒': '2', '꧓': '3', '꧔': '4', '꧕': '5', '꧖': '6', '꧗': '7', '꧘': '8', '꧙': '9',
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
    '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
    '零': '0'
}


def to_latin_numeral(s):
    if not s:
        return ''
    return ''.join([digits_to_latin_dict.get(letter, letter) for letter in str(s)])


def int(s):
    if isinstance(s, str):
        return int_saver(to_latin_numeral(s))
    return int_saver(s)


def is_int(n):
    try:
        int(n)
        return True
    except Exception:
        return False


def get_num_sys(value):
    if isinstance(value, Value):
        return value.numeral_system
    for num_sys, digits in num_sys_to_digits_dict.items():
        if all(n in digits for n in str(value) if is_int(n)):
            return num_sys
    return None


def localize(value, num_sys=None, bools=None):
    if value is None or value == '':
        return ''

    if bools and type(bools) is dict and True in bools and False in bools:
        boolean_values = bools
    else:
        boolean_values = {True: 'True', False: 'False'}

    if type(value) is bool:
        return boolean_values[value]
    if value == 'True':
        return boolean_values[True]
    if value == 'False':
        return boolean_values[False]

    value = str(value)
    result_type = str

    sign = ''
    if value[0] == '-':
        sign = '-'
        value = value[1:]

    if num_sys and isinstance(num_sys, str) and num_sys in num_sys_to_digits_dict:
        numeral_system = num_sys
    else:
        numeral_system = 'Latin'

    # The conversion to the latin numeral system is required because '١'.isnumeric() returns True in Python
    # (so our tests succeed), but returns False in Skulpt (and the code fails in the browser).
    number_candidate = to_latin_numeral(value)
    if number_candidate.replace('.', '', 1).isnumeric():
        numerals_list = num_sys_to_digits_dict[numeral_system]
        if '.' in number_candidate:
            tokens = number_candidate.split('.')
            all_numerals_converted = [numerals_list[int(digit)] for digit in tokens[0]]
            all_numerals_converted.append('.')
            all_numerals_converted.extend(numerals_list[int(digit)] for digit in tokens[1])
            if numeral_system == 'Latin':
                result_type = float
        else:
            all_numerals_converted = [numerals_list[int(digit)] for digit in number_candidate]
            if numeral_system == 'Latin':
                result_type = int
        value = ''.join(all_numerals_converted)
    return result_type(f'{sign}{value}')


def int_with_error(s, err):
    if isinstance(s, Value):
        s = s.data
    try:
        return int(str(s))
    except ValueError:
        raise Exception(err.format(s))


def number_with_error(s, err):
    if isinstance(s, Value):
        s = s.data
    try:
        return int(str(s))
    except ValueError:
        try:
            return float(str(s))
        except ValueError:
            raise Exception(err.format(s))


def sum_with_error(left, right, err):
    try:
        if isinstance(left, Value):
            if isinstance(left.data, str):
                left = f'{left}'
            else:
                left = left.data
        if isinstance(right, Value):
            if isinstance(right.data, str):
                right = f'{right}'
            else:
                right = right.data
        return left + right
    except Exception:
        raise Exception(err.format(left, right))


class Value:
    def __init__(self, data, num_sys=None, bools=None):
        self.data = data
        self.numeral_system = num_sys
        self.boolean_values = bools

    def __str__(self):
        if type(self.data) is list:
            return ', '.join([localize(d.data, d.numeral_system, d.boolean_values) for d in self.data])
        return str(localize(self.data, self.numeral_system, self.boolean_values))

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.data == other.data
        return False
