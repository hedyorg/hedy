from lark import Lark
from lark.exceptions import VisitError, LarkError
from lark import Tree, Transformer, Visitor
from lark.indenter import Indenter

reserved_words = ['and','except','lambda','with','as','finally','nonlocal','while','assert','false','None','yield','break','for','not','class','from','or','continue','global','pass','def','if','raise','del','import','return','elif','in','True','else','is','try']

def closest_command(command, commands):
    #simple string distance, could be more sophisticated MACHINE LEARNING!
    min = 1000
    min_command = ''
    for c in commands:
        min_c = minimum_distance(c, command)
        if min_c < min:
            min = min_c
            min_command = c
    return min_command

def minimum_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances
    return distances[-1]

class HedyException(Exception):
    def __init__(self, message, **arguments):
        self.error_code = message
        self.arguments = arguments

class ExtractAST(Transformer):
    # simplyfies the tree: f.e. flattens arguments of text, var and punctuation for further processing
    def text(self, args):
        return Tree('text', [''.join([str(c) for c in args])])

    #level 2
    def var(self, args):
        return Tree('var', [''.join([str(c) for c in args])])
    def punctuation(self, args):
        return Tree('punctuation', [''.join([str(c) for c in args])])
    def index(self, args):
        return ''.join([str(c) for c in args])
    def list_access(self, args):
        if type(args[1]) == Tree:
            return Tree('list_access', [args[0], 'random'])
        else:
            return Tree('list_access', [args[0], args[1]])

    #level 5
    def number(self, args):
        return Tree('number', ''.join([str(c) for c in args]))
    #level 6 (and up)
    def indent(self, args):
        return ''
    def dedent(self, args):
        return ''

def flatten(args):
    flattened_args = []
    if isinstance(args, str):
        return args
    elif isinstance(args, Tree):
        return args
    else:
        for a in args:
            if type(a) is list:
                for x in a:
                    flattened_args.append(flatten(x))
            else:
                flattened_args.append(a)
        return flattened_args

class AllAssignmentCommands(Transformer):
    # returns only variable assignments AND places where variables are accessed
    # so these can be excluded when printing

    def program(self, args):
        return flatten(args)

    def repeat(self, args):
        commands = args[1:]
        return flatten(commands)

    def command(self, args):
        return flatten(args)

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
    def var_access(self,args):
        return args[0].children

    #list access is accessing a variable, so must be escaped
    def list_access(self, args):
        listname = args[0].children[0]
        if args[1] == 'random':
            return 'random.choice(' + listname + ')'
        else:
            return listname + '[' + args[1] + ']'
    def print(self, args):
        return args


def create_parser(level):
    with open(f"grammars/level{str(level)}.txt", "r") as file:
        grammar = file.read()
    return Lark(grammar)

def all_arguments_true(args):
    bool_arguments = [x[0] for x in args]
    arguments_of_false_nodes = [x[1] for x in args if not x[0]]
    return all(bool_arguments), arguments_of_false_nodes

# this class contains code shared between IsValid and IsComplete, which are quite similar
# because both filter out some types of 'wrong' nodes
class Filter(Transformer):
    def program(self, args):
        bool_arguments = [x[0] for x in args]
        if all(bool_arguments):
            return [True] #all complete
        else:
            command_num = 1
            for a in args:
                if not a[0]:
                    return False, a[1], command_num
                command_num += 1

    def command(self, args):
        return all_arguments_true(args)

    def assign(self, args):
        return all_arguments_true(args)
    def assign_list(self, args):
        return all_arguments_true(args)
    def assign_sum(self, args):
        return all_arguments_true(args)
    def list_access(self, args):
        return all_arguments_true(args)

    # level 4 commands
    def list_access_var(self, args):
        return all_arguments_true(args)
    def ifs(self, args):
        return all_arguments_true(args)
    def ifelse(self, args):
        return all_arguments_true(args)
    def condition(self, args):
        return all_arguments_true(args)
    def equality_check(self, args):
        return all_arguments_true(args)
    def in_list_check(self, args):
        return all_arguments_true(args)

    # level 5 command
    def repeat(self, args):
        return all_arguments_true(args)

    # level 6
    def addition(self, args):
        return all_arguments_true(args)
    def substraction(self, args):
        return all_arguments_true(args)
    def multiplication(self, args):
        return all_arguments_true(args)
    def division(self, args):
        return all_arguments_true(args)

    #leafs are treated differently, they are True + their arguments flattened
    def random(self, args):
        return True, 'random'
    def index(self, args):
        return True, ''.join([str(c) for c in args])
    def punctuation(self, args):
        return True, ''.join([c for c in args])
    def number(self, args):
        return True, ''.join([c for c in args])
    def invalid(self, args):
        # return the first argument to place in the error message
        # TODO: this will not work for misspelling 'at', needs to be improved!
        return False, args[0][1]

