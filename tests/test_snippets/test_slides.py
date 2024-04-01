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

Hedy_snippets = [(s.name, s) for s in snippet_tester.collect_slides_snippets(
    path=path.join(snippet_tester.rootdir(), 'content/slides'))]

assert len(snippets) == len(Hedy_snippets)


Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)

# lang = 'zh_hans' #useful if you want to test just 1 language
lang = None
level = None
Hedy_snippets = snippet_tester.filter_snippets(Hedy_snippets, lang=lang, level=level)

if lang:
    Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.language[:2] == lang]


class TestsSlidesPrograms(snippet_tester.HedySnippetTester):
    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_slide_programs(self, name, snippet):
        self.do_snippet(snippet, yaml_locator=slides_locator)


def slides_locator(snippet, yaml):
    """Returns where in the Slides YAML we found a Slides snippet."""
    return snippet_tester.YamlLocation(
        dict=yaml['levels'][snippet.level][snippet.field_name],
        key='code')
