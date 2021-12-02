def insert(input_string, line, column, new_string):
    """"insert new_string at (line, column)"""
    rows = input_string.splitlines()
    rows[line] = rows[line][:column + 1] + new_string + rows[line][column + 1:]

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
    # the only repair we can do now is remove leading spaces, more can be added!
    return '\n'.join([x.lstrip() for x in input_string.split('\n')])
