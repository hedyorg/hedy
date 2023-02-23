import textwrap

import lark
from flask_babel import gettext
from lark import Lark
from lark.exceptions import UnexpectedEOF, UnexpectedCharacters, VisitError
from lark import Tree, Transformer, visitors, v_args
from os import path

import warnings
import hedy
import hedy_translation
from hedy_content import ALL_KEYWORD_LANGUAGES
import utils
from collections import namedtuple
import re
import regex
from dataclasses import dataclass, field
import exceptions
import program_repair
import yaml

# Some useful constants
from hedy_content import KEYWORDS

HEDY_MAX_LEVEL = 18
MAX_LINES = 100
LEVEL_STARTING_INDENTATION = 8

# Boolean variables to allow code which is under construction to not be executed
local_keywords_enabled = True

# dictionary to store transpilers
TRANSPILER_LOOKUP = {}

# builtins taken from 3.11.0 docs: https://docs.python.org/3/library/functions.html
PYTHON_BUILTIN_FUNCTIONS = [
    'abs',
    'aiter',
    'all',
    'any',
    'anext',
    'ascii',
    'bin',
    'bool',
    'breakpoint',
    'bytearray',
    'bytes',
    'callable',
    'chr',
    'classmethod',
    'compile',
    'complex',
    'delattr',
    'dict',
    'dir',
    'divmod',
    'enumerate',
    'eval',
    'exec',
    'filter',
    'float',
    'format',
    'frozenset',
    'getattr',
    'globals',
    'hasattr',
    'hash',
    'help',
    'hex',
    'id',
    'input',
    'int',
    'isinstance',
    'issubclass',
    'iter',
    'len',
    'list',
    'locals',
    'map',
    'max',
    'memoryview',
    'min',
    'next',
    'object',
    'oct',
    'open',
    'ord',
    'pow',
    'print',
    'property',
    'range',
    'repr',
    'reversed',
    'round',
    'set',
    'setattr',
    'slice',
    'sorted',
    'staticmethod',
    'str',
    'sum',
    'super',
    'tuple',
    'type',
    'vars',
    'zip']
PYTHON_KEYWORDS = [
    'and',
    'except',
    'lambda',
    'with',
    'as',
    'finally',
    'nonlocal',
    'while',
    'assert',
    'False',
    'None',
    'yield',
    'break',
    'for',
    'not',
    'class',
    'from',
    'or',
    'continue',
    'global',
    'pass',
    'def',
    'if',
    'raise',
    'del',
    'import',
    'return',
    'elif',
    'in',
    'True',
    'else',
    'is',
    'try',
    'int']
# Python keywords and function names need hashing when used as var names
reserved_words = set(PYTHON_BUILTIN_FUNCTIONS + PYTHON_KEYWORDS)

# Let's retrieve all keywords dynamically from the cached KEYWORDS dictionary
indent_keywords = {}
for lang, keywords in KEYWORDS.items():
    indent_keywords[lang] = []
    for keyword in ['if', 'elif', 'for', 'repeat', 'while', 'else']:
        indent_keywords[lang].append(keyword)  # always also check for En
        indent_keywords[lang].append(keywords.get(keyword))

# These are the preprocessor rules that we use to specify changes in the rules that
# are expected to work across several rules
# Example
# for<needs_colon> instead of defining the whole rule again.


def needs_colon(rule):
    pos = rule.find('_EOL (_SPACE command)')
    return f'{rule[0:pos]} _COLON {rule[pos:]}'


PREPROCESS_RULES = {
    'needs_colon': needs_colon
}


class Command:
    print = 'print'
    ask = 'ask'
    echo = 'echo'
    turn = 'turn'
    forward = 'forward'
    sleep = 'sleep'
    color = 'color'
    add_to_list = 'add to list'
    remove_from_list = 'remove from list'
    list_access = 'at random'
    in_list = 'in list'
    equality = 'is (equality)'
    repeat = 'repeat'
    for_list = 'for in'
    for_loop = 'for in range'
    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    smaller = '<'
    smaller_equal = '<='
    bigger = '>'
    bigger_equal = '>='
    not_equal = '!='
    pressed = 'pressed'
    clear = 'clear'


translatable_commands = {Command.print: ['print'],
                         Command.ask: ['ask'],
                         Command.echo: ['echo'],
                         Command.turn: ['turn'],
                         Command.sleep: ['sleep'],
                         Command.color: ['color'],
                         Command.forward: ['forward'],
                         Command.add_to_list: ['add', 'to_list'],
                         Command.remove_from_list: ['remove', 'from'],
                         Command.list_access: ['at', 'random'],
                         Command.in_list: ['in'],
                         Command.equality: ['is', '=', '=='],
                         Command.repeat: ['repeat', 'times'],
                         Command.for_list: ['for', 'in'],
                         Command.for_loop: ['in', 'range', 'to']}


class HedyType:
    any = 'any'
    none = 'none'
    string = 'string'
    integer = 'integer'
    list = 'list'
    float = 'float'
    boolean = 'boolean'
    input = 'input'


# Type promotion rules are used to implicitly convert one type to another, e.g. integer should be auto converted
# to float in 1 + 1.5. Additionally, before level 12, we want to convert numbers to strings, e.g. in equality checks.
int_to_float = (HedyType.integer, HedyType.float)
int_to_string = (HedyType.integer, HedyType.string)
float_to_string = (HedyType.float, HedyType.string)
input_to_int = (HedyType.input, HedyType.integer)
input_to_float = (HedyType.input, HedyType.float)
input_to_string = (HedyType.input, HedyType.string)


def promote_types(types, rules):
    for (from_type, to_type) in rules:
        if to_type in types:
            types = [to_type if t == from_type else t for t in types]
    return types


# Commands per Hedy level which are used to suggest the closest command when kids make a mistake
commands_per_level = {
    1: ['print', 'ask', 'echo', 'turn', 'forward', 'color'],
    2: ['print', 'ask', 'is', 'turn', 'forward', 'color', 'sleep'],
    3: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from'],
    4: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'clear'],
    5: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'clear'],
    6: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'clear'],
    7: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'repeat', 'times', 'clear'],
    8: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'repeat', 'times', 'clear'],
    9: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'repeat', 'times', 'clear'],
    10: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'repeat', 'times', 'for', 'clear'],
    11: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'for', 'range', 'repeat', 'clear'],
    12: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'for', 'range', 'repeat', 'clear'],
    13: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'for', 'range', 'repeat', 'and', 'or', 'clear'],
    14: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'for', 'range', 'repeat', 'and', 'or', 'clear'],
    15: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'for', 'range', 'repeat', 'and', 'or', 'while', 'clear'],
    16: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'for', 'range', 'repeat', 'and', 'or', 'while', 'clear'],
    17: ['ask', 'is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'not in', 'if', 'else', 'pressed', 'button', 'for', 'range', 'repeat', 'and', 'or', 'while', 'elif', 'clear'],
    18: ['is', 'print', 'forward', 'turn', 'color', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'not in', 'else', 'for', 'pressed', 'button', 'range', 'repeat', 'and', 'or', 'while', 'elif', 'input', 'clear'],
}

command_turn_literals = ['right', 'left']
command_make_color = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow']

# Commands and their types per level (only partially filled!)
commands_and_types_per_level = {
    Command.print: {
        1: [HedyType.string, HedyType.integer, HedyType.input],
        12: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float],
        16: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.list]
    },
    Command.ask: {
        1: [HedyType.string, HedyType.integer, HedyType.input],
        12: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float],
        16: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.list]
    },
    Command.turn: {1: command_turn_literals,
                   2: [HedyType.integer, HedyType.input],
                   12: [HedyType.integer, HedyType.input, HedyType.float]
                   },
    Command.color: {1: command_make_color,
                    2: [command_make_color, HedyType.string, HedyType.input]},
    Command.forward: {1: [HedyType.integer, HedyType.input],
                      12: [HedyType.integer, HedyType.input, HedyType.float]
                      },
    Command.sleep: {1: [HedyType.integer, HedyType.input]},
    Command.list_access: {1: [HedyType.list]},
    Command.in_list: {1: [HedyType.list]},
    Command.add_to_list: {1: [HedyType.list]},
    Command.remove_from_list: {1: [HedyType.list]},
    Command.equality: {1: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float],
                       14: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.list]},
    Command.addition: {
        6: [HedyType.integer, HedyType.input],
        12: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float]
    },
    Command.subtraction: {
        1: [HedyType.integer, HedyType.input],
        12: [HedyType.integer, HedyType.float, HedyType.input],
    },
    Command.multiplication: {
        1: [HedyType.integer, HedyType.input],
        12: [HedyType.integer, HedyType.float, HedyType.input],
    },
    Command.division: {
        1: [HedyType.integer, HedyType.input],
        12: [HedyType.integer, HedyType.float, HedyType.input],
    },
    Command.repeat: {7: [HedyType.integer, HedyType.input]},
    Command.for_list: {10: {HedyType.list}},
    Command.for_loop: {11: [HedyType.integer, HedyType.input]},
    Command.smaller: {14: [HedyType.integer, HedyType.float, HedyType.input]},
    Command.smaller_equal: {14: [HedyType.integer, HedyType.float, HedyType.input]},
    Command.bigger: {14: [HedyType.integer, HedyType.float, HedyType.input]},
    Command.bigger_equal: {14: [HedyType.integer, HedyType.float, HedyType.input]},
    Command.not_equal: {14: [HedyType.integer, HedyType.float, HedyType.string, HedyType.input, HedyType.list]},
    Command.pressed: {5: [HedyType.string]}  # TODO: maybe use a seperate type character in the future.
}

# we generate Python strings with ' always, so ' needs to be escaped but " works fine
# \ also needs to be escaped because it eats the next character
characters_that_need_escaping = ["\\", "'"]

character_skulpt_cannot_parse = re.compile('[^a-zA-Z0-9_]')


def get_list_keywords(commands, to_lang):
    """ Returns a list with the local keywords of the argument 'commands'
    """

    translation_commands = []
    dir = path.abspath(path.dirname(__file__))
    path_keywords = dir + "/content/keywords"

    to_yaml_filesname_with_path = path.join(path_keywords, to_lang + '.yaml')
    en_yaml_filesname_with_path = path.join(path_keywords, 'en' + '.yaml')

    with open(en_yaml_filesname_with_path, 'r', encoding='utf-8') as stream:
        en_yaml_dict = yaml.safe_load(stream)

    try:
        with open(to_yaml_filesname_with_path, 'r', encoding='utf-8') as stream:
            to_yaml_dict = yaml.safe_load(stream)
        for command in commands:
            try:
                translation_commands.append(to_yaml_dict[command])
            except Exception:
                translation_commands.append(en_yaml_dict[command])
    except Exception:
        for command in commands:
            translation_commands.append(en_yaml_dict[command])

    return translation_commands


def get_suggestions_for_language(lang, level):
    if not local_keywords_enabled:
        lang = 'en'

    lang_commands = get_list_keywords(commands_per_level[level], lang)

    # if we allow multiple keyword languages:
    en_commands = get_list_keywords(commands_per_level[level], 'en')
    en_lang_commands = list(set(en_commands + lang_commands))

    return en_lang_commands


def escape_var(var):
    var_name = var.name if type(var) is LookupEntry else var
    return "_" + var_name if var_name in reserved_words else var_name


def closest_command(invalid_command, known_commands, threshold=2):
    # closest_command() searches for a similar command (distance smaller than threshold)
    # TODO: make the result value be tuple instead of a ugly None & string mix
    # returns None if the invalid command does not contain any known command.
    # returns 'keyword' if the invalid command is exactly a command (so shoudl not be suggested)

    min_command = closest_command_with_min_distance(invalid_command, known_commands, threshold)

    # Check if we are not returning the found command
    # In that case we have no suggestion
    # This is to prevent "print is not a command in Hedy level 3, did you mean print?" error message

    if min_command == invalid_command:
        return 'keyword'
    return min_command


