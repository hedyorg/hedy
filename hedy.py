import textwrap

from lark import Lark
from lark.exceptions import LarkError, UnexpectedEOF, UnexpectedCharacters, VisitError
from lark import Tree, Transformer, visitors, v_args
from os import path

import hedy
import utils
from collections import namedtuple
import hashlib
import re
from dataclasses import dataclass, field
import exceptions

# Some useful constants
HEDY_MAX_LEVEL = 14
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
                      22: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while', 'turn', 'forward'],
                      23: ['print', 'ask', 'is', 'if', 'for', 'elif', 'while', 'turn', 'forward']
                      }

# Commands and their types per level (only partially filled!)
commands_and_types_per_level = {
    1: {'print': ['string', 'integer'],
        'ask': ['string'],
        'turn': ['string', 'integer'],
        'forward': ['integer']},
    2: {'at random': ['list']},
    5: {'sum': ['integer'],
        'addition': ['integer', 'float']},
    10: {'for_loop': ['integer']},
    11: {'sum': ['integer', 'float'],
         'addition': ['integer', 'float', 'string'],
         'print': ['string', 'integer', 'float']},
    12: {'input': ['string']},
    13: {'print': ['string', 'integer', 'float', 'list']}
  }

# we generate Python strings with ' always, so ' needs to be escaped but " works fine
# \ also needs to be escaped because it eats the next character
characters_that_need_escaping = ["\\", "'"]

character_skulpt_cannot_parse = re.compile('[^a-zA-Z0-9_]')

def hash_needed(name):
    # this function is now applied on something str sometimes Assignment
    # no pretty but it will all be removed once we no longer need hashing (see issue #959) so ok for now

    if not isinstance(name, str):
        name = name.name

    # some elements are not names but processed names, i.e. random.choice(dieren)
    # they should not be hashed
    # these are either of type assignment and operation or already processed and then contain ( or [
    if (type(name) is LookupEntry and name.skip_hashing) or (isinstance(name, str) and '[' in name or '(' in name):
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
    return style_closest_command(min_command)


def style_closest_command(command):
    return f'<span class="command-highlighted">{command}</span>'

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


@dataclass
class InvalidInfo:
    error_type: str
    command: str = ''
    arguments: list = field(default_factory=list)
    line: int = 0


# used in to construct lookup table entries and infer their type
@dataclass
class LookupEntry:
    name: str
    tree: Tree
    skip_hashing: bool
    type_: str = None


class TypedTree(Tree):
    def __init__(self, data, children, meta, type_):
        super().__init__(data, children, meta)
        self.type_ = type_


class ExtractAST(Transformer):
    # simplifies the tree: f.e. flattens arguments of text, var and punctuation for further processing
    def text(self, args):
        return Tree('text', [''.join([str(c) for c in args])])

    def INT(self, args):
        return Tree('integer', [str(args)])

    #level 2
    def var(self, args):
        return Tree('var', [''.join([str(c) for c in args])])

    def punctuation(self, args):
        return Tree('punctuation', [''.join([str(c) for c in args])])

    def list_access(self, args):
        if type(args[1]) == Tree:
            if "random" in args[1].data:
                return Tree('list_access', [args[0], 'random'])
            else:
                return Tree('list_access', [args[0], args[1].children[0]])
        else:
            return Tree('list_access', [args[0], args[1]])

    #level 5
    def unsupported_number(self, args):
        return Tree('unsupported_number', [''.join([str(c) for c in args])])

    #level 11
    def NUMBER(self, args):
        return Tree('number', [str(args)])


# This visitor collects all entries that should be part of the lookup table. It only stores the name of the entry
# (e.g. 'animal') and its value as a tree node (e.g. Tree['text', ['cat']]) which is later used to infer the type
# of the entry. This preliminary traversal is needed to avoid issues with loops in which an iterator variable is
# used in the inner commands which are visited before the iterator variable is added to the lookup.
class LookupEntryCollector(visitors.Visitor):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.lookup = []

    def ask(self, tree):
        # in level 1 there is no variable name on the left side of the ask command
        if self.level > 1:
            self.add_to_lookup(tree.children[0].children[0], tree)

    def input(self, tree):
        var_name = tree.children[0].children[0]
        self.add_to_lookup(var_name, tree)

    def assign(self, tree):
        var_name = tree.children[0].children[0]
        self.add_to_lookup(var_name, tree.children[1])

    def assign_list(self, tree):
        var_name = tree.children[0].children[0]
        self.add_to_lookup(var_name, tree)

    # list access is added to the lookup table not because it must be escaped
    # for example we print(dieren[1]) not print('dieren[1]')
    def list_access(self, tree):
        list_name = hash_var(tree.children[0].children[0])
        if tree.children[1] == 'random':
            name = f'random.choice({list_name})'
        else:
            # We want list access to be 1-based instead of 0-based, hence the -1
            name = f'{list_name}[{tree.children[1]}-1]'
        self.add_to_lookup(name, tree, True)

    def list_access_var(self, tree):
        self.add_to_lookup(tree.children[0].children[0], tree, True)

    def change_list_item(self, tree):
        self.add_to_lookup(tree.children[0].children[0], tree, True)

    def repeat_list(self, tree):
        iterator = str(tree.children[0].children[0])
        # the tree is trimmed to skip contain the inner commands of the loop since
        # they are not needed to infer the type of the iterator variable
        trimmed_tree = Tree(tree.data, tree.children[0:2], tree.meta)
        self.add_to_lookup(iterator, trimmed_tree)

    def for_loop(self, tree):
        iterator = str(tree.children[0])
        # the tree is trimmed to skip contain the inner commands of the loop since
        # they are not needed to infer the type of the iterator variable
        trimmed_tree = Tree(tree.data, tree.children[0:3], tree.meta)
        self.add_to_lookup(iterator, trimmed_tree)

    def add_to_lookup(self, name, tree, skip_hashing=False):
        self.lookup.append(LookupEntry(name, tree, skip_hashing))


