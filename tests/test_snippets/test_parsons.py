from os import path

from tests.Tester import HedyTester
from parameterized import parameterized
from . import snippet_tester


Hedy_snippets = [(s.name, s) for s in snippet_tester.collect_parsons_snippets(
    path=path.join(snippet_tester.rootdir(), 'content/parsons'))]
Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)

# lang = 'zh_hans' #useful if you want to test just 1 language
lang = None
level = None
Hedy_snippets = snippet_tester.filter_snippets(Hedy_snippets, lang=lang, level=level)


class TestsParsonsPrograms(snippet_tester.HedySnippetTester):
    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_parsons(self, name, snippet):
        self.do_snippet(snippet, yaml_locator=parsons_locator)


def parsons_locator(snippet, yaml):
    """Returns where in the Parsons YAML we found a Parsons snippet."""
    return snippet_tester.YamlLocation(
        dict=yaml['levels'][snippet.level],
        key=int(snippet.field_name))