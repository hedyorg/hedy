import textwrap
from parameterized import parameterized
import hedy_translation
from hedy_content import ALL_KEYWORD_LANGUAGES
from tests.Tester import HedyTester

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel14(HedyTester):
    level = 14
    

    