# The transformer infers the type of the partial trees collected in the lookup entries. The type 'any' is used when the
# type cannot be inferred, and the type 'None' is used when the node does not have a return type, e.g. a command.
# The transformer is meant to be non-intrusive and avoid false positives. However, it will raise an error if the type
# of a lookup entry is inferred and it is obviously wrong, e.g:
# a is 'test'
# b is a + 1
@v_args(tree=True)
class TypeInferrer(Transformer):
    def __init__(self, lookup, level):
        super().__init__()
        self.lookup = lookup
        self.level = level

    def ask(self, tree):
        return self.to_typed_tree(tree, 'any')

    def input(self, tree):
        return self.to_typed_tree(tree, 'any')

    def assign_list(self, tree):
        return self.to_typed_tree(tree, 'list')

    # TODO: list_access, list_access_var and repeat_list types can be inferred but for now use 'any'
    def list_access(self, tree):
        return self.to_typed_tree(tree, 'any')

    def list_access_var(self, tree):
        return self.to_typed_tree(tree, 'any')

    def repeat_list(self, tree):
        return self.to_typed_tree(tree, 'any')

    def for_loop(self, tree):
        command = 'for_loop'
        allowed_types = get_allowed_types(command, self.level)

        start_type = self.check_type_allowed(command, allowed_types, tree.children[1])
        self.check_type_allowed(command, allowed_types, tree.children[2])

        return self.to_typed_tree(tree, start_type)

    def integer(self, tree):
        return self.to_typed_tree(tree, 'integer')

    def text(self, tree):
        return self.to_typed_tree(tree, 'string')

    def text_in_quotes(self, tree):
        return self.to_typed_tree(tree, 'string')

    def var_access(self, tree):
        return self.to_typed_tree(tree, 'string')

    def var(self, tree):
        type_ = self.get_type(tree)
        return self.to_typed_tree(tree, type_)

    def number(self, tree):
        number = tree.children[0]
        if is_int(number):
            return self.to_typed_tree(tree, 'integer')
        if is_float(number):
            return self.to_typed_tree(tree, 'float')
        # We managed to parse a number that cannot be parsed by python
        raise exceptions.ParseException(level=self.level, location='', found=number)

    def substraction(self, tree):
        return self.to_sum_typed_tree(tree, 'sum')

    def addition(self, tree):
        return self.to_sum_typed_tree(tree, 'addition')

    def multiplication(self, tree):
        return self.to_sum_typed_tree(tree, 'sum')

    def division(self, tree):
        return self.to_sum_typed_tree(tree, 'sum')

    def to_sum_typed_tree(self, tree, command):
        expr_type = self.get_sum_type(tree, command)
        return TypedTree(tree.data, tree.children, tree.meta, expr_type)

    def get_sum_type(self, tree, command):
        allowed_types = get_allowed_types(command, self.level)

        left_type = self.check_type_allowed(command, allowed_types, tree.children[0])
        right_type = self.check_type_allowed(command, allowed_types, tree.children[1])

        if self.ignore_type(left_type) or self.ignore_type(right_type):
            return 'any'

        if (left_type == 'string' or right_type == 'string') and left_type != right_type:
            # TODO: probably this requires a separate exception
            raise exceptions.InvalidArgumentTypeException(command=command, invalid_type=right_type, invalid_argument='',
                                                          allowed_types=allowed_types)
        if left_type == 'float' or right_type == 'float':
            return 'float'

        return left_type

    def get_type(self, tree):
        if type(tree) is TypedTree:
            # TypedTree with type 'None' and 'string' could be in the lookup
            if tree.type_ in ['None', 'string']:
                in_lookup, type_in_lookup = self.try_get_type_from_lookup(tree.children[0])
                if in_lookup:
                    return type_in_lookup
            # If the value is not in the lookup or the type is other than 'None' or 'string', return evaluated type
            return tree.type_
        else:
            name = tree.children[0] if type(tree) is Tree else str(tree)
            in_lookup, type_in_lookup = self.try_get_type_from_lookup(name)
            if in_lookup:
                return type_in_lookup
            # For now default to 'string' type
            return 'string'

    def check_type_allowed(self, command, allowed_types, tree):
        arg_type = self.get_type(tree)
        if arg_type not in allowed_types and not self.ignore_type(arg_type):
            raise_invalid_type_error(allowed_types, command, str(tree), arg_type)
        return arg_type

    def ignore_type(self, type_):
        return type_ in ['any', 'None']

    def try_get_type_from_lookup(self, name):
        # TODO: we should not just take the first match
        matches = [entry for entry in self.lookup if entry.name == name]
        if matches:
            return True, self.lookup_type_fallback(matches[0].type_)
        hashed_matches = [entry for entry in self.lookup if entry.name == hash_var(name)]
        if hashed_matches:
            return True, self.lookup_type_fallback(hashed_matches[0].type_)
        return False, None

    def lookup_type_fallback(self, type_in_lookup):
        # If the entry is in the lookup table but its type has not been evaluated yet, then most probably this is a
        # variable referenced before it is defined. In this case, we rely on python to return an error. For now.
        return 'any' if type_in_lookup is None else type_in_lookup

    def to_typed_tree(self, tree, type_='None'):
        return TypedTree(tree.data, tree.children, tree.meta, type_)

    def __default__(self, data, children, meta):
        return TypedTree(data, children, meta, 'None')


