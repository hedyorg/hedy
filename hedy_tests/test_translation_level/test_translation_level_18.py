import textwrap
import hedy.translation as hedy_translation
from tests.Tester import HedyTester

# tests should be ordered as follows:
# * Translation from English to Dutch
# * Translation from Dutch to English
# * Translation to several languages
# * Error handling


class TestsTranslationLevel18(HedyTester):
    level = 18
