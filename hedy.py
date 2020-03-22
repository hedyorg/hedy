from lark import Lark
from lark import Tree, Transformer, Visitor
from lark.indenter import Indenter

class HedyException(Exception):
    def __init__(self, message, **arguments):
        self.error_code = message
        self.arguments = arguments



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
    def counter(self, args):
        return Tree('counter', ''.join([str(c) for c in args]))

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
    def ask(self, args):
        #todo: this also uses this arg for level 1, where it should not be used
        #(since then it has no var as 1st argument)
        #we should actually loop the level in here to distinguish on
        return args[0].children
    def assign(self, args):
        return args[0].children
    def assign_list(self, args):
        return args[0].children
    def list_access_var(self, args):
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
    with open(f"grammars/level{str(level)}.txt", "r") as file:
        grammar = file.read()
    return Lark(grammar)

class IsValid(Transformer):
    # all rules are valid except for the invalid production rule
    # used to generate more informative error messages
    # tree is transformed to a node of [Bool, args]
    def pass_arguments(self, args):
        bool_arguments = [x[0] for x in args]
        arguments_of_false_nodes = [x[1] for x in args if not x[0]]
        return all(bool_arguments), arguments_of_false_nodes

    #would be lovely if there was some sort of default rule! Not sure Lark supports that
    def program(self, args):
        return self.pass_arguments(args)
    def command(self, args):
        return self.pass_arguments(args)
    def ask(self, args):
        return self.pass_arguments(args)
    def print(self, args):
        return self.pass_arguments(args)
    def echo(self, args):
        return self.pass_arguments(args)
    def assign(self, args):
        return self.pass_arguments(args)
    def assign_list(self, args):
        return self.pass_arguments(args)
    def list_access(self, args):
        return self.pass_arguments(args)
    #level 4 commands
    def list_access_var(self, args):
        return self.pass_arguments(args)
    def ifs(self, args):
        return self.pass_arguments(args)
    def ifelse(self, args):
        return self.pass_arguments(args)
    def equality_check(self, args):
        return self.pass_arguments(args)
    #level 5 command
    def repeat(self, args):
        return self.pass_arguments(args)

    #leafs are treated differently, they are True + their arguments flattened
    def random(self, args):
        return True, 'random'
    def index(self, args):
        return True, ''.join([str(c) for c in args])
    def var(self, args):
        return all(args), ''.join([c for c in args])
    def text(self, args):
        return all(args), ''.join([c for c in args])
    def punctuation(self, args):
        return True, ''.join([c for c in args])
    def counter(self, args):
        return True, ''.join([c for c in args])
    def invalid(self, args):
        # return the first argument to place in the error message
        # TODO: this will not work for misspelling 'at', needs to be improved!
        return False, args[0][1]


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
    def ask(self, args):
        var = args[0]
        all_parameters = ["'" + a + "'" for a in args[1:]]
        return f'{var} = input(' + '+'.join(all_parameters) + ")"
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


#TODO: lookuptable and punctuation chars not be needed for level2 and up anymore, could be removed
class ConvertToPython_3(ConvertToPython_2):
    def text(self, args):
        return ''.join([str(c) for c in args])
    def print(self, args):
        #opzoeken is nu niet meer nodig
        return "print(" + '+'.join(args) + ')'

def indent(s):
    lines = s.split('\n')
    return '\n'.join(['  ' + l for l in lines])

class ConvertToPython_4(ConvertToPython_3):
    def list_access_var(self, args):
        var = args[0]
        if args[2].data == 'random':
            return var + '=random.choice(' + args[1] + ')'
        else:
            return var + '=' + args[1] + '[' + args[2].children[0] + ']'
    def ifs(self, args):
        return f"""if {args[0]}:
{indent(args[1])}"""
    def equality_check(self, args):
        if len(args) == 2:
            return f"{args[0]} == '{args[1]}'" #no and statements
        else:
            return f"{args[0]} == '{args[1]}' and {args[2]}"
    def ifelse(self, args):
        return f"""if {args[0]}:
{indent(args[1])}
else:
{indent(args[2])}"""

class ConvertToPython_5(ConvertToPython_4):
    def repeat(self, args):
        times = args[0].children[0]
        command = args[1]
        return f"""for i in range({times}):
{indent(command)}"""

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

def create_grammar(level):
    with open("grammars/level" + str(level) + ".txt", "r") as file:
        return file.read()

def transpile(input_string, level):
    if level <= 5:
        punctuation_symbols = ['!', '?', '.']
        level = int(level)
        parser = create_parser(level)
        try:
            program_root = parser.parse(input_string).children[0]  # getting rid of the root could also be done in the transformer would be nicer
            lookup_table = all_assignments(program_root)
            flattened_tree = FlattenText().transform(program_root)
        except Exception as e:
            # TODO: here we could translate Lark error messages into more sensible texts!
            raise HedyException('Parse', level=level, parse_error=e.args[0])

        is_valid = IsValid().transform(program_root)

        if is_valid[0]:
            if level == 1:
                python = ConvertToPython_1(punctuation_symbols, lookup_table).transform(program_root)
                return python
            elif level == 2:
                python = 'import random\n'
                python += ConvertToPython_2(punctuation_symbols, lookup_table).transform(program_root)
                return python
            elif level == 3:
                python = 'import random\n'
                python += ConvertToPython_3(punctuation_symbols, lookup_table).transform(program_root)
                return python
            elif level == 4:
                python = 'import random\n'
                python += ConvertToPython_4(punctuation_symbols, lookup_table).transform(program_root)
                return python
            elif level == 5:
                python = 'import random\n'
                python += ConvertToPython_5(punctuation_symbols, lookup_table).transform(program_root)
                return python
        else:
            invalid_command = is_valid[1]
            raise HedyException('Invalid', command=invalid_command, level=level)

    #todo: we need to be able to 'valid check' levels 6 and 8+ also, skipping for now (requires changes to grammar)
    elif level >= 6:
        parser = Lark(create_grammar(level), parser='lalr', postlex=BasicIndenter(), debug=True)
        python = 'import random\n'
        python += ConvertToPython().transform(
            parser.parse(input_string + '\n'))  # TODO: temporary fix, statements have to end with _EOL
        return python
    else:
        raise Exception('Levels 5 to 7 are not implemented yet')


def execute(input_string):
    python = transpile(input_string)
    exec(python)


# f = open('output.py', 'w+')
# f.write(python)
# f.close()





