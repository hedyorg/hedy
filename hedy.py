import textwrap

from lark import Lark
from lark.exceptions import LarkError, UnexpectedEOF, UnexpectedCharacters
from lark import Tree, Transformer, visitors
from os import path
import utils
from collections import namedtuple
import hashlib
import re

# Some useful constants
HEDY_MAX_LEVEL = 23
MAX_LINES = 100

#dictionary to store transpilers
TRANSPILER_LOOKUP = {}

# Python keywords need hashing when used as var names
reserved_words = ['and', 'except', 'lambda', 'with', 'as', 'finally', 'nonlocal', 'while', 'assert', 'False', 'None', 'yield', 'break', 'for', 'not', 'class', 'from', 'or', 'continue', 'global', 'pass', 'def', 'if', 'raise', 'del', 'import', 'return', 'elif', 'in', 'True', 'else', 'is', 'try']

# Commands per Hedy level which are used to suggest the closest command when kids make a mistake
commands_per_level = {1: ['print', 'ask', 'echo', 'turn', 'forward'] ,
                      2: ['print', 'ask', 'is', 'turn', 'forward'],
                      3: ['print', 'ask', 'is', 'turn', 'forward'],
                      4: ['print', 'ask', 'is', 'if', 'turn', 'forward'],
                      5: ['print', 'ask', 'is', 'if', 'repeat', 'turn', 'forward'],
                      6: ['print', 'ask', 'is', 'if', 'repeat', 'turn', 'forward'],
                      7: ['print', 'ask', 'is', 'if', 'repeat', 'turn', 'forward'],
                      8: ['print', 'ask', 'is', 'if', 'for', 'turn', 'forward'],
                      9: ['print', 'ask', 'is', 'if', 'for', 'elif', 'turn', 'forward'],
                      10: ['print', 'ask', 'is', 'if', 'for', 'elif', 'turn', 'forward'],
                      11: ['print', 'ask', 'is', 'if', 'for', 'elif', 'turn', 'forward'],
                      12: ['print', 'ask', 'is', 'if', 'for', 'elif', 'turn', 'forward'],
                      13: ['print', 'ask', 'is', 'if', 'for', 'elif', 'turn', 'forward'],
                      14: ['print', 'ask', 'is', 'if', 'for', 'elif', 'turn', 'forward'],
                      15: ['print', 'ask', 'is', 'if', 'for', 'elif', 'turn', 'forward'],
                      16: ['print', 'ask', 'is', 'if', 'for', 'elif', 'turn', 'forward'],
                      17: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while', 'turn', 'forward'],
                      18: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while', 'turn', 'forward'],
                      19: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while', 'turn', 'forward'],
                      20: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while', 'turn', 'forward'],
                      21: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while', 'turn', 'forward'],
                      22: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while', 'turn', 'forward']
                      }

# we generate Python strings with ' always, so ' needs to be escaped but " works fine
# \ also needs to be escaped because it eats the next character
characters_that_need_escaping = ["\\", "'"]

character_skulpt_cannot_parse = re.compile('[^a-zA-Z0-9_]')

def hash_needed(name):
    # some elements are not names but processed names, i.e. random.choice(dieren)
    # they should not be hashed (this won't break because these characters cannot be used in vars
    if '[' in name or '(' in name:
        return False

    return name in reserved_words or character_skulpt_cannot_parse.search(name) != None

def hash_var(name):
    if hash_needed(name):
        # hash "illegal" var names
        # being reservered keywords
        # or non-latin vars to comply with Skulpt, which does not implement PEP3131 :(
        # prepend with v for when hash starts with a number

        hash_object = hashlib.md5(name.encode())
        return "v" + hash_object.hexdigest()
    else:
        return name

def closest_command(invalid_command, known_commands):
    # First search for 100% match of known commands
    #
    #  closest_command() searches for known commands in an invalid command.
    #
    #  It will return the known command which is closest positioned at the beginning.
    #  It will return '' if the invalid command does not contain any known command.
    #
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

class InvalidSpaceException(HedyException):
    def __init__(self, level, line_number, fixed_code):
        super().__init__('Invalid Space')
        self.level = level
        self.line_number = line_number
        self.fixed_code = fixed_code