def raise_invalid_type_error(allowed_types, command, variable, used_invalid_type):
    # we first try to raise if we expect 1 thing exactly for more precise error messages
    if len(allowed_types) == 1:
        # TODO: the exception could be reused not only for lists
        if allowed_types[0] == 'list':
            raise exceptions.RequiredArgumentTypeException(command=command, variable=variable,
                                                           required_type=allowed_types[0])

    raise exceptions.InvalidArgumentTypeException(command=command, invalid_type=used_invalid_type,
                                                  invalid_argument='', allowed_types=allowed_types)


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
            if all(type(c) == bool for c in children):
                return any(children) # children? if any is true there is a Turtle leaf
            else:
                return False # some nodes like text and punctuation have text children (their letters) these are not turtles


    def forward(self, args):
        return True

    def turn(self, args):
        return True

    # somehow tokens are not picked up by the default rule so they need their own rule
    def INT(self, args):
        return False

    def NAME(self, args):
        return False

    def NUMBER(self, args):
        return False




class IsValid(Filter):
    # all rules are valid except for the "Invalid" production rule
    # this function is used to generate more informative error messages
    # tree is transformed to a node of [Bool, args, command number]
    def program(self, args):
        if len(args) == 0:
            return False, InvalidInfo("empty program"), 1
        return super().program(args)

    def invalid_space(self, args):
        # return space to indicate that line starts in a space
        return False, InvalidInfo(" ")

    def print_nq(self, args):
        # return error source to indicate what went wrong
        return False, InvalidInfo("print without quotes")

    def invalid(self, args):
        # TODO: this will not work for misspelling 'at', needs to be improved!
        # TODO: add more information to the InvalidInfo
        error = InvalidInfo('invalid command', args[0][1], [a[1] for a in args[1:]])
        return False, error

    def unsupported_number(self, args):
        error = InvalidInfo('unsupported number', arguments=[str(args[0])])
        return False, error

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
        value = value.replace(c, f'\\{c}')
    return value


def get_allowed_types(command, level):
    # get only the allowed types of the command for all levels before the requested level
    allowed = [values[command] for key, values in commands_and_types_per_level.items()
               if command in values and key <= level]
    # use the allowed types of the highest level available
    return allowed[-1] if allowed else []


# decorator used to store each class in the lookup table
def hedy_transpiler(level):
    def decorator(c):
        TRANSPILER_LOOKUP[level] = c
        c.level = level
        return c
    return decorator

@hedy_transpiler(level=1)
class ConvertToPython_1(Transformer):

    def __init__(self, punctuation_symbols, lookup):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup
        __class__.level = 1

    def get_fresh_var(self, name):
        while is_variable(name, self.lookup):
            name = '_' + name
        return name

    def program(self, args):
        return '\n'.join([str(c) for c in args])
    def command(self, args):
        return args[0]

    def text(self, args):
        return ''.join([str(c) for c in args])
    def integer(self, args):
        return str(args[0])
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

    def forward(self, args):
        if len(args) == 0:
            return self.make_forward(50)

        self.check_args_type_allowed(args, 'forward', self.level)

        parameter = int(get_value(args[0]))
        return self.make_forward(parameter)

    def make_forward(self, parameter):
        return f"t.forward({parameter})""\ntime.sleep(0.1)"

    def turn(self, args):
        if len(args) == 0:
            return "t.right(90)" #no arguments works, and means a right turn

        argument = args[0]
        if is_variable(argument, self.lookup):        #is the argument a variable? if so, use that
            return f"t.right({argument})"
        elif argument.isnumeric():         #numbers can also be passed through
            return f"t.right({argument})"
        elif argument == 'left':
            return "t.left(90)"
        elif argument == 'right':
            return "t.right(90)"
        else:
            raise exceptions.InvalidArgumentTypeException(command='turn', invalid_type='',
                                                            allowed_types=['right', 'left', 'number'],
                                                            invalid_argument=argument)

    def check_args_type_allowed(self, args, command, level):
        allowed_types = get_allowed_types(command, level)
        for arg in args:
            assignment = self.find_in_lookup(arg)
            if assignment:
                if assignment.type_ not in ['any'] and assignment.type_ not in allowed_types:
                    raise_invalid_type_error(allowed_types, command, assignment.name, assignment.type_)
            else:
                type_ = self.get_arg_type(arg)
                if type_ not in ['any'] and type_ not in allowed_types:
                    raise exceptions.InvalidArgumentTypeException(command=command, invalid_type='',
                                                                  allowed_types=allowed_types,
                                                                  invalid_argument=arg if isinstance(arg, str) else args[0].children[0])

    def get_arg_type(self, arg):
        # TODO: Improve type inferring logic. For now, fallback to 'any' which means no type checks will be done if
        #  the arg is a Tree. Note that we do not have access to the TypeInferrer logic (and we cannot use it to
        #  determine the type since we do not have the full Tree object here). Maybe we can still reuse some logic?
        if type(arg) is Tree:
            return 'any'
        if is_int(arg):
            return 'integer'
        if is_float(arg):
            return 'float'
        return 'string'


    def find_in_lookup(self, variable):
        lookup_vars = [a for a in self.lookup if a.name == variable]
        # this now grabs the last occurrence, once we have slicing we want to be more precise!
        return lookup_vars[-1] if lookup_vars else None

# todo: could be moved into the transpiler class
def is_variable(name, lookup):
    all_names = [a.name for a in lookup]
    return name in all_names


def get_value(arg):
    # TODO: this func compensates for the mixed approach of handling leaf nodes, e.g. text => string and
    #  integer => Tree('integer', ['5']). Ideally, they will be handled in the same manner
    if isinstance(arg, Tree):
        if type(arg.children) is list:
            return arg.children[0]
        return arg.children
    return arg

