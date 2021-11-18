def calc_index(input_string, row):
    current_row = 0
    current_index = 0

    while current_row != row:
        for char in input_string:
            current_index += 1

            if char == '\n':
                current_row += 1

    return current_index

# TODO: turn row and column parameters into one parameter index for insert, delete and replace


def insert(input_string, row, column, new_string):
    """"insert new_string at position (row, column) of input_string"""
    start_row = calc_index(input_string, row)

    return input_string[:start_row + column] + new_string + input_string[start_row + column:]


def delete(input_string, row, column, length):
    """"delete length chars at (row, column)"""
    start_row = calc_index(input_string, row)

    return input_string[:start_row + column] + input_string[start_row + column + length:]


def replace(input_string, row, column, length, new_string):
    """"replace at (row, column) length chars with new_string"""
    result = delete(input_string, row, column, length)
    result = insert(result, row, column, new_string)

    return result


# 1 Invalid: "{invalid_command} is not a Hedy level {level} command. Did you mean {guessed_command}?"
def replace_invalid_command(input_string, row, column, length, new_string):
    return replace(input_string, row, column, length, new_string)


# 2 Invalid Space: "Oops! You started a line with a space on line {line_number}.
#   Spaces confuse computers, can you remove it?"
def remove_leading_spaces(input_string):
    # the only repair we can do now is remove leading spaces, more can be added!
    return '\n'.join([x.lstrip() for x in input_string.split('\n')])


# 3 Parse: "The code you entered is not valid Hedy code.
#   There is a mistake on line {location[0]}, at position {location[1]}.
#   You typed {character_found}, but that is not allowed."
def remove_parse_error(input_string, row, column):
    return delete(input_string, row, column, 1)


# 5 Var Undefined: "You tried to print the variable {name}, but you did not set it.
# It is also possible that you were trying to print the word {name} but forgot quotation marks."
def define_var():
    # make var or add quotation marks?
    return None


# 6 Unexpected Indentation: "You used too many spaces in line {line_number}.
#   You uses {leading_spaces} spaces, which is too much. Start every new block with {indent_size} spaces."
def remove_indent(input_string, row, column, length):
    return delete(input_string, row, column, length)
