import json
import hedy
from tests.Tester import HedyTester, Snippet
from parameterized import parameterized
from app import app
from hedy_error import get_error_text
from flask_babel import force_locale
import exceptions

most_recent_file_name = 'tests/test_public_programs/filtered-programs-2023-12-12.json'
public_snippets = []

# this file tests all public programs in the database
# while saving, they were not broken (no Parse error or other Hedy exception)
# these tests make sure we aren't accidentally breaking public programs

with open(most_recent_file_name, 'r') as public_programs_file:
    text = public_programs_file.read()
    public_programs = json.loads(text)

for p in public_programs:
    s = Snippet(filename='file',
                level=int(p['level']),
                field_name=None,
                code=p['code'],
                language=p['language'],
                error=p['error']
                )
    public_snippets.append(s)

p2 = [(s.name, s) for s in public_snippets]

passed_snippets = []


class TestsPublicPrograms(HedyTester):
    @parameterized.expand(p2)
    def test_programs(self, name, snippet):
        # test correct programs
        if snippet is not None and len(snippet.code) > 0 and len(snippet.code) < 100 and snippet.error:
            try:
                self.single_level_tester(
                    code=snippet.code,
                    level=int(snippet.level),
                    lang=snippet.language,
                    translate=False,
                    skip_faulty=False
                )

                # useful code if you want to test what erroneous snippets are now passing
                # passed_snippets.append(str(snippet.level) + '\n' + snippet.code + '\n--------\n')
                # try:
                #     with open('output.txt', 'w') as f:
                #         f.writelines(passed_snippets)
                # except Exception as e:
                #     pass

            except OSError:
                return None  # programs with ask cannot be tested with output :(
            except hedy.exceptions.ParseException as PE:
                # TODO: Can we use 'self.output_test_error' here?

                try:
                    location = PE.error_location
                except BaseException:
                    location = 'No Location Found'

                # Must run this in the context of the Flask app, because FlaskBabel requires that.
                with app.app_context():
                    with force_locale('en'):
                        error_message = get_error_text(PE, 'en')
                        error_message = error_message.replace('<span class="command-highlighted">', '`')
                        error_message = error_message.replace('</span>', '`')
                        print(f'\n----\n{snippet.code}\n----')
                        print(f'in language {snippet.language} from level {snippet.level} gives error:')
                        print(f'{error_message} at line {location}')
                        raise PE
            except exceptions.HedyException:
                pass  # we only care about parse errors
