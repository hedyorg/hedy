from parameterized import parameterized

from app import app, translate_error
from hedy import exceptions
from hedy_content import ALL_LANGUAGES
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


class TestsTranslationError(HedyTester):

    @parameterized.expand(exception_language_input(), name_func=custom_name_func)
    def test_translate_hedy_exception(self, exception, language):
        with app.test_request_context(headers={'Accept-Language': language}):
            translate_error(exception.error_code, exception.arguments, language)
