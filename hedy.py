from lark import Lark
from lark.exceptions import LarkError, UnexpectedEOF, UnexpectedCharacters
from lark import Tree, Transformer
from os import path
import sys
import utils

reserved_words = ['and','except','lambda','with','as','finally','nonlocal','while','assert','False','None','yield','break','for','not','class','from','or','continue','global','pass','def','if','raise','del','import','return','elif','in','True','else','is','try']

#
# Commands per Hedy level which are used to suggest the closest command when kids make a mistake
#

commands_per_level = {1: ['print', 'ask', 'echo'] ,
                      2: ['print', 'ask', 'echo', 'is'],
                      3: ['print', 'ask', 'is'],
                      4: ['print', 'ask', 'is', 'if'],
                      5: ['print', 'ask', 'is', 'if', 'repeat'],
                      6: ['print', 'ask', 'is', 'if', 'repeat'],
                      7: ['print', 'ask', 'is', 'if', 'repeat'],
                      8: ['print', 'ask', 'is', 'if', 'for'],
                      9: ['print', 'ask', 'is', 'if', 'for', 'elif'],
                      10: ['print', 'ask', 'is', 'if', 'for', 'elif'],
                      11: ['print', 'ask', 'is', 'if', 'for', 'elif'],
                      12: ['print', 'ask', 'is', 'if', 'for', 'elif'],
                      13: ['print', 'ask', 'is', 'if', 'for', 'elif'],
                      14: ['print', 'ask', 'is', 'if', 'for', 'elif'],
                      15: ['print', 'ask', 'is', 'if', 'for', 'elif'],
                      16: ['print', 'ask', 'is', 'if', 'for', 'elif'],
                      17: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while'],
                      18: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while'],
                      19: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while'],
                      20: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while'],
                      21: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while'],
                      22: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while']
                      }

#
#  closest_command() searches for known commands in an invalid command.
#
#  It will return the known command which is closest positioned at the beginning.
#  It will return '' if the invalid command does not contain any known command.
#

def closest_command(invalid_command, known_commands):
    # First search for 100% match of known commands
    min_position = len(invalid_command)
    min_command = ''
    for known_command in known_commands:
        position = invalid_command.find(known_command)
        if position != -1 and position < min_position:
            min_position = position
            min_command = known_command

    # If not found, search for partial match of know commands
    if min_command == '':
        min_command = closest_command_with_min_distance(invalid_command, known_commands)

    # Check if we are not returning the found command
    # In that case we have no suggestion
    # This is to prevent "print is not a command in Hedy level 3, did you mean print?" error message

    if min_command == invalid_command:
        return None

    return min_command


def closest_command_with_min_distance(command, commands):
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
    """Return string distance between 2 strings."""
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
    # simplifies the tree: f.e. flattens arguments of text, var and punctuation for further processing
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
            if "random" in args[1].data:
                return Tree('list_access', [args[0], 'random'])
            else:
                return Tree('list_access', [args[0], args[1].children[0]])
        else:
            return Tree('list_access', [args[0], args[1]])

    #level 5
    def number(self, args):
        return Tree('number', ''.join([str(c) for c in args]))

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

    def for_loop(self, args):
        commands = args[1:]
        return flatten(commands)
    def while_loop(self, args):
        commands = args[1:]
        return flatten(commands)

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
    def change_list_item(self, args):
        return args[0].children
    def comment(self, args):
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
    def input(self,args):
        return args[0].children

    def smaller(self, args):
        return args[0].children
    def bigger(self, args):
        return args[0].children

    def not_equal(self, args):
        return args[0].children

    def smaller_equal(self, args):
        return args[0].children
    def bigger_equal(self, args):
        return args[0].children