def style_command(command):
    return f'<span class="command-highlighted">{command}</span>'


def closest_command_with_min_distance(invalid_command, commands, threshold):
    # FH, early 2020: simple string distance, could be more sophisticated MACHINE LEARNING!

    minimum_distance = 1000
    closest_command = None
    for command in commands:
        minimum_distance_for_command = calculate_minimum_distance(command, invalid_command)
        if minimum_distance_for_command < minimum_distance and minimum_distance_for_command <= threshold:
            minimum_distance = minimum_distance_for_command
            closest_command = command

    return closest_command


def calculate_minimum_distance(s1, s2):
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
    column: int = 0


# used in to construct lookup table entries and infer their type
@dataclass
class LookupEntry:
    name: str
    tree: Tree
    linenumber: int
    skip_hashing: bool
    type_: str = None
    currently_inferring: bool = False  # used to detect cyclic type inference


class TypedTree(Tree):
    def __init__(self, data, children, meta, type_):
        super().__init__(data, children, meta)
        self.type_ = type_


@v_args(meta=True)
class ExtractAST(Transformer):
    # simplifies the tree: f.e. flattens arguments of text, var and punctuation for further processing
    def text(self, meta, args):
        return Tree('text', [' '.join([str(c) for c in args])], meta)

    def INT(self, args):
        return Tree('integer', [str(args)])

    def NUMBER(self, args):
        return Tree('number', [str(args)])

    def POSITIVE_NUMBER(self, args):
        return Tree('number', [str(args)])

    def NEGATIVE_NUMBER(self, args):
        return Tree('number', [str(args)])

    # level 2
    def var(self, meta, args):
        return Tree('var', [''.join([str(c) for c in args])], meta)

    def list_access(self, meta, args):
        # FH, may 2022 I don't fully understand why we remove INT here and just plemp
        # the number in the tree. should be improved but that requires rewriting the further processing code too (TODO)
        if type(args[1]) == Tree:
            if "random" in args[1].data:
                return Tree('list_access', [args[0], 'random'], meta)
            elif args[1].data == "var_access":
                return Tree('list_access', [args[0], args[1].children[0]], meta)
            else:
                # convert to latin int
                latin_int_index = str(int(args[1].children[0]))
                return Tree('list_access', [args[0], latin_int_index], meta)
        else:
            return Tree('list_access', [args[0], args[1]], meta)

    # level 5
    def error_unsupported_number(self, meta, args):
        return Tree('unsupported_number', [''.join([str(c) for c in args])], meta)


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
            self.add_to_lookup(tree.children[0].children[0], tree, tree.meta.line)

    def input_empty_brackets(self, tree):
        self.input(tree)

    def input(self, tree):
        var_name = tree.children[0].children[0]
        self.add_to_lookup(var_name, tree, tree.meta.line)

    def assign(self, tree):
        var_name = tree.children[0].children[0]
        self.add_to_lookup(var_name, tree.children[1], tree.meta.line)

    def assign_list(self, tree):
        var_name = tree.children[0].children[0]
        self.add_to_lookup(var_name, tree, tree.meta.line)

    # list access is added to the lookup table not because it must be escaped
    # for example we print(dieren[1]) not print('dieren[1]')

    def list_access(self, tree):
        list_name = escape_var(tree.children[0].children[0])
        position_name = escape_var(tree.children[1])
        if position_name == 'random':
            name = f'random.choice({list_name})'
        else:
            # We want list access to be 1-based instead of 0-based, hence the -1
            name = f'{list_name}[int({position_name})-1]'
        self.add_to_lookup(name, tree, tree.meta.line, True)

    def change_list_item(self, tree):
        self.add_to_lookup(tree.children[0].children[0], tree, tree.meta.line, True)

    def for_list(self, tree):
        iterator = str(tree.children[0].children[0])
        # the tree is trimmed to skip contain the inner commands of the loop since
        # they are not needed to infer the type of the iterator variable
        trimmed_tree = Tree(tree.data, tree.children[0:2], tree.meta)
        self.add_to_lookup(iterator, trimmed_tree, tree.meta.line)

    def for_loop(self, tree):
        iterator = str(tree.children[0].children[0])
        # the tree is trimmed to skip contain the inner commands of the loop since
        # they are not needed to infer the type of the iterator variable
        trimmed_tree = Tree(tree.data, tree.children[0:3], tree.meta)
        self.add_to_lookup(iterator, trimmed_tree, tree.meta.line)

    def add_to_lookup(self, name, tree, linenumber, skip_hashing=False):
        entry = LookupEntry(name, tree, linenumber, skip_hashing)
        hashed_name = escape_var(entry)
        entry.name = hashed_name
        self.lookup.append(entry)


# The transformer traverses the whole AST and infers the type of each node. It alters the lookup table entries with
# their inferred type. It also performs type validation for commands, e.g. 'text' + 1 results in error.
@v_args(tree=True)
class TypeValidator(Transformer):
    def __init__(self, lookup, level, lang, input_string):
        super().__init__()
        self.lookup = lookup
        self.level = level
        self.lang = lang
        self.input_string = input_string

    def print(self, tree):
        self.validate_args_type_allowed(Command.print, tree.children, tree.meta)

        return self.to_typed_tree(tree)

    def ask(self, tree):
        if self.level > 1:
            self.save_type_to_lookup(tree.children[0].children[0], HedyType.input)
        self.validate_args_type_allowed(Command.ask, tree.children[1:], tree.meta)
        return self.to_typed_tree(tree, HedyType.input)

    def input(self, tree):
        self.validate_args_type_allowed(Command.ask, tree.children[1:], tree.meta)
        return self.to_typed_tree(tree, HedyType.input)

    def forward(self, tree):
        if tree.children:
            self.validate_args_type_allowed(Command.forward, tree.children, tree.meta)
        return self.to_typed_tree(tree)

    def color(self, tree):
        if tree.children:
            self.validate_args_type_allowed(Command.color, tree.children, tree.meta)
        return self.to_typed_tree(tree)

    def turn(self, tree):
        if tree.children:
            name = tree.children[0].data
            if self.level > 1 or name not in command_turn_literals:
                self.validate_args_type_allowed(Command.turn, tree.children, tree.meta)
        return self.to_typed_tree(tree)

    def sleep(self, tree):
        if tree.children:
            self.validate_args_type_allowed(Command.sleep, tree.children, tree.meta)
        return self.to_typed_tree(tree)

    def assign(self, tree):
        try:
            type_ = self.get_type(tree.children[1])
            self.save_type_to_lookup(tree.children[0].children[0], type_)
        except hedy.exceptions.UndefinedVarException as ex:
            if self.level >= 12:
                raise hedy.exceptions.UnquotedAssignTextException(text=ex.arguments['name'])
            else:
                raise

        return self.to_typed_tree(tree, HedyType.none)

    def assign_list(self, tree):
        self.save_type_to_lookup(tree.children[0].children[0], HedyType.list)
        return self.to_typed_tree(tree, HedyType.list)

    def list_access(self, tree):
        self.validate_args_type_allowed(Command.list_access, tree.children[0], tree.meta)

        list_name = escape_var(tree.children[0].children[0])
        if tree.children[1] == 'random':
            name = f'random.choice({list_name})'
        else:
            # We want list access to be 1-based instead of 0-based, hence the -1
            name = f'{list_name}[int({tree.children[1]})-1]'
        self.save_type_to_lookup(name, HedyType.any)

        return self.to_typed_tree(tree, HedyType.any)

    def add(self, tree):
        self.validate_args_type_allowed(Command.add_to_list, tree.children[1], tree.meta)
        return self.to_typed_tree(tree)

    def remove(self, tree):
        self.validate_args_type_allowed(Command.remove_from_list, tree.children[1], tree.meta)
        return self.to_typed_tree(tree)

    def in_list_check(self, tree):
        self.validate_args_type_allowed(Command.in_list, tree.children[1], tree.meta)
        return self.to_typed_tree(tree, HedyType.boolean)

    def equality_check(self, tree):
        if self.level < 12:
            rules = [int_to_float, int_to_string, float_to_string, input_to_string, input_to_int, input_to_float]
        else:
            rules = [int_to_float, input_to_string, input_to_int, input_to_float]
        self.validate_binary_command_args_type(Command.equality, tree, rules)
        return self.to_typed_tree(tree, HedyType.boolean)

    def repeat(self, tree):
        command = Command.repeat
        allowed_types = get_allowed_types(command, self.level)
        self.check_type_allowed(command, allowed_types, tree.children[0], tree.meta)
        return self.to_typed_tree(tree, HedyType.none)

    def for_list(self, tree):
        command = Command.for_list
        allowed_types = get_allowed_types(command, self.level)
        self.check_type_allowed(command, allowed_types, tree.children[1], tree.meta)
        self.save_type_to_lookup(tree.children[0].children[0], HedyType.any)
        return self.to_typed_tree(tree, HedyType.none)

    def for_loop(self, tree):
        command = Command.for_loop
        allowed_types = get_allowed_types(command, self.level)

        start_type = self.check_type_allowed(command, allowed_types, tree.children[1], tree.meta)
        self.check_type_allowed(command, allowed_types, tree.children[2], tree.meta)

        iterator = str(tree.children[0])
        self.save_type_to_lookup(iterator, start_type)

        return self.to_typed_tree(tree, HedyType.none)

    def integer(self, tree):
        return self.to_typed_tree(tree, HedyType.integer)

    def text(self, tree):
        # under level 12 integers appear as text, so we parse them
        if self.level < 12:
            type_ = HedyType.integer if ConvertToPython.is_int(tree.children[0]) else HedyType.string
        else:
            type_ = HedyType.string
        return self.to_typed_tree(tree, type_)

    def text_in_quotes(self, tree):
        return self.to_typed_tree(tree.children[0], HedyType.string)

    def var_access(self, tree):
        return self.to_typed_tree(tree, HedyType.string)

    def var_access_print(self, tree):
        return self.var_access(tree)

    def var(self, tree):
        return self.to_typed_tree(tree, HedyType.none)

    def number(self, tree):
        number = tree.children[0]
        if ConvertToPython.is_int(number):
            return self.to_typed_tree(tree, HedyType.integer)
        if ConvertToPython.is_float(number):
            return self.to_typed_tree(tree, HedyType.float)
        # We managed to parse a number that cannot be parsed by python
        raise exceptions.ParseException(level=self.level, location='', found=number)

    def subtraction(self, tree):
        return self.to_sum_typed_tree(tree, Command.subtraction)

    def addition(self, tree):
        return self.to_sum_typed_tree(tree, Command.addition)

    def multiplication(self, tree):
        return self.to_sum_typed_tree(tree, Command.multiplication)

    def division(self, tree):
        return self.to_sum_typed_tree(tree, Command.division)

    def to_sum_typed_tree(self, tree, command):
        rules = [int_to_float, input_to_int, input_to_float]
        prom_left_type, prom_right_type = self.validate_binary_command_args_type(command, tree, rules)
        return TypedTree(tree.data, tree.children, tree.meta, prom_left_type)

    def smaller(self, tree):
        return self.to_comparison_tree(Command.smaller, tree)

    def smaller_equal(self, tree):
        return self.to_comparison_tree(Command.smaller_equal, tree)

    def bigger(self, tree):
        return self.to_comparison_tree(Command.bigger, tree)

    def bigger_equal(self, tree):
        return self.to_comparison_tree(Command.bigger_equal, tree)

    def not_equal(self, tree):
        rules = [int_to_float, input_to_int, input_to_float, input_to_string]
        self.validate_binary_command_args_type(Command.not_equal, tree, rules)
        return self.to_typed_tree(tree, HedyType.boolean)

    def to_comparison_tree(self, command, tree):
        allowed_types = get_allowed_types(command, self.level)
        self.check_type_allowed(command, allowed_types, tree.children[0], tree.meta)
        self.check_type_allowed(command, allowed_types, tree.children[1], tree.meta)
        return self.to_typed_tree(tree, HedyType.boolean)

    def validate_binary_command_args_type(self, command, tree, type_promotion_rules):
        allowed_types = get_allowed_types(command, self.level)

        left_type = self.check_type_allowed(command, allowed_types, tree.children[0], tree.meta)
        right_type = self.check_type_allowed(command, allowed_types, tree.children[1], tree.meta)

        if self.ignore_type(left_type) or self.ignore_type(right_type):
            return HedyType.any, HedyType.any

        prom_left_type, prom_right_type = promote_types([left_type, right_type], type_promotion_rules)

        if prom_left_type != prom_right_type:
            left_arg = tree.children[0].children[0]
            right_arg = tree.children[1].children[0]
            raise hedy.exceptions.InvalidTypeCombinationException(command, left_arg, right_arg, left_type, right_type)
        return prom_left_type, prom_right_type

    def validate_args_type_allowed(self, command, children, meta):
        allowed_types = get_allowed_types(command, self.level)
        children = children if type(children) is list else [children]
        for child in children:
            self.check_type_allowed(command, allowed_types, child, meta)

    def check_type_allowed(self, command, allowed_types, tree, meta=None):
        arg_type = self.get_type(tree)
        if arg_type not in allowed_types and not self.ignore_type(arg_type):
            variable = tree.children[0]

            if command in translatable_commands:
                keywords = translatable_commands[command]
                result = hedy_translation.find_command_keywords(
                    self.input_string,
                    self.lang,
                    self.level,
                    keywords,
                    meta.line,
                    meta.end_line,
                    meta.column - 1,
                    meta.end_column - 2)
                result = {k: v for k, v in result.items()}
                command = ' '.join([v.strip() for v in result.values() if v is not None])
            raise exceptions.InvalidArgumentTypeException(command=command, invalid_type=arg_type,
                                                          invalid_argument=variable, allowed_types=allowed_types)
        return arg_type

    def get_type(self, tree):
        # The rule var_access is used in the grammars definitions only in places where a variable needs to be accessed.
        # So, if it cannot be found in the lookup table, then it is an undefined variable for sure.
        if tree.data == 'var_access':
            var_name = tree.children[0]
            in_lookup, type_in_lookup = self.try_get_type_from_lookup(var_name)
            if in_lookup:
                return type_in_lookup
            else:
                raise hedy.exceptions.UndefinedVarException(name=var_name, line_number=tree.meta.line)

        if tree.data == 'var_access_print':
            var_name = tree.children[0]
            in_lookup, type_in_lookup = self.try_get_type_from_lookup(var_name)
            if in_lookup:
                return type_in_lookup
            else:
                # is there a variable that is mildly similar?
                # if so, we probably meant that one

                # we first check if the list of vars is empty since that is cheaper than stringdistancing.
                # TODO: Can be removed since fall back handles that now
                if len(self.lookup) == 0:
                    raise hedy.exceptions.UnquotedTextException(
                        level=self.level, unquotedtext=var_name, line_number=tree.meta.line)
                else:
                    # TODO: decide when this runs for a while whether this distance small enough!
                    minimum_distance_allowed = 4
                    for var_in_lookup in self.lookup:
                        if calculate_minimum_distance(var_in_lookup.name, var_name) <= minimum_distance_allowed:
                            raise hedy.exceptions.UndefinedVarException(name=var_name, line_number=tree.meta.line)

                    # nothing found? fall back to UnquotedTextException
                    raise hedy.exceptions.UnquotedTextException(
                        level=self.level, unquotedtext=var_name, line_number=tree.meta.line)

        # TypedTree with type 'None' and 'string' could be in the lookup because of the grammar definitions
        # If the tree has more than 1 child, then it is not a leaf node, so do not search in the lookup
        if tree.type_ in [HedyType.none, HedyType.string] and len(tree.children) == 1:
            in_lookup, type_in_lookup = self.try_get_type_from_lookup(tree.children[0])
            if in_lookup:
                return type_in_lookup
        # If the value is not in the lookup or the type is other than 'None' or 'string', return evaluated type
        return tree.type_

    def ignore_type(self, type_):
        return type_ in [HedyType.any, HedyType.none]

    def save_type_to_lookup(self, name, inferred_type):
        for entry in self.lookup:
            if entry.name == escape_var(name):
                entry.type_ = inferred_type

    # Usually, variable definitions are sequential and by the time we need the type of a lookup entry, it would already
    #  be inferred. However, there are valid cases in which the lookup entries will be accessed before their type
    #  is inferred. This is the case with for loops:
    #      for i in 1 to 10
    #          print i
    #  In the above case, we visit `print i`, before the definition of i in the for cycle. In this case, the tree of
    #  lookup entry is used to infer the type and continue the started validation. This approach might cause issues
    #  in case of cyclic references, e.g. b is b + 1. The flag `inferring` is used as a guard against these cases.
    def try_get_type_from_lookup(self, name):
        matches = [entry for entry in self.lookup if entry.name == escape_var(name)]
        if matches:
            match = matches[0]
            if not match.type_:
                if match.currently_inferring:  # there is a cyclic var reference, e.g. b = b + 1
                    raise exceptions.CyclicVariableDefinitionException(variable=match.name)
                else:
                    match.currently_inferring = True
                    try:
                        TypeValidator(self.lookup, self.level, self.lang, self.input_string).transform(match.tree)
                    except VisitError as ex:
                        raise ex.orig_exc
                    match.currently_inferring = False

            return True, self.lookup_type_fallback(matches[0].type_)
        return False, None

    def lookup_type_fallback(self, type_in_lookup):
        # If the entry is in the lookup table but its type has not been evaluated yet, then most probably this is a
        # variable referenced before it is defined. In this case, we rely on python to return an error. For now.
        return HedyType.any if type_in_lookup is None else type_in_lookup

    def to_typed_tree(self, tree, type_=HedyType.none):
        return TypedTree(tree.data, tree.children, tree.meta, type_)

    def __default__(self, data, children, meta):
        return TypedTree(data, children, meta, HedyType.none)


