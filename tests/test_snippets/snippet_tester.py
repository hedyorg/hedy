"""Shared helper functions for the snippet tester functionality.

This code is there to test the code examples in all YAML files.

This file has been put together quickly to solve a problem. It can be cleaned up.

TODO:
- The collection routines are very similar; combine them.
- Snippets can hold on to the information where in the YAML file they were
  discovered. That way, individual test suites don't have to supply a
  'yaml_locator'.
"""

import os
from os import path
from fnmatch import fnmatchcase
from collections import namedtuple

from dataclasses import dataclass
import exceptions
import hedy
import utils
from tests.Tester import HedyTester, Snippet, YamlSnippet
from website.yaml_file import YamlFile
from typing import List, Callable, Tuple, Dict, Union

fix_error = False
# set this to True to revert broken snippets to their en counterpart automatically
# this is useful for large Weblate PRs that need to go through, this fixes broken snippets
if os.getenv('fix_for_weblate') or os.getenv('FIX_FOR_WEBLATE'):
    fix_error = True


check_stories = False


def rootdir():
    """Return the repository root directory."""
    return os.path.join(os.path.dirname(__file__), '..', '..')


COLLECT, COLLECT_MARKDOWN, SKIP, RECURSE = 'COLLECT', 'COLLECT_MARKDOWN', 'SKIP', 'RECURSE'


def collect_yaml_snippets(repository_path: str, locator: Union[Callable, Dict[str, str]]) -> List[YamlSnippet]:
    """Collect all YAML snippets in a directory.

    Snippet() has many fields; this function only sets 'filename', 'code' and 'field_path', which are used
    in the rest of the snippet tester to revert failing snippets to English.

    locator can be either a function, which will be called for every YAML entry and
    should retur a decision (recurse, skip, collect snippets here and if so what's
    their level?), or be a map that will be passed to `make_locator`.
    """
    path = os.path.join(rootdir(), repository_path)
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]

    locator = locator if callable(locator) else make_locator(locator)

    ret = []
    for f in files:
        filename = os.path.join(path, f)
        lang = f.split(".")[0]

        yaml = YamlFile.for_file(os.path.join(path, f))

        for field_path, level, code in recurse_yaml(yaml, [], locator):
            ret.append(YamlSnippet(
                filename=filename,
                code=code,
                level=level,
                field_path=field_path,
                language=lang))

    return ret


def locator_decision_from_map(field_path, path_map):
    """Source the decision for a YAML locator from a map.

    The field_path will be compared as a string agains the entries from the map.

    Here's a typical example of the map that should be passed to this function:

    ```
    {
        'adventures.default': snippet_tester.SKIP,
        'adventures.debugging': snippet_tester.SKIP,
        'adventures.*.levels.<LEVEL>.story_text*': snippet_tester.COLLECT_MARKDOWN,
        'adventures.*.levels.<LEVEL>.example_code*': snippet_tester.COLLECT_MARKDOWN,
    }
    ```
    """

    for pattern, effect in path_map.items():
        # Treat '<LEVEL>' as * for the purposes of matching
        match_pattern = pattern.replace('<LEVEL>', '*')

        if fnmatchcase(field_path, match_pattern):
            # Return the effect. If the effect is one of the collects, we must pattern match the level out of the path.
            if effect == COLLECT or effect == COLLECT_MARKDOWN:
                level_ix = pattern.split('.').index('<LEVEL>')
                if level_ix == -1:
                    raise RuntimeError('A pattern with COLLECT must contain the matcher <LEVEL> somewhere')
                level = int(field_path.split('.')[level_ix])
                return (effect, level)

            return effect


def make_locator(path_map):
    """Returns a locator from a path map."""
    def locator(entry):
        return locator_decision_from_map(entry.field_path, path_map)

    return locator


def path_match(field_path, patterns):
    return any(fnmatchcase(field_path, pattern) for pattern in patterns)


YamlEntry = namedtuple('YamlEntry', ('field_path', 'value'))


