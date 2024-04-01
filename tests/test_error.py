from parameterized import parameterized

from app import app
from hedy import exceptions
from hedy_content import ALL_LANGUAGES
from hedy_error import get_error_text, _highlight, _get_missing_arguments
from tests.Tester import HedyTester


def exception_language_input():
    exceptions_ = create_exceptions()
    languages = ALL_LANGUAGES.keys()
    return [(ex, lang) for lang in languages for ex in exceptions_]


def custom_name_func(testcase_func, _, param):
    (ex, lang) = param.args
    return parameterized.to_safe_name(
        f"{testcase_func.__name__}_{ex.__class__.__name__}_to_{lang}_lang")


def create_exceptions():
    exception_classes = [cls for cls in exceptions.HedyException.__subclasses__()]
    return [create_exception(exception_class) for exception_class in exception_classes]


def create_exception(ex_class):
    ex_args = [
        f'{n}-value' for n in ex_class.__init__.__code__.co_varnames if n not in ['self', 'arguments']]
    return ex_class(*ex_args)


def highlighted(v):
    return f'<span class="command-highlighted">{v}</span>'


class TestErrors(HedyTester):

    # The test ensures the error templates can be formatted with the arguments of the hedy exceptions in all languages
    @parameterized.expand(exception_language_input(), name_func=custom_name_func)
    def test_translate_hedy_exception(self, exception, language):
        with app.test_request_context(headers={'Accept-Language': language}):
            get_error_text(exception, language)

    def test_error_text_format_fails_on_unknown_key(self):
        lang = 'en'
        with app.test_request_context(headers={'Accept-Language': lang}):
            with self.assertRaises(KeyError):
                error = exceptions.HedyException('Non-existent {code}')
                get_error_text(error, lang)

    def test_missing_arguments_none(self):
        result = _get_missing_arguments('The input {command} is invalid', {'command': 'go'}, 'en')
        self.assertEqual(0, len(result))

    def test_missing_argument_keyword(self):
        result = _get_missing_arguments('The input {command} is not {print}', {'command': 'go'}, 'en')
        self.assertEqual(1, len(result))
        self.assertIn('print', result)

    def test_missing_argument_keyword_translated(self):
        result = _get_missing_arguments('The input {command} is not {ask}', {'command': 'go'}, 'nl')
        self.assertEqual(1, len(result))
        self.assertIn('ask', result)
        self.assertEqual('vraag', result['ask'])

    def test_missing_argument_unknown_keyword(self):
        result = _get_missing_arguments('This is {unknown}', {}, 'en')
        self.assertEqual(0, len(result))

    def test_highlight_template_without_highlighting(self):
        text = 'Error template without highlighting'
        result = _highlight(text)
        self.assertEqual(text, result)

    def test_highlight_whole_template(self):
        result = _highlight('`Error template`')
        expected = highlighted("Error template")
        self.assertEqual(expected, result)

    def test_highlight_template_start(self):
        result = _highlight('`Error` template with highlighting')
        expected = f'{highlighted("Error")} template with highlighting'
        self.assertEqual(expected, result)

    def test_highlight_template_end(self):
        result = _highlight('Template highlighting `error`')
        expected = f'Template highlighting {highlighted("error")}'
        self.assertEqual(expected, result)

    def test_highlight_template_start_end(self):
        result = _highlight('`start` and `end`')
        expected = f'{highlighted("start")} and {highlighted("end")}'
        self.assertEqual(expected, result)

    def test_highlight_template_multiple_parts(self):
        result = _highlight('this commands `start`,`middle`,`end`.')
        expected = f'this commands {highlighted("start")},{highlighted("middle")},{highlighted("end")}.'
        self.assertEqual(expected, result)

    def test_highlight_template_consecutive_parts(self):
        result = _highlight('this commands `start``middle``end`.')
        expected = f'this commands {highlighted("start")}{highlighted("middle")}{highlighted("end")}.'
        self.assertEqual(expected, result)

    def test_highlight_whole_template_triple_backquotes(self):
        text = '```incorrect quotes```'
        result = _highlight(text)
        self.assertEqual(highlighted("incorrect quotes"), result)

    def test_highlight_template_multiple_parts_triple_backquotes(self):
        result = _highlight('this is ```incorrect quotes``` but I will use it ```again```')
        expected = f'this is {highlighted("incorrect quotes")} but I will use it {highlighted("again")}'
        self.assertEqual(expected, result)