class IsValid(Filter):
    # all rules are valid except for the invalid production rule
    # this function is used to generate more informative error messages
    # tree is transformed to a node of [Bool, args, linenumber]

    #would be lovely if there was some sort of default rule! Not sure Lark supports that

    def ask(self, args):
        return all_arguments_true(args)
    def print(self, args):
        return all_arguments_true(args)
    def echo(self, args):
        return all_arguments_true(args)


    #leafs with tokens need to be all true
    def var(self, args):
        return all(args), ''.join([c for c in args])
    def text(self, args):
        return all(args), ''.join([c for c in args])
    def addition(self, args):
        return all(args), ''.join([c for c in args])

    def invalid_space(self, args):
        # return space to indicate that line start in a space
        return False, " "


class IsComplete(Filter):
    # print, ask an echo can miss arguments and then are not complete
    # used to generate more informative error messages
    # tree is transformed to a node of [True] or [False, args, line_number]

    #would be lovely if there was some sort of default rule! Not sure Lark supports that

    def ask(self, args):
        return args != [], 'ask'
    def print(self, args):
        return args != [], 'print'
    def echo(self, args):
        #echo may miss an argument
        return True, 'echo'

    #leafs with tokens need to be all true
    def var(self, args):
        return all(args), ''.join([c for c in args])
    def text(self, args):
        return all(args), ''.join([c for c in args])
    def addition(self, args):
        return all(args), ''.join([c for c in args])


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
        all_parameters = ["'" + a + "'+" for a in args]
        return "print(" + ''.join(all_parameters) + "answer)"
    def ask(self, args):
        all_parameters = ["'" + a + "'" for a in args]
        return 'answer = input(' + '+'.join(all_parameters) + ")"

def wrap_non_var_in_quotes(argument, lookup):
    if argument in lookup:
        return argument
    else:
        return "'" + argument + "'"

