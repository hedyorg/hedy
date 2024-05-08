import csv
import json
import hedy
from tests.Tester import Snippet

most_recent_file_name = 'tools/botswana-programs.json'
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


level = get_column_number_by_name('level')
code_id = get_column_number_by_name('code')
experiment_language = get_column_number_by_name('Botswana_language')
error_id = get_column_number_by_name('server_error')
language = get_column_number_by_name('lang')
adventure_name = get_column_number_by_name('name')
username = get_column_number_by_name('username')

for p in public_programs['rows']:
    s = Snippet(filename='file',
                level=p[level],
                field_name=None,
                code=p[code_id],
                username=p[username],
                language=p[language],
                # storing the classname in adventurename so I don't have to add one more field
                adventure_name=p[adventure_name],
                experiment_language=p[experiment_language],
                error=p[error_id]
                )
    snippets.append(s)

with open('analysis.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['program_id', 'username', 'language', 'experiment_language', 'class', 'number of lines',
                    'number of variables', 'number of commands', 'number of distinct commands', 'level', 'error_message'])


program_id = 0

for snippet in snippets:
    program_id += 1
    if not snippet.error:
        try:

            all_commands = hedy.all_commands(snippet.code, snippet.level, snippet.language)
            try:
                all_variables = hedy.all_variables(snippet.code, snippet.level, snippet.language)
            except:
                all_variables = []

            lines = len(snippet.code.split('\n'))

            with open('analysis.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([program_id, snippet.username, snippet.language, snippet.experiment_language, snippet.adventure_name, lines, len(
                    all_variables), len(all_commands), len(set(all_commands)), snippet.level, ''])

            print(program_id, len(snippets), round(100 * program_id / len(snippets), 2))

        except Exception as E:
            with open('analysis.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [program_id, snippet.username, snippet.language, snippet.experiment_language,
                     snippet.adventure_name,
                     0, 0, 0, 0, snippet.level, str(E)])
    else:
        with open('analysis.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [program_id, snippet.username, snippet.language, snippet.experiment_language, snippet.adventure_name,
                 0, 0, 0, 0, snippet.level, snippet.error])