class ParseException(HedyException):
    def __init__(self, level, location, keyword_found=None, character_found=None):
        super().__init__('Parse')
        self.level = level
        self.location = location
        self.keyword_found = keyword_found
        self.character_found = character_found

class UndefinedVarException(HedyException):
    def __init__(self, **arguments):
        super().__init__('Var Undefined', **arguments)

class WrongLevelException(HedyException):
    def __init__(self, **arguments):
        super().__init__('Wrong Level', **arguments)

class InputTooBigException(HedyException):
    def __init__(self, **arguments):
        super().__init__('Too Big', **arguments)

class InvalidCommandException(HedyException):
    def __init__(self, **arguments):
        super().__init__('Invalid', **arguments)

class IncompleteCommandException(HedyException):
    def __init__(self, **arguments):
        super().__init__('Incomplete', **arguments)

class UnquotedTextException(HedyException):
    def __init__(self, **arguments):
        super().__init__('Unquoted Text', **arguments)

class EmptyProgramException(HedyException):
    def __init__(self):
        super().__init__('Empty Program')

class LonelyEchoException(HedyException):
    def __init__(self):
        super().__init__('Lonely Echo')

class CodePlaceholdersPresentException(HedyException):
    def __init__(self):
        super().__init__('Has Blanks')

class IndentationException(HedyException):
    def __init__(self, **arguments):
        super().__init__('Unexpected Indentation', **arguments)

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

class AllAssignmentCommands(Transformer):
    # returns a list of variable and list access
    # so these can be excluded when printing

    # relevant nodes (list acces, ask, assign) are transformed into strings
    # higher in the tree (through default rule), we filter on only string arguments, of lists with string arguments

    def filter_ask_assign(self, args):
        ask_assign = []
        for a in args:
            # strings (vars remaining in the tree) are added directly
            if type(a) is str:
                ask_assign.append(a)
            # lists are seached further for string members (vars)
            elif type(a) is list:
                sub_a_ask_assign = self.filter_ask_assign(a)
                for sub_a in sub_a_ask_assign:
                    ask_assign.append(sub_a)
        return ask_assign

    def for_loop(self, args):
      # for loop iterator is a var so should be added to the list of vars
      iterator = str(args[0])
      commands = args[1:]
      return [iterator] + self.filter_ask_assign(args)

    def input(self, args):
        # return left side of the =
        return args[0]

    def ask(self, args):
        # try is needed cause in level 1 ask has not variable in front
        try:
            return args[0]
        except:
            return None

    def assign(self, args):
        return args[0]

    def assign_list(self, args):
        return args[0]

    # list access is accessing a variable, so must be escaped
    # for example we print(dieren[1]) not print('dieren[1]')
    def list_access(self, args):
        listname = args[0]
        if args[1] == 'random':
            return 'random.choice(' + listname + ')'
        else:
            return listname + '[' + args[1] + ']'

    # additions Laura, to be checked for higher levels:
    def list_access_var(self, args):
        return args[0]

    def change_list_item(self, args):
        return args[0]

    def text(self, args):
        # text never contains a variable
        return None

    def var_access(self, args):
        # just accessing (printing) a variable does not count toward the lookup table
        return None

    def var(self, args):
        # the var itself (when in an assignment) should be added
        name = args[0]
        return name

    def punctuation(self, args):
        # is never a variable (but should be removed from the tree or it will be seen as one!)
        return None

    def __default__(self, args, children, meta):
        return self.filter_ask_assign(children)

