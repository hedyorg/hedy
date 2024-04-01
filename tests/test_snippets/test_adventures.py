from os import path

from parameterized import parameterized

from tests.Tester import HedyTester
from . import snippet_tester


snippets = snippet_tester.collect_yaml_snippets('content/adventures', {
    # the default tab sometimes contains broken code to make a point to learners about changing syntax.
    'adventures.default': snippet_tester.SKIP,
    'adventures.debugging': snippet_tester.SKIP,
    'adventures.*.levels.<LEVEL>.story_text*': snippet_tester.COLLECT_MARKDOWN,
    'adventures.*.levels.<LEVEL>.example_code*': snippet_tester.COLLECT_MARKDOWN,
})

snippets = HedyTester.translate_keywords_in_snippets(snippets)

# lang = 'zh_hans' #useful if you want to test just 1 language
lang = None
level = None
snippets = snippet_tester.filter_snippets(snippets, lang=lang, level=level)


class TestsAdventurePrograms(snippet_tester.HedySnippetTester):
    @parameterized.expand(snippet_tester.snippets_with_names(snippets), skip_on_empty=True)
    def test_adventures(self, name, snippet):
        self.do_snippet(snippet)
