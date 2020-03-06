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

class AllCommandsAssignments(Transformer):
    #returns only assignments
    def program(self, args):
        if len(args) == 1:
            #alleen assignments teruggeven (de rest bottom up 'opeten' en dan in de twee takken samenvoegen'
            maybe_assign_child = args[0].children[0]
            if type(maybe_assign_child) == str:
                pass #this is not assignment, don't return
            elif maybe_assign_child.data == 'assign':
                return [maybe_assign_child.children[0], maybe_assign_child.children[1]]
            elif maybe_assign_child.data == 'assign_list':
                pass
        else:
            return [a.children for a in args if a.data == 'assign' or a.data == 'assign_list']
    def text(self, args):
            return Tree('text', ''.join([str(c) for c in args]))
    def var(self, args):
            return Tree('var', ''.join([str(c) for c in args]))
    def punctuation(self, args):
            return Tree('punctuation', ''.join([str(c) for c in args]))
    def index(self, args):
            return ''.join([str(c) for c in args])

def all_commands(tree):
    flattened_tree = FlattenText().transform(tree)
    commands = AllCommands().transform(flattened_tree)
    return commands

def all_assignments(tree):
    flattened_tree = FlattenText().transform(tree)
    assignments = AllCommandsAssignments().transform(flattened_tree)
    variables = {}
    if assignments is not None:
        for a in assignments:
            variables[a[0]] = a[1:]

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
        lookup_table = all_assignments(program_root)
        commands = all_commands(program_root)
        python_lines = [transpile_command(c, level, lookup_table) for c in commands]
        return '\n'.join(python_lines)
    elif level == 3:
        lookup_table = all_assignments(program_root)
        commands = all_commands(program_root)
        python_lines = [transpile_command(c, level, lookup_table) for c in commands]
        return 'import random\n'+'\n'.join(python_lines)

# deze transpile moet natuurlijk ook een transformer worden
# op een dag :)
def transpile_command(tree, level, lookup_table = None):

    if tree.data == 'print':
        command = 'print'
        if level == 1:
            parameter = tree.children[0].children
            return command + "('" + parameter + "')"
        elif level == 2:
            all_arguments = tree.children

            #in level 2 moeten we gaan opzoeken of er een var of een str geprint wordt

            all_arguments_converted = []
            i = 0
            for argument in all_arguments:
                if i == len(all_arguments)-1 or all_arguments[i+1].data == 'punctuation':
                    space = ''
                else:
                    space = "+' '"
                if argument in lookup_table:
                    all_arguments_converted.append(argument.children + space)
                else:
                    all_arguments_converted.append("'" + argument.children + "'" + space)
                i = i + 1
            parameter_list = '+'.join(all_arguments_converted)
            return command + '(' + parameter_list + ')'
        elif level == 3:
            parameters = []
            for child in tree.children:
                if child.data == 'text':
                    parameters.append("'"+child.children+" '")
                elif child.data == 'list_access':
                    if type(child.children[1]) == Tree:
                        parameters.append('random.choice(' + child.children[0].children + ')')
                    else:
                        parameters.append(child.children[0].children + '[' + child.children[1] + ']')
                else:
                    parameters.append("".join(child.children))
            return command + '(' + '+'.join(parameters) + ')'
    elif tree.data == 'echo':
        if level == 1:
            command = 'print'
            all_parameters = []
            for child in tree.children:
                all_parameters.append("'"+child.children+"'")
            return command + "(" + '+'.join(all_parameters) + "+ ' '" + " + answer)"
        elif level == 2:
            command = 'print'
            all_parameters = []
            for child in tree.children:
                all_parameters.append("'"+child.children+"'")
            return command + "(" + '+'.join(all_parameters) + "+ ' '" + " + answer)"

    elif tree.data == 'ask':
        all_parameters = []
        for child in tree.children:
            all_parameters.append("'"+child.children+"'")
        command = 'answer = input'
        return command + "(" + '+'.join(all_parameters) + ")"
    elif tree.data == 'assign':
        parameter = tree.children[0].children
        value = tree.children[1].children
        return parameter + " = '" + value + "'"
    elif tree.data == 'assign_list':
        parameter = tree.children[0].children
        values = ["'" + a.children + "'" for a in tree.children[1:]]
        return parameter + " = [" + ", ".join(values) + "]"
    elif tree.data == 'wronglevel':
        raise Exception("Don't forget the quotation marks around text in level 3!")
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





