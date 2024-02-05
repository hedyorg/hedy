import os
from app import translate_error, app
from flask_babel import force_locale
import exceptions

from parameterized import parameterized

import hedy
from tests.Tester import HedyTester, Snippet
from website.yaml_file import YamlFile

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))


def collect_snippets(path):
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


Hedy_snippets = [(s.name, s) for s in collect_snippets(
    path='../../content/slides')]
Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)

lang = None
# lang = 'zh_hans' #useful if you want to test just 1 language

if lang:
    Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.language[:2] == lang]

# # level = 5
# if level:
#     Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.level == level]

# This allows filtering out languages locally, but will throw an error
# on GitHub Actions (or other CI system) so nobody accidentally commits this.
if os.getenv('CI') and (lang):
    raise RuntimeError('Whoops, it looks like you left a snippet filter in!')


class TestsSlidesPrograms(HedyTester):

    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_slide_programs(self, name, snippet):
        if snippet is not None and len(snippet.code) > 0:
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
                        print(f'in language {snippet.language} from level {snippet.level} gives error:')
                        print(f'{error_message} at line {location}')
                        raise E
