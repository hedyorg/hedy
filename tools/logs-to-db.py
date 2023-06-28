import json
import sqlite3
import os

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()
columns = ['session', 'date', 'lang', 'level', 'code', 'server_error',
           'exception', 'version', 'username', 'adventurename', 'read_aloud']
value_string = ','.join('?' * len(columns))

cursor.execute('DROP TABLE if exists Logs;')
cursor.execute('Create Table Logs '
               '(session Text, '
               'date datetime, '
               'lang Text, '
               'level TinyINT, '
               'code LONGTEXT, '
               'server_error Text, '
               'exception Text,'
               'version Text,'
               'username Text,'
               'adventurename Text,'
               'read_aloud Bool'
               ')')

defaults = {'lang': 'en', 'server_error': None, 'exception': None,
            'username': None, 'adventurename': None, 'read_aloud': None}


def add_defaults(x):
    keys = []
    for c in columns:
        try:
            keys.append(json_dict[c])
        except KeyError:  # no value? grap the default for this column
            keys.append(defaults[c])

    return keys


directory = 'aws-logs'

files = []
for root, d_names, f_names in os.walk(directory):
    for f in f_names:
        extension = os.path.splitext(f)[1]
        if extension == '.jsonl':
            files.append(os.path.join(root, f))

i = 0
for filename in files:
    # checking if it is a file

    i += 1
    if i % 10000 == 0:
        print(f'{round(i / len(files) * 100, 2)}% complete')

    with open(filename, 'r') as file:
        contents = file.readlines()  # a file with one or more lines of json

        for json_line in contents:
            try:
                json_dict = json.loads(json_line)
            except json.decoder.JSONDecodeError:
                pass  # skip for now!

            keys = tuple(add_defaults(json_dict))

            try:
                cursor.execute(f'insert into Logs values({value_string})', keys)
            except UnicodeEncodeError:
                print(f'{json_dict["session"]} data not inserted!!')


connection.commit()
connection.close()
