from os import path

from parameterized import parameterized

from tests.Tester import HedyTester
from . import snippet_tester

Hedy_snippets = [(s.name, s) for s in snippet_tester.collect_cheatsheet_snippets(
    path=path.join(snippet_tester.rootdir(), 'content/cheatsheets'))]
Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)

# lang = 'zh_hans' #useful if you want to test just 1 language
lang = None
level = None
Hedy_snippets = snippet_tester.filter_snippets(Hedy_snippets, lang=lang, level=level)

class TestsCheatsheetPrograms(snippet_tester.HedySnippetTester):

    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_cheatsheets_programs(self, name, snippet):
        self.do_snippet(snippet)