import hedy


def insert(line, column, new_string):
    """"insert new_string at column from line"""
    result = line[:column - 1] + new_string + line[column - 1:]

    return result


def delete(line, column, length):
    """"delete length chars starting at column from line"""
    result = line[:column - 1] + line[column - 1 + length:]

    return result


def replace(line, column, length, new_string):
    """"replace at column length chars with new_string"""
    result = delete(line, column, length)
    result = insert(line, column, new_string)

    return result


def make_mutants(input_string, row):
    mutants = []
    mutated_lines = []
    lines = input_string.splitlines()
    line = lines[row - 1]
    # +2 because we start counting from 1, and we are adding a character
    length = len(line) + 2
    for i in range(1, length):  # make mutant lines
        mutated_lines.append(insert(line, i, '\''))
    for mutated_line in mutated_lines:  # replace the line with mutated lines
        lines[row - 1] = mutated_line
        mutants.append('\n'.join(lines))
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


def remove_char(input_string, row, column):
    lines = input_string.splitlines()
    line = lines[row - 1]
    lines[row - 1] = delete(line, column, 1)

    return '\n'.join(lines)


def fix_indent(input_string, row, leading_spaces, indent_size):
    lines = input_string.splitlines()
    line = lines[row - 1]
    if leading_spaces < indent_size:
        # not enough spaces, add spaces
        lines[row - 1] = insert(line, 1, ' ' * (indent_size - leading_spaces))
        return '\n'.join(lines)
    else:
        # too many spaces, remove spaces
        lines[row - 1] = delete(line, 1, leading_spaces - indent_size)
        return '\n'.join(lines)