def flatten_list_of_lists_to_list(args):
    flat_list = []
    for element in args:
        if isinstance(
                element,
                str):  # str needs a special case before list because a str is also a list and we don't want to split all letters out
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
@v_args(meta=True)
class Filter(Transformer):
    def __default__(self, data, children, meta):
        result, args = are_all_arguments_true(children)
        return result, args, meta

    def program(self, meta, args):
        bool_arguments = [x[0] for x in args]
        if all(bool_arguments):
            return [True]  # all complete
        else:
            for a in args:
                if not a[0]:
                    return False, a[1]

    # leafs are treated differently, they are True + their arguments flattened
    def var(self, meta, args):
        return True, ''.join([str(c) for c in args]), meta

    def random(self, meta, args):
        return True, 'random', meta

    def number(self, meta, args):
        return True, ''.join([c for c in args]), meta

    def NEGATIVE_NUMBER(self, args):
        return True, ''.join([c for c in args]), None

    def text(self, meta, args):
        return all(args), ''.join([c for c in args]), meta


class UsesTurtle(Transformer):
    def __default__(self, args, children, meta):
        if len(children) == 0:  # no children? you are a leaf that is not Turn or Forward, so you are no Turtle command
            return False
        else:
            return any(type(c) == bool and c is True for c in children)

    # returns true if Forward or Turn are in the tree, false otherwise
    def forward(self, args):
        return True

    def color(self, args):
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

    def POSITIVE_NUMBER(self, args):
        return False

    def NEGATIVE_NUMBER(self, args):
        return False


class UsesPyGame(Transformer):
    def __default__(self, args, children, meta):
        if len(children) == 0:  # no children? you are a leaf that is not Pressed, so you are no PyGame command
            return False
        else:
            return any(type(c) == bool and c is True for c in children)

    def ifpressed(self, args):
        return True

    def ifpressed_else(self, args):
        return True

    def assign_button(self, args):
        return True


class AllCommands(Transformer):
    def __init__(self, level):
        self.level = level

    def translate_keyword(self, keyword):
        # some keywords have names that are not a valid name for a command
        # that's why we call them differently in the grammar
        # we have to translate them to the regular names here for further communciation
        if keyword in ['assign', 'assign_list']:
            return 'is'
        if keyword == 'ifelse':
            return 'else'
        if keyword == 'ifs':
            return 'if'
        if keyword == 'elifs':
            return 'elif'
        if keyword == 'for_loop':
            return 'for'
        if keyword == 'for_list':
            return 'for'
        if keyword == 'or_condition':
            return 'or'
        if keyword == 'and_condition':
            return 'and'
        if keyword == 'while_loop':
            return 'while'
        if keyword == 'in_list_check':
            return 'in'
        if keyword == 'input_empty_brackets':
            return 'input'
        if keyword == 'print_empty_brackets':
            return 'print'
        return str(keyword)

    def __default__(self, args, children, meta):
        # if we are matching a rule that is a command
        production_rule_name = self.translate_keyword(args)
        leaves = flatten_list_of_lists_to_list(children)
        # for the achievements we want to be able to also detct which operators were used by a kid
        operators = ['addition', 'subtraction', 'multiplication', 'division']

        if production_rule_name in commands_per_level[self.level] or production_rule_name in operators:
            if production_rule_name == 'else':  # use of else also has an if
                return ['if', 'else'] + leaves
            return [production_rule_name] + leaves
        else:
            return leaves  # 'pop up' the children

    def command(self, args):
        return args

    def program(self, args):
        return flatten_list_of_lists_to_list(args)

    # somehow tokens are not picked up by the default rule so they need their own rule
    def INT(self, args):
        return []

    def NAME(self, args):
        return []

    def NUMBER(self, args):
        return []

    def POSITIVE_NUMBER(self, args):
        return []

    def NEGATIVE_NUMBER(self, args):
        return []

    def text(self, args):
        return []


def all_commands(input_string, level, lang='en'):
    input_string = process_input_string(input_string, level, lang)
    program_root = parse_input(input_string, level, lang)

    return AllCommands(level).transform(program_root)


class AllPrintArguments(Transformer):
    def __init__(self, level):
        self.level = level

    def __default__(self, args, children, meta):
        leaves = flatten_list_of_lists_to_list(children)

        if args == 'print':
            return children
        else:
            return leaves  # 'pop up' the children

    def program(self, args):
        return flatten_list_of_lists_to_list(args)

    # somehow tokens are not picked up by the default rule so they need their own rule
    def INT(self, args):
        return []

    def NAME(self, args):
        return []

    def NUMBER(self, args):
        return []

    def POSITIVE_NUMBER(self, args):
        return []

    def NEGATIVE_NUMBER(self, args):
        return []

    def text(self, args):
        return ''.join(args)


def all_print_arguments(input_string, level, lang='en'):
    input_string = process_input_string(input_string, level, lang)
    program_root = parse_input(input_string, level, lang)

    return AllPrintArguments(level).transform(program_root)