class AllAssignmentCommandsHashed(Transformer):
    # returns a list of variable and list access
    # so these can be excluded when printing

    # this version returns all hashed var names

    def filter_ask_assign(self, args):
        ask_assign = []
        for a in args:
            # strings (vars remaining in the tree) are added directly
            if type(a) is str:
                ask_assign.append(a)
            # lists are seached further for string members (vars)
            elif type(a) is list:
                sub_a_ask_assign = self.filter_ask_assign(a)
                for sub_a in sub_a_ask_assign:
                    ask_assign.append(sub_a)
        return ask_assign

    def for_loop(self, args):
      # for loop iterator is a var so should be added to the list of vars
      iterator = str(args[0])
      iterator_hashed = hash_var(iterator)
      return [iterator_hashed] + self.filter_ask_assign(args)

    def input(self, args):
        # return left side of the =
        return hash_var(args[0])

    def ask(self, args):
        # try is needed cause in level 1 ask has not variable in front
        try:
            return hash_var(args[0])
        except:
            return None

    def assign(self, args):
        return hash_var(args[0])

    def assign_list(self, args):
        return hash_var(args[0])

    # list access is accessing a variable, so must be escaped
    # for example we print(dieren[1]) not print('dieren[1]')
    def list_access(self, args):
        listname = hash_var(args[0])
        if args[1] == 'random':
            return 'random.choice(' + listname + ')'
        else:
            return listname + '[' + args[1] + ']'

    # additions Laura, to be checked for higher levels:
    def list_access_var(self, args):
        return hash_var(args[0])

    def change_list_item(self, args):
        return hash_var(args[0])

    def text(self, args):
        # text never contains a variable
        return None

    def var_access(self, args):
        # just accessing (printing) a variable does not count toward the lookup table
        return None

    def var(self, args):
        # the var itself (when in an assignment) should be added
        name = hash_var(args[0])
        return name

    def punctuation(self, args):
        # is never a variable (but should be removed from the tree or it will be seen as one!)
        return None

    def __default__(self, args, children, meta):
        return self.filter_ask_assign(children)

def flatten_list_of_lists_to_list(args):
    flat_list = []
    for element in args:
        if isinstance(element, str): #str needs a special case before list because a str is also a list and we don't want to split all letters out
            flat_list.append(element)
        elif isinstance(element, list):
            flat_list += flatten_list_of_lists_to_list(element)
        else:
            flat_list.append(element)
    return flat_list

def are_all_arguments_true(args):
    bool_arguments = [x[0] for x in args]
    arguments_of_false_nodes = flatten_list_of_lists_to_list([x[1] for x in args if not x[0]])
    return all(bool_arguments), arguments_of_false_nodes

# this class contains code shared between IsValid and IsComplete, which are quite similar
# because both filter out some types of 'wrong' nodes
# TODO: this could also use a default lark rule like AllAssignmentCommands does now
class Filter(Transformer):
    def __default__(self, args, children, meta):
        return are_all_arguments_true(children)

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
    def text(self, args):
        return all(args), ''.join([c for c in args])

class UsesTurtle(Transformer):
    # returns true if Forward or Turn are in the tree, false otherwise
    def __default__(self, args, children, meta):
        if len(children) == 0:  # no children? you are a leaf that is not Turn or Forward, so you are no Turtle command
            return False
        else:
            if type(children[0]) == bool:
                return any(children) # children? if any is true there is a Turtle leaf
            else:
                return False # some nodes like text and punctuation have text children (their letters) these are not turtles

    def forward(self, args):
        return True

    def turn(self, args):
        return True

    # somehow a token (or only this token?) is not picked up by the default rule so it needs
    # its own rule
    def NUMBER(self, args):
        return False

    def NAME(self, args):
        return False





class IsValid(Filter):
    # all rules are valid except for the "Invalid" production rule
    # this function is used to generate more informative error messages
    # tree is transformed to a node of [Bool, args, command number]
    def program(self, args):
        if len(args) == 0:
            return False, "empty program", 1
        return super().program(args)

    def invalid_space(self, args):
        # return space to indicate that line starts in a space
        return False, " "

    def print_nq(self, args):
        # return error source to indicate what went wrong
        return False, "print without quotes"

    def invalid(self, args):
        # return the first argument to place in the error message
        # TODO: this will not work for misspelling 'at', needs to be improved!
        return False, args[0][1]

    #other rules are inherited from Filter

def valid_echo(ast):
    commands = ast.children
    command_names = [x.children[0].data for x in commands]
    no_echo = not 'echo' in command_names

    #no echo is always ok!

    #otherwise, both have to be in the list and echo shold come after
    return no_echo or ('echo' in command_names and 'ask' in command_names) and command_names.index('echo') > command_names.index('ask')