def are_all_arguments_true(args):
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
        return are_all_arguments_true(args)

    def assign(self, args):
        return are_all_arguments_true(args)
    def assign_list(self, args):
        return are_all_arguments_true(args)
    def assign_sum(self, args):
        return are_all_arguments_true(args)
    def list_access(self, args):
        return are_all_arguments_true(args)

    # level 4 commands
    def list_access_var(self, args):
        return are_all_arguments_true(args)
    def ifs(self, args):
        return are_all_arguments_true(args)
    def valid_command(self, args):
        return are_all_arguments_true(args)
    def ifelse(self, args):
        return are_all_arguments_true(args)
    def condition(self, args):
        return are_all_arguments_true(args)
    def equality_check(self, args):
        return are_all_arguments_true(args)
    def in_list_check(self, args):
        return are_all_arguments_true(args)

    # level 5 command
    def repeat(self, args):
        return are_all_arguments_true(args)

    # level 6
    def addition(self, args):
        return are_all_arguments_true(args)
    def substraction(self, args):
        return are_all_arguments_true(args)
    def multiplication(self, args):
        return are_all_arguments_true(args)
    def division(self, args):
        return are_all_arguments_true(args)

    #level 7
    def elses(self, args):
        return are_all_arguments_true(args)

    # level 8
    def for_loop(self, args):
        return are_all_arguments_true(args)

    # level 9
    def elifs(self, args):
        return are_all_arguments_true(args)

    # level 12
    def change_list_item(self, args):
        return are_all_arguments_true(args)

    # level 14
    def andcondition(self, args):
        return are_all_arguments_true(args)
    def orcondition(self, args):
        return are_all_arguments_true(args)
    # level 15
    def comment(self, args):
        return are_all_arguments_true(args)

    # level 16
    def smaller(self, args):
        return are_all_arguments_true(args)
    def bigger(self, args):
        return are_all_arguments_true(args)

    # level 17
    def while_loop(self, args):
        return are_all_arguments_true(args)

    # level 19
    def length(self, args):
        return True, ''.join([str(c) for c in args])

    # level 21
    def not_equal(self, args):
        return are_all_arguments_true(args)

    # level 22
    def smaller_equal(self, args):
        return are_all_arguments_true(args)
    def bigger_equal(self, args):
        return are_all_arguments_true(args)

    #leafs are treated differently, they are True + their arguments flattened
    def var(self, args):
        return True, ''.join([str(c) for c in args])
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
    # all rules are valid except for the "Invalid" production rule
    # this function is used to generate more informative error messages
    # tree is transformed to a node of [Bool, args, linenumber]

    #would be lovely if there was some sort of default rule! Not sure Lark supports that

    # note! If this function errors out with:
    # Error trying to process rule "program" Tree object not subscriptable
    # that means you added a production rule but did not add a method for the rule here

    def ask(self, args):
        return are_all_arguments_true(args)
    def print(self, args):
        return are_all_arguments_true(args)
    def echo(self, args):
        return are_all_arguments_true(args)
    def for_loop(self, args):
        return are_all_arguments_true(args)
    def while_loop(self, args):
        return are_all_arguments_true(args)
    def comment(self, args):
        return are_all_arguments_true(args)
    def length(self, args):
        return are_all_arguments_true(args)

    #leafs with tokens need to be all true
    def var(self, args):
        return all(args), ''.join([c for c in args])
    def text(self, args):
        return all(args), ''.join([c for c in args])
    def invalid_space(self, args):
        # return space to indicate that line starts in a space
        return False, " "

    def print_nq(self, args):
        # return error source to indicate what went wrong
        return False, "print without quotes"
    def input(self, args):
        return are_all_arguments_true(args)



class IsComplete(Filter):
    # print, ask an echo can miss arguments and then are not complete
    # used to generate more informative error messages
    # tree is transformed to a node of [True] or [False, args, line_number]

    #would be lovely if there was some sort of default rule! Not sure Lark supports that

    # note! If this function errors out with:
    # Error trying to process rule "program" Tree object not subscriptable
    # that means you added a production rule but did not add a method for the rule here

    def ask(self, args):
        return args != [], 'ask'
    def print(self, args):
        return args != [], 'print'
    def print_nq(self, args):
        return args != [], 'print level 2'
    def echo(self, args):
        #echo may miss an argument
        return True, 'echo'

    #leafs with tokens need to be all true
    def var(self, args):
        return all(args), ''.join([c for c in args])
    def text(self, args):
        return all(args), ''.join([c for c in args])
    def input(self, args):
        return args != [], 'input'
    def length(self, args):
        return args != [], 'len'