def process_variable(arg, lookup):
    #processes a variable by hashing and escaping when needed
    name = get_value(arg)
    if is_variable(name, lookup):
        return hash_var(name)
    elif is_quoted(name): #sometimes kids accidentally quote strings, then we do not want them quoted again
        return f"{name}"
    else:
        return f"'{name}'"

def process_variable_for_fstring(name, lookup):
    if is_variable(name, lookup):
        return "{" + hash_var(name) + "}"
    else:
        return name

def process_variable_for_fstring_padded(name, lookup):
    # used to transform variables in comparisons
    if is_variable(name, lookup):
        return f"str({hash_var(name)}).zfill(100)"
    elif is_float(name):
        return f"str({name}).zfill(100)"
    else:
        return f"'{name}'.zfill(100)"

@hedy_transpiler(level=2)
class ConvertToPython_2(ConvertToPython_1):

    def ask_dep_2(self, args):
        # ask is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1, 'ask', "ask_needs_var")
    def echo_dep_2(self, args):
        # echo is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1,  'echo', "echo_out")

    def check_var_usage(self, args):
        # this function checks whether arguments are valid
        # we can proceed if all arguments are either quoted OR all variables

        args_to_process = [a for a in args if not isinstance(a, Tree)]#we do not check trees (calcs) they are always ok

        unquoted_args = [a for a in args_to_process if not is_quoted(a)]
        unquoted_in_lookup = [is_variable(a, self.lookup) for a in unquoted_args]

        if unquoted_in_lookup == [] or all(unquoted_in_lookup):
            # all good? return for further processing
            return args
        else:
            # return first name with issue
            # note this is where issue #832 can be addressed by checking whether
            # first_unquoted_var ius similar to something in the lookup list
            first_unquoted_var = unquoted_args[0]
            raise exceptions.UndefinedVarException(name=first_unquoted_var)

    def punctuation(self, args):
        return ''.join([str(c) for c in args])
    def var(self, args):
        name = args[0]
        return hash_var(name)
    def var_access(self, args):
        name = args[0]
        return hash_var(name)
    def print(self, args):
        # grab the allowed arguments from the dictionary
        self.check_args_type_allowed(args, 'print', self.level)

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

            argument_string += process_variable_for_fstring(argument, self.lookup) + space

            i = i + 1

        return f"print(f'{argument_string}')"

    def forward(self, args):
        if len(args) == 0:
            return self.make_forward(50)

        self.check_args_type_allowed(args, 'forward', self.level)

        # if the parameter is a number, use it as is
        # otherwise, see if we got a defined variable. if not, give an error
        try:
            parameter = int(get_value(args[0]))
        except:
            if is_variable(args[0], self.lookup):
                parameter = args[0]
            else:
                raise exceptions.InvalidArgumentTypeException(command='forward', invalid_type='',
                                                   allowed_types=get_allowed_types('forward', self.level),
                                                   invalid_argument=args[0])
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
        values = ["'" + get_value(a) + "'" for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

    def list_access(self, args):
        # check the arguments (except when they are random or numbers, that is not quoted nor a var but is allowed)
        self.check_var_usage(a for a in args if a != 'random' and not a.isnumeric())
        self.check_args_type_allowed([args[0]], 'at random', self.level)

        if args[1] == 'random':
            return 'random.choice(' + args[0] + ')'
        else:
            return args[0] + '[' + args[1] + '-1]'

def is_quoted(s):
    return s[0] == "'" and s[-1] == "'"

def make_f_string(args, lookup):
    argument_string = ''
    for argument in args:
        if is_variable(argument, lookup):
            # variables are placed in {} in the f string
            argument_string += "{" + hash_var(argument) + "}"
        else:
            # strings are written regularly
            # however we no longer need the enclosing quotes in the f-string
            # the quotes are only left on the argument to check if they are there.
            argument_string += argument.replace("'", '')

    return f"print(f'{argument_string}')"


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
        # we can print if all arguments are either quoted OR they are all variables

        unquoted_args = [a for a in args if not is_quoted(a)]
        unquoted_in_lookup = [is_variable(a, self.lookup) for a in unquoted_args]

        if unquoted_in_lookup == [] or all(unquoted_in_lookup):
            # all good? return for further processing
            return args
        else:
            # return first name with issue
            # note this is where issue #832 can be addressed by checking whether
            # first_unquoted_var ius similar to something in the lookup list
            first_unquoted_var = unquoted_args[0]
            raise exceptions.UndefinedVarException(name=first_unquoted_var)

    def print(self, args):
        args = self.check_print_arguments(args)
        self.check_args_type_allowed(args, 'print', self.level)
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
        self.check_args_type_allowed(remaining_args, 'ask', self.level)
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
            return var + '=' + args[1] + '[' + args[2].children[0] + '-1]'

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
        self.check_var_usage(args)
        self.check_args_type_allowed(args, 'print', self.level)

        #force all to be printed as strings (since there can not be int arguments)
        args_new = []
        for a in args:
            if isinstance(a, Tree):
                args_new.append("{" + a.children[0] + "}")
            else:
                a = a.replace("'", "") #no quotes needed in fstring
                args_new.append(process_variable_for_fstring(a, self.lookup))

        arguments = ''.join(args_new)
        return "print(f'" + arguments + "')"

    def equality_check(self, args):
        arg0 = process_variable(args[0], self.lookup)
        arg1 = process_variable(args[1], self.lookup)
        #TODO if we start using fstrings here, this str can go
        if len(args) == 2:
            return f"str({arg0}) == str({arg1})" #no and statements
        else:
            return f"str({arg0}) == str({arg1}) and {args[2]}"

    def assign(self, args):
        parameter = args[0]
        value = args[1]
        if type(value) is Tree:
            return parameter + " = " + value.children[0]
        else:
            #assigns may contain string (accidentally) i.e. name = 'Hedy'
            value = process_characters_needing_escape(value)
            return parameter + " = '" + value + "'"

    def process_token_or_tree(self, argument):
        if type(argument) is Tree:
            return f'{str(argument.children[0])}'
        return f"int({argument})"

    def process_calculation(self, args, operator):
        # arguments of a sum are either a token or a
        # tree resulting from earlier processing
        # for trees we need to grap the inner string
        # for tokens we add int around them

        self.check_args_type_allowed(args, 'sum', self.level)

        args = [self.process_token_or_tree(a) for a in args]
        return Tree('sum', [f'{args[0]} {operator} {args[1]}'])

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
    def repeat(self, args):
        var_name = self.get_fresh_var('i')
        times = process_variable(args[0], self.lookup)
        command = args[1]
        return f"""for {var_name} in range(int({str(times)})):
{indent(command)}"""

@hedy_transpiler(level=7)
@hedy_transpiler(level=8)
class ConvertToPython_7_8(ConvertToPython_6):
    def __init__(self, punctuation_symbols, lookup):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup

    def command(self, args):
        return "".join(args)

    def repeat(self, args):
        all_lines = [indent(x) for x in args[1:]]
        return "for i in range(int(" + str(get_value(args[0])) + ")):\n" + "\n".join(all_lines)

    def ifs(self, args):
        args = [a for a in args if a != ""] # filter out in|dedent tokens

        all_lines = [indent(x) for x in args[1:]]

        return "if " + args[0] + ":\n" + "\n".join(all_lines)

    def elses(self, args):
        args = [a for a in args if a != ""] # filter out in|dedent tokens

        all_lines = [indent(x) for x in args]

        return "\nelse:\n" + "\n".join(all_lines)

    def var_access(self, args):
        if len(args) == 1: #accessing a var
            return hash_var(args[0])
        else:
        # this is list_access
            return hash_var(args[0]) + "[" + str(hash_var(args[1])) + "]" if type(args[1]) is not Tree else "random.choice(" + str(hash_var(args[0])) + ")"

@hedy_transpiler(level=9)
class ConvertToPython_9(ConvertToPython_7_8):
    def repeat_list(self, args):
      args = [a for a in args if a != ""]  # filter out in|dedent tokens

      body = "\n".join([indent(x) for x in args[2:]])

      return f"for {args[0]} in {args[1]}:\n{body}"

@hedy_transpiler(level=10)
class ConvertToPython_10(ConvertToPython_9):
    def for_loop(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        body = "\n".join([indent(x) for x in args[3:]])
        stepvar_name = self.get_fresh_var('step')
        return f"""{stepvar_name} = 1 if int({get_value(args[1])}) < int({get_value(args[2])}) else -1
for {args[0]} in range(int({get_value(args[1])}), int({get_value(args[2])}) + {stepvar_name}, {stepvar_name}):
{body}"""


def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def is_float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def is_random(s):
    return 'random.choice' in s


@hedy_transpiler(level=11)
class ConvertToPython_11(ConvertToPython_10):
    def number(self, args):
        return ''.join(args)

    def process_token_or_tree(self, argument):
        if isinstance(argument, Tree):
            return f'{str(argument.children[0])}'
        else:
            return f'{argument}'


    def ask(self, args):
        var = args[0]
        remaining_args = args[1:]
        self.check_args_type_allowed(remaining_args, 'ask', self.level)

        assign = f'{var} = input(' + '+'.join(remaining_args) + ")"

        tryblock = textwrap.dedent(f"""
        try:
          {var} = int({var})
        except ValueError:
          try:
            {var} = float({var})
          except ValueError:
            pass""") #no number? leave as string
        return assign + tryblock

    def process_calculation(self, args, operator):
        # arguments of a sum are either a token or a
        # tree resulting from earlier processing
        # for trees we need to grap the inner string
        # for tokens we simply return the argument (no more casting to str needed)

        args = [self.process_token_or_tree(a) for a in args]

        return Tree('sum', [f'{args[0]} {operator} {args[1]}'])

    def print(self, args):
        # TODO: new type checking is needed for string assignment
        self.check_var_usage(args)
        self.check_args_type_allowed(args, 'print', self.level)

        args_new = []
        for a in args:
            if isinstance(a, Tree):
                args_new.append("{" + get_value(a) + "}")
            else:
                a = a.replace("'", "")  # no quotes needed in fstring
                args_new.append(process_variable_for_fstring(a, self.lookup))

        arguments = ''.join(args_new)
        return "print(f'" + arguments + "')"

    def text_in_quotes(self, args):
        text = args[0]
        return "'" + text + "'" # keep quotes in the Python code (producing name = 'Henk')

    def assign_list(self, args):
        parameter = args[0]
        values = args[1:]
        return parameter + " = [" + ", ".join(values) + "]"

    def assign(self, args):
        right_hand_side = args[1]

        # we now need to check if the right hand side of te assign is
        # either a var or quoted, if it is not (and undefined var is raised)
        # the real issue is probably that the kid forgot quotes
        try:
            correct_rhs = self.check_var_usage([right_hand_side]) #check_var_usage expects a list of arguments so place this one in a list.
        except exceptions.UndefinedVarException as E:
            # is the text a number? then no quotes are fine. if not, raise maar!

            if not (is_int(right_hand_side) or is_float(right_hand_side) or is_random(right_hand_side)):
                raise exceptions.UnquotedAssignTextException(text = args[1])

        parameter = args[0]
        value = args[1]

        if isinstance(value, Tree):
            return parameter + " = " + value.children[0]
        else:
            # we no longer escape quotes here because they are now needed
            return parameter + " = " + value + ""

@hedy_transpiler(level=12)
class ConvertToPython_12(ConvertToPython_11):
    def process_comparison(self, args, operator):

        # we are generating an fstring now
        arg0 = process_variable_for_fstring_padded(args[0], self.lookup)
        arg1 = process_variable_for_fstring_padded(args[1], self.lookup)

        # zfill(100) in process_variable_for_fstring_padded leftpads variables to length 100 with zeroes (hence the z fill)
        # that is to make sure that string comparison works well "ish" for numbers
        # this at one point could be improved with a better type system, of course!
        # the issue is that we can't do everything in here because
        # kids submit things with the ask command that wew do not ask them to cast (yet)

        simple_comparison = arg0 + operator + arg1

        if len(args) == 2:
            return simple_comparison  # no and statements
        else:
            return f"{simple_comparison} and {args[2]}"


    def smaller(self, args):
        return self.process_comparison(args, "<")

    def bigger(self, args):
        return self.process_comparison(args, ">")

    def smaller_equal(self, args):
        return self.process_comparison(args, "<=")

    def bigger_equal(self, args):
        return self.process_comparison(args, ">=")

    def not_equal(self, args):
        return self.process_comparison(args, "!=")

@hedy_transpiler(level=13)
class ConvertToPython_13(ConvertToPython_12):
    def while_loop(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [indent(x) for x in args[1:]]
        return "while " + args[0] + ":\n"+"\n".join(all_lines)

@hedy_transpiler(level=14)
class ConvertToPython_14(ConvertToPython_13):
    def assign_list(self, args):
        parameter = args[0]
        values = [a for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

    def change_list_item(self, args):
        return args[0] + '[' + args[1] + '-1] = ' + args[2]


# @hedy_transpiler(level=10)
# @hedy_transpiler(level=11)
# class ConvertToPython_10_11(ConvertToPython_9):
#     def elifs(self, args):
#         args = [a for a in args if a != ""]  # filter out in|dedent tokens
#         all_lines = [indent(x) for x in args[1:]]
#         return "\nelif " + args[0] + ":\n" + "\n".join(all_lines)
#
# @hedy_transpiler(level=12)
# class ConvertToPython_12(ConvertToPython_10_11):
#     def input(self, args):
#         args_new = []
#         var = args[0]
#         arguments = args[1:]
#         self.check_arg_types(arguments, 'input', self.level)
#         for a in arguments:
#             if type(a) is Tree:
#                 args_new.append(f'str({a.children})')
#             elif "'" not in a:
#                 args_new.append(f'str({a})')
#             else:
#                 args_new.append(a)
#
#         return f'{var} = input(' + '+'.join(args_new) + ")"
#
# @hedy_transpiler(level=13)
# class ConvertToPython_13(ConvertToPython_12):
#     def print(self, args):
#         # we only check non-Tree (= non calculation) arguments
#         self.check_var_usage(args)
#         self.check_arg_types(args, 'print', self.level)
#
#         #force all to be printed as strings (since there can not be int arguments)
#         args_new = []
#         for a in args:
#             if type(a) is Tree:
#                 args_new.append("{" + a.children + "}")
#             else:
#                 args_new.append(process_variable_for_fstring(a, self.lookup).replace("'",""))
#
#         arguments = ''.join(args_new)
#         return "print(f'" + arguments + "')"

# @hedy_transpiler(level=14)
# class ConvertToPython_14(ConvertToPython_13):
#     def print(self,args):
#         return ConvertToPython_5.print(self,args)
#     def assign(self, args):  # TODO: needs to be merged with 6, when 6 is improved to with printing expressions directly
#         if len(args) == 2:
#             parameter = args[0]
#             value = args[1]
#             if type(value) is Tree:
#                 return parameter + " = " + value.children
#             else:
#                 if "'" in value or 'random.choice' in value:  # TODO: should be a call to wrap nonvarargument is quotes!
#                     return parameter + " = " + value
#                 else:
#                     # FH, June 21 the addition of _true/false is a bit of a hack. cause they are first seen as vars that at reserved words, they are then hashed and we undo that here
#                     # could/should be fixed in the grammar!
#
#                     if value == 'true' or value == 'True' or value == hash_var('True') or value == hash_var('true'):
#                         return parameter + " = True"
#                     elif value == 'false' or value == 'False' or value == hash_var('False') or value == hash_var('false'):
#                         return parameter + " = False"
#                     else:
#                         return parameter + " = '" + value + "'"
#         else:
#             parameter = args[0]
#             values = args[1:]
#             return parameter + " = [" + ", ".join(values) + "]"
#
#     def equality_check(self, args):
#         arg0 = process_variable(args[0], self.lookup)
#         arg1 = process_variable(args[1], self.lookup)
#         if arg1 == '\'True\'' or arg1 == '\'true\'':
#             return f"{arg0} == True"
#         elif arg1 == '\'False\'' or arg1 == '\'false\'':
#             return f"{arg0} == False"
#         else:
#             return f"str({arg0}) == str({arg1})" #no and statements
#
# @hedy_transpiler(level=15)
# class ConvertToPython_15(ConvertToPython_14):
#     def andcondition(self, args):
#         return ' and '.join(args)
#     def orcondition(self, args):
#         return ' or '.join(args)
#
# @hedy_transpiler(level=16)
# class ConvertToPython_16(ConvertToPython_15):
#     def comment(self, args):
#         return f"# {args}"
#

#
# @hedy_transpiler(level=19)
# @hedy_transpiler(level=20)
# class ConvertToPython_19_20(ConvertToPython_18):
#     def length(self, args):
#         arg0 = args[0]
#         length_string = f"len({arg0})"
#
#         # when accessing len we need to know it is a var
#         # todo (could be done in the AllAssignments?)
#         self.lookup.append(Assignment(length_string, 'operation'))
#         return length_string
#
#     def assign(self, args):  # TODO: needs to be merged with 6, when 6 is improved to with printing expressions directly
#         if len(args) == 2:
#             parameter = args[0]
#             value = args[1]
#             if type(value) is Tree:
#                 return parameter + " = " + value.children
#             else:
#                 if "'" in value or 'random.choice' in value:  # TODO: should be a call to wrap nonvarargument is quotes!
#                     return parameter + " = " + value
#                 elif "len(" in value:
#                     return parameter + " = " + value
#                 else:
#                     if value == 'true' or value == 'True':
#                         return parameter + " = True"
#                     elif value == 'false' or value == 'False':
#                         return parameter + " = False"
#                     else:
#                         return parameter + " = '" + value + "'"
#         else:
#             parameter = args[0]
#             values = args[1:]
#             return parameter + " = [" + ", ".join(values) + "]"
#
# @hedy_transpiler(level=21)
# class ConvertToPython_21(ConvertToPython_19_20):
#     def equality_check(self, args):
#         if type(args[0]) is Tree:
#             return args[0].children + " == int(" + args[1] + ")"
#         if type(args[1]) is Tree:
#             return "int(" + args[0] + ") == " + args[1].children
#         arg0 = process_variable(args[0], self.lookup)
#         arg1 = process_variable(args[1], self.lookup)
#         if arg1 == '\'True\'' or arg1 == '\'true\'':
#             return f"{arg0} == True"
#         elif arg1 == '\'False\'' or arg1 == '\'false\'':
#             return f"{arg0} == False"
#         else:
#             return f"str({arg0}) == str({arg1})"  # no and statements
#




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


def create_grammar(level, lang="en"):
    # start with creating the grammar for level 1
    result = get_full_grammar_for_level(1)
    keys = get_keywords_for_language(lang)
    result = merge_grammars(result, keys)
    # then keep merging new grammars in
    for i in range(2, level+1):
        grammar_text_i = get_additional_rules_for_level(i)
        result = merge_grammars(result, grammar_text_i)

    # ready? Save to file to ease debugging
    # this could also be done on each merge for performance reasons
    save_total_grammar_file(level, result, lang)

    return result

def save_total_grammar_file(level, grammar, lang):
    # Load Lark grammars relative to directory of current file
    script_dir = path.abspath(path.dirname(__file__))
    filename = "level" + str(level) + "." + lang + "-Total.lark"
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

def get_keywords_for_language(language):
    script_dir = path.abspath(path.dirname(__file__))
    filename = "keywords-" + str(language) + ".lark"
    with open(path.join(script_dir, "grammars", filename), "r", encoding="utf-8") as file:
        grammar_text = file.read()
    return grammar_text

PARSER_CACHE = {}


def get_parser(level, lang="en"):
    """Return the Lark parser for a given level.

    Uses caching if Hedy is NOT running in development mode.
    """
    key = str(level) + "." + lang
    existing = PARSER_CACHE.get(key)
    if existing and not utils.is_debug_mode():
        return existing
    grammar = create_grammar(level, lang)
    ret = Lark(grammar, regex=True) #ambiguity='explicit'
    PARSER_CACHE[key] = ret
    return ret

ParseResult = namedtuple('ParseResult', ['code', 'has_turtle'])

def transpile(input_string, level, lang="en"):
    transpile_result = transpile_inner(input_string, level, lang)
    return transpile_result




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
    elif s == '\n':
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

def needs_indentation(code):
    # this is done a bit half-assed, clearly *parsing* the one line would be superior
    # because now a line like
    # repeat is 5 would also require indentation!
    all_words = code.split()
    if len(all_words) == 0:
        return False

    first_keyword = all_words[0]
    return first_keyword == "for" or first_keyword == "repeat" or first_keyword == "if"



def preprocess_blocks(code, level):
    processed_code = []
    lines = code.split("\n")
    current_number_of_indents = 0
    previous_number_of_indents = 0
    indent_size = None # we don't fix indent size but the first encounter sets it
    line_number = 0
    next_line_needs_indentation = False
    for line in lines:
        leading_spaces = find_indent_length(line)

        line_number += 1
        #first encounter sets indent size for this program
        if indent_size == None and leading_spaces > 0:
            indent_size = leading_spaces

        # ignore whitespace-only lines
        if leading_spaces == len(line):
            continue

        #calculate nuber of indents if possible
        if indent_size != None:
            if (leading_spaces % indent_size) != 0:
                # there is inconsistent indentation, not sure if that is too much or too little!
                if leading_spaces < current_number_of_indents * indent_size:
                    raise hedy.exceptions.NoIndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                                 indent_size=indent_size)
                else:
                    raise hedy.exceptions.IndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                                 indent_size=indent_size)

            current_number_of_indents = leading_spaces // indent_size
            if current_number_of_indents > 1 and level == 7:
                raise hedy.exceptions.LockedLanguageFeatureException(concept="nested blocks")

        if next_line_needs_indentation and current_number_of_indents <= previous_number_of_indents:
            raise hedy.exceptions.NoIndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                         indent_size=indent_size)

        if needs_indentation(line):
            next_line_needs_indentation = True
        else:
            next_line_needs_indentation = False

        if current_number_of_indents - previous_number_of_indents > 1:
            raise hedy.exceptions.IndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                            indent_size=indent_size)



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