class ConvertToPython_2(ConvertToPython_1):
    def punctuation(self, args):
        return ''.join([str(c) for c in args])
    def var(self, args):
        name = ''.join(args)
        return "_" + name if name in reserved_words else name
    def print(self, args):
        all_arguments_converted = []
        i = 0
        for argument in args:
            if i == len(args)-1 or args[i+1] in self.punctuation_symbols:
                space = ''
            else:
                space = "+' '"
            all_arguments_converted.append(wrap_non_var_in_quotes(argument, self.lookup) + space)
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
    def assign_list(self, args):
        parameter = args[0]
        values = ["'" + a + "'" for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

    def list_access(self, args):
        if args[1] == 'random':
            return 'random.choice(' + args[0] + ')'
        else:
            return args[0] + '[' + args[1] + ']'



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
    def ifelse(self, args):
        return f"""if {args[0]}:
{indent(args[1])}
else:
{indent(args[2])}"""
    def condition(self, args):
        return ' and '.join(args)
    def equality_check(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        return f"{arg0} == {arg1}" #no and statements
    def in_list_check(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        return f"{arg0} in {arg1}"

class ConvertToPython_5(ConvertToPython_4):
    def number(self, args):
        return ''.join(args)

    def repeat(self, args):
        times = wrap_non_var_in_quotes(args[0], self.lookup)
        command = args[1]
        return f"""for i in range(int({str(times)})):
{indent(command)}"""

class ConvertToPython_6(ConvertToPython_5):

    def print(self, args):
        #force all to be printed as strings (since there can not be int arguments)
        args_new = []
        for a in args:
            if type(a) is Tree:
                args_new.append(f'str({a.children})')
            elif "'" not in a:
                args_new.append(f'str({a})')
            else:
                args_new.append(a)

        return "print(" + '+'.join(args_new) + ')'

    #we can now have ints as types so chck must force str
    def equality_check(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        if len(args) == 2:
            return f"str({arg0}) == str({arg1})" #no and statements
        else:
            return f"str({arg0}) == str({arg1}) and {args[2]}"

    def assign(self, args):
        if len(args) == 2:
            parameter = args[0]
            value = args[1]
            if type(value) is Tree:
                return parameter + " = " + value.children
            else:
                return parameter + " = '" + value + "'"
        else:
            parameter = args[0]
            values = args[1:]
            return parameter + " = [" + ", ".join(values) + "]"


    def addition(self, args):
        return Tree('sum', f'int({str(args[0])}) + int({str(args[1])})')

    def substraction(self, args):
        return Tree('sum', f'int({str(args[0])}) - int({str(args[1])})')

    def multiplication(self, args):
        return Tree('sum', f'int({str(args[0])}) * int({str(args[1])})')

    def division(self, args):
        return Tree('sum', f'int({str(args[0])}) // int({str(args[1])})')

class ConvertToPython_7(ConvertToPython_6):
    def __init__(self, punctuation_symbols, lookup, indent_level):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup
        self.indent_level = indent_level

    def indent(self, args):
        self.indent_level += 1
        return ""

    def dedent(self, args):
        self.indent_level -= 1
        return ""

    def command(self, args):
        return "".join([self.indent_level * "    " + x for x in args if x != ""])

    def repeat(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        return "for i in range(int(" + str(args[0]) + ")):\n" + "\n".join(args[1:])

    def ifs(self, args):
        args = [a for a in args if a != ""] # filter out in|dedent tokens
        return "if " + args[0] + ":\n" + "\n".join(args[1:])

    def elses(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        return "\nelse:\n" + "\n".join(args)

    def assign(self, args): #TODO: needs to be merged with 6, when 6 is improved to with printing exprestions directly
        if len(args) == 2:
            parameter = args[0]
            value = args[1]
            if type(value) is Tree:
                return parameter + " = " + value.children
            else:
                if "'" in value or 'random.choice' in value: #TODO: should be a call to wrap nonvarargument is quotes!
                    return parameter + " = " + value
                else:
                    return parameter + " = '" + value + "'"
        else:
            parameter = args[0]
            values = args[1:]
            return parameter + " = [" + ", ".join(values) + "]"

    def var_access(self, args):
        if len(args) == 1: #accessing a var
            return wrap_non_var_in_quotes(args[0], self.lookup)
            # this was used to produce better error messages, but needs more work
            # (because plain text strings are now also var_access and not textwithoutspaces
            # since we no longer have priority rules
            # if args[0] in self.lookup:
            #     return args[0]
            # else:
            #     raise HedyException('VarUndefined', level=7, name=args[0])
        else:
        # dit was list_access
            return args[0] + "[" + str(args[1]) + "]" if type(args[1]) is not Tree else "random.choice(" + str(args[0]) + ")"

class ConvertToPython(Transformer):

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
        return "for i in range(" +args[0] + "):\n" + "".join(args[1:])

    def ranged_loop(self, args):
        return "for " + args[0] + " in range(" + args[1] + "," + args[2] +  "):\n" + "".join(args[3:])

    def assignment(self, args):
        return args[0] + "=" + str(args[1])

    # for now. expressions to Bool are not implemented (not sure we'd need them until 13)
    # def eq(self, args):
    #     return str(args[0]) + "==" + str(args[1])
    #
    # def ne(self, args):
    #     return str(args[0]) + "!=" + str(args[1])
    #
    # def le(self, args):
    #     return str(args[0]) + "<=" + str(args[1])
    #
    # def ge(self, args):
    #     return str(args[0]) + ">=" + str(args[1])
    #
    # def lt(self, args):
    #     return str(args[0]) + "<" + str(args[1])
    #
    # def gt(self, args):
    #     return str(args[0]) + ">" + str(args[1])

    # migrated to level 6
    # def addition(self, args):
    #     return str(args[0]) + "+" + str(args[1])
    #
    # def substraction(self, args):
    #     return str(args[0]) + "-" + str(args[1])
    #
    # def multiplication(self, args):
    #     return str(args[0]) + "*" + str(args[1])
    #
    # def division(self, args):
    #     return str(args[0]) + "/" + str(args[1])

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
    try:
        return transpile_inner(input_string, level)
    except Exception as E:
        #we retry HedyExceptions of the type Parse (and Lark Errors) but we raise Invalids
        if E.args[0] == 'Parse':
            #try 1 level lower
            if level > 1:
                try:
                    new_level = level-1
                    result = transpile_inner(input_string, level-1)
                    raise HedyException('Wrong Level', correct_code = result, original_level=level, working_level=new_level)
                except LarkError as e:
                    raise HedyException('Parse', level=level, parse_error=e.args[0])
            else:
                raise E
        else:
            raise E

def repair(input_string):
    #the only repair we can do now is remove leading spaces, more can be added!
    return '\n'.join([x.lstrip() for x in input_string.split('\n')])



def transpile_inner(input_string, level):
    if level <= 6:
        punctuation_symbols = ['!', '?', '.']
        level = int(level)
        parser = Lark(create_grammar(level))

        try:
            program_root = parser.parse(input_string+ '\n').children[0]  # getting rid of the root could also be done in the transformer would be nicer
            abstract_syntaxtree = ExtractAST().transform(program_root)
            lookup_table = AllAssignmentCommands().transform(abstract_syntaxtree)

        except Exception as e:
            # TODO: if all else fails, here we could translate Lark error messages into more sensible texts!
            raise HedyException('Parse', level=level, parse_error=e.args[0])

        is_valid = IsValid().transform(program_root)
        if not is_valid[0]:
            if is_valid[1] == ' ':
                line = is_valid[2]
                #the error here is a space at the beginning of a line, we can fix that!

                fixed_code = repair(input_string)
                if fixed_code != input_string: #only if we have made a successful fix
                    result = transpile_inner(fixed_code, level)
                raise HedyException('Invalid Space', level=level, line_number=line, fixed_code = result)
            else:
                invalid_command = is_valid[1]
                closest = closest_command(invalid_command, ['print', 'ask', 'echo'])
                raise HedyException('Invalid', invalid_command=invalid_command, level=level, guessed_command=closest)

        is_complete = IsComplete().transform(program_root)
        if not is_complete[0]:
            incomplete_command = is_complete[1]
            line = is_complete[2]
            raise HedyException('Incomplete', incomplete_command=incomplete_command, level=level, line_number=line)



        if level == 1:
            python = ConvertToPython_1(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
            return python
        elif level == 2:
            python = 'import random\n'
            python += ConvertToPython_2(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
            return python
        elif level == 3:
            python = 'import random\n'
            python += ConvertToPython_3(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
            return python
        elif level == 4:
            python = 'import random\n'
            python += ConvertToPython_4(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
            return python
        elif level == 5:
            python = 'import random\n'
            python += ConvertToPython_5(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
            return python
        elif level == 6:
            python = 'import random\n'
            python += ConvertToPython_6(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
            return python

    #todo: we need to be able to 'valid check' levels 6 and 8+ also, skipping for now (requires changes to grammar)
    elif level >= 7:
        parser = Lark(create_grammar(level), parser='lalr', postlex=BasicIndenter(), debug=True)
        punctuation_symbols = ['!', '?', '.']
        program_root = parser.parse(input_string + '\n').children[0]  # TODO: temporary fix, statements have to end with _EOL
        abstract_syntaxtree = ExtractAST().transform(program_root)
        lookup_table = AllAssignmentCommands().transform(abstract_syntaxtree)
        if level == 7:
            try:
                python = 'import random\n'
                result = ConvertToPython_7(punctuation_symbols, lookup_table, 0).transform(program_root)
                return python + result
            except VisitError as E:
                raise E.orig_exc
    else:
        raise Exception('Levels over 7 are not implemented yet')


def execute(input_string):
    python = transpile(input_string)
    exec(python)


# f = open('output.py', 'w+')
# f.write(python)
# f.close()





