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
import exceptions
import hedy
import utils
from tests.Tester import HedyTester, Snippet
from website.yaml_file import YamlFile

fix_error = False
# set this to True to revert broken snippets to their en counterpart automatically
# this is useful for large Weblate PRs that need to go through, this fixes broken snippets
if os.getenv('fix_for_weblate') or os.getenv('FIX_FOR_WEBLATE'):
    fix_error = True


check_stories = False


def rootdir():
    """Return the repository root directory."""
    return os.path.join(os.path.dirname(__file__), '..', '..')


def collect_adventures_snippets(path, filtered_language=None):
    Hedy_snippets = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
    for f in files:
        lang = f.split(".")[0]
        # we always store the English snippets, to use them if we need to restore broken code
        if not filtered_language or (filtered_language and (lang == filtered_language or lang == 'en')):
            f = os.path.join(path, f)
            yaml = YamlFile.for_file(f)

            for key, adventure in yaml['adventures'].items():
                # the default tab sometimes contains broken code to make a point to learners about changing syntax.
                if not key == 'default' and not key == 'debugging':
                    for level_number in adventure['levels']:
                        if level_number > hedy.HEDY_MAX_LEVEL:
                            print('content above max level!')
                        else:
                            level = adventure['levels'][level_number]
                            adventure_name = adventure['name']

                            for adventure_part, text in level.items():
                                # This block is markdown, and there can be multiple code blocks inside it
                                codes = [tag.contents[0].contents[0]
                                         for tag in utils.markdown_to_html_tags(text)
                                         if tag.name == 'pre' and tag.contents and tag.contents[0].contents]

                                if check_stories and adventure_part == 'story_text' and codes != []:
                                    # Can be used to catch languages with example codes in the story_text
                                    # at once point in time, this was the default and some languages still use this old
                                    # structure

                                    feedback = f"Example code in story text {lang}, {adventure_name},\
                                    {level_number}, not recommended!"
                                    raise Exception(feedback)

                                for i, code in enumerate(codes):
                                    Hedy_snippets.append(Snippet(
                                        filename=f,
                                        level=level_number,
                                        field_name=adventure_part,
                                        code=code,
                                        adventure_name=adventure_name,
                                        key=key,
                                        counter=1))

    return Hedy_snippets


def collect_cheatsheet_snippets(path):
    Hedy_snippets = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
    for file in files:
        lang = file.split(".")[0]
        file = os.path.join(path, file)
        yaml = YamlFile.for_file(file)

        for level in yaml:
            level_number = int(level)
            if level_number > hedy.HEDY_MAX_LEVEL:
                print('content above max level!')
            else:
                try:
                    # commands.k.demo_code
                    for k, command in enumerate(yaml[level]):
                        snippet = Snippet(
                            filename=file,
                            level=level,
                            field_name=str(k),
                            code=command['demo_code'])
                        Hedy_snippets.append(snippet)
                except BaseException:
                    print(f'Problem reading commands yaml for {lang} level {level}')

    return Hedy_snippets


def collect_parsons_snippets(path):
    Hedy_snippets = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
    for file in files:
        lang = file.split(".")[0]
        file = os.path.join(path, file)
        yaml = YamlFile.for_file(file)
        levels = yaml.get('levels')

        for level, content in levels.items():
            level_number = int(level)
            if level_number > hedy.HEDY_MAX_LEVEL:
                print('content above max level!')
            else:
                try:
                    for exercise_id, exercise in levels[level].items():
                        code = exercise.get('code')
                        snippet = Snippet(
                            filename=file,
                            level=level,
                            field_name=f"{exercise_id}",
                            code=code)
                        Hedy_snippets.append(snippet)
                except BaseException:
                    print(f'Problem reading commands yaml for {lang} level {level}')

    return Hedy_snippets


def collect_slides_snippets(path):
    Hedy_snippets = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
    for file in files:
        lang = file.split(".")[0]
        file = os.path.join(path, file)
        yaml = YamlFile.for_file(file)
        levels = yaml.get('levels')

        for level, content in levels.items():
            level_number = int(level)
            if level_number > hedy.HEDY_MAX_LEVEL:
                print('content above max level!')
            else:
                try:
                    number = 0
                    # commands.k.demo_code
                    for x, y in content.items():
                        if 'code' in y.keys() and 'debug' not in y.keys():
                            snippet = Snippet(
                                filename=file,
                                level=level_number if level_number > 0 else 1,
                                language=lang,
                                field_name=f'snippet {number}',
                                code=y['code'])
                            Hedy_snippets.append(snippet)
                            number += 1
                except BaseException:
                    print(f'Problem reading commands yaml for {lang} level {level}')

    return Hedy_snippets


def filter_snippets(snippets, level=None, lang=None):
    if (lang or level) and os.getenv('CI'):
        raise RuntimeError('Whoops, it looks like you left a snippet filter in!')

    if lang:
        snippets = [(name, snippet) for (name, snippet) in snippets if snippet.language[:2] == lang]

    if level:
        snippets = [(name, snippet) for (name, snippet) in snippets if snippet.level == level]

    return snippets


@dataclass
class YamlLocation:
    dict: dict
    key: str


class HedySnippetTester(HedyTester):
    """Base class for all other snippet testers.

    The logic is the same between all of them, so we can combine it.

    'yaml_locator' is a function that, given a snippet, will tell us where
    in the file it was found, by returning a pair of `(containing_dict,
    """

    def do_snippet(self, snippet, yaml_locator=None):
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

            if fix_error and yaml_locator:
                self.restore_snippet_to_english(snippet, yaml_locator)

                with open(path.join(rootdir(), 'snippet-report.md.txt'), 'a') as f:
                    f.write(error_message + '\n')
                    f.write('This snippet has been reverted to English.\n\n')
            else:
                print(error_message)
                raise E

    def restore_snippet_to_english(self, snippet, yaml_locator):
        # English file is always 'en.yaml' in the same dir
        en_file = path.join(path.dirname(snippet.filename), 'en.yaml')

        # Read English yaml file
        original_yaml = YamlFile.for_file(en_file)
        original_loc = yaml_locator(snippet, original_yaml)

        # Read broken yaml file
        broken_yaml = utils.load_yaml_rt(snippet.filename)
        broken_loc = yaml_locator(snippet, broken_yaml)

        # Restore to English version
        broken_loc.dict[broken_loc.key] = original_loc.dict[original_loc.key]
        with open(snippet.filename, 'w') as file:
            file.write(utils.dump_yaml_rt(broken_yaml))
