import json
import os


# TODO:
# teacher content/answers
# schildpadje in de uitvoer zetten ipv regels

templates = {
    'text': '''**{icon} Vraag**: {question} <br>
{note}
{lines} <br>
''',
    'output': '''**{icon} Vraag**: Wat is de uitvoer van deze code? <br>
Code:									                        Uitvoer:
```hedy
{textfields}							
```
''',

    'define': '''**{icon} Vraag**: {question}
Antwoord: ____________________________________________________________________________________________________<br>
''',

    'MC': '''**{icon} Vraag**: {question}
Antwoord: {options}
''',

    'MC-code': '''**{icon} Vraag**: {question}
```hedy
{code}							
```
Antwoord: {options}
''',
    'input': '''**{icon} Vraag**: Welke code hoort bij deze uitvoer? <br>
Code:									                        Uitvoer:
```hedy
{textfields}							
```
''',
    'element selection': '''**{icon} Opdracht**: {question}									
```hedy
{code}							
```
''',
}


line = '____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>\n'


def convert_json(json):
    assignment_type = json['assignment']
    template = templates[assignment_type]

    if 'lines' in json.keys():
        number_of_lines = json['lines']

        numbered = 'numbered' in json.keys()
        if numbered:
            # replace the number of lines with actual lines
            json['lines'] = ''.join([str(x) + '. ' + line for x in range(1, number_of_lines+1)])
        else:
            # replace the number of lines with actual lines
            json['lines'] = line * number_of_lines

    if 'note' in json.keys():
        json['note'] += '<br>'  # add a newline if we have a note
    else:
        json['note'] = ''

    if assignment_type == 'output':
        textfields = ''
        turtle = 'type' in json.keys() and json['type'] == 'turtle'
        code_lines = json['code'].split('\n')
        number_of_input_lines = len(code_lines)
        number_of_output_lines = number_of_lines

        for i in range(max(number_of_input_lines, number_of_output_lines)):
            output_line = ''
            if i < number_of_input_lines:
                output_line = code_lines[i]
                output_line = output_line.ljust(50, ' ')
            if i < number_of_output_lines and not turtle:
                if i == 0 and turtle:
                    output_line += '🐢'
                output_line = output_line.ljust(76, '_')

            textfields += output_line + '\n'

        json['textfields'] = textfields

        # # todo: add more empty lines if we need more (not an issue till we get to loops)

    if assignment_type == 'input':
        textfields = ''
        number_of_input_lines = len(json['answer'].split('\n'))+1
        output_lines = json['output'].split('\n')
        number_of_output_lines = len(output_lines)

        for i in range(max(number_of_input_lines, number_of_output_lines)-1):
            newline = ''
            if i < number_of_input_lines:
                newline += '_' * 40

            if i < number_of_output_lines:
                output_line = output_lines[i]
                newline += ' ' * 10 + output_line

            textfields += newline + '\n'

        json['textfields'] = textfields

    if 'options' in json.keys():
        all = json['options']
        json['options'] = '<br> 〇 ' + '<br> 〇 '.join(all)

    return template.format(**json)


def process_workbook(lesson, current_directory):
    file_path = f"/lesson{lesson}/les{lesson}a.md"
    workbook_output = ''
    json_found = ''
    inside_json = False

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Strip leading and trailing whitespace

                if not line.startswith('{'):
                    if inside_json:
                        json_found += line  # Add line to the buffer
                    else:
                        # this is not JSON, but markdown, just output
                        workbook_output += line + '\n'

                # Start of a JSON object
                else:
                    inside_json = True
                    json_found = line  # Start buffering JSON content

                # End of JSON
                if line.endswith('}'):
                    inside_json = False
                    # Try to parse the buffered content as JSON
                    try:
                        json_part = json.loads(json_found)
                        workbook_output += convert_json(json_part)
                        # print(workbook_output)
                        f = open(current_directory + 'tester.md', "w")
                        f.write(workbook_output)
                        f.close()

                    except json.JSONDecodeError as E:
                        # Skip the buffer if it's not valid JSON
                        print(E)
                        print(json_part)
                    finally:
                        json_found = ""  # Reset buffer after attempting to parse

    except FileNotFoundError:
        print(f"File {file_path} not found.")

    return workbook_output


