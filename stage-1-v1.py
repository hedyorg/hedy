from lark import Lark

l = Lark('''start: "print " text -> print
                 | "ask " text -> ask
            
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


def transpile(tree):

    if tree.data == 'print':
        command = 'print'
    elif tree.data == 'ask':
        command = 'input'
    else:
        raise Exception('First word is not a command')

    parameter = flatten_test(tree.children[0])
    return command + '("' + parameter + '")'

tree = l.parse("as felienne 123")

python = transpile(tree)
print(python)

exec(python)

# f = open('output.py', 'w+')
# f.write(python)
# f.close()





