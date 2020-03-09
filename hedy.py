from lark import Lark
from lark import Tree, Transformer
from lark.indenter import Indenter

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

def create_grammar(level):
    with open("grammars/level" + str(level) + ".txt", "r") as file:
        return file.read() 

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

class ConvertToPython(Transformer):
    indent_level = 0

    def start(self, args): 
        return "".join(args)

    def statement(self, args):
        return "".join([self.indent_level * "\t" + x + ("\n" if x[-1] != '\n' else "") for x in args if x != ""]) 

    def if_statement(self, args): 
        return "if " + args[0] + ":\n" + "".join(args[1:])

    def elif_statement(self, args): 
        return "elif " + args[0] + ":\n" + "".join(args[1:]) 

    def else_statement(self, args): 
        return "else:\n" + "".join(args) 

    def repeat(self, args): 
        return "for _ in range(" +args[0] + "):\n" + "".join(args[1:])

    def ranged_loop(self, args):
        return "for " + args[0] + " in range(" + args[1] + "," + args[2] +  "):\n" + "".join(args[3:])

    def assignment(self, args): 
        return args[0] + "=" + str(args[1])

    def eq(self, args): 
        return str(args[0]) + "==" + str(args[1])

    def ne(self, args): 
        return str(args[0]) + "!=" + str(args[1])

    def le(self, args): 
        return str(args[0]) + "<=" + str(args[1])

    def ge(self, args): 
        return str(args[0]) + ">=" + str(args[1])

    def lt(self, args): 
        return str(args[0]) + "<" + str(args[1])

    def gt(self, args): 
        return str(args[0]) + ">" + str(args[1])

    def addition(self, args): 
        return str(args[0]) + "+" + str(args[1])

    def substraction(self, args): 
        return str(args[0]) + "-" + str(args[1])

    def multiplication(self, args): 
        return str(args[0]) + "*" + str(args[1])

    def division(self, args): 
        return str(args[0]) + "/" + str(args[1])

    def list(self, args): 
        return str(args)

    def list_access(self, args):
        return  args[0] + "[" + str(args[1]) + "]" if args[1] != "random" else "random.choice(" + str(args[0]) + ")"

    def function_call(self, args):
        return args[0] + "(" + ", ".join(args[1:]) + ")"

    def INTEGER(self, args): 
        return int(args.value)

    def FLOAT(self, args): 
        return float(args.value)

    def NAME(self, args): 
        return str(args.value)

    def STRING(self, args): 
        return args.value

    def INDENT(self, args): 
        self.indent_level += 1 
        return "" 

    def DEDENT(self, args): 
        self.indent_level -= 1
        return "" 

class BasicIndenter(Indenter):
    NL_type = "_EOL"
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = "INDENT"
    DEDENT_type = "DEDENT"
    tab_len = 4 

def transpile(input_string, level): 
    level = int(level)

    if level == 1:
        punctuation_symbols = ['!', '?', '.']
        parser = create_parser(level)
        program_root = parser.parse(input_string).children[0] #getting rid of the root could also be done in the transformer would be nicer
        lookup_table = all_assignments(program_root)
        flattened_tree = FlattenText().transform(program_root) 
        python = ConvertToPython_1(punctuation_symbols, lookup_table).transform(program_root)
    elif level == 2:
        punctuation_symbols = ['!', '?', '.']
        parser = create_parser(level)
        program_root = parser.parse(input_string).children[0] #getting rid of the root could also be done in the transformer would be nicer
        lookup_table = all_assignments(program_root)
        flattened_tree = FlattenText().transform(program_root) 
        python = 'import random\n'
        python += ConvertToPython_2(punctuation_symbols, lookup_table).transform(program_root)
    elif level == 3:
        punctuation_symbols = ['!', '?', '.']
        parser = create_parser(level)
        program_root = parser.parse(input_string).children[0] #getting rid of the root could also be done in the transformer would be nicer
        lookup_table = all_assignments(program_root)
        flattened_tree = FlattenText().transform(program_root) 

        python = 'import random\n'
        python += ConvertToPython_3(punctuation_symbols, lookup_table).transform(program_root)
    elif level >= 8 or level == 4: 
        parser = Lark(create_grammar(level), parser='lalr', postlex=BasicIndenter(), debug=True) 
        python = 'import random\n' 
        python += ConvertToPython().transform(parser.parse(input_string + '\n')) #TODO: temporary fix, statements have to end with _EOL
        print(python)

    return python

def execute(input_string):
    python = transpile(input_string)
    exec(python)


# f = open('output.py', 'w+')
# f.write(python)
# f.close()





