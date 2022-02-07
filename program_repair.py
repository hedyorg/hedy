fixed_code = None
mutants_made = False
import hedy

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
    mutants = []
    length = len(input_string.splitlines()[line - 1]) + 2
    for i in range(1, length):
        mutants.append(insert(input_string, line, i, '\''))
    return mutants


def mutation_repair(input_string, line, level, lang):
    mutants = make_mutants(input_string, line)
    while mutants:
        mutant = mutants.pop(0)
        try:
            program_root = hedy.parse_input(mutant, level, lang)
            hedy.is_program_valid(program_root, input_string, level, lang)
            # TODO Dolfein: here we would like to do a few further (focused!!) checks like
            # checking whether it does not result in another error (such as undefined variable), but not a full
            # transpile because that leads to potential recursion and is expensive

            return mutant
        except hedy.exceptions.HedyException as E:
            # current mutant contains (another) error, pass and try next
            pass

    return None # no mutants found that compile

def remove_leading_spaces(input_string):
    return '\n'.join([x.lstrip() for x in input_string.split('\n')])


def remove_char(input_string, line, column):
    return delete(input_string, line, column, 1)


def fix_indent(input_string, line, leading_spaces, indent_size):
    if leading_spaces < indent_size:
        # not enough spaces, add spaces
        return insert(input_string, line, 1, ' ' * (indent_size - leading_spaces))
    else:
        # too many spaces, remove spaces
        return delete(input_string, line, 1, leading_spaces - indent_size)


