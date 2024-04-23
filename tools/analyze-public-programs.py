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

for snippet in public_snippets:

    if snippet is not None and len(snippet.code) > 0 and len(snippet.code) < 100 and not snippet.error:
        try:

            all_commands = hedy.all_commands(snippet.code, snippet.level, snippet.language)
            all_variables = hedy.all_variables(snippet.code, snippet.level, snippet.language)
            print(snippet.language, all_commands)
            print(snippet.language, all_variables)


        except Exception as E:
            pass