def recurse_yaml(yaml_value, field_path: List[str], locator: Callable[[List[str]], str]):
    # Protocol: locator must return either SKIP, RECURSE, or (COLLECT, <level>) or (COLLECT_MARKDOWN, <level>)
    # RECURSE is the default action
    entry = YamlEntry('.'.join((str(x) for x in field_path)), yaml_value)
    orig_decision = locator(entry) or RECURSE
    level = None
    if isinstance(orig_decision, tuple):
        level = orig_decision[1]
        decision = orig_decision[0]
    else:
        decision = orig_decision

    def assert_decision(*args):
        if not decision in args:
            raise RuntimeError(f'For path {field_path} decision must be one of {args}, got: {decision}')

    if isinstance(yaml_value, str):
        assert_decision(COLLECT, COLLECT_MARKDOWN, SKIP, RECURSE)

        codes = []
        if decision == COLLECT:
            codes = [yaml_value]
        if decision == COLLECT_MARKDOWN:
            codes = [tag.contents[0].contents[0]
                     for tag in utils.markdown_to_html_tags(yaml_value)
                     if tag.name == 'pre' and tag.contents and tag.contents[0].contents]

        for code in codes:
            if not level:
                raise RuntimeError(f'A locator returning COLLECT must also return a level (got {orig_decision})')
            yield (field_path, level, code)

    if isinstance(yaml_value, list):
        assert_decision(RECURSE, SKIP)
        if decision == RECURSE:
            for i, value in enumerate(yaml_value):
                yield from recurse_yaml(value, field_path + [i], locator)
        return
    if hasattr(yaml_value, 'items'):
        assert_decision(RECURSE, SKIP)
        if decision == RECURSE:
            for key, value in yaml_value.items():
                yield from recurse_yaml(value, field_path + [key], locator)
        return


def filter_snippets(snippets, level=None, lang=None):
    if (lang or level) and os.getenv('CI'):
        raise RuntimeError('Whoops, it looks like you left a snippet filter in!')

    def snippet_from(x):
        """From either a (name, snippet) pair or just a snippet, return the snippet."""
        if isinstance(x, tuple):
            return x[1]
        return x

    if lang:
        snippets = [x for x in snippets if snippet_from(x).language[:2] == lang]

    if level:
        snippets = [x for x in snippets if snippet_from(x).level == level]

    return snippets


def snippets_with_names(snippets):
    """Expand a set of snippets to pairs of (name, snippet). This is necessary to stick it into @parameterized.expand."""
    return ((s.name, s) for s in snippets)


@dataclass
class YamlLocation:
    dict: dict
    key: str


class HedySnippetTester(HedyTester):
    """Base class for all other snippet testers.

    The logic is the same between all of them, so we can combine it.
    """

    def do_snippet(self, snippet):
        if snippet is None or len(snippet.code) == 0:
            return

        try:
            self.single_level_tester(
                code=snippet.code,
                level=int(snippet.level),
                lang=snippet.language,
                unused_allowed=True,
                translate=False,
                skip_faulty=False
            )

        except hedy.exceptions.CodePlaceholdersPresentException:  # Code with blanks is allowed
            pass
        except OSError:
            return None  # programs with ask cannot be tested with output :(
        except exceptions.HedyException as E:
            error_message = self.format_test_error_md(E, snippet)

            if fix_error and isinstance(snippet, YamlSnippet):
                self.restore_snippet_to_english(snippet)

                with open(path.join(rootdir(), 'snippet-report.md.tmp'), 'a') as f:
                    f.write(error_message + '\n')
                    f.write('This snippet has been reverted to English.\n\n')
            else:
                print(error_message)
                raise E

    def restore_snippet_to_english(self, snippet):
        # English file is always 'en.yaml' in the same dir
        en_file = path.join(path.dirname(snippet.filename), 'en.yaml')

        # Read English yaml file
        original_yaml = YamlFile.for_file(en_file)
        original_loc = locate_snippet_in_yaml(original_yaml, snippet, yaml_locator)

        # Read broken yaml file
        broken_yaml = utils.load_yaml_rt(snippet.filename)
        broken_loc = locate_snippet_in_yaml(broken_yaml, snippet, yaml_locator)

        # Restore to English version
        broken_loc.dict[broken_loc.key] = original_loc.dict[original_loc.key]
        with open(snippet.filename, 'w') as file:
            file.write(utils.dump_yaml_rt(broken_yaml))


def locate_snippet_in_yaml(root, snippet):
    """Given a snippet, locate its containing object and key.

    Use the information in the snippet itself if it is a YamlSnippet, otherwise uses
    the locator function.
    """
    path = snippet.field_path.copy()
    print(path)
    while len(path) > 1:
        root = root[path[0]]
        path = path[1:]
    return YamlLocation(dict=root, key=path[0])