def check_program_size_is_valid(input_string):
    number_of_lines = input_string.count('\n')
    # parser is not made for huge programs!
    if number_of_lines > MAX_LINES:
        raise exceptions.InputTooBigException(lines_of_code=number_of_lines, max_lines=MAX_LINES)


def process_input_string(input_string, level):
    result = input_string.replace('\r\n', '\n')

    if contains_blanks(result):
        raise exceptions.CodePlaceholdersPresentException()

    if level >= 3:
        result = result.replace("\\", "\\\\")

    # In level 7 we add indent-dedent blocks to the code before parsing
    if level >= 7:
        result = preprocess_blocks(result, level)

    return result


def parse_input(input_string, level, lang):
    parser = get_parser(level, lang)
    try:
        parse_result = parser.parse(input_string + '\n')
        return parse_result.children[0]  # getting rid of the root could also be done in the transformer would be nicer
    except UnexpectedCharacters as e:
        try:
            location = e.line, e.column
            characters_expected = str(e.allowed) #not yet in use, could be used in the future (when our parser rules are better organize, now it says ANON*__12 etc way too often!)
            character_found = beautify_parse_error(e.char)
            # print(e.args[0])
            # print(location, character_found, characters_expected)
            raise exceptions.ParseException(level=level, location=location, found=character_found) from e
        except UnexpectedEOF:
            # this one can't be beautified (for now), so give up :)
            raise e


