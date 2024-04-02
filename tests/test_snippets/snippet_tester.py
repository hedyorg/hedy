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

from dataclasses import dataclass
import functools
import exceptions
import hedy
import utils
from tests.Tester import HedyTester, YamlSnippet
from website.yaml_file import YamlFile

fix_error = False
# set this to True to revert broken snippets to their en counterpart automatically
# this is useful for large Weblate PRs that need to go through, this fixes broken snippets
if os.getenv('fix_for_weblate') or os.getenv('FIX_FOR_WEBLATE'):
    fix_error = True


def rootdir():
    """Return the repository root directory."""
    return os.path.join(os.path.dirname(__file__), '..', '..')


def listify(fn):
    """Turns a function written as a generator into a function that returns a list.

    Writing a function that produces elements one by one is convenient to write
    as a generator (using `yield`), but the return value can only be iterated once.
    The caller needs to know that the function is a generator and call `list()` on
    the result.

    This decorator does that from the function side: `list()` is automatically
    called, so the caller doesn't need to know anything, yet the function is still
    nice to read and write.
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return list(fn(*args, **kwargs))
    return wrapper


@listify
def collect_adventures_snippets():
    """Find the snippets for adventures."""
    for filename, language, yaml in find_yaml_files('content/adventures'):
        for adventure_key, adventure in yaml['adventures'].items():
            # the default tab sometimes contains broken code to make a point to learners about changing syntax.
            if adventure_key in ['default', 'debugging']:
                continue

            for level_number, level in adventure['levels'].items():
                for adventure_part, markdown_text in level.items():
                    for code in markdown_code_blocks(markdown_text):
                        yield YamlSnippet(
                            code=code,
                            filename=filename,
                            language=language,
                            level=level_number,
                            # The path in the YAML we took to get here
                            yaml_path=['adventures', adventure_key, 'levels', level_number, adventure_part])


@listify
def collect_cheatsheet_snippets():
    """Find the snippets in cheatsheets."""
    for filename, language, yaml in find_yaml_files('content/cheatsheets'):
        for level_number, level in yaml.items():
            for command_index, command in enumerate(level):
                if code := command.get('demo_code'):
                    yield YamlSnippet(
                        code=code,
                        filename=filename,
                        language=language,
                        level=level_number,
                        # The path in the YAML we took to get here
                        yaml_path=[level_number, command_index, 'demo_code'])


@listify
def collect_parsons_snippets():
    """Find the snippets in Parsons YAMLs."""
    for filename, language, yaml in find_yaml_files('content/parsons'):
        for level_number, level in yaml['levels'].items():
            for exercise_nr, exercise in level.items():
                yield YamlSnippet(
                    code=exercise['code'],
                    filename=filename,
                    language=language,
                    level=level_number,
                    # The path in the YAML we took to get here
                    yaml_path=['levels', level_number, exercise_nr, 'code'])


@listify
def collect_slides_snippets():
    """Find the snippets in slides YAMLs."""
    for filename, language, yaml in find_yaml_files('content/slides'):
        for level_number, level in yaml['levels'].items():
            for slide_nr, slide in level.items():
                # Some slides have code that is designed to fail
                if slide.get('debug'):
                    continue

                if code := slide.get('code'):
                    yield YamlSnippet(
                        code=code,
                        filename=filename,
                        language=language,
                        # Level 0 needs to be treated as level 1
                        level=max(1, level_number),
                        # The path in the YAML we took to get here
                        yaml_path=['levels', level_number, slide_nr, 'code'])


def find_yaml_files(repository_path):
    """Find all YAML files in a given directory, relative to the repository root.

    Returns an iterator of (filename, language, yaml_object).
    """
    path = os.path.join(rootdir(), repository_path)
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]

    for f in files:
        filename = os.path.join(path, f)
        lang = f.split(".")[0]
        yaml = YamlFile.for_file(os.path.join(path, f))

        yield (filename, lang, yaml)


def markdown_code_blocks(text):
    """Parse the text as MarkDown and return all code blocks in here."""
    return [tag.contents[0].contents[0]
            for tag in utils.markdown_to_html_tags(text)
            if tag.name == 'pre' and tag.contents and tag.contents[0].contents]


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
    """Expand a set of snippets to pairs of (name, snippet).

    This is necessary to stick it into @parameterized.expand.
    """
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
    """Given a YamlSnippet, locate its containing object and key.

    This uses the `yaml_path` to descend into the given YAML object bit
    by bit (by indexing the dictionary or list with the next string
    or int) until we arrive at the parent object of the string we're
    looking for.
    """
    path = snippet.yaml_path.copy()
    while len(path) > 1:
        root = root[path[0]]
        path = path[1:]
    return YamlLocation(dict=root, key=path[0])
