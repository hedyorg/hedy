from os import path

from tests.Tester import HedyTester
from parameterized import parameterized
from . import snippet_tester


snippets = snippet_tester.collect_parsons_snippets()

HedyTester.translate_keywords_in_snippets(snippets)

# lang = 'zh_hans' #useful if you want to test just 1 language
lang = None
level = None
snippets = snippet_tester.filter_snippets(snippets, lang=lang, level=level)


class TestsParsonsPrograms(snippet_tester.HedySnippetTester):

    @parameterized.expand(snippet_tester.snippets_with_names(snippets), skip_on_empty=True)
    def test_parsons(self, name, snippet):
        self.do_snippet(snippet)