def is_program_valid(program_root, input_string, level, lang):
    # IsValid returns (True,) or (False, args, line)
    is_valid = IsValid().transform(program_root)

    if not is_valid[0]:
        _, invalid_info, line = is_valid

        # Apparently, sometimes 'args' is a string, sometimes it's a list of
        # strings ( are these production rule names?). If it's a list of
        # strings, just take the first string and proceed.
        if isinstance(invalid_info, list):
            invalid_info = invalid_info[0]
        if invalid_info.error_type == ' ':
            # the error here is a space at the beginning of a line, we can fix that!
            fixed_code = repair(input_string)
            if fixed_code != input_string:  # only if we have made a successful fix
                result = transpile_inner(fixed_code, level, lang)
            raise exceptions.InvalidSpaceException(level=level, line_number=line, fixed_code=fixed_code,
                                                   fixed_result=result)
        elif invalid_info.error_type == 'print without quotes':
            # grammar rule is agnostic of line number so we can't easily return that here
            raise exceptions.UnquotedTextException(level=level)
        elif invalid_info.error_type == 'empty program':
            raise exceptions.EmptyProgramException()
        elif invalid_info.error_type == 'unsupported number':
            raise exceptions.UnsupportedFloatException(value=''.join(invalid_info.arguments))
        else:
            invalid_command = invalid_info.command
            closest = closest_command(invalid_command, commands_per_level[level])
            if closest == None:  # we couldn't find a suggestion because the command itself was found
                # making the error super-specific for the turn command for now
                # is it possible to have a generic and meaningful syntax error message for different commands?
                if invalid_command == 'turn':
                    raise hedy.exceptions.InvalidArgumentTypeException(command=invalid_info.command, invalid_type='',
                                                                       allowed_types=['right', 'left', 'number'],
                                                                       invalid_argument=''.join(invalid_info.arguments))
                # clearly the error message here should be better or it should be a different one!
                raise exceptions.ParseException(level=level, location=["?", "?"], found=invalid_command)
            raise exceptions.InvalidCommandException(invalid_command=invalid_command, level=level,
                                                     guessed_command=closest, line_number=line)


