def insert(input_string, line, column, new_string):
    """"insert new_string before (line, column)"""
    rows = input_string.splitlines()
    rows[line] = rows[line][:column] + new_string + rows[line][column:]

    return '\n'.join(rows)


def delete(input_string, line, column, length):
    """"delete length chars starting at (line, column)"""
    rows = input_string.splitlines()
    rows[line] = rows[line][:column] + rows[line][column + length:]

    return '\n'.join(rows)


def replace(input_string, line, column, length, new_string):
    """"replace at (line, column) length chars with new_string"""
    result = delete(input_string, line, column, length)
    result = insert(result, line, column, new_string)

    return result


def remove_leading_spaces(input_string):
    return '\n'.join([x.lstrip() for x in input_string.split('\n')])


def remove_unexpected_char(input_string, line, column):
    return delete(input_string, line, column, 1)


# TODO: check if the user tried to print a variable
def add_missing_quote(input_string, line, column, length):
    if input_string.splitlines()[line][column] == '\'':
        # add quote at the end
        return insert(input_string, line, column + length, '\'')
    else:
        # add quote at the beginning
        return insert(input_string, line, column, '\'')


def define_var_low_level(input_string, variable):
    # put "variable is Hello" at the beginning
    return insert(input_string, 0, 0, variable + ' is Hello\n')


def define_var_high_level(input_string, variable):
    # put "variable is 'Hello'" at the beginning
    return insert(input_string, 0, 0, variable + ' is \'Hello\'\n')


def fix_indent(input_string, line, leading_spaces, indent_size):
    if leading_spaces < indent_size:
        # not enough spaces
        return insert(input_string, line, 0, ' ' * (indent_size - leading_spaces))
    else:
        # too many spaces
        return delete(input_string, line, 0, leading_spaces - indent_size)
