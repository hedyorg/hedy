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

class FlattenText(Transformer):
    #flattens arguments of code for more easy debugging
    def text(self, args):
            return ''.join([str(c) for c in args])

class AllCommandsAssignments(Transformer):
    #returns only assignments
    def program(self, args):
        if len(args) == 1:
            #alleen assignments teruggeven (de rest bottom up 'opeten' en dan in de twee tak samenvoegen'
            assign_child = args[0].children[0]
            if assign_child.data == 'assign':
                return [assign_child.children[0], assign_child.children[1]]
        else:
            list_of_not_none_arguments = []
            if not args[0] is None:
                list_of_not_none_arguments.append(args[0])
            if not args[2] is None:
                list_of_not_none_arguments.append(args[2][0])
            return [(a.children[0]).children for a in list_of_not_none_arguments if a.children[0].data == 'assign']

def all_commands(tree):
    flattened_tree = FlattenText().transform(tree)
    commands = AllCommands().transform(flattened_tree)
    commands = [x for [x] in commands]
    return commands

def all_assignments(tree):
    flattened_tree = FlattenText().transform(tree)
    assignments = AllCommandsAssignments().transform(flattened_tree)
    variables = {}
    if assignments is not None:
        for a in assignments:
            variables[a[0]] = a[1]

    return variables #leeg dus als er geen assignments gevonden zijn



def create_parser(level):
    #note that the order matters here, so print is tried first, then ask, then text (error)

    with open("grammars/level" + str(level) + ".txt", "r") as file:
        grammar = file.read()

    return Lark(grammar)


def flatten_test(tree):
    if tree.data == 'text':
        return ''.join([str(c) for c in tree.children])
    else:
        raise Exception('Attemping to print or ask non-text element')


def transpile(input_string, level):
    level = int(level)
    parser = create_parser(level)
    program_root = parser.parse(input_string).children[0] #getting rid of the root could also be done in the transformer would be nicer
    python = ''
    if level == 1:
        commands = all_commands(program_root)
        python_lines = [transpile_command(c, level) for c in commands]
        return '\n'.join(python_lines)
    elif level == 2:
        lookup = all_assignments(program_root)
        global table
        table = lookup
        commands = all_commands(program_root)
        python_lines = [transpile_command(c, level) for c in commands]
        return '\n'.join(python_lines)

# deze transpile moet natuurlijk ook een transformer worden
# op een dag :)
def transpile_command(tree, level):
    parameter = tree.children[0]
    if tree.data == 'print':
        command = 'print'
        if level == 1:
            return command + "('" + parameter + "')"
        elif level == 2:
            #in level 2 moeten we gaan opzoeken of er een var of een str geprint wordt
            if parameter in table:
                return command + "(" + parameter + ")"
            else:
                return command + "('" + parameter + "')"
    elif tree.data == 'echo':
        command = 'print'
        return command + "('" + parameter + " ' + answer)"
    elif tree.data == 'ask':
        command = 'answer = input'
        return command + "('" + parameter + "')"
    elif tree.data == 'assign':
        value = tree.children[1]
        return parameter + " = '" + value + "'"
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