def is_program_complete(abstract_syntax_tree, level):
    is_complete = IsComplete(level).transform(abstract_syntax_tree)
    if not is_complete[0]:
        incomplete_command = is_complete[1][0]
        line = is_complete[2]
        raise exceptions.IncompleteCommandException(incomplete_command=incomplete_command, level=level,
                                                    line_number=line)


def create_lookup_table(abstract_syntax_tree, level):
    visitor = LookupEntryCollector(level)
    visitor.visit_topdown(abstract_syntax_tree)
    entries = visitor.lookup

    for entry in entries:
        typed_tree = TypeInferrer(entries, level).transform(entry.tree)
        entry.type_ = typed_tree.type_

    # For now the lookup table should contain the entries with their names in plain text and hashed
    return entries + [LookupEntry(hash_var(e.name), e.tree, e.skip_hashing, e.type_) for e in entries]


def transpile_inner(input_string, level, lang="en"):
    check_program_size_is_valid(input_string)

    punctuation_symbols = ['!', '?', '.']

    level = int(level)
    if level > HEDY_MAX_LEVEL:
        raise Exception(f'Levels over {HEDY_MAX_LEVEL} not implemented yet')

    input_string = process_input_string(input_string, level)

    program_root = parse_input(input_string, level, lang)
    is_program_valid(program_root, input_string, level, lang)

    try:
        abstract_syntax_tree = ExtractAST().transform(program_root)

        is_program_complete(abstract_syntax_tree, level)

        if not valid_echo(abstract_syntax_tree):
            raise exceptions.LonelyEchoException()

        lookup_table = create_lookup_table(abstract_syntax_tree, level)

        # grab the right transpiler from the lookup
        transpiler = TRANSPILER_LOOKUP[level]
        python = transpiler(punctuation_symbols, lookup_table).transform(abstract_syntax_tree)


        has_turtle = UsesTurtle().transform(abstract_syntax_tree)
        return ParseResult(python, has_turtle)
    except VisitError as E:
        # Exceptions raised inside visitors are wrapped inside VisitError. Unwrap it if it is a
        # HedyException to show the intended error message.
        if isinstance(E.orig_exc, exceptions.HedyException):
            raise E.orig_exc
        else:
            raise E


def execute(input_string, level):
    python = transpile(input_string, level)
    if python.has_turtle:
        raise exceptions.HedyException("hedy.execute doesn't support turtle")
    exec(python.code)

# f = open('output.py', 'w+')
# f.write(python)
# f.close()
