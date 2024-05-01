import json
import hedy
from tests.Tester import HedyTester, Snippet

most_recent_file_name = 'tools/alpha-logs.json'
snippets = []

# this file analyzes logs from the database
# logs are saved in 'tools/alpha-logs.json' and extracted from the database
# by running: select * from logs


with open(most_recent_file_name, 'r') as public_programs_file:
    text = public_programs_file.read()
    public_programs = json.loads(text)


def get_column_number_by_name(name):
    columns = public_programs['columns']
    level_row = [x for x in columns if x['displayName'] == name][0]
    return columns.index(level_row)


level_id = get_column_number_by_name('level')
code_id = get_column_number_by_name('code')
language_id = get_column_number_by_name('lang')
error_id = get_column_number_by_name('server_error')

for p in public_programs['rows']:
    s = Snippet(filename='file',
                level=p[level_id],
                field_name=None,
                code=p[code_id],
                language=p[language_id],
                error=p[error_id]
                )
    snippets.append(s)

for snippet in snippets:

    if snippet is not None and len(snippet.code) > 0 and len(snippet.code) < 100 and not snippet.error:
        try:

            all_commands = hedy.all_commands(snippet.code, snippet.level, snippet.language)
            all_variables = hedy.all_variables(snippet.code, snippet.level, snippet.language)
            print(snippet.language, all_commands)
            print(snippet.language, all_variables)

        except Exception as E:
            print(E)
