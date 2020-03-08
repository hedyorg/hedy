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
    def program(self, args):
        flattened_args = []
        for a in args:
            if type(a) == list:
                for x in a:
                    flattened_args.append(x)
            else:
                flattened_args.append(a)
        return flattened_args
    def print(self, args):
        return args
    def command(self, args):
        return args
    def assign(self, args):
        return args[0].children
    def assign_list(self, args):
        return args[0].children
    def list_access(self, args):
        if type(args[1]) == Tree:
            return 'random.choice(' + args[0].children + ')'
        else:
            return args[0].children + '[' + args[1] + ']'

def all_commands(tree):
    commands = AllCommands().transform(tree)
    return commands

def all_assignments(tree):
    flat = FlattenText().transform(tree)
    assignments = AllCommandsAssignments().transform(tree)
    return assignments #leeg dus als er geen assignments gevonden zijn

def create_parser(level):
    with open("grammars/level" + str(level) + ".txt", "r") as file:
        grammar = file.read()
    return Lark(grammar)

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
    def var(self, args):
        return ''.join([str(c) for c in args])
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
    def list_access(self, args):
        if args[1].data == 'random':
            return 'random.choice(' + args[0] + ')'
        else:
            return args[0] + '[' + args[1].children[0] + ']'
    def assign_list(self, args):
        parameter = args[0]
        values = ["'" + a + "'" for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

class ConvertToPython_3(ConvertToPython_2):
    def text(self, args):
        return ''.join([str(c) for c in args])
    def print(self, args):
        #opzoeken is nu niet meer nodig
        return "print(" + '+'.join(args) + ')'


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
        python = 'import random\n'
        python += ConvertToPython_2(punctuation_symbols, lookup_table).transform(program_root)
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





