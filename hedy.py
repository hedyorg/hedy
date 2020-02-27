from lark import Lark

def create_parser(level):
    file = open("grammars/level" + str(level) + ".txt", "r")
    grammar = file.read()
    #note that the order matters here, so print is tried first, then ask, then text (error)
    return Lark(grammar)

def flatten_test(tree):
    if tree.data == 'text':
        return ''.join([str(c) for c in tree.children])
    else:
        raise Exception('Attemping to print or ask non-text element')


def transpile(input_string, level):
    return transpile_command(input_string, level)

def transpile_command(input_string, level):
    parser_level_1 = create_parser(level)
    tree = parser_level_1.parse(input_string)

    if tree.data == 'print':
        command = 'print'
        parameter = str(flatten_test(tree.children[0]))
        return command + "('" + parameter + "')"
    elif tree.data == 'echo':
        command = 'print(answer)'
        return command
    elif tree.data == 'ask':
        parameter = str(flatten_test(tree.children[0]))
        command = 'answer = input'
        return command + "('" + parameter + "')"
    else:
        raise Exception('First word is not a command')

    parameter = str(flatten_test(tree.children[0]))
    return command + "('" + parameter + "')"

def execute(input_string):
    python = transpile(input_string)
    exec(python)


# f = open('output.py', 'w+')
# f.write(python)
# f.close()





