def calc_index(input_string, line, column):
    """"returns the index of char at (line, column) from input_string"""
    # lark starts counting line and column from 1
    current_line = 1
    current_index = column - 1

    for char in input_string:
        if char == '\n':
            current_line += 1

        current_index += 1

        if current_line == line:
            break

    return current_index


def insert(input_string, index, new_string):
    """"insert new_string at input_string[index]"""
    return input_string[:index + 1] + new_string + input_string[index + 1:]


def delete(input_string, index, length):
    """"delete length chars from input_string[index]"""
    return input_string[:index + 1] + input_string[index + 1 + length:]


def replace(input_string, index, length, new_string):
    """"replace at input_string[index] length chars with new_string"""
    result = delete(input_string, index, length)
    result = insert(result, index, new_string)

    return result


def remove_leading_spaces(input_string):
    # the only repair we can do now is remove leading spaces, more can be added!
    return '\n'.join([x.lstrip() for x in input_string.split('\n')])
