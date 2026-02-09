import textwrap
from parameterized import parameterized
import hedy.translation as hedy_translation
from hedy.content import ALL_KEYWORD_LANGUAGES
from ..Tester import HedyTester

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel14(HedyTester):
    level = 14
