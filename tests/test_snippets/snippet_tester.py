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
                for markdown_text in level.values():
                    for code in markdown_code_blocks(markdown_text.as_string()):
                        yield YamlSnippet(
                            code=code,
                            filename=filename,
                            language=language,
                            level=level_number,
                            yaml_path=markdown_text.yaml_path)


@listify
def collect_cheatsheet_snippets():
    """Find the snippets in cheatsheets."""
    for filename, language, yaml in find_yaml_files('content/cheatsheets'):
        for level_number, level in yaml.items():
            for command in level:
                if code := command.get('demo_code'):
                    yield YamlSnippet(
                        code=code.as_string(),
                        filename=filename,
                        language=language,
                        level=level_number,
                        yaml_path=code.yaml_path)


@listify
def collect_parsons_snippets():
    """Find the snippets in Parsons YAMLs."""
    for filename, language, yaml in find_yaml_files('content/parsons'):
        for level_number, level in yaml['levels'].items():
            for exercise in level:
                code = exercise['code']
                yield YamlSnippet(
                    code=code.as_string(),
                    filename=filename,
                    language=language,
                    level=level_number,
                    yaml_path=code.yaml_path)


@listify
def collect_slides_snippets():
    """Find the snippets in slides YAMLs."""
    for filename, language, yaml in find_yaml_files('content/slides'):
        for level_number, level in yaml['levels'].items():
            for slide in level:
                # Some slides have code that is designed to fail
                if slide.get('debug'):
                    continue

                if code := slide.get('code'):
                    yield YamlSnippet(
                        code=code.as_string(),
                        filename=filename,
                        language=language,
                        # Level 0 needs to be treated as level 1
                        level=max(1, level_number),
                        yaml_path=code.yaml_path)


def find_yaml_files(repository_path):
    """Find all YAML files in a given directory, relative to the repository root.

    Returns an iterator of (filename, language, located_yaml_object).

    The `located_yaml_object` is a `LocatedYamlValue` representing the root of the
    YAML file, which can be indexed using `[]` and by using `.items()` and `.values()`.
    """
    path = os.path.join(rootdir(), repository_path)
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]

    for f in files:
        filename = os.path.join(path, f)
        lang = f.split(".")[0]
        yaml = YamlFile.for_file(os.path.join(path, f))

        yield (filename, lang, LocatedYamlValue(yaml, []))


def markdown_code_blocks(text):
    """Parse the text as MarkDown and return all code blocks in here.

    Returns all code blocks, except those tagged as 'not_hedy_code'.
    """
    return [c.code
            for c in utils.code_blocks_from_markdown(text)
            if c.info != 'not_hedy_code']


def filter_snippets(snippets, level=None, lang=None):
    if (lang or level) and os.getenv('CI'):
        raise RuntimeError('Whoops, it looks like you left a snippet filter in!')

    if lang:
        snippets = [s for s in snippets if s.language[:len(lang)] == lang]

    if level:
        snippets = [s for s in snippets if s.level == level]

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
        original_loc = locate_snippet_in_yaml(original_yaml, snippet)

        # Read broken yaml file
        broken_yaml = utils.load_yaml_rt(snippet.filename)
        broken_loc = locate_snippet_in_yaml(broken_yaml, snippet)

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


class LocatedYamlValue:
    """A value in a YAML file, along with its path inside that YAML file.

    Has features to descend into children of the wrapped value, which also
    emits `LocatedYamlValue`s with their paths automatically baked in.

    For example, if we have a referece to the adventure `1` (with path
    `['adventures', 1]` in the following YAML:

        adventures:
            1:
                code: |
                print hello

    And we would write:

        code = level['code']

    `code` would be a string that knew its path is `['adventures', 1, 'code']`.

    This makes it so that the authors of YAML traversal functions don't have to
    keep track of the path of strings, when they finally construct a
    `YamlSnippet`.
    """

    def __init__(self, inner, yaml_path):
        self.inner = inner
        self.yaml_path = yaml_path

    def items(self):
        """Returns a set of (key, LocatedYamlValue) values, one for every element of the inner value.

        The inner value must be a dict-like or list. For a list, the indexes will be returned as keys.
        """
        if hasattr(self.inner, 'items'):
            # Dict-like
            return [(k, LocatedYamlValue(v, self.yaml_path + [k])) for k, v in self.inner.items()]
        if isinstance(self.inner, list):
            # A list can be treated as a dict-like using integer indexes
            return [(i, LocatedYamlValue(v, self.yaml_path + [i])) for i, v in enumerate(self.inner)]
        raise TypeError('Can only call .items() on a value of type dict or list, got %r' % self.inner)

    def values(self):
        """Returns a list of `LocatedYamlValue`s, one for every element in this collection.

        Ignores keys.
        """
        return [v for _, v in self.items()]

    def __getitem__(self, key):
        """Retrieve a single item from the inner value."""
        ret = self.inner[key]
        return LocatedYamlValue(ret, self.yaml_path + [key])

    def get(self, key, default=None):
        if self.inner is None:
            return None
        """Retrieve a single item from the inner value."""
        ret = self.inner.get(key, default)
        if ret is None:
            return None
        return LocatedYamlValue(ret, self.yaml_path + [key])

    def __iter__(self):
        """Returns an iterator over the values of this container.

        Note that this function behaves differently from a normal dict for dict values:
        normal dicts will iterate over dictionary keys, while this type of dict will
        iterate over dictionary values.
        """
        return iter(self.values())

    def as_string(self):
        """Returns the inner value, failing if it's not a string."""
        if not isinstance(self.inner, str):
            raise TypeError('as_string(): expect inner value to be a string, got a %s: %r' %
                            (type(self.inner), self.inner))
        return self.inner