class ConvertToPython_1(Transformer):

    def process_single_quote(self, value):
        # defines what happens if a kids uses ' in a string
        value = value.replace("'", "\\'")
        return value


    def __init__(self, punctuation_symbols, lookup):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup

    def program(self, args):
        return '\n'.join([str(c) for c in args])
    def command(self, args):
        return args[0]
    def text(self, args):
        return ''.join([str(c) for c in args])
    def print(self, args):
        # escape quotes if kids accidentally use them at level 1
        argument = self.process_single_quote(args[0])

        return "print('" + argument + "')"
    def echo(self, args):
        if len(args) == 0:
            return "print(answer)" #no arguments, just print answer

        argument = self.process_single_quote(args[0])
        return "print('" + argument + "'+answer)"
    def ask(self, args):
        argument = self.process_single_quote(args[0])
        return "answer = input('" + argument + "')"

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
            # escape quotes if kids accidentally use them at level 2
            argument = self.process_single_quote(argument)

            # final argument and punctuation arguments do not have to be separated with a space, other do
            if i == len(args)-1 or args[i+1] in self.punctuation_symbols:
                space = ''
            else:
                space = "+' '"
            all_arguments_converted.append(wrap_non_var_in_quotes(argument, self.lookup) + space)
            i = i + 1
        return 'print(' + '+'.join(all_arguments_converted) + ')'
    def ask(self, args):
        var = args[0]
        all_parameters = ["'" + self.process_single_quote(a) + "'" for a in args[1:]]
        return f'{var} = input(' + '+'.join(all_parameters) + ")"
    def assign(self, args):
        parameter = args[0]
        value = args[1]
        #if the assigned value contains single quotes, escape them
        value = self.process_single_quote(value)
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
    def print_nq(self, args):
        return ConvertToPython_2.print(self, args)

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
    def __init__(self, punctuation_symbols, lookup):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup

    def command(self, args):
        return "".join(args)

    def repeat(self, args):
        all_lines = [indent(x) for x in args[1:]]
        return "for i in range(int(" + str(args[0]) + ")):\n" + "\n".join(all_lines)

    def ifs(self, args):
        args = [a for a in args if a != ""] # filter out in|dedent tokens

        all_lines = [indent(x) for x in args[1:]]

        return "if " + args[0] + ":\n" + "\n".join(all_lines)

    def elses(self, args):
        args = [a for a in args if a != ""] # filter out in|dedent tokens

        all_lines = [indent(x) for x in args]

        return "\nelse:\n" + "\n".join(all_lines)

    def assign(self, args):  # TODO: needs to be merged with 6, when 6 is improved to with printing expressions directly
        if len(args) == 2:
            parameter = args[0]
            value = args[1]
            if type(value) is Tree:
                return parameter + " = " + value.children
            else:
                if "'" in value or 'random.choice' in value:  # TODO: should be a call to wrap nonvarargument is quotes!
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

