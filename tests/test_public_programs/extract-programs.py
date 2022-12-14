import json

# This file is used to extract all programs only from the public programs log file (in DynamoDB)
# The log file itself is not in the repo since it also contains dates & usernames
# Felienne will periodically update the filtered file for testing purposes

date = '2022-12-01'

with open(f'public-programs-{date}.json', 'r') as public_programs:
    text = public_programs.read()
    all_programs = json.loads(text)
    new_programs = []

for program in all_programs:
    try:
        error = program['error']['BOOL']
    except Exception:
        error = True
    new_program = {
        'code': program['code']['S'],
        'level': program['level']['N'],
        'error': error,
        'language': program['lang']['S']
    }
    new_programs.append(new_program)

with open(f'filtered-programs-{date}.json', 'w') as public_programs:
    save_text = json.dumps(new_programs)
    public_programs.write(save_text)
