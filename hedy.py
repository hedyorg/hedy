from lark import Lark

def create_parser_level_1():
    #note that the order matters here, so print is tried first, then ask, then text (error)
    return Lark('''start: "print " text -> print
                      | "ask " text -> ask
                      |  text " " text -> invalid

                text: (LETTER | DIGIT | WS_INLINE)+

                %import common.LETTER   // imports from terminal library
                %import common.DIGIT   // imports from terminal library
                %import common.WS_INLINE   // imports from terminal library
             ''')

def flatten_test(tree):
    if tree.data == 'text':
        return ''.join([str(c) for c in tree.children])
    else:
        raise Exception('Attemping to print or ask non-text element')


def transpile(input_string):
    parser_level_1 = create_parser_level_1()
    tree = parser_level_1.parse(input_string)
    if tree.data == 'print':
        command = 'print'
    elif tree.data == 'ask':
        command = 'input'
    else:
        raise Exception('First word is not a command')

    parameter = flatten_test(tree.children[0])
    return command + "('" + parameter + "')"

def execute(input_string):
    python = transpile(input_string)
    exec(python)


# f = open('output.py', 'w+')
# f.write(python)
# f.close()