@v_args(meta=True)
class IsValid(Filter):
    # all rules are valid except for the "Invalid" production rule
    # this function is used to generate more informative error messages
    # tree is transformed to a node of [Bool, args, command number]

    def error_invalid_space(self, meta, args):
        # return space to indicate that line starts in a space
        return False, InvalidInfo(" ", line=args[0][2].line, column=args[0][2].column), meta

    def error_print_nq(self, meta, args):
        words = [x[1] for x in args]  # second half of the list is the word
        text = ' '.join(words)
        return False, InvalidInfo("print without quotes", arguments=[
                                  text], line=meta.line, column=meta.column), meta

    def error_invalid(self, meta, args):
        # TODO: this will not work for misspelling 'at', needs to be improved!

        error = InvalidInfo('invalid command', command=args[0][1], arguments=[
                            [a[1] for a in args[1:]]], line=meta.line, column=meta.column)
        return False, error, meta

    def error_unsupported_number(self, meta, args):
        error = InvalidInfo('unsupported number', arguments=[str(args[0])], line=meta.line, column=meta.column)
        return False, error, meta

    def error_condition(self, meta, args):
        error = InvalidInfo('invalid condition', arguments=[str(args[0])], line=meta.line, column=meta.column)
        return False, error, meta

    def error_repeat_no_command(self, meta, args):
        error = InvalidInfo('invalid repeat', arguments=[str(args[0])], line=meta.line, column=meta.column)
        return False, error, meta

    def error_repeat_no_print(self, meta, args):
        error = InvalidInfo('repeat missing print', arguments=[str(args[0])], line=meta.line, column=meta.column)
        return False, error, meta

    def error_repeat_no_times(self, meta, args):
        error = InvalidInfo('repeat missing times', arguments=[str(args[0])], line=meta.line, column=meta.column)
        return False, error, meta

    def error_text_no_print(self, meta, args):
        error = InvalidInfo('lonely text', arguments=[str(args[0])], line=meta.line, column=meta.column)
        return False, error, meta

    def error_list_access_at(self, meta, args):
        error = InvalidInfo('invalid at keyword', arguments=[str(args[0])], line=meta.line, column=meta.column)
        return False, error, meta
    # other rules are inherited from Filter


def valid_echo(ast):
    commands = ast.children
    command_names = [x.children[0].data for x in commands]
    no_echo = 'echo' not in command_names

    # no echo is always ok!

    # otherwise, both have to be in the list and echo shold come after
    return no_echo or ('echo' in command_names and 'ask' in command_names) and command_names.index(
        'echo') > command_names.index('ask')


@v_args(meta=True)
class IsComplete(Filter):
    def __init__(self, level):
        self.level = level
    # print, ask and echo can miss arguments and then are not complete
    # used to generate more informative error messages
    # tree is transformed to a node of [True] or [False, args, line_number]

    def ask(self, meta, args):
        # in level 1 ask without arguments means args == []
        # in level 2 and up, ask without arguments is a list of 1, namely the var name
        incomplete = (args == [] and self.level == 1) or (len(args) == 1 and self.level >= 2)
        if meta is not None:
            return not incomplete, ('ask', meta.line)
        else:
            return not incomplete, ('ask', 1)

    def print(self, meta, args):
        return args != [], ('print', meta.line)

    def input(self, meta, args):
        return len(args) > 1, ('input', meta.line)

    def length(self, meta, args):
        return args != [], ('len', meta.line)

    def error_print_nq(self, meta, args):
        return args != [], ('print level 2', meta.line)

    def echo(self, meta, args):
        # echo may miss an argument
        return True, ('echo', meta.line)

    # other rules are inherited from Filter


def process_characters_needing_escape(value):
    # defines what happens if a kids uses ' or \ in in a string
    for c in characters_that_need_escaping:
        value = value.replace(c, f'\\{c}')
    return value


def get_allowed_types(command, level):
    # get only the allowed types of the command for all levels before the requested level
    allowed = [values for key, values in commands_and_types_per_level[command].items() if key <= level]
    # use the allowed types of the highest level available
    return allowed[-1] if allowed else []


# decorator used to store each class in the lookup table
def hedy_transpiler(level):
    def decorator(c):
        TRANSPILER_LOOKUP[level] = c
        c.level = level
        return c
    return decorator


