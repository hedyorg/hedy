from lark import Lark
from lark import Tree, Transformer

class AllCommands(Transformer):
    #creates a list of all commands in a tree for further processing
    # it removes command and program nodes
    def program(self, args):
        commands = []
        for c in args:
                commands.append(c)
        return commands
    def command(self, args):
        return args
    def text(self, args):
        return Tree('text', ''.join([str(c) for c in args]))
    def var(self, args):
        return Tree('var', ''.join([str(c) for c in args]))
    def punctuation(self, args):
        return Tree('punctuation', ''.join([str(c) for c in args]))

class FlattenText(Transformer):
    #flattens arguments of text, var and punctuation for more easy debugging
    def text(self, args):
            return Tree('text', ''.join([str(c) for c in args]))
    def var(self, args):
            return Tree('var', ''.join([str(c) for c in args]))
    def punctuation(self, args):
            return Tree('punctuation', ''.join([str(c) for c in args]))
    def index(self, args):
            return ''.join([str(c) for c in args])

class AllCommandsAssignments(FlattenText):
    #returns only assignments
    #todo could be made simpler by transforming assogns directly
    def program(self, args):
        if len(args) != 1:
            assign_args = [a for a in args if a.data == 'assign' or a.data == 'assign_list']
            if assign_args == []:
                return []
            else:
                return [[a.children for a in assign_args[0].children]]

def all_commands(tree):
    commands = AllCommands().transform(tree)
    return commands

def all_assignments(tree):
    assignments = AllCommandsAssignments().transform(tree)
    variables = {}
    if assignments is not None:
        for a in assignments:
            variables[a[0]] = a[1]

    return variables #leeg dus als er geen assignments gevonden zijn

def create_parser(level):
    with open("grammars/level" + str(level) + ".txt", "r") as file:
        grammar = file.read()
    return Lark(grammar)

def flatten_test(tree):
    if tree.data == 'text':
        return ''.join([str(c) for c in tree.children])
    else:
        raise Exception('Attemping to print or ask non-text element')

class ConvertToPython_1(Transformer):
    def __init__(self, punctuation_symbols, lookup):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup

    def program(self, args):
        return '\n'.join([str(c) for c in args])
    def command(self, args):
        return args
    def text(self, args):
        return ''.join([str(c) for c in args])
    def print(self, args):
        return "print('" + args[0] + "')"
    def echo(self, args):
        all_parameters = ["'" + a + "'" for a in args]
        return "print(" + '+'.join(all_parameters) + " + answer)"
    def ask(self, args):
        all_parameters = ["'" + a + "'" for a in args]
        return 'answer = input(' + '+'.join(all_parameters) + ")"
    def punctuation(self, args):
        return ''.join([str(c) for c in args])

class ConvertToPython_2(ConvertToPython_1):
    def print(self, args):
        all_arguments_converted = []
        i = 0
        for argument in args:
            if i == len(args)-1 or args[i+1] in self.punctuation_symbols:
                space = ''
            else:
                space = "+' '"
            if argument in self.lookup:
                all_arguments_converted.append(argument + space)
            else:
                all_arguments_converted.append("'" + argument + "'" + space)
            i = i + 1
        return 'print(' + '+'.join(all_arguments_converted) + ')'
    def assign(self, args):
        parameter = args[0]
        value = args[1]
        return parameter + " = '" + value + "'"

class ConvertToPython_3(ConvertToPython_2):
    def text(self, args):
        return ''.join([str(c) for c in args])
    def var(self, args):
        return ''.join([str(c) for c in args])
    def print(self, args):
        #opzoeken is nu niet meer nodig
        return "print(" + '+'.join(args) + ')'
    def list_access(self, args):
        if args[1].data == 'random':
            return 'random.choice(' + args[0] + ')'
        else:
            return args[0] + '[' + args[1].children[0] + ']'

    def assign_list(self, args):
        parameter = args[0]
        values = ["'" + a + "'" for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"


def transpile(input_string, level):
    punctuation_symbols = ['!', '?', '.']
    level = int(level)
    parser = create_parser(level)
    program_root = parser.parse(input_string).children[0] #getting rid of the root could also be done in the transformer would be nicer
    lookup_table = all_assignments(program_root)
    flattened_tree = FlattenText().transform(program_root)
    if level == 1:
        python = ConvertToPython_1(punctuation_symbols, lookup_table).transform(program_root)
    elif level == 2:
        python = ConvertToPython_2(punctuation_symbols, lookup_table).transform(program_root)
    elif level == 3:
        python = 'import random\n'
        python += ConvertToPython_3(punctuation_symbols, lookup_table).transform(program_root)
    return python

def execute(input_string):
    python = transpile(input_string)
    exec(python)


# f = open('output.py', 'w+')
# f.write(python)
# f.close()





