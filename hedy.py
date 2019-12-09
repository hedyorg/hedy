from lark import Lark

# de volgorde maakt uit in deze grammatica!
# dat kunnen we exploiten voor deze regels,
# eerst print, dan ask, dan text

# wel weer grappig dat hij bij pr felienne 123 pr felienne als text ziet
# maak ok (kunnen we zelf wel hakken tot de eerste spatie)

# mooi trouwens ook, op zo'n simpele taal kunnen we
# veel makkelijker program repair doen OMG!

l = Lark('''start: "print " text -> print
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
    tree = l.parse(input_string)
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





