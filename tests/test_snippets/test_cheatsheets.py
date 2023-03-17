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

        for level in yaml:
            level_number = int(level)
            if level_number > hedy.HEDY_MAX_LEVEL:
                print('content above max level!')
            else:
                try:
                    # commands.k.demo_code
                    for k, command in enumerate(yaml[level]):
                        command_text_short = \
                            command['name'] if 'name' in command.keys()\
                            else command['explanation'][0:10]

                        snippet = Snippet(
                            filename=file,
                            level=level,
                            field_name='command ' +
                            command_text_short +
                            ' demo_code',
                            code=command['demo_code'])
                        Hedy_snippets.append(snippet)
                except BaseException:
                    print(f'Problem reading commands yaml for {lang} level {level}')

    return Hedy_snippets


Hedy_snippets = [(s.name, s) for s in collect_snippets(
    path='../../content/cheatsheets')]
Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)

lang = None
# lang = 'en' #useful if you want to test just 1 language

if lang:
    Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.language[:2] == lang]

# This allows filtering out languages locally, but will throw an error
# on GitHub Actions (or other CI system) so nobody accidentally commits this.
if os.getenv('CI') and (lang):
    raise RuntimeError('Whoops, it looks like you left a snippet filter in!')


class TestsCheatsheetPrograms(HedyTester):

    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_cheatsheets_programs(self, name, snippet):
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
