mutants = []
fixed_code = None
fixed_result = None
mutants_made = False


def insert(input_string, line, column, new_string):
    """"insert new_string at (line, column)"""
    rows = input_string.splitlines()
    rows[line - 1] = rows[line - 1][:column - 1] + new_string + rows[line - 1][column - 1:]

    return '\n'.join(rows)


def delete(input_string, line, column, length):
    """"delete length chars starting at (line, column)"""
    rows = input_string.splitlines()
    rows[line - 1] = rows[line - 1][:column - 1] + rows[line - 1][column - 1 + length:]

    return '\n'.join(rows)


def replace(input_string, line, column, length, new_string):
    """"replace at (line, column) length chars with new_string"""
    result = delete(input_string, line, column, length)
    result = insert(result, line, column, new_string)

    return result


def make_mutants(input_string, line):
    global mutants_made
    if not mutants_made:  # make list only once
        mutants_made = True
        length = len(input_string.splitlines()[line - 1]) + 2
        print('length', length)
        for i in range(1, length):
            mutants.append(add_quote(input_string, line, i))


def clear_mutants():
    global fixed_code, fixed_result, mutants_made, mutants
    fixed_code = None
    fixed_result = None
    mutants_made = False
    mutants = []


def save_mutant(mutant, mutant_result):
    global fixed_code, fixed_result
    fixed_code = mutant
    fixed_result = mutant_result


def remove_leading_spaces(input_string):
    # the only repair we can do now is remove leading spaces, more can be added!
    return '\n'.join([x.lstrip() for x in input_string.split('\n')])


def remove_unexpected_char(input_string, line, column):
    return delete(input_string, line, column, 1)


def fix_indent(input_string, line, leading_spaces, indent_size):
    if leading_spaces < indent_size:
        # not enough spaces, add spaces
        return insert(input_string, line, 1, ' ' * (indent_size - leading_spaces))
    else:
        # too many spaces, remove spaces
        return delete(input_string, line, 1, leading_spaces - indent_size)


def add_quote(input_string, line, column):
    return insert(input_string, line, column, '\'')
