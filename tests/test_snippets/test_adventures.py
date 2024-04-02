from os import path

from parameterized import parameterized

from tests.Tester import HedyTester
from . import snippet_tester


# Can be used to catch languages with example codes in the story_text
# at once point in time, this was the default and some languages still use this old
# structure
check_stories = False

snippets = snippet_tester.collect_adventures_snippets()

if check_stories:
    for snippet in snippets:
        if snippet.field_path[-1].startswith('story_text'):
            raise Exception(f"Example code in story text: {snippet.location}, not recommended!")

HedyTester.translate_keywords_in_snippets(snippets)

# lang = 'zh_hans' #useful if you want to test just 1 language
lang = None
level = None
snippets = snippet_tester.filter_snippets(snippets, lang=lang, level=level)


class TestsAdventurePrograms(snippet_tester.HedySnippetTester):
    @parameterized.expand(snippet_tester.snippets_with_names(snippets), skip_on_empty=True)
    def test_adventures(self, name, snippet):
        self.do_snippet(snippet)