class ConvertToPython_8(ConvertToPython_7):
    def for_loop(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [indent(x) for x in args[3:]]
        return "for " + args[0] + " in range(" + "int(" + args[1] + ")" + ", " + "int(" + args[2] + ")+1" + "):\n"+"\n".join(all_lines)

class ConvertToPython_9_10(ConvertToPython_8):
    def elifs(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [indent(x) for x in args[1:]]
        return "\nelif " + args[0] + ":\n" + "\n".join(all_lines)

class ConvertToPython_11(ConvertToPython_9_10):
    def input(self, args):
        args_new = []
        var = args[0]
        for a in args[1:]:
            if type(a) is Tree:
                args_new.append(f'str({a.children})')
            elif "'" not in a:
                args_new.append(f'str({a})')
            else:
                args_new.append(a)

        return f'{var} = input(' + '+'.join(args_new) + ")"

class ConvertToPython_12(ConvertToPython_11):
    def assign_list(self, args):
        parameter = args[0]
        values = [a for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

    def list_access_var(self, args):
        var = args[0]
        if not isinstance(args[2], str):
            if args[2].data == 'random':
                return var + '=random.choice(' + args[1] + ')'
        else:
            return var + '=' + args[1] + '[' + args[2] + '-1]'

    def list_access(self, args):
        if args[1] == 'random':
            return 'random.choice(' + args[0] + ')'
        else:
            return args[0] + '[' + args[1] + '-1]'

    def change_list_item(self, args):
        return args[0] + '[' + args[1] + '-1] = ' + args[2]
# Custom transformer that can both be used bottom-up or top-down

class ConvertToPython_13(ConvertToPython_12):
    def assign(self, args):  # TODO: needs to be merged with 6, when 6 is improved to with printing expressions directly
        if len(args) == 2:
            parameter = args[0]
            value = args[1]
            if type(value) is Tree:
                return parameter + " = " + value.children
            else:
                if "'" in value or 'random.choice' in value:  # TODO: should be a call to wrap nonvarargument is quotes!
                    return parameter + " = " + value
                else:
                    # FH, June 21 the addition of _true/false is a bit of a hack. cause they are first seen as vars that at reserved words, they egt and _ and we undo that here.
                    # could/should be fixed in the grammar!
                    if value == 'true' or value == 'True' or value == '_True':
                        return parameter + " = True"
                    elif value == 'false' or value == 'False' or value == '_False':
                        return parameter + " = False"
                    else:
                        return parameter + " = '" + value + "'"
        else:
            parameter = args[0]
            values = args[1:]
            return parameter + " = [" + ", ".join(values) + "]"

    def equality_check(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        if arg1 == '\'True\'' or arg1 == '\'true\'':
            return f"{arg0} == True"
        elif arg1 == '\'False\'' or arg1 == '\'false\'':
            return f"{arg0} == False"
        else:
            return f"str({arg0}) == str({arg1})" #no and statements

class ConvertToPython_14(ConvertToPython_13):
    def andcondition(self, args):
        return ' and '.join(args)
    def orcondition(self, args):
        return ' or '.join(args)

class ConvertToPython_15(ConvertToPython_14):
    def comment(self, args):
        return f"# {args}"

class ConvertToPython_16(ConvertToPython_15):
    def smaller(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        if len(args) == 2:
            return f"str({arg0}) < str({arg1})"  # no and statements
        else:
            return f"str({arg0}) < str({arg1}) and {args[2]}"

    def bigger(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        if len(args) == 2:
            return f"str({arg0}) > str({arg1})"  # no and statements
        else:
            return f"str({arg0}) > str({arg1}) and {args[2]}"

class ConvertToPython_17(ConvertToPython_16):
    def while_loop(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [indent(x) for x in args[1:]]
        return "while " + args[0] + ":\n"+"\n".join(all_lines)

class ConvertToPython_18_19(ConvertToPython_17):
    def length(self, args):
        arg0 = args[0]
        return f"len({arg0})"

    def assign(self, args):  # TODO: needs to be merged with 6, when 6 is improved to with printing expressions directly
        if len(args) == 2:
            parameter = args[0]
            value = args[1]
            if type(value) is Tree:
                return parameter + " = " + value.children
            else:
                if "'" in value or 'random.choice' in value:  # TODO: should be a call to wrap nonvarargument is quotes!
                    return parameter + " = " + value
                elif "len(" in value:
                    return parameter + " = " + value
                else:
                    if value == 'true' or value == 'True':
                        return parameter + " = True"
                    elif value == 'false' or value == 'False':
                        return parameter + " = False"
                    else:
                        return parameter + " = '" + value + "'"
        else:
            parameter = args[0]
            values = args[1:]
            return parameter + " = [" + ", ".join(values) + "]"

class ConvertToPython_20(ConvertToPython_18_19):
    def equality_check(self, args):
        if type(args[0]) is Tree:
            return args[0].children + " == int(" + args[1] + ")"
        if type(args[1]) is Tree:
            return "int(" + args[0] + ") == " + args[1].children
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        if arg1 == '\'True\'' or arg1 == '\'true\'':
            return f"{arg0} == True"
        elif arg1 == '\'False\'' or arg1 == '\'false\'':
            return f"{arg0} == False"
        else:
            return f"str({arg0}) == str({arg1})"  # no and statements

class ConvertToPython_21(ConvertToPython_20):
    def not_equal(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        if len(args) == 2:
            return f"str({arg0}) != str({arg1})"  # no and statements
        else:
            return f"str({arg0}) != str({arg1}) and {args[2]}"

class ConvertToPython_22(ConvertToPython_21):
    def smaller_equal(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        if len(args) == 2:
            return f"str({arg0}) <= str({arg1})"  # no and statements
        else:
            return f"str({arg0}) <= str({arg1}) and {args[2]}"

    def bigger_equal(self, args):
        arg0 = wrap_non_var_in_quotes(args[0], self.lookup)
        arg1 = wrap_non_var_in_quotes(args[1], self.lookup)
        if len(args) == 2:
            return f"str({arg0}) >= str({arg1})"  # no and statements
        else:
            return f"str({arg0}) >= str({arg1}) and {args[2]}"


class ConvertTo():
    def __default_child_call(self, name, children):
        return self._call_children(children)

    def _call_children(self, children):
        result = []
        for x in children:
            if type(x) == Tree:
                try:
                    method = getattr(self, x.data)
                except AttributeError:
                    result.append(self.__default_child_call(x.data, x.children))
                else:
                    result.append(method(x.children))
            else:
                result.append(x)
        return result

    def transform(self, tree):
            return getattr(self, tree.data)(tree.children)

class ConvertToPython(ConvertTo):

    def start(self, children):
        return "".join(self._call_children(children))

    def if_statement(self, children):
        args = self._call_children(children)
        return "if " + args[0] + ":\n" + args[1]

    def elif_statement(self, children):
        args = self._call_children(children)
        return "elif " + args[0] + ":\n" + args[1]

    def else_statement(self, children):
        args = self._call_children(children)
        return "else:\n" + args[0]

    def repeat(self, children):
        args = self._call_children(children)
        return "for _ in range(" + args[0] + "):\n" + args[1]

    def for_loop(self, children):
        args = self._call_children(children)
        return "for " + args[0] + " in range(" + args[1] + ", " + args[2] +  "):\n" + args[3]

    def assignment(self, children):
        args = self._call_children(children)
        return args[0] + " = " + args[1] + "\n"

    def eq(self, children):
        args = self._call_children(children)
        return args[0] + " == " + args[1]

    def ne(self, children):
        args = self._call_children(children)
        return args[0] + " != " + args[1]

    def le(self, children):
        args = self._call_children(children)
        return args[0] + " <= " + args[1]

    def ge(self, children):
        args = self._call_children(children)
        return args[0] + " >= " + args[1]

    def lt(self, children):
        args = self._call_children(children)
        return args[0] + " < " + args[1]

    def gt(self, children):
        args = self._call_children(children)
        return args[0] + " > " + args[1]

    def addition(self, children):
        args = self._call_children(children)
        return args[0] + " + " + args[1]

    def substraction(self, children):
        args = self._call_children(children)
        return args[0] + " - " + args[1]

    def multiplication(self, children):
        args = self._call_children(children)
        return args[0] + " * " + args[1]

    def division(self, children):
        args = self._call_children(children)
        return args[0] + " / " + args[1]

    def modulo(self, children):
        args = self._call_children(children)
        return args[0] + " % " + args[1]

    def unary_plus(self, children):
        args = self._call_children(children)
        return args[0]

    def unary_minus(self, children):
        args = self._call_children(children)
        return "-" + args[0]

    def parenthesis(self, children):
        args = self._call_children(children)
        return "(" + args[0] + ")"

    def list_access(self, children):
        args = self._call_children(children)
        return args[0] + "[" + args[1] + "]" if args[1] != "random" else "random.choice(" + args[0] + ")"

    def list(self, children):
        args = self._call_children(children)
        return "[" + ", ".join(args) + "]"

    def print(self, children):
        args = self._call_children(children)
        return "print("  + ", ".join(args) + ")\n"

    def ask(self, children):
        args = self._call_children(children)
        return "input("  + " + ".join(args) + ")"

def merge_grammars(grammar_text_1, grammar_text_2):
    # this function takes two grammar files and merges them into one
    # rules that are redefined in the second file are overridden
    # rule that are new in the second file are added (remaining_rules_grammar_2)

    merged_grammar = []

    rules_grammar_1 = grammar_text_1.split('\n')
    remaining_rules_grammar_2 = grammar_text_2.split('\n')
    for line_1 in rules_grammar_1:
        if line_1 == '' or line_1[0] == '/': #skip comments and empty lines:
            continue
        parts = line_1.split(':')
        name_1, definition_1 = parts[0], ''.join(parts[1:]) #get part before are after : (this is a join because there can be : in the rule)

        rules_grammar_2 = grammar_text_2.split('\n')
        override_found = False
        for line_2 in rules_grammar_2:
            if line_2 == '' or line_2[0] == '/':  # skip comments and empty lines:
                continue
            parts = line_2.split(':')
            name_2, definition_2 = parts[0], ''.join(parts[1]) #get part before are after :
            if name_1 == name_2:
                override_found = True
                new_rule = line_2
                # this rule is now in the grammar, remove form this list
                remaining_rules_grammar_2.remove(new_rule)
                break

        # new rule found? print that. nothing found? print org rule
        if override_found:
            merged_grammar.append(new_rule)
        else:
            merged_grammar.append(line_1)

    #all rules that were not overlapping are new in the grammar, add these too
    for rule in remaining_rules_grammar_2:
        if not(rule == '' or rule[0] == '/'):
            merged_grammar.append(rule)

    merged_grammar = sorted(merged_grammar)
    return '\n'.join(merged_grammar)


def create_grammar(level, sub):
    # Load Lark grammars relative to directory of current file
    script_dir = path.abspath(path.dirname(__file__))

    if sub:
      filename = "level" + str(level) + "-" + str (sub) + ".lark"
      with open(path.join(script_dir, "grammars", filename), "r", encoding="utf-8") as file:
          return file.read()
    else:

        # Load Lark grammars relative to directory of current file
        script_dir = path.abspath(path.dirname(__file__))

        # we start with creating the grammar for level 1
        grammar_text_1 = get_full_grammar_for_level(1)

        #grep
        if level == 1:
            grammar_text = get_full_grammar_for_level(level)
            return grammar_text

        grammar_text_2 = get_additional_rules_for_level(2)

        #start at 1 and keep merging new grammars in
        new = merge_grammars(grammar_text_1, grammar_text_2)

        for i in range(3, level+1):
            grammar_text_i = get_additional_rules_for_level(i)
            new = merge_grammars(new, grammar_text_i)

        # ready? Save to file to ease debugging
        # this could also be done on each merge for performance reasons
        filename = "level" + str(level) + "-Total.lark"
        loc = path.join(script_dir, "grammars-Total", filename)
        file = open(loc, "w", encoding="utf-8")
        file.write(new)
        file.close()

    return new

def get_additional_rules_for_level(level):
    script_dir = path.abspath(path.dirname(__file__))
    filename = "level" + str(level) + "-Additions.lark"
    with open(path.join(script_dir, "grammars", filename), "r", encoding="utf-8") as file:
        grammar_text = file.read()
    return grammar_text

def get_full_grammar_for_level(level):
    script_dir = path.abspath(path.dirname(__file__))
    filename = "level" + str(level) + ".lark"
    with open(path.join(script_dir, "grammars", filename), "r", encoding="utf-8") as file:
        grammar_text = file.read()
    return grammar_text

PARSER_CACHE = {}


def get_parser(level, sub):
    """Return the Lark parser for a given level.

    Uses caching if Hedy is NOT running in development mode.
    """
    key = str(level) + "." + str(sub)
    existing = PARSER_CACHE.get(key)
    if existing and not utils.is_debug_mode():
        return existing
    grammar = create_grammar(level, sub)
    ret = Lark(grammar)
    PARSER_CACHE[key] = ret
    return ret


def transpile(input_string, level, sub = 0):
    try:
        return transpile_inner(input_string, level, sub)
    except Exception as E:
        # This is the 'fall back' transpilation
        # that should surely be improved!!
        # we retry HedyExceptions of the type Parse (and Lark Errors) but we raise Invalids
        if E.args[0] == 'Parse':
            #try 1 level lower
            if level > 1 and sub == 0:
                try:
                    new_level = level - 1
                    result = transpile_inner(input_string, new_level, sub)
                except (LarkError, HedyException) as innerE:
                    # Parse at `level - 1` failed as well, just re-raise original error
                    raise E
                # If the parse at `level - 1` succeeded, then a better error is "wrong level"
                raise HedyException('Wrong Level', correct_code=result, original_level=level, working_level=new_level) from E
        raise E

def repair(input_string):
    #the only repair we can do now is remove leading spaces, more can be added!
    return '\n'.join([x.lstrip() for x in input_string.split('\n')])

def translate_characters(s):
# this method is used to make it more clear to kids what is meant in error messages
# for example ' ' is hard to read, space is easier
# this could (should?) be localized so we can call a ' "Hoge komma" for example (Felienne, dd Feb 25, 2021)
    if s == ' ':
        return 'space'
    elif s == ',':
        return 'comma'
    elif s == '?':
        return 'question mark'
    elif s == '\\n':
        return 'newline'
    elif s == '.':
        return 'period'
    elif s == '!':
        return 'exclamation mark'
    elif s == '*':
        return 'star'
    elif s == "'":
        return 'single quotes'
    elif s == '"':
        return 'double quotes'
    elif s == '/':
        return 'slash'
    elif s == '-':
        return 'dash'
    elif s >= 'a' and s <= 'z' or s >= 'A' and s <= 'Z':
        return s
    else:
        return s

def filter_and_translate_terminals(list):
    # in giving error messages, it does not make sense to include
    # ANONs, and some things like EOL need kid friendly translations
    new_terminals = []
    for terminal in list:
        if terminal[:4] == "ANON":
            continue

        if terminal == "EOL":
            new_terminals.append("Newline")
            break

        #not translated or filtered out? simply add as is:
        new_terminals.append(terminal)

    return new_terminals

def beautify_parse_error(error_message):
    character_found = error_message.split("'")[1]
    character_found = translate_characters(character_found)
    return character_found

def find_indent_length(line):
    number_of_spaces = 0
    for x in line:
        if x == ' ':
            number_of_spaces += 1
        else:
            break
    return number_of_spaces

def preprocess_blocks(code):
    processed_code = []
    lines = code.split("\n")
    current_number_of_indents = 0
    previous_number_of_indents = 0
    indent_size = None #we don't fix indent size but the first encounter sets it
    for line in lines:
        leading_spaces = find_indent_length(line)

        #first encounter sets indent size for this program
        if indent_size == None and leading_spaces > 0:
            indent_size = leading_spaces

        #calculate nuber of indents if possible
        if indent_size != None:
            current_number_of_indents = leading_spaces // indent_size

        if current_number_of_indents < previous_number_of_indents:
            # we springen 'terug' dus er moeten end-blocken in
            # bij meerdere terugsprongen sluiten we ook meerdere blokken

            difference_in_indents = (previous_number_of_indents - current_number_of_indents)

            for i in range(difference_in_indents):
                processed_code.append('end-block')

        #save to compare for next line
        previous_number_of_indents = current_number_of_indents

        #if indent remains the same, do nothing, just add line
        processed_code.append(line)

    # if the last line is indented, the end of the program is also the end of all indents
    # so close all blocks
    for i in range(current_number_of_indents):
        processed_code.append('end-block')
    return "\n".join(processed_code)


def transpile_inner(input_string, level, sub = 0):
    punctuation_symbols = ['!', '?', '.']
    level = int(level)

    parser = get_parser(level, sub)

    if level >= 8:
        input_string = preprocess_blocks(input_string)
        # print(input_string)

    try:
        program_root = parser.parse(input_string+ '\n').children[0]  # getting rid of the root could also be done in the transformer would be nicer
        abstract_syntaxtree = ExtractAST().transform(program_root)
        lookup_table = AllAssignmentCommands().transform(abstract_syntaxtree)

    except UnexpectedCharacters as e:
        try:
            location = e.line, e.column
            characters_expected = str(e.allowed) #not yet in use, could be used in the future (when our parser rules are better organize, now it says ANON*__12 etc way too often!)
            character_found  = beautify_parse_error(e.args[0])
            # print(e.args[0])
            # print(location, character_found, characters_expected)
            raise HedyException('Parse', level=level, location=location, character_found=character_found) from e
        except UnexpectedEOF:
            # this one can't be beautified (for now), so give up :)
            raise e

    # IsValid returns (True,) or (False, args, line)
    is_valid = IsValid().transform(program_root)

    if not is_valid[0]:
        _, args, line = is_valid

        # Apparently, sometimes 'args' is a string, sometimes it's a list of
        # strings ( are these production rule names?). If it's a list of
        # strings, just take the first string and proceed.
        if isinstance(args, list):
            args = args[0]
        if args == ' ':
            #the error here is a space at the beginning of a line, we can fix that!
            fixed_code = repair(input_string)
            if fixed_code != input_string: #only if we have made a successful fix
                result = transpile_inner(fixed_code, level, sub)
            raise HedyException('Invalid Space', level=level, line_number=line, fixed_code = result)
        elif args == 'print without quotes':
            # grammar rule is ignostic of line number so we can't easily return that here
            raise HedyException('Unquoted Text', level=level)
        else:
            invalid_command = args
            closest = closest_command(invalid_command, commands_per_level[level])
            if closest == None: #we couldn't find a suggestion because the command itself was found
                # clearly the error message here should be better or it should be a different one!
                raise HedyException('Parse', level=level, location=["?", "?"], keyword_found=invalid_command)
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
        python = ConvertToPython_2(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 3:
        python = ConvertToPython_3(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 4:
        python = ConvertToPython_4(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 5:
        python = ConvertToPython_5(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 6:
        python = ConvertToPython_6(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 7:
        if sub == 0:
            python = ConvertToPython_7(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        elif sub == 1:
            # Code conversion is the same as level 8
            python = ConvertToPython_8(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 8:
        python = ConvertToPython_8(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 9:
        python = ConvertToPython_9_10(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 10:
        # Code does not change for nesting
        python = ConvertToPython_9_10(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 11:
        python = ConvertToPython_11(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 12:
        python = ConvertToPython_12(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 13:
        python = ConvertToPython_13(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 14:
        python = ConvertToPython_14(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 15:
        python = ConvertToPython_15(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 16:
        python = ConvertToPython_16(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 17:
        python = ConvertToPython_17(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 18:
        python = ConvertToPython_18_19(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 19:
        python = ConvertToPython_18_19(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 20:
        python = ConvertToPython_20(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 21:
        python = ConvertToPython_21(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python
    elif level == 22:
        python = ConvertToPython_22(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        return python

    #Laura & Thera: hier kun je code voor de nieuwe levels toevoegen

    else:
        raise Exception('Levels over 7 are not implemented yet')

def execute(input_string, level):
    python = transpile(input_string, level)
    exec(python)

# f = open('output.py', 'w+')
# f.write(python)
# f.close()
