import os
from app import translate_error, app
from flask_babel import force_locale

from parameterized import parameterized

import exceptions
import hedy
import utils
from tests.Tester import HedyTester, Snippet
from website.yaml_file import YamlFile

fix_error = False
# set this to True to revert broken snippets to their en counterpart automatically
# this is useful for large Weblate PRs that need to go through, this fixes broken snippets
if os.getenv('fix_for_weblate'):
    fix_error = True

check_stories = False

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

filtered_language = None
level = None


def collect_snippets(path, filtered_language=None):
    Hedy_snippets = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
    for f in files:
        lang = f.split(".")[0]
        # we always grab the en snippets to restore broken code
        if not filtered_language or (filtered_language and (lang == filtered_language or lang == 'en')):
            f = os.path.join(path, f)
            yaml = YamlFile.for_file(f)

            for key, adventure in yaml['adventures'].items():
                # the default tab sometimes contains broken code to make a point to learners about changing syntax.
                if not key == 'default':
                    for level_number in adventure['levels']:
                        if level_number > hedy.HEDY_MAX_LEVEL:
                            print('content above max level!')
                        else:
                            level = adventure['levels'][level_number]
                            adventure_name = adventure['name']

                            for adventure_part, text in level.items():
                                is_markdown = adventure_part != 'start_code'

                                if is_markdown:
                                    # If we have Markdown, there can be multiple code blocks inside it
                                    codes = [tag.contents[0].contents[0]
                                             for tag in utils.markdown_to_html_tags(text)
                                             if tag.name == 'pre' and tag.contents and tag.contents[0].contents]
                                else:
                                    # If we don't have Markdown (this happensin the start_code field)
                                    # the entire field is a single code block
                                    codes = [text]

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


# filtered_language = 'tr'
# use this to filter on 1 lang, zh_Hans for Chinese, nb_NO for Norwegian, pt_PT for Portuguese


Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../content/adventures',
                                                       filtered_language=filtered_language)]

# level = 6
# if level:
#     Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.level == level]

# This allows filtering out languages locally, but will throw an error
# on GitHub Actions (or other CI system) so nobody accidentally commits this.
if os.getenv('CI') and (filtered_language or level):
    raise RuntimeError('Whoops, it looks like you left a snippet filter in!')

Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)


class TestsAdventurePrograms(HedyTester):

    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_adventures(self, name, snippet):
        if snippet is not None and len(snippet.code) > 0:
            try:
                self.single_level_tester(
                    code=snippet.code,
                    level=int(snippet.level),
                    lang=snippet.language,
                    translate=False
                )

            except hedy.exceptions.CodePlaceholdersPresentException:  # Code with blanks is allowed
                pass
            except OSError:
                return None  # programs with ask cannot be tested with output :(
            except exceptions.HedyException as E:
                if fix_error:
                    # Read English yaml file
                    original_yaml = YamlFile.for_file('../../content/adventures/en.yaml')
                    original_text_part_1 = original_yaml['adventures'][snippet.key]['levels']
                    original_text = original_text_part_1[snippet.level][snippet.field_name]

                    # Read broken yaml file
                    broken_yaml = utils.load_yaml_rt(snippet.filename)
                    broken_yaml['adventures'][snippet.key]['levels'][snippet.level][snippet.field_name] = \
                        original_text

                    with open(snippet.filename, 'w') as file:
                        file.write(utils.dump_yaml_rt(broken_yaml))

                else:
                    try:
                        location = E.error_location
                    except BaseException:
                        location = 'No Location Found'

                    # Must run this in the context of the Flask app, because FlaskBabel requires that.
                    with app.app_context():
                        with force_locale('en'):
                            error_message = translate_error(E.error_code, E.arguments, 'en')
                            error_message = error_message.replace('<span class="command-highlighted">', '`')
                            error_message = error_message.replace('</span>', '`')
                            print(f'\n----\n{snippet.code}\n----')
                            print(f'from adventure {snippet.adventure_name}')
                            print(f'in language {snippet.language} from level {snippet.level} gives error:')
                            print(f'{error_message} at line {location}')
                            raise E
