from os import path

from parameterized import parameterized

from tests.Tester import HedyTester
from . import snippet_tester


def slides_locator(entry):
    """Locator for snippets in the slides YAML.

    More complicated than the regular locators.
    """
    if isinstance(entry.value, dict) and entry.value.get('debug'):
        # Some entries are designed to fail, skip those
        return snippet_tester.SKIP

    return at_least_level_1(snippet_tester.locator_decision_from_map(entry.field_path, {
        'levels.<LEVEL>.*.code': snippet_tester.COLLECT,
    }))


def at_least_level_1(decision):
    # The slides contain level=0 entries, which should be treated as level=1
    if isinstance(decision, tuple):
        if decision[1] == 0:
            return decision[0], 1
    return decision


snippets = snippet_tester.collect_yaml_snippets('content/slides', slides_locator)

snippets = HedyTester.translate_keywords_in_snippets(snippets)

# lang = 'zh_hans' #useful if you want to test just 1 language
lang = None
level = None
snippets = snippet_tester.filter_snippets(snippets, lang=lang, level=level)


class TestsSlidesPrograms(snippet_tester.HedySnippetTester):
    @parameterized.expand(snippet_tester.snippets_with_names(snippets), skip_on_empty=True)
    def test_slide_programs(self, name, snippet):
        self.do_snippet(snippet)