@v_args(meta=True)
class ConvertToPython(Transformer):
    def __init__(self, lookup, numerals_language="Latin"):
        self.lookup = lookup
        self.numerals_language = numerals_language

    # default for line number is max lines so if it is not given, there
    # is no check on whether the var is defined
    def is_variable(self, variable_name, access_line_number=100):
        all_names = [a.name for a in self.lookup]
        all_names_before_access_line = [a.name for a in self.lookup if a.linenumber <= access_line_number]

        if variable_name in all_names and variable_name not in all_names_before_access_line:
            # referenced before assignment!
            definition_line_number = [a.linenumber for a in self.lookup if a.name == variable_name][0]
            raise hedy.exceptions.AccessBeforeAssign(
                name=variable_name,
                access_line_number=access_line_number,
                definition_line_number=definition_line_number)

        return escape_var(variable_name) in all_names_before_access_line

    def process_variable(self, arg, access_line_number=100):
        # processes a variable by hashing and escaping when needed
        if self.is_variable(arg, access_line_number):
            return escape_var(arg)
        if ConvertToPython.is_quoted(arg):
            arg = arg[1:-1]
        return f"'{process_characters_needing_escape(arg)}'"

    def process_variable_for_fstring(self, variable_name, access_line_number=100):
        if self.is_variable(variable_name, access_line_number):
            return "{" + escape_var(variable_name) + "}"
        else:
            return process_characters_needing_escape(variable_name)

    def process_variable_for_comparisons(self, name):
        # used to transform variables in comparisons
        if self.is_variable(name):
            return f"convert_numerals('{self.numerals_language}', {escape_var(name)})"
        elif ConvertToPython.is_float(name):
            return f"convert_numerals('{self.numerals_language}', {name})"
        elif ConvertToPython.is_quoted(name):
            return f"{name}"

    def make_f_string(self, args):
        argument_string = ''
        for argument in args:
            if self.is_variable(argument):
                # variables are placed in {} in the f string
                argument_string += "{" + escape_var(argument) + "}"
            else:
                # strings are written regularly
                # however we no longer need the enclosing quotes in the f-string
                # the quotes are only left on the argument to check if they are there.
                argument_string += argument.replace("'", '')

        return f"print(f'{argument_string}')"

    def get_fresh_var(self, name):
        while self.is_variable(name):
            name = '_' + name
        return name

    def check_var_usage(self, args, var_access_linenumber=100):
        # this function checks whether arguments are valid
        # we can proceed if all arguments are either quoted OR all variables

        def is_var_candidate(arg) -> bool:
            return not isinstance(arg, Tree) and \
                not ConvertToPython.is_int(arg) and \
                not ConvertToPython.is_float(arg)

        args_to_process = [a for a in args if is_var_candidate(a)]  # we do not check trees (calcs) they are always ok

        unquoted_args = [a for a in args_to_process if not ConvertToPython.is_quoted(a)]
        unquoted_in_lookup = [self.is_variable(a, var_access_linenumber) for a in unquoted_args]

        if unquoted_in_lookup == [] or all(unquoted_in_lookup):
            # all good? return for further processing
            return args
        else:
            # TODO: check whether this is really never raised??
            # return first name with issue
            first_unquoted_var = unquoted_args[0]
            raise exceptions.UndefinedVarException(name=first_unquoted_var, line_number=var_access_linenumber)

    # static methods
    @staticmethod
    def is_quoted(s):
        return len(s) > 1 and ((s[0] == "'" and s[-1] == "'") or (s[0] == '"' and s[-1] == '"'))

    @staticmethod
    def is_int(n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_random(s):
        return 'random.choice' in s

    @staticmethod
    def is_list(s):
        return '[' in s and ']' in s

    @staticmethod
    def indent(s, spaces_amount=2):
        lines = s.split('\n')
        return '\n'.join([' ' * spaces_amount + line for line in lines])


@v_args(meta=True)
@hedy_transpiler(level=1)
class ConvertToPython_1(ConvertToPython):

    def __init__(self, lookup, numerals_language):
        self.numerals_language = numerals_language
        self.lookup = lookup
        __class__.level = 1

    def program(self, meta, args):
        return '\n'.join([str(c) for c in args])

    def command(self, meta, args):
        return args[0]

    def text(self, meta, args):
        return ''.join([str(c) for c in args])

    def integer(self, meta, args):
        # remove whitespaces
        return str(int(args[0].replace(' ', '')))

    def number(self, meta, args):
        return str(int(args[0]))

    def NEGATIVE_NUMBER(self, meta, args):
        return str(int(args[0]))

    def print(self, meta, args):
        # escape needed characters
        argument = process_characters_needing_escape(args[0])
        return "print('" + argument + "')"

    def ask(self, meta, args):
        argument = process_characters_needing_escape(args[0])
        return "answer = input('" + argument + "')"

    def echo(self, meta, args):
        if len(args) == 0:
            return "print(answer)"  # no arguments, just print answer

        argument = process_characters_needing_escape(args[0])
        return "print('" + argument + " '+answer)"

    def comment(self, meta, args):
        return f"#{''.join(args)}"

    def empty_line(self, meta, args):
        return ''

    def forward(self, meta, args):
        if len(args) == 0:
            return sleep_after('t.forward(50)', False)
        return self.make_forward(int(args[0]))

    def color(self, meta, args):
        if len(args) == 0:
            return "t.pencolor('black')"  # no arguments defaults to black ink

        arg = args[0].data
        if arg in command_make_color:
            return f"t.pencolor('{arg}')"
        else:
            # the TypeValidator should protect against reaching this line:
            raise exceptions.InvalidArgumentTypeException(command=Command.color, invalid_type='', invalid_argument=arg,
                                                          allowed_types=get_allowed_types(Command.color, self.level))

    def turn(self, meta, args):
        if len(args) == 0:
            return "t.right(90)"  # no arguments defaults to a right turn

        arg = args[0].data
        if arg == 'left':
            return "t.left(90)"
        elif arg == 'right':
            return "t.right(90)"
        else:
            # the TypeValidator should protect against reaching this line:
            raise exceptions.InvalidArgumentTypeException(command=Command.turn, invalid_type='', invalid_argument=arg,
                                                          allowed_types=get_allowed_types(Command.turn, self.level))

    def make_turn(self, parameter):
        return self.make_turtle_command(parameter, Command.turn, 'right', False, 'int')

    def make_forward(self, parameter):
        return self.make_turtle_command(parameter, Command.forward, 'forward', True, 'int')

    def make_color(self, parameter):
        return self.make_turtle_color_command(parameter, Command.color, 'pencolor')

    def make_turtle_command(self, parameter, command, command_text, add_sleep, type):
        exception = ''
        if isinstance(parameter, str):
            exception = self.make_catch_exception([parameter])
        variable = self.get_fresh_var('__trtl')
        transpiled = exception + textwrap.dedent(f"""\
            {variable} = {parameter}
            try:
              {variable} = {type}({variable})
            except ValueError:
              raise Exception(f'While running your program the command {style_command(command)} received the value {style_command('{' + variable + '}')} which is not allowed. Try changing the value to a number.')
            t.{command_text}(min(600, {variable}) if {variable} > 0 else max(-600, {variable}))""")
        if add_sleep:
            return sleep_after(transpiled, False)
        return transpiled

    def make_turtle_color_command(self, parameter, command, command_text):
        variable = self.get_fresh_var('__trtl')
        return textwrap.dedent(f"""\
            {variable} = f'{parameter}'
            if {variable} not in {command_make_color}:
              raise Exception(f'While running your program the command {style_command(command)} received the value {style_command('{' + variable + '}')} which is not allowed. Try using another color.')
            t.{command_text}({variable})""")

    def make_catch_exception(self, args):
        lists_names = []
        list_args = []
        var_regex = r"[\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+|[\p{Mn}\p{Mc}\p{Nd}\p{Pc}·]+"
        # List usage comes in indexation and random choice
        list_regex = fr"(({var_regex})+\[int\(({var_regex})\)-1\])|(random\.choice\(({var_regex})\))"
        for arg in args:
            # Expressions come inside a Tree object, so unpack them
            if isinstance(arg, Tree):
                arg = arg.children[0]
            for group in regex.findall(list_regex, arg):
                if group[0] != '':
                    list_args.append(group[0])
                    lists_names.append(group[1])
                else:
                    list_args.append(group[3])
                    lists_names.append(group[4])
        code = ""
        exception_text_template = gettext('catch_index_exception')
        for i, list_name in enumerate(lists_names):
            exception_text = exception_text_template.replace('{list_name}', style_command(list_name))
            code += textwrap.dedent(f"""\
            try:
              {list_args[i]}
            except IndexError:
              raise Exception('{exception_text}')
            """)
        return code


@v_args(meta=True)
@hedy_transpiler(level=2)
class ConvertToPython_2(ConvertToPython_1):

    def error_ask_dep_2(self, meta, args):
        # ask is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1, 'ask', "ask_needs_var")

    def error_echo_dep_2(self, meta, args):
        # echo is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1, 'echo', "echo_out")

    def color(self, meta, args):
        if len(args) == 0:
            return "t.pencolor('black')"
        arg = args[0]
        if type(arg) != str:
            arg = arg.data

        arg = self.process_variable_for_fstring(arg)

        return self.make_color(arg)

    def turn(self, meta, args):
        if len(args) == 0:
            return "t.right(90)"  # no arguments defaults to a right turn
        arg = args[0]
        if self.is_variable(arg):
            return self.make_turn(escape_var(arg))
        if arg.lstrip("-").isnumeric():
            return self.make_turn(arg)

    def var(self, meta, args):
        name = args[0]
        return escape_var(name)

    def var_access(self, meta, args):
        name = args[0]
        self.check_var_usage(args, meta.line)
        return escape_var(name)

    def var_access_print(self, meta, args):
        return self.var_access(meta, args)

    def print(self, meta, args):
        args_new = []
        for a in args:
            # list access has been already rewritten since it occurs lower in the tree
            # so when we encounter it as a child of print it will not be a subtree, but
            # transpiled code (for example: random.choice(dieren))
            # therefore we should not process it anymore and thread it as a variable:
            # we set the line number to 100 so there is never an issue with variable access before
            # assignment (regular code will not work since random.choice(dieren) is never defined as var as such)
            if "random.choice" in a or "[" in a:
                args_new.append(self.process_variable_for_fstring(a, meta.line))
            else:
                # this regex splits words from non-letter characters, such that name! becomes [name, !]
                res = regex.findall(
                    r"[\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}\p{Mn}\p{Mc}\p{Nd}\p{Pc}]+|[^\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}]+", a)
                args_new.append(''.join([self.process_variable_for_fstring(x, meta.line) for x in res]))
        exception = self.make_catch_exception(args)
        argument_string = ' '.join(args_new)
        return exception + f"print(f'{argument_string}')"

    def ask(self, meta, args):
        var = args[0]
        all_parameters = ["'" + process_characters_needing_escape(a) + "'" for a in args[1:]]
        return f'{var} = input(' + '+'.join(all_parameters) + ")"

    def forward(self, meta, args):
        if len(args) == 0:
            return sleep_after('t.forward(50)', False)

        if ConvertToPython.is_int(args[0]):
            parameter = int(args[0])
        else:
            # if not an int, then it is a variable
            parameter = args[0]

        return self.make_forward(parameter)

    def assign(self, meta, args):
        parameter = args[0]
        value = args[1]
        if self.is_random(value) or self.is_list(value):
            exception = self.make_catch_exception([value])
            return exception + parameter + " = " + value
        else:
            if self.is_variable(value):
                value = self.process_variable(value, meta.line)
                return parameter + " = " + value
            else:
                # if the assigned value is not a variable and contains single quotes, escape them
                value = process_characters_needing_escape(value)
                return parameter + " = '" + value + "'"

    def sleep(self, meta, args):
        if not args:
            return "time.sleep(1)"
        else:
            value = f'"{args[0]}"' if self.is_int(args[0]) else args[0]
            exceptions = self.make_catch_exception(args)
            try_prefix = "try:\n" + textwrap.indent(exceptions, "  ")
            code = try_prefix + textwrap.dedent(f"""\
                  time.sleep(int({value}))
                except ValueError:
                  raise Exception(f'While running your program the command {style_command(Command.sleep)} received the value {style_command('{' + value + '}')} which is not allowed. Try changing the value to a number.')""")
            return code


@v_args(meta=True)
@hedy_transpiler(level=3)
class ConvertToPython_3(ConvertToPython_2):
    def assign_list(self, meta, args):
        parameter = args[0]
        values = [f"'{process_characters_needing_escape(a)}'" for a in args[1:]]
        return f"{parameter} = [{', '.join(values)}]"

    def list_access(self, meta, args):
        args = [escape_var(a) for a in args]

        # check the arguments (except when they are random or numbers, that is not quoted nor a var but is allowed)
        self.check_var_usage([a for a in args if a != 'random' and not a.isnumeric()], meta.line)

        if args[1] == 'random':
            return 'random.choice(' + args[0] + ')'
        else:
            return args[0] + '[int(' + args[1] + ')-1]'

    def process_argument(self, meta, arg):
        # only call process_variable if arg is a string, else keep as is (ie.
        # don't change 5 into '5', my_list[1] into 'my_list[1]')
        if arg.isnumeric() and isinstance(arg, int):  # is int/float
            return arg
        elif (self.is_list(arg)):  # is list indexing
            before_index, after_index = arg.split(']', 1)
            return before_index + '-1' + ']' + after_index   # account for 1-based indexing
        else:
            return self.process_variable(arg, meta.line)

    def add(self, meta, args):
        value = self.process_argument(meta, args[0])
        list_var = args[1]
        return f"{list_var}.append({value})"

    def remove(self, meta, args):
        value = self.process_argument(meta, args[0])
        list_var = args[1]
        return textwrap.dedent(f"""\
        try:
          {list_var}.remove({value})
        except:
          pass""")


@v_args(meta=True)
@hedy_transpiler(level=4)
class ConvertToPython_4(ConvertToPython_3):

    def process_variable_for_fstring(self, name):
        if self.is_variable(name):
            if self.numerals_language == "Latin":
                converted = escape_var(name)
            else:
                converted = f'convert_numerals("{self.numerals_language}",{escape_var(name)})'
            return "{" + converted + "}"
        else:
            if self.is_quoted(name):
                name = name[1:-1]
            return name.replace("'", "\\'")  # at level 4 backslashes are escaped in preprocessing, so we escape only '

    def var_access(self, meta, args):
        name = args[0]
        return escape_var(name)

    def var_access_print(self, meta, args):
        name = args[0]
        return escape_var(name)

    def print_ask_args(self, meta, args):
        args = self.check_var_usage(args, meta.line)
        result = ''
        for argument in args:
            argument = self.process_variable_for_fstring(argument)
            result += argument
        return result

    def print(self, meta, args):
        argument_string = self.print_ask_args(meta, args)
        exceptions = self.make_catch_exception(args)
        return exceptions + f"print(f'{argument_string}')"

    def ask(self, meta, args):
        var = args[0]
        argument_string = self.print_ask_args(meta, args[1:])
        return f"{var} = input(f'{argument_string}')"

    def error_print_nq(self, meta, args):
        return ConvertToPython_2.print(self, meta, args)

    def clear(self, meta, args):
        return f"""extensions.clear()
try:
    # If turtle is being used, reset canvas
    t.hideturtle()
    turtle.resetscreen()
    t.left(90)
    t.showturtle()
except NameError:
    pass"""


@v_args(meta=True)
@hedy_transpiler(level=5)
class ConvertToPython_5(ConvertToPython_4):
    def __init__(self, lookup, numerals_language):
        super().__init__(lookup, numerals_language)
        self.ifpressed_prefix_added = False

    def ifs(self, meta, args):
        return f"""if {args[0]}:
{ConvertToPython.indent(args[1])}"""

    def ifelse(self, meta, args):
        return f"""if {args[0]}:
{ConvertToPython.indent(args[1])}
else:
{ConvertToPython.indent(args[2])}"""

    def condition(self, meta, args):
        return ' and '.join(args)

    def condition_spaces(self, meta, args):
        arg0 = self.process_variable(args[0], meta.line)
        arg1 = self.process_variable(' '.join(args[1:]))
        return f"{arg0} == {arg1}"

    def equality_check(self, meta, args):
        arg0 = self.process_variable(args[0], meta.line)
        arg1 = ' '.join([self.process_variable(a) for a in args[1:]])
        return f"{arg0} == {arg1}"
        # TODO, FH 2021: zelfde change moet ik ook nog ff maken voor equal. check in hogere levels

    def in_list_check(self, meta, args):
        arg0 = self.process_variable(args[0], meta.line)
        arg1 = self.process_variable(args[1], meta.line)
        return f"{arg0} in {arg1}"

    def not_in_list_check(self, meta, args):
        arg0 = self.process_variable(args[0], meta.line)
        arg1 = self.process_variable(args[1], meta.line)
        return f"{arg0} not in {arg1}"

    def assign_button(self, meta, args):
        button_name = self.process_variable(args[0], meta.line)
        return f"""create_button({button_name})"""

    def make_ifpressed_command(self, command, button=False):
        command_suffix = (f"""\
while not pygame_end:
  pygame.display.update()
  event = pygame.event.wait()
  if event.type == pygame.QUIT:
    pygame_end = True
    pygame.quit()
    break""")

        if button:
            command = f"""\
  if event.type == pygame.USEREVENT:
{ConvertToPython.indent(command, 4)}"""
        else:
            command = f"""\
  if event.type == pygame.KEYDOWN:
{ConvertToPython.indent(command, 4)}"""

        if self.ifpressed_prefix_added:
            return command
        else:
            self.ifpressed_prefix_added = True
            return command_suffix + "\n" + command

    def ifpressed(self, meta, args):
        button_name = self.process_variable(args[0], meta.line)
        var_or_button = args[0]
        # for now we assume a var is a letter, we can check this lateron by searching for a ... = button
        if self.is_variable(var_or_button):
            return self.make_ifpressed_command(f"""\
if event.unicode == {args[0]}:
{ConvertToPython.indent(args[1])}
  break""", False)
        elif len(var_or_button) > 1:
            return self.make_ifpressed_command(f"""\
if event.key == {button_name}:
{ConvertToPython.indent(args[1])}
  break""", True)
        else:
            return self.make_ifpressed_command(f"""\
if event.unicode == '{args[0]}':
{ConvertToPython.indent(args[1])}
  break""")

    def ifpressed_else(self, meta, args):
        var_or_button = args[0]
        if self.is_variable(var_or_button):
            return self.make_ifpressed_command(f"""\
if event.key == {var_or_button}:
{ConvertToPython.indent(args[1])}
  break
else:
{ConvertToPython.indent(args[2])}
  break""", False)
        elif len(var_or_button) > 1:
            button_name = self.process_variable(args[0], meta.line)
            return self.make_ifpressed_command(f"""\
if event.key == {button_name}:
{ConvertToPython.indent(args[1])}
  break
else:
{ConvertToPython.indent(args[2])}
  break""", True)
        else:
            return self.make_ifpressed_command(f"""\
if event.unicode == '{args[0]}':
{ConvertToPython.indent(args[1])}
  break
else:
{ConvertToPython.indent(args[2])}
  break""")


@v_args(meta=True)
@hedy_transpiler(level=6)
class ConvertToPython_6(ConvertToPython_5):

    def print_ask_args(self, meta, args):
        # we only check non-Tree (= non calculation) arguments
        self.check_var_usage(args, meta.line)

        # force all to be printed as strings (since there can not be int arguments)
        args_new = []
        for a in args:
            if isinstance(a, Tree):
                if self.numerals_language == "Latin":
                    args_new.append("{" + a.children[0] + "}")
                else:
                    converted = f'convert_numerals("{self.numerals_language}",{a.children[0]})'
                    args_new.append("{" + converted + "}")
            else:
                args_new.append(self.process_variable_for_fstring(a))

        return ''.join(args_new)

    def equality_check(self, meta, args):
        arg0 = self.process_variable(args[0], meta.line)
        remaining_text = ' '.join(args[1:])
        arg1 = self.process_variable(remaining_text, meta.line)

        # FH, 2022 this used to be str but convert_numerals in needed to accept non-latin numbers
        # and works exactly as str for latin numbers (i.e. does nothing on str, makes 3 into '3')
        return f"convert_numerals('{self.numerals_language}', {arg0}) == convert_numerals('{self.numerals_language}', {arg1})"

    def assign(self, meta, args):
        parameter = args[0]
        value = args[1]
        if type(value) is Tree:
            return parameter + " = " + value.children[0]
        else:
            if self.is_variable(value):
                value = self.process_variable(value, meta.line)
                if self.is_list(value) or self.is_random(value):
                    exception = self.make_catch_exception([value])
                    return exception + parameter + " = " + value
                else:
                    return parameter + " = " + value
            else:
                # if the assigned value is not a variable and contains single quotes, escape them
                value = process_characters_needing_escape(value)
                return parameter + " = '" + value + "'"

    def process_token_or_tree(self, argument):
        if type(argument) is Tree:
            return f'{str(argument.children[0])}'
        if argument.isnumeric():
            latin_numeral = int(argument)
            return f'int({latin_numeral})'
        return f'int({argument})'

    def process_calculation(self, args, operator):
        # arguments of a sum are either a token or a
        # tree resulting from earlier processing
        # for trees we need to grap the inner string
        # for tokens we add int around them

        args = [self.process_token_or_tree(a) for a in args]
        return Tree('sum', [f'{args[0]} {operator} {args[1]}'])

    def addition(self, meta, args):
        return self.process_calculation(args, '+')

    def subtraction(self, meta, args):
        return self.process_calculation(args, '-')

    def multiplication(self, meta, args):
        return self.process_calculation(args, '*')

    def division(self, meta, args):
        return self.process_calculation(args, '//')

    def turn(self, meta, args):
        if len(args) == 0:
            return "t.right(90)"  # no arguments defaults to a right turn
        arg = args[0]
        if self.is_variable(arg):
            return self.make_turn(escape_var(arg))
        if isinstance(arg, Tree):
            return self.make_turn(arg.children[0])
        return self.make_turn(int(arg))

    def forward(self, meta, args):
        if len(args) == 0:
            return sleep_after('t.forward(50)', False)
        arg = args[0]
        if self.is_variable(arg):
            return self.make_forward(escape_var(arg))
        if isinstance(arg, Tree):
            return self.make_forward(arg.children[0])
        return self.make_forward(int(args[0]))


def sleep_after(commands, indent=True):
    lines = commands.split()
    if lines[-1] == "time.sleep(0.1)":  # we don't sleep double so skip if final line is a sleep already
        return commands

    sleep_command = "time.sleep(0.1)" if indent is False else "  time.sleep(0.1)"
    return commands + "\n" + sleep_command


@v_args(meta=True)
@hedy_transpiler(level=7)
class ConvertToPython_7(ConvertToPython_6):
    def repeat(self, meta, args):
        var_name = self.get_fresh_var('__i__')
        times = self.process_variable(args[0], meta.line)
        command = args[1]
        # in level 7, repeats can only have 1 line as their arguments
        command = sleep_after(command, False)
        self.ifpressed_prefix_added = False  # add ifpressed prefix again after repeat
        return f"""for {var_name} in range(int({str(times)})):
{ConvertToPython.indent(command)}"""


@v_args(meta=True)
@hedy_transpiler(level=8)
@v_args(meta=True)
@hedy_transpiler(level=9)
class ConvertToPython_8_9(ConvertToPython_7):

    def command(self, meta, args):
        return "".join(args)

    def repeat(self, meta, args):
        # todo fh, may 2022, could be merged with 7 if we make
        # indent a boolean parameter?

        var_name = self.get_fresh_var('i')
        times = self.process_variable(args[0], meta.line)

        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        body = "\n".join(all_lines)
        body = sleep_after(body)

        self.ifpressed_prefix_added = False  # add ifpressed prefix again after repeat
        return f"for {var_name} in range(int({times})):\n{body}"

    def ifs(self, meta, args):
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        return "if " + args[0] + ":\n" + "\n".join(all_lines)

    def ifpressed(self, met, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens

        all_lines = '\n'.join([x for x in args[1:]])
        all_lines = ConvertToPython.indent(all_lines)
        var_or_key = args[0]
        # if this is a variable, we assume it is a key (for now)
        if self.is_variable(var_or_key):
            return self.make_ifpressed_command(f"""\
if event.unicode == {args[0]}:
{all_lines}
  break""")
        elif len(var_or_key) == 1:  # one character? also a key!
            return self.make_ifpressed_command(f"""\
if event.unicode == '{args[0]}':
{all_lines}
  break""")
        else:  # otherwise we mean a button
            button_name = self.process_variable(args[0], met.line)
            return self.make_ifpressed_command(f"""\
if event.key == {button_name}:
{all_lines}
  break""", True)

    def ifpressed_else(self, met, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens

        all_lines = '\n'.join([x for x in args[1:]])
        all_lines = ConvertToPython.indent(all_lines)

        if (len(args[0]) > 1):
            button_name = self.process_variable(args[0], met.line)
            return self.make_ifpressed_command(f"""\
if event.key == {button_name}:
{all_lines}
  break
    """, True)
        else:
            return self.make_ifpressed_command(f"""\
if event.unicode == '{args[0]}':
{all_lines}
  break
    """)

    def elses(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args]

        return "\nelse:\n" + "\n".join(all_lines)

    def ifpressed_elses(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        args += ["  break\n"]

        all_lines = "\n".join(
            [ConvertToPython.indent(x, 4) for x in args]
        )

        return all_lines

    def var_access(self, meta, args):
        if len(args) == 1:  # accessing a var
            return escape_var(args[0])
        else:
            # this is list_access
            return escape_var(args[0]) + "[" + str(escape_var(args[1])) + "]" if type(args[1]
                                                                                      ) is not Tree else "random.choice(" + str(escape_var(args[0])) + ")"

    def var_access_print(self, meta, args):
        return self.var_access(meta, args)


@v_args(meta=True)
@hedy_transpiler(level=10)
class ConvertToPython_10(ConvertToPython_8_9):
    def for_list(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        times = self.process_variable(args[0], meta.line)

        body = "\n".join([ConvertToPython.indent(x) for x in args[2:]])

        body = sleep_after(body, True)
        self.ifpressed_prefix_added = False
        return f"for {times} in {args[1]}:\n{body}"


@v_args(meta=True)
@hedy_transpiler(level=11)
class ConvertToPython_11(ConvertToPython_10):
    def for_loop(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        iterator = escape_var(args[0])
        body = "\n".join([ConvertToPython.indent(x) for x in args[3:]])
        body = sleep_after(body)
        stepvar_name = self.get_fresh_var('step')
        begin = self.process_token_or_tree(args[1])
        end = self.process_token_or_tree(args[2])
        self.ifpressed_prefix_added = False  # add ifpressed prefix again after for loop
        return f"""{stepvar_name} = 1 if {begin} < {end} else -1
for {iterator} in range({begin}, {end} + {stepvar_name}, {stepvar_name}):
{body}"""


@v_args(meta=True)
@hedy_transpiler(level=12)
class ConvertToPython_12(ConvertToPython_11):
    def number(self, meta, args):
        # try all ints? return ints
        try:
            all_int = [str(int(x)) == x for x in args]
            if all(all_int):
                return ''.join(args)
            else:
                # int succeeds but does not return the same? these are non-latin numbers
                # and need to be casted
                return ''.join([str(int(x)) for x in args])
        except Exception:
            # if not? make into all floats
            numbers = [str(float(x)) for x in args]
            return ''.join(numbers)

    def NEGATIVE_NUMBER(self, meta, args):
        numbers = [str(float(x)) for x in args]
        return ''.join(numbers)

    def text_in_quotes(self, meta, args):
        # We need to re-add the quotes, so that the Python code becomes name = 'Jan' or "Jan's"
        text = args[0]
        if "'" in text:
            return f'"{text}"'
        return f"'{text}'"

    def process_token_or_tree(self, argument):
        if isinstance(argument, Tree):
            return f'{str(argument.children[0])}'
        else:
            return argument

    def print_ask_args(self, meta, args):
        result = super().print_ask_args(meta, args)
        if "'''" in result:
            raise exceptions.UnsupportedStringValue(invalid_value="'''")
        return result

    def print(self, meta, args):
        argument_string = self.print_ask_args(meta, args)
        exception = self.make_catch_exception(args)
        return exception + f"print(f'''{argument_string}''')"

    def ask(self, meta, args):
        var = args[0]
        argument_string = self.print_ask_args(meta, args[1:])
        assign = f"{var} = input(f'''{argument_string}''')"

        return textwrap.dedent(f"""\
        {assign}
        try:
          {var} = int({var})
        except ValueError:
          try:
            {var} = float({var})
          except ValueError:
            pass""")  # no number? leave as string

    def assign_list(self, meta, args):
        parameter = args[0]
        values = args[1:]
        return parameter + " = [" + ", ".join(values) + "]"

    def assign(self, meta, args):
        right_hand_side = args[1]
        left_hand_side = args[0]

        # we now need to check if the right hand side of te assign is
        # either a var or quoted, if it is not (and undefined var is raised)
        # the real issue is probably that the kid forgot quotes
        try:
            # check_var_usage expects a list of arguments so place this one in a list.
            self.check_var_usage([right_hand_side], meta.line)
        except exceptions.UndefinedVarException:
            # is the text a number? then no quotes are fine. if not, raise maar!

            if not (ConvertToPython.is_int(right_hand_side) or ConvertToPython.is_float(
                    right_hand_side) or ConvertToPython.is_random(right_hand_side)):
                raise exceptions.UnquotedAssignTextException(text=args[1])

        if isinstance(right_hand_side, Tree):
            exception = self.make_catch_exception([right_hand_side.children[0]])
            return exception + left_hand_side + " = " + right_hand_side.children[0]
        else:
            # we no longer escape quotes here because they are now needed
            exception = self.make_catch_exception([right_hand_side])
            return exception + left_hand_side + " = " + right_hand_side + ""

    def var(self, meta, args):
        name = args[0]
        self.check_var_usage(args, meta.line)
        return escape_var(name)

    def turn(self, meta, args):
        if len(args) == 0:
            return "t.right(90)"  # no arguments defaults to a right turn
        arg = args[0]
        if self.is_variable(arg):
            return self.make_turn(escape_var(arg))
        if isinstance(arg, Tree):
            return self.make_turn(arg.children[0])
        return self.make_turn(float(arg))

    def forward(self, meta, args):
        if len(args) == 0:
            return sleep_after('t.forward(50)', False)
        arg = args[0]
        if self.is_variable(arg):
            return self.make_forward(escape_var(arg))
        if isinstance(arg, Tree):
            return self.make_forward(arg.children[0])
        return self.make_forward(float(args[0]))

    def make_turn(self, parameter):
        return self.make_turtle_command(parameter, Command.turn, 'right', False, 'float')

    def make_forward(self, parameter):
        return self.make_turtle_command(parameter, Command.forward, 'forward', True, 'float')

    def division(self, meta, args):
        return self.process_calculation(args, '/')


@v_args(meta=True)
@hedy_transpiler(level=13)
class ConvertToPython_13(ConvertToPython_12):
    def and_condition(self, meta, args):
        return ' and '.join(args)

    def or_condition(self, meta, args):
        return ' or '.join(args)


@v_args(meta=True)
@hedy_transpiler(level=14)
class ConvertToPython_14(ConvertToPython_13):
    def process_comparison(self, meta, args, operator):

        arg0 = self.process_variable_for_comparisons(args[0])
        arg1 = self.process_variable_for_comparisons(args[1])

        simple_comparison = arg0 + operator + arg1

        if len(args) == 2:
            return simple_comparison  # no and statements
        else:
            return f"{simple_comparison} and {args[2]}"

    def equality_check_dequals(self, meta, args):
        return super().equality_check(meta, args)

    def smaller(self, meta, args):
        return self.process_comparison(meta, args, "<")

    def bigger(self, meta, args):
        return self.process_comparison(meta, args, ">")

    def smaller_equal(self, meta, args):
        return self.process_comparison(meta, args, "<=")

    def bigger_equal(self, meta, args):
        return self.process_comparison(meta, args, ">=")

    def not_equal(self, meta, args):
        return self.process_comparison(meta, args, "!=")


@v_args(meta=True)
@hedy_transpiler(level=15)
class ConvertToPython_15(ConvertToPython_14):
    def while_loop(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        body = "\n".join(all_lines)
        body = sleep_after(body)
        exceptions = self.make_catch_exception([args[0]])
        self.ifpressed_prefix_added = False  # add ifpressed prefix again after while loop
        return exceptions + "while " + args[0] + ":\n" + body


@v_args(meta=True)
@hedy_transpiler(level=16)
class ConvertToPython_16(ConvertToPython_15):
    def assign_list(self, meta, args):
        parameter = args[0]
        values = [a for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

    def change_list_item(self, meta, args):
        left_side = args[0] + '[' + args[1] + '-1]'
        right_side = args[2]
        exception_text = gettext('catch_index_exception').replace('{list_name}', style_command(args[0]))
        exception = textwrap.dedent(f"""\
        try:
          {left_side}
        except IndexError:
          raise Exception('{exception_text}')
        """)
        return exception + left_side + ' = ' + right_side

    def ifs(self, meta, args):
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        exceptions = self.make_catch_exception([args[0]])
        return exceptions + "if " + args[0] + ":\n" + "\n".join(all_lines)


@v_args(meta=True)
@hedy_transpiler(level=17)
class ConvertToPython_17(ConvertToPython_16):
    def elifs(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        return "\nelif " + args[0] + ":\n" + "\n".join(all_lines)


@v_args(meta=True)
@hedy_transpiler(level=18)
class ConvertToPython_18(ConvertToPython_17):
    def input(self, meta, args):
        return self.ask(meta, args)

    def input_is(self, meta, args):
        return self.input(meta, args)

    def input_equals(self, meta, args):
        return self.input(meta, args)

    def input_empty_brackets(self, meta, args):
        return self.input(meta, args)

    def print_empty_brackets(self, meta, args):
        return self.print(meta, args)


def merge_grammars(grammar_text_1, grammar_text_2, level):
    # this function takes two grammar files and merges them into one
    # rules that are redefined in the second file are overridden
    # rules that are new in the second file are added (remaining_rules_grammar_2)

    merged_grammar = []

    rules_grammar_1 = grammar_text_1.split('\n')
    remaining_rules_grammar_2 = grammar_text_2.split('\n')
    for line_1 in rules_grammar_1:
        if line_1 == '' or line_1[0] == '/':  # skip comments and empty lines:
            continue
        parts = line_1.split(':')
        # get part before are after : (this is a join because there can be : in the rule)
        name_1, definition_1 = parts[0], ''.join(parts[1:])

        rules_grammar_2 = grammar_text_2.split('\n')
        override_found = False
        for line_2 in rules_grammar_2:
            if line_2 == '' or line_2[0] == '/':  # skip comments and empty lines:
                continue

            needs_preprocessing = re.match(r'((\w|_)+)<((\w|_)+)>', line_2)
            if needs_preprocessing:
                name_2 = f'{needs_preprocessing.group(1)}'
                processor = needs_preprocessing.group(3)
            else:
                parts = line_2.split(':')
                name_2, definition_2 = parts[0], ''.join(parts[1])  # get part before are after :

            if name_1 == name_2:
                override_found = True
                if needs_preprocessing:
                    definition_2 = PREPROCESS_RULES[processor](definition_1)
                    line_2_processed = f'{name_2}: {definition_2}'
                else:
                    line_2_processed = line_2
                if definition_1.strip() == definition_2.strip():
                    warn_message = f"The rule {name_1} is duplicated on level {level}. Please check!"
                    warnings.warn(warn_message)
                # Used to compute the rules that use the merge operators in the grammar
                # namely +=, -= and >
                new_rule = merge_rules_operator(definition_1, definition_2, name_1, line_2_processed)
                # Already procesed so remove it
                remaining_rules_grammar_2.remove(line_2)
                break
        # new rule found? print that. nothing found? print org rule
        if override_found:
            merged_grammar.append(new_rule)
        else:
            merged_grammar.append(line_1)

    # all rules that were not overlapping are new in the grammar, add these too
    for rule in remaining_rules_grammar_2:
        if not (rule == '' or rule[0] == '/'):
            merged_grammar.append(rule)

    merged_grammar = sorted(merged_grammar)
    return '\n'.join(merged_grammar)


def merge_rules_operator(prev_definition, new_definition, name, complete_line):
    # Check if the rule is adding or substracting new rules
    has_add_op = new_definition.startswith('+=')
    has_sub_op = has_add_op and '-=' in new_definition
    has_last_op = has_add_op and '>' in new_definition
    if has_sub_op:
        # Get the rules we need to substract
        part_list = new_definition.split('-=')
        add_list, sub_list = (part_list[0], part_list[1]) if has_sub_op else (part_list[0], '')
        add_list = add_list[3:]
        # Get the rules that need to be last
        sub_list = sub_list.split('>')
        sub_list, last_list = (sub_list[0], sub_list[1]) if has_last_op else (sub_list[0], '')
        sub_list = sub_list + '|' + last_list
        result_cmd_list = get_remaining_rules(prev_definition, sub_list)
    elif has_add_op:
        # Get the rules that need to be last
        part_list = new_definition.split('>')
        add_list, sub_list = (part_list[0], part_list[1]) if has_last_op else (part_list[0], '')
        add_list = add_list[3:]
        last_list = sub_list
        result_cmd_list = get_remaining_rules(prev_definition, sub_list)
    else:
        result_cmd_list = prev_definition

    if has_last_op:
        new_rule = f"{name}: {result_cmd_list} | {add_list} | {last_list}"
    elif has_add_op:
        new_rule = f"{name}: {result_cmd_list} | {add_list}"
    else:
        new_rule = complete_line
    return new_rule


def get_remaining_rules(orig_def, sub_def):
    orig_cmd_list = [command.strip() for command in orig_def.split('|')]
    unwanted_cmd_list = [command.strip() for command in sub_def.split('|')]
    result_cmd_list = [cmd for cmd in orig_cmd_list if cmd not in unwanted_cmd_list]
    result_cmd_list = ' | '.join(result_cmd_list)  # turn the result list into a string
    return result_cmd_list


def create_grammar(level, lang="en"):
    # start with creating the grammar for level 1
    result = get_full_grammar_for_level(1)
    keywords = get_keywords_for_language(lang)

    result = merge_grammars(result, keywords, 1)
    # then keep merging new grammars in
    for i in range(2, level + 1):
        grammar_text_i = get_additional_rules_for_level(i)
        result = merge_grammars(result, grammar_text_i, i)

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


def get_additional_rules_for_level(level, sub=0):
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

# TODO FH, May 2022. I feel there are other places in the code where we also do this
# opportunity to combine?


def get_keywords_for_language(language):
    script_dir = path.abspath(path.dirname(__file__))
    try:
        if not local_keywords_enabled:
            raise FileNotFoundError("Local keywords are not enabled")
        filename = "keywords-" + str(language) + ".lark"
        with open(path.join(script_dir, "grammars", filename), "r", encoding="utf-8") as file:
            keywords = file.read()
    except FileNotFoundError:
        filename = "keywords-en.lark"
        with open(path.join(script_dir, "grammars", filename), "r", encoding="utf-8") as file:
            keywords = file.read()
    return keywords


PARSER_CACHE = {}


def get_parser(level, lang="en", keep_all_tokens=False):
    """Return the Lark parser for a given level.

    Uses caching if Hedy is NOT running in development mode.
    """
    key = str(level) + "." + lang + '.' + str(keep_all_tokens)
    existing = PARSER_CACHE.get(key)
    if existing and not utils.is_debug_mode():
        return existing
    grammar = create_grammar(level, lang)
    ret = Lark(grammar, regex=True, propagate_positions=True, keep_all_tokens=keep_all_tokens)  # ambiguity='explicit'
    PARSER_CACHE[key] = ret
    return ret


ParseResult = namedtuple('ParseResult', ['code', 'has_turtle', 'has_pygame'])


def transpile(input_string, level, lang="en"):
    transpile_result = transpile_inner(input_string, level, lang)
    return transpile_result


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


def line_requires_indentation(line, lang):
    # this is done a bit half-assed, clearly *parsing* the one line would be superior
    # because now a line like `repeat is 5` would also require indentation!

    line = line.lstrip()  # remove spaces since also `    for    ` requires indentation
    if lang not in indent_keywords.keys():  # some language like Greek or Czech do not have local keywords
        lang = 'en'

    local_indent_keywords = indent_keywords[lang]

    for k in local_indent_keywords:
        # does the line start with this keyword?
        # We can't just split since some langs like French have keywords containing a space
        # We also have to check space/lineending/: after or forward 100 wil also require indentation
        end_of_line_or_word = (len(line) > len(k) and (
            line[len(k)] == " " or line[len(k)] == ":")) or len(line) == len(k)
        if end_of_line_or_word and line[:len(k)] == k:
            return True
    return False


def preprocess_blocks(code, level, lang):
    processed_code = []
    lines = code.split("\n")
    current_number_of_indents = 0
    previous_number_of_indents = 0
    indent_size = 4  # set at 4 for now
    indent_size_adapted = False  # FH We can remove this now since we changed in indenter a bit in Nov 2022
    line_number = 0
    next_line_needs_indentation = False
    for line in lines:
        if ' _ ' in line or line == '_':
            raise hedy.exceptions.CodePlaceholdersPresentException

        leading_spaces = find_indent_length(line)

        # ignore whitespace-only lines
        if leading_spaces == len(line):
            processed_code.append('')
            continue

        line_number += 1

        # first encounter sets indent size for this program
        if not indent_size_adapted and leading_spaces > 0:
            indent_size = leading_spaces
            indent_size_adapted = True

        # indentation size not 4
        if (leading_spaces % indent_size) != 0:
            # there is inconsistent indentation, not sure if that is too much or too little!
            if leading_spaces < current_number_of_indents * indent_size:
                fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
                raise hedy.exceptions.NoIndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                             indent_size=indent_size, fixed_code=fixed_code)
            else:
                fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
                raise hedy.exceptions.IndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                           indent_size=indent_size, fixed_code=fixed_code)

        # happy path, multiple of 4 spaces:
        current_number_of_indents = leading_spaces // indent_size
        if current_number_of_indents > 1 and level == hedy.LEVEL_STARTING_INDENTATION:
            raise hedy.exceptions.LockedLanguageFeatureException(concept="nested blocks")

        if current_number_of_indents > previous_number_of_indents and not next_line_needs_indentation:
            # we are indenting, but this line is not following* one that even needs indenting, raise
            # * note that we have not yet updated the value of 'next line needs indenting' so if refers to this line!
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            raise hedy.exceptions.IndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                       indent_size=indent_size, fixed_code=fixed_code)

        if next_line_needs_indentation and current_number_of_indents <= previous_number_of_indents:
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            raise hedy.exceptions.NoIndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                         indent_size=indent_size, fixed_code=fixed_code)

        if current_number_of_indents - previous_number_of_indents > 1:
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            raise hedy.exceptions.IndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                       indent_size=indent_size, fixed_code=fixed_code)

        if current_number_of_indents < previous_number_of_indents:
            # we are dedenting ('jumping back) so we need to and an end-block
            # (multiple if multiple dedents are happening)

            difference_in_indents = (previous_number_of_indents - current_number_of_indents)
            for i in range(difference_in_indents):
                processed_code[-1] += '#ENDBLOCK'

        if line_requires_indentation(line, lang):
            next_line_needs_indentation = True
        else:
            next_line_needs_indentation = False

        # save to compare for next line
        previous_number_of_indents = current_number_of_indents

        # if indent remains the same, do nothing, just add line
        processed_code.append(line)

    # if the last line is indented, the end of the program is also the end of all indents
    # so close all blocks
    for i in range(current_number_of_indents):
        processed_code[-1] += '#ENDBLOCK'
    return "\n".join(processed_code)


def preprocess_ifs(code, lang='en'):
    processed_code = []
    lines = code.split("\n")

    def starts_with(command, line):
        if lang in ALL_KEYWORD_LANGUAGES:
            command_plus_translated_command = [command, KEYWORDS[lang].get(command)]
            for c in command_plus_translated_command:
                #  starts with the keyword and next character is a space
                if line[0:len(c)] == c and (len(c) == len(line) or line[len(c)] == ' '):
                    return True
            return False
        else:
            return line[0:len(command)] == command

    def starts_with_after_repeat(command, line):
        elements_in_line = line.split()
        repeat_plus_translated = ['repeat', KEYWORDS[lang].get('repeat')]
        times_plus_translated = ['times', KEYWORDS[lang].get('times')]

        if len(elements_in_line) > 2 and elements_in_line[0] in repeat_plus_translated and elements_in_line[2] in times_plus_translated:
            line = ' '.join(elements_in_line[3:])

        if lang in ALL_KEYWORD_LANGUAGES:
            command_plus_translated_command = [command, KEYWORDS[lang].get(command)]
            for c in command_plus_translated_command:
                #  starts with the keyword and next character is a space
                if line[0:len(c)] == c and (len(c) == len(line) or line[len(c)] == ' '):
                    return True
            return False
        else:
            return line[0:len(command)] == command

    def contains(command, line):
        if lang in ALL_KEYWORD_LANGUAGES:
            command_plus_translated_command = [command, KEYWORDS[lang].get(command)]
            for c in command_plus_translated_command:
                if c in line:
                    return True
            return False
        else:
            return command in line

    def contains_any_of(commands, line):
        # translation is not needed here, happens in contains
        if lang in ALL_KEYWORD_LANGUAGES:
            for c in commands:
                if contains(c, line):
                    return True
            return False
        else:
            for c in commands:
                if contains(c, line):
                    return True
            return False

    for i in range(len(lines) - 1):
        line = lines[i]
        next_line = lines[i + 1]

        # if this line starts with if but does not contain an else, and the next line too is not an else.
        if (starts_with('if', line) or starts_with_after_repeat('if', line)) and (not starts_with('else', next_line)) and (not contains('else', line)):
            # is this line just a condition and no other keyword (because that is no problem)
            commands = ["print", "ask", "forward", "turn"]

            if (
                contains_any_of(commands, line)
            ):  # and this should also (TODO) check for a second `is` cause that too is problematic.
                # a second command, but also no else in this line -> check next line!

                # no else in next line?
                # add a nop (like 'Pass' but we just insert a meaningless assign)
                line = line + " else _ is x"

        processed_code.append(line)
    processed_code.append(lines[-1])  # always add the last line (if it has if and no else that is no problem)
    return "\n".join(processed_code)


def contains_blanks(code):
    return (" _ " in code) or (" _" in code) or ("_ " in code) or (" _\n" in code)


def check_program_size_is_valid(input_string):
    number_of_lines = input_string.count('\n')
    # parser is not made for huge programs!
    if number_of_lines > MAX_LINES:
        raise exceptions.InputTooBigException(lines_of_code=number_of_lines, max_lines=MAX_LINES)


def process_input_string(input_string, level, lang, escape_backslashes=True):
    result = input_string.replace('\r\n', '\n')

    if contains_blanks(result):
        raise exceptions.CodePlaceholdersPresentException()

    if escape_backslashes and level >= 4:
        result = result.replace("\\", "\\\\")

    # In levels 5 to 8 we do not allow if without else, we add an empty print to make it possible in the parser
    if level >= 5 and level <= 8:
        result = preprocess_ifs(result, lang)

    # In level 8 we add indent-dedent blocks to the code before parsing
    if level >= hedy.LEVEL_STARTING_INDENTATION:
        result = preprocess_blocks(result, level, lang)

    return result


def parse_input(input_string, level, lang):
    parser = get_parser(level, lang)
    try:
        parse_result = parser.parse(input_string + '\n')
        return parse_result.children[0]  # getting rid of the root could also be done in the transformer would be nicer
    except lark.UnexpectedEOF:
        lines = input_string.split('\n')
        last_line = len(lines)
        raise exceptions.UnquotedEqualityCheck(line_number=last_line)
    except UnexpectedCharacters as e:
        try:
            location = e.line, e.column
            # not yet in use, could be used in the future (when our parser rules are
            # better organize, now it says ANON*__12 etc way too often!)
            # characters_expected = str(e.allowed)
            character_found = beautify_parse_error(e.char)
            # print(e.args[0])
            # print(location, character_found, characters_expected)
            fixed_code = program_repair.remove_unexpected_char(input_string, location[0], location[1])
            raise exceptions.ParseException(
                level=level,
                location=location,
                found=character_found,
                fixed_code=fixed_code) from e
        except UnexpectedEOF:
            # this one can't be beautified (for now), so give up :)
            raise e


def is_program_valid(program_root, input_string, level, lang):
    # IsValid returns (True,) or (False, args)
    instance = IsValid()
    instance.level = level  # TODO: could be done in a constructor once we are sure we will go this way
    is_valid = instance.transform(program_root)

    if not is_valid[0]:
        _, invalid_info = is_valid

        # Apparently, sometimes 'args' is a string, sometimes it's a list of
        # strings ( are these production rule names?). If it's a list of
        # strings, just take the first string and proceed.
        if isinstance(invalid_info, list):
            invalid_info = invalid_info[0]

        line = invalid_info.line
        column = invalid_info.column
        if invalid_info.error_type == ' ':

            # the error here is a space at the beginning of a line, we can fix that!
            fixed_code = program_repair.remove_leading_spaces(input_string)
            if fixed_code != input_string:  # only if we have made a successful fix
                try:
                    fixed_result = transpile_inner(fixed_code, level, lang)
                    result = fixed_result
                    raise exceptions.InvalidSpaceException(
                        level=level, line_number=line, fixed_code=fixed_code, fixed_result=result)
                except exceptions.HedyException:
                    invalid_info.error_type = None
                    transpile_inner(fixed_code, level)
                    # The fixed code contains another error. Only report the original error for now.
                    pass
            raise exceptions.InvalidSpaceException(
                level=level, line_number=line, fixed_code=fixed_code, fixed_result=result)
        elif invalid_info.error_type == 'invalid condition':
            raise exceptions.UnquotedEqualityCheck(line_number=line)
        elif invalid_info.error_type == 'invalid repeat':
            raise exceptions.MissingInnerCommandException(command='repeat', level=level, line_number=line)
        elif invalid_info.error_type == 'repeat missing print':
            raise exceptions.IncompleteRepeatException(command='print', level=level, line_number=line)
        elif invalid_info.error_type == 'repeat missing times':
            raise exceptions.IncompleteRepeatException(command='times', level=level, line_number=line)
        elif invalid_info.error_type == 'print without quotes':
            unquotedtext = invalid_info.arguments[0]
            raise exceptions.UnquotedTextException(
                level=level, unquotedtext=unquotedtext, line_number=invalid_info.line)
        elif invalid_info.error_type == 'unsupported number':
            raise exceptions.UnsupportedFloatException(value=''.join(invalid_info.arguments))
        elif invalid_info.error_type == 'lonely text':
            raise exceptions.LonelyTextException(level=level, line_number=line)
        elif invalid_info.error_type == 'invalid at keyword':
            raise exceptions.InvalidAtCommandException(command='at', level=level, line_number=invalid_info.line)
        else:
            invalid_command = invalid_info.command
            closest = closest_command(invalid_command, get_suggestions_for_language(lang, level))

            if closest == 'keyword':  # we couldn't find a suggestion
                invalid_command_en = hedy_translation.translate_keyword_to_en(invalid_command, lang)
                if invalid_command_en == Command.turn:
                    arg = invalid_info.arguments[0][0]
                    raise hedy.exceptions.InvalidArgumentException(command=invalid_info.command,
                                                                   allowed_types=get_allowed_types(Command.turn, level),
                                                                   invalid_argument=arg)
                # clearly the error message here should be better or it should be a different one!
                raise exceptions.ParseException(level=level, location=[line, column], found=invalid_command)
            elif closest is None:
                raise exceptions.MissingCommandException(level=level, line_number=line)

            else:

                fixed_code = None
                result = None
                fixed_code = input_string.replace(invalid_command, closest)
                if fixed_code != input_string:  # only if we have made a successful fix
                    try:
                        fixed_result = transpile_inner(fixed_code, level)
                        result = fixed_result
                    except exceptions.HedyException:
                        # The fixed code contains another error. Only report the original error for now.
                        pass

            raise exceptions.InvalidCommandException(invalid_command=invalid_command, level=level,
                                                     guessed_command=closest, line_number=line,
                                                     fixed_code=fixed_code, fixed_result=result)


def is_program_complete(abstract_syntax_tree, level):
    is_complete = IsComplete(level).transform(abstract_syntax_tree)
    if not is_complete[0]:
        incomplete_command_and_line = is_complete[1][0]
        incomplete_command = incomplete_command_and_line[0]
        line = incomplete_command_and_line[1]
        raise exceptions.IncompleteCommandException(incomplete_command=incomplete_command, level=level,
                                                    line_number=line)


def create_lookup_table(abstract_syntax_tree, level, lang, input_string):
    visitor = LookupEntryCollector(level)
    visitor.visit_topdown(abstract_syntax_tree)
    entries = visitor.lookup

    TypeValidator(entries, level, lang, input_string).transform(abstract_syntax_tree)

    return entries


def transpile_inner(input_string, level, lang="en"):
    check_program_size_is_valid(input_string)

    level = int(level)
    if level > HEDY_MAX_LEVEL:
        raise Exception(f'Levels over {HEDY_MAX_LEVEL} not implemented yet')

    input_string = process_input_string(input_string, level, lang)
    program_root = parse_input(input_string, level, lang)

    # checks whether any error production nodes are present in the parse tree
    is_program_valid(program_root, input_string, level, lang)

    try:
        abstract_syntax_tree = ExtractAST().transform(program_root)

        is_program_complete(abstract_syntax_tree, level)

        if not valid_echo(abstract_syntax_tree):
            raise exceptions.LonelyEchoException()

        lookup_table = create_lookup_table(abstract_syntax_tree, level, lang, input_string)

        # FH, may 2022. for now, we just out arabic numerals when the language is ar
        # this can be changed into a profile setting or could be detected
        # in usage of programs

        if lang == "ar":
            numerals_language = "Arabic"
        else:
            numerals_language = "Latin"
        # grab the right transpiler from the lookup
        convertToPython = TRANSPILER_LOOKUP[level]
        python = convertToPython(lookup_table, numerals_language).transform(abstract_syntax_tree)

        has_turtle = UsesTurtle().transform(abstract_syntax_tree)
        has_pygame = UsesPyGame().transform(abstract_syntax_tree)
        return ParseResult(python, has_turtle, has_pygame)
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
