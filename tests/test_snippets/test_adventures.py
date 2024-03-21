from os import path

from parameterized import parameterized

from tests.Tester import HedyTester
from . import snippet_tester


check_stories = False

Hedy_snippets = [(s.name, s) for s in snippet_tester.collect_adventures_snippets(
    path=path.join(snippet_tester.rootdir(), 'content/adventures'))]
Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)

# lang = 'zh_hans' #useful if you want to test just 1 language
lang = None
level = None
Hedy_snippets = snippet_tester.filter_snippets(Hedy_snippets, lang=lang, level=level)


class TestsAdventurePrograms(snippet_tester.HedySnippetTester):
    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_adventures(self, name, snippet):
        self.do_snippet(snippet, yaml_locator=adventure_locator)


def adventure_locator(snippet, yaml):
    """Returns where in the adventures YAML we found an adventure snippet."""
    return snippet_tester.YamlLocation(
        dict=yaml['adventures'][snippet.key]['levels'][snippet.level],
        key=snippet.field_name)