class IsComplete(Filter):
    def __init__(self, level):
        self.level = level
    # print, ask an echo can miss arguments and then are not complete
    # used to generate more informative error messages
    # tree is transformed to a node of [True] or [False, args, line_number]

    def ask(self, args):
        # in level 1 ask without arguments means args == []
        # in level 2 and up, ask without arguments is a list of 1, namely the var name
        incomplete = (args == [] and self.level==1) or (len(args) == 1 and self.level >= 2)
        return not incomplete, 'ask'
    def print(self, args):
        return args != [], 'print'
    def input(self, args):
        return args != [], 'input'
    def length(self, args):
        return args != [], 'len'
    def print_nq(self, args):
        return args != [], 'print level 2'
    def echo(self, args):
        #echo may miss an argument
        return True, 'echo'

    #other rules are inherited from Filter

def process_characters_needing_escape(value):
    # defines what happens if a kids uses ' or \ in in a string
    for c in characters_that_need_escaping:
        value = value.replace(c, f'\{c}')
    return value

#decorator used to store each class in the lookup table
def hedy_transpiler(level):
  def decorator(c):
    TRANSPILER_LOOKUP[level] = c
    return c
  return decorator

@hedy_transpiler(level=1)
class ConvertToPython_1(Transformer):

    def __init__(self, punctuation_symbols, lookup):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup

    def get_fresh_var(self, name):
        while name in self.lookup:
            name = '_' + name
        return name

    def program(self, args):
        return '\n'.join([str(c) for c in args])
    def command(self, args):
        return args[0]

    def text(self, args):
        return ''.join([str(c) for c in args])
    def print(self, args):
        # escape needed characters
        argument = process_characters_needing_escape(args[0])

        return "print('" + argument + "')"
    def echo(self, args):
        if len(args) == 0:
            return "print(answer)" #no arguments, just print answer

        argument = process_characters_needing_escape(args[0])
        return "print('" + argument + "'+answer)"

    def ask(self, args):

        argument = process_characters_needing_escape(args[0])
        return "answer = input('" + argument + "')"

    def forward(self,args):
        # when a not-number is given, we simply use 50 as default
        try:
            parameter = int(args[0])
        except:
            parameter = 50
        return self.make_forward(parameter)

    def make_forward(self, parameter):
        return f"t.forward({parameter})""\ntime.sleep(0.1)"

    def turn(self, args):
        if len(args) == 0:
            return "t.right(90)" #no arguments works, and means a right turn

        argument = args[0]
        if argument in self.lookup:        #is the argument a variable? if so, use that
            return f"t.right({argument})"
        elif argument.isnumeric():         #numbers can also be passed through
            return f"t.right({argument})"
        elif argument == 'left':
            return "t.left(90)"
        else:
            return "t.right(90)" #something else also defaults to right turn

def process_variable(name, lookup):
    #processes a variable by hashing and escaping when needed
    if name in lookup:
        return hash_var(name)
    else:
        return f"'{name}'"

def process_variable_for_fstring(name, lookup):
    #processes a variable by hashing and escaping when needed
    if name in lookup:
        return "{" + hash_var(name) + "}"
    else:
        return name

@hedy_transpiler(level=2)
class ConvertToPython_2(ConvertToPython_1):
    def punctuation(self, args):
        return ''.join([str(c) for c in args])
    def var(self, args):
        name = ''.join(args)
        name = args[0]
        return hash_var(name)
        # return "_" + name if name in reserved_words else name
    def print(self, args):
        argument_string = ""
        i = 0

        for argument in args:
            # escape quotes if kids accidentally use them at level 2
            argument = process_characters_needing_escape(argument)

            # final argument and punctuation arguments do not have to be separated with a space, other do
            if i == len(args)-1 or args[i+1] in self.punctuation_symbols:
                space = ''
            else:
                space = " "

            argument_string += process_variable_for_fstring(argument, self.lookup)
            argument_string += space

            i = i + 1

        return f"print(f'{argument_string}')"

    def forward(self, args):
        # no args received? default to 50
        parameter = 50

        if len(args) > 0:
            parameter = args[0]

        #if the parameter is a variable, print as is
        # otherwise, see if we got a number. if not, simply use 50 as default
        try:
            if parameter not in self.lookup:
                parameter = int(parameter)
        except:
            parameter = 50
        return self.make_forward(parameter)

    def ask(self, args):
        var = args[0]
        all_parameters = ["'" + process_characters_needing_escape(a) + "'" for a in args[1:]]
        return f'{var} = input(' + '+'.join(all_parameters) + ")"
    def assign(self, args):
        parameter = args[0]
        value = args[1]
        #if the assigned value contains single quotes, escape them
        value = process_characters_needing_escape(value)
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

def is_quoted(s):
    return s[0] == "'" and s[-1] == "'"

#TODO: punctuation chars not be needed for level2 and up anymore, could be removed
@hedy_transpiler(level=3)
class ConvertToPython_3(ConvertToPython_2):

    def var_access(self, args):
        name = args[0]
        return hash_var(name)

    def text(self, args):
        return ''.join([str(c) for c in args])

    def check_print_arguments(self, args):
        # this function checks whether arguments of a print are valid
        #we can print if all arguments are either quoted OR they are all variables

        unquoted_args = [a for a in args if not is_quoted(a)]
        unquoted_in_lookup = [a in self.lookup for a in unquoted_args]

        if unquoted_in_lookup == [] or all(unquoted_in_lookup):
            # all good? return for further processing
            return args
        else:
            # return first name with issue
            # note this is where issue #832 can be addressed by checking whether
            # first_unquoted_var ius similar to something in the lookup list
            first_unquoted_var = unquoted_args[0]
            raise UndefinedVarException(name=first_unquoted_var)

    def print(self, args):
        args = self.check_print_arguments(args)
        argument_string = ''
        for argument in args:
            argument = argument.replace("'", '') #no quotes needed in fstring
            argument_string += process_variable_for_fstring(argument, self.lookup)

        return f"print(f'{argument_string}')"

    def print_nq(self, args):
        return ConvertToPython_2.print(self, args)

    def ask(self, args):
        args_new = []
        var = args[0]
        remaining_args = args[1:]

        return f'{var} = input(' + '+'.join(remaining_args) + ")"

def indent(s):
    lines = s.split('\n')
    return '\n'.join(['  ' + l for l in lines])

@hedy_transpiler(level=4)
class ConvertToPython_4(ConvertToPython_3):
    def list_access_var(self, args):
        var = hash_var(args[0])
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
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        return f"{arg0} == {arg1}" #no and statements
    def in_list_check(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        return f"{arg0} in {arg1}"

@hedy_transpiler(level=5)
class ConvertToPython_5(ConvertToPython_4):

    def print(self, args):
        # we only check non-Tree (= non calculation) arguments
        self.check_print_arguments([a for a in args if not type(a) is Tree])


        #force all to be printed as strings (since there can not be int arguments)
        args_new = []
        for a in args:
            if type(a) is Tree:
                args_new.append("{" + a.children + "}")
            else:
                a = a.replace("'", "") #no quotes needed in fstring
                args_new.append(process_variable_for_fstring(a, self.lookup))

        arguments = ''.join(args_new)
        return "print(f'" + arguments + "')"

    #we can now have ints as types so chck must force str
    def equality_check(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        #TODO if we start using fstrings here, this str can go
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

    def process_token_or_tree(self, argument):
        if type(argument) is Tree:
            return f'{str(argument.children)}'
        else:
            return f'int({argument})'

    def process_calculation(self, args, operator):
        # arguments of a sum are either a token or a
        # tree resulting from earlier processing
        # for trees we need to grap the inner string
        # for tokens we add int around them

        args = [self.process_token_or_tree(a) for a in args]
        return Tree('sum', f'{args[0]} {operator} {args[1]}')

    def addition(self, args):
        return self.process_calculation(args, '+')

    def substraction(self, args):
        return self.process_calculation(args, '-')

    def multiplication(self, args):
        return self.process_calculation(args, '*')

    def division(self, args):
        return self.process_calculation(args, '//')

@hedy_transpiler(level=6)
class ConvertToPython_6(ConvertToPython_5):
    def number(self, args):
        return ''.join(args)

    def repeat(self, args):
        var_name = self.get_fresh_var('i')
        times = process_variable(args[0], self.lookup)
        command = args[1]
        return f"""for {var_name} in range(int({str(times)})):
{indent(command)}"""

@hedy_transpiler(level=7)
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
            return args[0]
        else:
        # this is list_access
            return args[0] + "[" + str(args[1]) + "]" if type(args[1]) is not Tree else "random.choice(" + str(args[0]) + ")"

@hedy_transpiler(level=8)
class ConvertToPython_8(ConvertToPython_7):
    def repeat_list(self, args):
      args = [a for a in args if a != ""]  # filter out in|dedent tokens

      body = "\n".join([indent(x) for x in args[2:]])

      return f"for {args[0]} in {args[1]}:\n{body}"



@hedy_transpiler(level=9)
class ConvertToPython_9(ConvertToPython_8):
    def for_loop(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        body = "\n".join([indent(x) for x in args[3:]])
        stepvar_name = self.get_fresh_var('step')
        return f"""{stepvar_name} = 1 if int({args[1]}) < int({args[2]}) else -1
for {args[0]} in range(int({args[1]}), int({args[2]}) + {stepvar_name}, {stepvar_name}):
{body}"""
@hedy_transpiler(level=10)
@hedy_transpiler(level=11)
class ConvertToPython_10_11(ConvertToPython_9):
    def elifs(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [indent(x) for x in args[1:]]
        return "\nelif " + args[0] + ":\n" + "\n".join(all_lines)

@hedy_transpiler(level=12)
class ConvertToPython_12(ConvertToPython_10_11):
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

@hedy_transpiler(level=13)
class ConvertToPython_13(ConvertToPython_12):
    def assign_list(self, args):
        parameter = args[0]
        values = [a for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

    def list_access_var(self, args):
        var = hash_var(args[0])
        if not isinstance(args[2], str):
            if args[2].data == 'random':
                return var + '=random.choice(' + args[1] + ')'
        else:
            return var + '=' + args[1] + '[' + args[2] + '-1]'

    def list_access(self, args):
        if args[1] == 'random':
            return 'random.choice(' + args[0] + ')'
        else:
            list_access_shifted = args[0] + '[' + args[1] + '-1]'
            # when printing later, we need to know this is a var
            self.lookup.append(list_access_shifted)
            return list_access_shifted

    def change_list_item(self, args):
        return args[0] + '[' + args[1] + '-1] = ' + args[2]
# Custom transformer that can both be used bottom-up or top-down

@hedy_transpiler(level=14)
class ConvertToPython_14(ConvertToPython_13):
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
                    # FH, June 21 the addition of _true/false is a bit of a hack. cause they are first seen as vars that at reserved words, they are then hashed and we undo that here
                    # could/should be fixed in the grammar!

                    if value == 'true' or value == 'True' or value == hash_var('True') or value == hash_var('true'):
                        return parameter + " = True"
                    elif value == 'false' or value == 'False' or value == hash_var('False') or value == hash_var('false'):
                        return parameter + " = False"
                    else:
                        return parameter + " = '" + value + "'"
        else:
            parameter = args[0]
            values = args[1:]
            return parameter + " = [" + ", ".join(values) + "]"

    def equality_check(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        if arg1 == '\'True\'' or arg1 == '\'true\'':
            return f"{arg0} == True"
        elif arg1 == '\'False\'' or arg1 == '\'false\'':
            return f"{arg0} == False"
        else:
            return f"str({arg0}) == str({arg1})" #no and statements

@hedy_transpiler(level=15)
class ConvertToPython_15(ConvertToPython_14):
    def andcondition(self, args):
        return ' and '.join(args)
    def orcondition(self, args):
        return ' or '.join(args)

@hedy_transpiler(level=16)
class ConvertToPython_16(ConvertToPython_15):
    def comment(self, args):
        return f"# {args}"

@hedy_transpiler(level=17)
class ConvertToPython_17(ConvertToPython_16):
    def smaller(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        if len(args) == 2:
            return f"int({arg0}) < int({arg1})"  # no and statements
        else:
            return f"int({arg0}) < int({arg1}) and {args[2]}"

    def bigger(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        if len(args) == 2:
            return f"int({arg0}) > int({arg1})"  # no and statements
        else:
            return f"int({arg0}) > int({arg1}) and {args[2]}"

@hedy_transpiler(level=18)
class ConvertToPython_18(ConvertToPython_17):
    def while_loop(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [indent(x) for x in args[1:]]
        return "while " + args[0] + ":\n"+"\n".join(all_lines)

@hedy_transpiler(level=19)
@hedy_transpiler(level=20)
class ConvertToPython_19_20(ConvertToPython_18):
    def length(self, args):
        arg0 = args[0]
        length_string = f"len({arg0})"

        #when accessing len we need to know it is a var
        self.lookup.append(length_string)
        return length_string

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

@hedy_transpiler(level=21)
class ConvertToPython_21(ConvertToPython_19_20):
    def equality_check(self, args):
        if type(args[0]) is Tree:
            return args[0].children + " == int(" + args[1] + ")"
        if type(args[1]) is Tree:
            return "int(" + args[0] + ") == " + args[1].children
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        if arg1 == '\'True\'' or arg1 == '\'true\'':
            return f"{arg0} == True"
        elif arg1 == '\'False\'' or arg1 == '\'false\'':
            return f"{arg0} == False"
        else:
            return f"str({arg0}) == str({arg1})"  # no and statements

@hedy_transpiler(level=22)
class ConvertToPython_22(ConvertToPython_21):
    def not_equal(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        if len(args) == 2:
            return f"str({arg0}) != str({arg1})"  # no and statements
        else:
            return f"str({arg0}) != str({arg1}) and {args[2]}"

@hedy_transpiler(level=23)
class ConvertToPython_23(ConvertToPython_22):
    def smaller_equal(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        if len(args) == 2:
            return f"int({arg0}) <= int({arg1})"  # no and statements
        else:
            return f"int({arg0}) <= int({arg1}) and {args[2]}"

    def bigger_equal(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        if len(args) == 2:
            return f"int({arg0}) >= int({arg1})"  # no and statements
        else:
            return f"int({arg0}) >= int({arg1}) and {args[2]}"


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


def create_grammar(level):
    # start with creating the grammar for level 1
    result = get_full_grammar_for_level(1)

    # then keep merging new grammars in
    for i in range(2, level+1):
        grammar_text_i = get_additional_rules_for_level(i)
        result = merge_grammars(result, grammar_text_i)

    # ready? Save to file to ease debugging
    # this could also be done on each merge for performance reasons
    save_total_grammar_file(level, result)

    return result

def save_total_grammar_file(level, grammar):
    # Load Lark grammars relative to directory of current file
    script_dir = path.abspath(path.dirname(__file__))
    filename = "level" + str(level) + "-Total.lark"
    loc = path.join(script_dir, "grammars-Total", filename)
    file = open(loc, "w", encoding="utf-8")
    file.write(grammar)
    file.close()

def get_additional_rules_for_level(level, sub = 0):
    script_dir = path.abspath(path.dirname(__file__))
    if sub:
        filename = "level" + str(level) + "-" + str(sub) + "-Additions.lark"
    else:
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


def get_parser(level):
    """Return the Lark parser for a given level.

    Uses caching if Hedy is NOT running in development mode.
    """
    key = str(level)
    existing = PARSER_CACHE.get(key)
    if existing and not utils.is_debug_mode():
        return existing
    grammar = create_grammar(level)
    ret = Lark(grammar, regex=True)
    PARSER_CACHE[key] = ret
    return ret

ParseResult = namedtuple('ParseResult', ['code', 'has_turtle'])

def transpile(input_string, level):
    try:
        transpile_result = transpile_inner(input_string, level)
        return transpile_result
    except ParseException as ex:
        # This is the 'fall back' transpilation
        # that should surely be improved!!
        # we retry HedyExceptions of the type Parse (and Lark Errors) but we raise Invalids

        #try 1 level lower
        if level > 1:
            try:
                new_level = level - 1
                result = transpile_inner(input_string, new_level)
            except (LarkError, HedyException) as innerE:
                # Parse at `level - 1` failed as well, just re-raise original error
                raise ex
            # If the parse at `level - 1` succeeded, then a better error is "wrong level"
            raise WrongLevelException(correct_code=result.code, working_level=new_level, original_level=level) from ex


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

def beautify_parse_error(character_found):
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
    line_number = 0
    for line in lines:
        line_number += 1
        leading_spaces = find_indent_length(line)

        #first encounter sets indent size for this program
        if indent_size == None and leading_spaces > 0:
            indent_size = leading_spaces

        #calculate nuber of indents if possible
        if indent_size != None:
            current_number_of_indents = leading_spaces // indent_size

        if current_number_of_indents - previous_number_of_indents > 1:
            raise IndentationException(line_number = line_number, leading_spaces = leading_spaces, indent_size = indent_size)

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

def contains_blanks(code):
    return (" _ " in code) or (" _\n" in code)


def transpile_inner(input_string, level):
    number_of_lines = input_string.count('\n')

    #parser is not made for huge programs!
    if number_of_lines > MAX_LINES:
        raise InputTooBigException(lines_of_code=number_of_lines, max_lines=MAX_LINES)

    input_string = input_string.replace('\r\n', '\n')
    punctuation_symbols = ['!', '?', '.']
    level = int(level)
    parser = get_parser(level)

    if contains_blanks(input_string):
        raise CodePlaceholdersPresentException()


    if level >= 3:
        input_string = input_string.replace("\\", "\\\\")

    #in level 7 we add indent-dedent blocks to the code before parsing
    if level >= 7:
        input_string = preprocess_blocks(input_string)

    try:
        program_root = parser.parse(input_string+ '\n').children[0]  # getting rid of the root could also be done in the transformer would be nicer
        abstract_syntaxtree = ExtractAST().transform(program_root)
        lookup_table = AllAssignmentCommands().transform(abstract_syntaxtree)

        # also add hashes to list
        # note that we do not (and cannot) hash the var names only, we also need to be able to process
        # random.choice(প্রাণী)
        hashed_lookups = AllAssignmentCommandsHashed().transform(abstract_syntaxtree)

        lookup_table += hashed_lookups

    except UnexpectedCharacters as e:
        try:
            location = e.line, e.column
            characters_expected = str(e.allowed) #not yet in use, could be used in the future (when our parser rules are better organize, now it says ANON*__12 etc way too often!)
            character_found  = beautify_parse_error(e.char)
            # print(e.args[0])
            # print(location, character_found, characters_expected)
            raise ParseException(level=level, location=location, character_found=character_found) from e
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
                result = transpile_inner(fixed_code, level)
            raise InvalidSpaceException(level, line, result.code)
        elif args == 'print without quotes':
            # grammar rule is ignostic of line number so we can't easily return that here
            raise UnquotedTextException(level=level)
        elif args == 'empty program':
            raise EmptyProgramException()
        else:
            invalid_command = args
            closest = closest_command(invalid_command, commands_per_level[level])
            if closest == None: #we couldn't find a suggestion because the command itself was found
                # clearly the error message here should be better or it should be a different one!
                raise ParseException(level=level, location=["?", "?"], keyword_found=invalid_command)
            raise InvalidCommandException(invalid_command=invalid_command, level=level, guessed_command=closest)

    is_complete = IsComplete(level).transform(program_root)
    if not is_complete[0]:
        incomplete_command = is_complete[1][0]
        line = is_complete[2]
        raise IncompleteCommandException(incomplete_command=incomplete_command, level=level, line_number=line)

    if not valid_echo(program_root):
        raise LonelyEchoException()

    try:
        if level <= HEDY_MAX_LEVEL:
            #grab the right transpiler from the lookup
            transpiler = TRANSPILER_LOOKUP[level]
            python = transpiler(punctuation_symbols, lookup_table).transform(abstract_syntaxtree)
        else:
           raise Exception(f'Levels over {HEDY_MAX_LEVEL} not implemented yet')
    except visitors.VisitError as E:
        # Exceptions raised inside visitors are wrapped inside VisitError. Unwrap it if it is a
        # HedyException to show the intended error message.
        if isinstance(E.orig_exc, HedyException):
            raise E.orig_exc
        else:
            raise E

    has_turtle = UsesTurtle().transform(program_root)

    return ParseResult(python, has_turtle)

def execute(input_string, level):
    python = transpile(input_string, level)
    if python.has_turtle:
        raise HedyException("hedy.execute doesn't support turtle")
    exec(python.code)

# f = open('output.py', 'w+')
# f.write(python)
# f.close()
