import textwrap
from functools import lru_cache

import lark
from flask_babel import gettext
from lark import Lark
from lark.exceptions import UnexpectedEOF, UnexpectedCharacters, VisitError
from lark import Tree, Transformer, visitors, v_args
from os import path, getenv

import hedy
import hedy_error
import hedy_grammar
import hedy_translation
from utils import atomic_write_file
from hedy_content import ALL_KEYWORD_LANGUAGES
from collections import namedtuple
import re
import regex
from dataclasses import dataclass, field
import exceptions
import program_repair
import yaml
import hashlib
import os
import pickle
import sys
import tempfile
import utils

# Some useful constants
from hedy_content import KEYWORDS
from hedy_sourcemap import SourceMap, source_map_transformer

from prefixes.music import present_in_notes_mapping
from prefixes.normal import get_num_sys

HEDY_MAX_LEVEL = 18
HEDY_MAX_LEVEL_SKIPPING_FAULTY = 5
MAX_LINES = 100
LEVEL_STARTING_INDENTATION = 8

# Boolean variables to allow code which is under construction to not be executed
local_keywords_enabled = True

# dictionary to store transpilers
TRANSPILER_LOOKUP = {}
MICROBIT_TRANSPILER_LOOKUP = {}

# define source-map
source_map = SourceMap()

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

LIBRARIES = ['time']
# Python keywords and function names need hashing when used as var names
reserved_words = set(PYTHON_BUILTIN_FUNCTIONS + PYTHON_KEYWORDS + LIBRARIES)

# Let's retrieve all keywords dynamically from the cached KEYWORDS dictionary
indent_keywords = {}
for lang_, keywords in KEYWORDS.items():
    indent_keywords[lang_] = []
    for keyword in ['if', 'elif', 'for', 'repeat', 'while', 'else', 'define', 'def']:
        indent_keywords[lang_].append(keyword)  # always also check for En
        indent_keywords[lang_].append(keywords.get(keyword))


def make_value_error(command, tip, lang, value='{}'):
    return make_error_text(exceptions.RuntimeValueException(command=command, value=value, tip=tip), lang)


def make_values_error(command, tip, lang):
    return make_error_text(exceptions.RuntimeValuesException(command=command, value='{}', tip=tip), lang)


def make_error_text(ex, lang):
    # The error text is transpiled in f-strings with ", ' and ''' quotes. The only option is to use """.
    return f'"""{hedy_error.get_error_text(ex, lang)}"""'


def translate_suggestion(suggestion_type):
    # Right now we only have three types of suggestion
    # In the future we might change this if the number increases
    if suggestion_type == 'number':
        return gettext('suggestion_number')
    elif suggestion_type == 'color':
        return gettext('suggestion_color')
    elif suggestion_type == 'note':
        return gettext('suggestion_note')
    elif suggestion_type == 'numbers_or_strings':
        return gettext('suggestion_numbers_or_strings')
    return ''


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
    not_in_list = 'not in list'
    equality = 'is (equality)'
    repeat = 'repeat'
    for_list = 'for in'
    for_loop = 'for in range'
    if_ = 'if'
    else_ = 'else'
    elif_ = 'elif'
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
    define = 'define'
    call = 'call'
    returns = 'return'
    play = 'play'
    while_ = 'while'


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
                         Command.not_in_list: ['not in'],
                         Command.equality: ['is', '=', '=='],
                         Command.repeat: ['repeat', 'times'],
                         Command.for_list: ['for', 'in'],
                         Command.for_loop: ['in', 'range', 'to'],
                         Command.define: ['define'],
                         Command.call: ['call'],
                         Command.returns: ['return'], }


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


def add_level(commands, level, add=None, remove=None):
    # Adds the commands for the given level by taking the commands of the previous level
    # and adjusting the list based on which keywords need to be added or/and removed
    if not add:
        add = []
    if not remove:
        remove = []
    commands[level] = [c for c in commands[level - 1] if c not in remove] + add


# Commands per Hedy level which are used to suggest the closest command when kids make a mistake
commands_per_level = {1: ['ask', 'color', 'echo', 'forward', 'play', 'print', 'turn']}
add_level(commands_per_level, level=2, add=['is', 'sleep'], remove=['echo'])
add_level(commands_per_level, level=3, add=['add', 'at', 'from', 'random', 'remove', 'to'])
add_level(commands_per_level, level=4, add=['clear'])
add_level(commands_per_level, level=5, add=['assign_button', 'else', 'if', 'if_pressed', 'in', 'not_in'])
add_level(commands_per_level, level=6)
add_level(commands_per_level, level=7, add=['repeat', 'times'])
add_level(commands_per_level, level=8)
add_level(commands_per_level, level=9)
add_level(commands_per_level, level=10, add=['for'])
add_level(commands_per_level, level=11, add=['range'], remove=['times'])
add_level(commands_per_level, level=12, add=['define', 'call'])
add_level(commands_per_level, level=13, add=['and', 'or'])
add_level(commands_per_level, level=14)
add_level(commands_per_level, level=15, add=['while'])
add_level(commands_per_level, level=16)
add_level(commands_per_level, level=17, add=['elif'])
add_level(commands_per_level, level=18, add=['input'], remove=['ask'])

command_turn_literals = ['right', 'left']
english_colors = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow']


def color_commands_local(language):
    colors_local = [hedy_translation.translate_keyword_from_en(k, language) for k in english_colors]
    return colors_local


def command_make_color_local(language):
    if language == "en":
        return english_colors
    else:
        return english_colors + color_commands_local(language)


# Commands and their types per level (only partially filled!)
commands_and_types_per_level = {
    Command.print: {
        1: [HedyType.string, HedyType.integer, HedyType.input, HedyType.list],
        4: [HedyType.string, HedyType.integer, HedyType.input],
        12: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float],
        15: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.boolean],
        16: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.boolean, HedyType.list]
    },
    Command.ask: {
        1: [HedyType.string, HedyType.integer, HedyType.input, HedyType.list],
        4: [HedyType.string, HedyType.integer, HedyType.input],
        12: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float],
        15: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.boolean],
        16: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.boolean, HedyType.list]
    },
    Command.turn: {
        1: command_turn_literals,
        2: [HedyType.integer, HedyType.input],
        12: [HedyType.integer, HedyType.input, HedyType.float]
    },
    Command.color: {
        1: [english_colors, HedyType.list],
        2: [english_colors, HedyType.string, HedyType.input, HedyType.list]},
    Command.forward: {
        1: [HedyType.integer, HedyType.input],
        12: [HedyType.integer, HedyType.input, HedyType.float]
    },
    Command.sleep: {
        1: [HedyType.integer, HedyType.input],
        12: [HedyType.integer, HedyType.input, HedyType.float]
    },
    Command.list_access: {1: [HedyType.list]},
    Command.in_list: {1: [HedyType.list]},
    Command.not_in_list: {1: [HedyType.list]},
    Command.add_to_list: {1: [HedyType.list]},
    Command.remove_from_list: {1: [HedyType.list]},
    Command.equality: {
        1: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float],
        14: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.list],
        15: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.list, HedyType.boolean]
    },
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
    Command.not_equal: {
        14: [HedyType.integer, HedyType.float, HedyType.string, HedyType.input, HedyType.list, HedyType.boolean]
    },
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
            if command == 'if_pressed':  # TODO: this is a bit of a hack
                command = 'pressed'  # since in the yamls they are called pressed
            if command == 'assign_button':  # but in the grammar 'if_pressed'
                command = 'button'  # should be changed in the yaml eventually!
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
    var_name = var
    if isinstance(var, LookupEntry):
        var_name = var.name
    return "_" + var_name if var_name in reserved_words else var_name


def style_command(command):
    return f'<span class="command-highlighted">{command}</span>'


def closest_command(input_, known_commands, threshold=2):
    # Find the closest command to the input, i.e. the one with the smallest distance within the threshold. Returns:
    #  (None, _)  No suggestion. There is no command similar enough to the input. For example, the distance
    #             between 'eechoooo' and 'echo' is higher than the specified threshold.
    #  (False, _) Invalid suggestion. The suggested command is identical to the input, so it is not a suggestion.
    #             This is to prevent "print is not a command in Hedy level 3, did you mean print?" error message.
    #  (True, 'sug') Valid suggestion. A command is similar enough to the input but not identical, e.g. 'aks' -> 'ask'

    # FH, early 2020: simple string distance, could be more sophisticated MACHINE LEARNING!
    minimum_distance = 1000
    result = None
    for command in known_commands:
        minimum_distance_for_command = calculate_minimum_distance(command, input_)
        if minimum_distance_for_command < minimum_distance and minimum_distance_for_command <= threshold:
            minimum_distance = minimum_distance_for_command
            result = command

    if result:
        if result != input_:
            return True, result  # Valid suggestion
        return False, ''  # Invalid suggestion
    return None, ''  # No suggestion


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
    definition_line: int
    access_line: int
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

    def NAME(self, args):
        return ''.join([str(c) for c in args])

    def INT(self, args):
        return Tree('integer', [str(args)])

    def NUMBER(self, args):
        return Tree('number', [str(args)])

    def POSITIVE_NUMBER(self, args):
        return Tree('number', [str(args)])

    def NEGATIVE_NUMBER(self, args):
        return Tree('number', [str(args)])

    def TRUE(self, args):
        return Tree('true', [str(args)])

    def FALSE(self, args):
        return Tree('false', [str(args)])

    def boolean(self, meta, args):
        return args[0]

    # level 2
    def var(self, meta, args):
        return Tree('var', [''.join([str(c) for c in args])], meta)

    def list_access(self, meta, args):
        if isinstance(args[1], Tree) and "random" in args[1].data:
            return Tree('list_access', [args[0], 'random'], meta)
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

    # def var_access(self, tree):
    #     variable_name = tree.children[0].children[0]
    #     # store the line of access (or string value) in the lookup table
    #     # so we know what variable is used where
    #     vars = [a for a in self.lookup if a.name == variable_name]
    #     if vars:
    #         corresponding_lookup_entry = vars[0]
    #         corresponding_lookup_entry.access_line = tree.meta.line

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
        index = tree.children[1].children[0] if isinstance(tree.children[1], Tree) else tree.children[1]
        try:
            index = str(int(index))  # needed to convert non-latin numbers
            name = f'{list_name}.data[int({index})-1]'
            name_old = f'{list_name}[int({index})-1]'
        except ValueError:
            if index == 'random':
                name = f'random.choice({list_name}.data)'
                name_old = f'random.choice({list_name})'
            else:
                name = f'{list_name}.data[int({escape_var(index)}.data)-1]'
                name_old = f'{list_name}[int({escape_var(index)})-1]'
        if self.level > 5:
            self.add_to_lookup(name, tree, tree.meta.line, True)
        else:
            self.add_to_lookup(name_old, tree, tree.meta.line, True)

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

    def define(self, tree):
        self.add_to_lookup(str(tree.children[0].children[0]) + "()", tree, tree.meta.line)

        # add arguments to lookup
        if tree.children[1].data == 'arguments':
            for x in (c for c in tree.children[1].children if isinstance(c, Tree)):
                self.add_to_lookup(x.children[0], tree.children[1], tree.meta.line)

    def call(self, tree):
        function_name = tree.children[0].children[0]
        names = [x.name for x in self.lookup]
        if function_name + "()" not in names:
            raise exceptions.UndefinedFunctionException(function_name, tree.meta.line)

        args_str = ""
        if len(tree.children) > 1:
            args_str = ", ".join(str(x.children[0]) if isinstance(x, Tree) else str(x)
                                 for x in tree.children[1].children)
        self.add_to_lookup(f"{function_name}({args_str})", tree, tree.meta.line)

    def add_to_lookup(self, name, tree, definition_line=None, access_line=None, skip_hashing=False):
        entry = LookupEntry(name, tree, definition_line, access_line, skip_hashing)
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
                raise hedy.exceptions.UnquotedAssignTextException(
                    text=ex.arguments['name'],
                    line_number=tree.meta.line)
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
            name = f'random.choice({list_name}.data)'
        else:
            # We want list access to be 1-based instead of 0-based, hence the -1
            name = f'{list_name}.data[int({tree.children[1]})-1]'
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

    def not_in_list_check(self, tree):
        self.validate_args_type_allowed(Command.not_in_list, tree.children[1], tree.meta)
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
        t = tree.children[0] if tree.children else tree
        return self.to_typed_tree(t, HedyType.string)

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

    def true(self, tree):
        return self.to_typed_tree(tree, HedyType.boolean)

    def false(self, tree):
        return self.to_typed_tree(tree, HedyType.boolean)

    def subtraction(self, tree):
        return self.to_sum_typed_tree(tree, Command.subtraction)

    def addition(self, tree):
        return self.to_sum_typed_tree(tree, Command.addition)

    def multiplication(self, tree):
        return self.to_sum_typed_tree(tree, Command.multiplication)

    def division(self, tree):
        return self.to_sum_typed_tree(tree, Command.division)

    def to_sum_typed_tree(self, tree, command):
        rules = [int_to_float, input_to_int, input_to_float, input_to_string]
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
            raise hedy.exceptions.InvalidTypeCombinationException(
                command, left_arg, right_arg, left_type, right_type, tree.meta.line)
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
                                                          invalid_argument=variable, allowed_types=allowed_types,
                                                          line_number=meta.line)
        return arg_type

    def get_type(self, tree):
        # The rule var_access is used in the grammars definitions only in places where a variable needs to be accessed.
        # var_access_print is identical to var_access and is introduced only to differentiate error messages.
        # So, if it cannot be found in the lookup table, then it is an undefined variable for sure.
        if tree.data in ['var_access', 'var_access_print']:
            var_name = tree.children[0]
            in_lookup, type_in_lookup = self.try_get_type_from_lookup(var_name)
            if in_lookup:
                return type_in_lookup
            else:
                self.get_var_access_error(tree, var_name)

        # TypedTree with type 'None' and 'string' could be in the lookup because of the grammar definitions
        # If the tree has more than 1 child, then it is not a leaf node, so do not search in the lookup
        if tree.type_ in [HedyType.none, HedyType.string] and len(tree.children) == 1:
            in_lookup, type_in_lookup = self.try_get_type_from_lookup(tree.children[0])
            if in_lookup:
                return type_in_lookup
        # If the value is not in the lookup or the type is other than 'None' or 'string', return evaluated type
        return tree.type_

    def get_var_access_error(self, tree, var_name):
        # var_access_print is a var_access used in print statements to provide the following better error messages
        if tree.data == 'var_access_print':
            # is there a variable that is mildly similar? if so, we probably meant that one
            minimum_distance_allowed = 4
            for var_in_lookup in self.lookup:
                if calculate_minimum_distance(var_in_lookup.name, var_name) <= minimum_distance_allowed:
                    raise hedy.exceptions.UndefinedVarException(name=var_name, line_number=tree.meta.line)

            # no variable which looks similar? Then, fall back to UnquotedTextException
            raise hedy.exceptions.UnquotedTextException(
                level=self.level, unquotedtext=var_name, line_number=tree.meta.line)

        # for all other var_access instances, use UndefinedVarException
        raise hedy.exceptions.UndefinedVarException(name=var_name, line_number=tree.meta.line)

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
                    raise exceptions.CyclicVariableDefinitionException(
                        variable=match.name, line_number=match.tree.meta.line)
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

    def true(self, meta, args):
        return True, args[0], meta

    def false(self, meta, args):
        return True, args[0], meta

    def text(self, meta, args):
        return all(args), ''.join([c for c in args]), meta


class AllCommands(Transformer):
    def __init__(self, level):
        self.level = level

    def standardize_keyword(self, keyword):
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
        production_rule_name = self.standardize_keyword(args)
        leaves = flatten_list_of_lists_to_list(children)
        # for the achievements we want to be able to also detect which operators were used by a kid
        operators = ['addition', 'subtraction', 'multiplication', 'division']

        if production_rule_name in commands_per_level[
                self.level] or production_rule_name in operators or production_rule_name == 'if_pressed_else':
            # if_pressed_else is not in the yamls, upsetting lookup code to get an alternative later
            # lookup should be fixed instead, making a special case for now
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
    """Return the commands used in a program string.

    This function is still used in the web frontend, and some tests, but no longer by 'transpile'.
    """
    input_string = process_input_string(input_string, level, lang)
    program_root = parse_input(input_string, level, lang)

    return AllCommands(level).transform(program_root)


def all_variables(input_string, level, lang='en'):
    """Return all variables used in a program string.

    This function is still used by the roles of variables detection
    """
    program_root = parse_input(input_string, level, lang)
    abstract_syntax_tree = ExtractAST().transform(program_root)
    vars = set()
    lookup = create_lookup_table(abstract_syntax_tree, level, lang, input_string)
    for x in lookup:
        name = str(x.name)
        if '[' not in name:  # we also stor list access but that is not needed here
            vars.add(name)

    return list(vars)


@v_args(meta=True)
class IsValid(Filter):
    # all rules are valid except for the "Invalid" production rule
    # this function is used to generate more informative error messages
    # tree is transformed to a node of [Bool, args, command number]

    def __init__(self, level, lang, input_string):
        self.level = level
        self.lang = lang
        self.input_string = input_string

    def error_invalid_space(self, meta, args):
        line = args[0][2].line
        # the error here is a space at the beginning of a line, we can fix that!
        fixed_code, result = repair_leading_space(self.input_string, self.lang, self.level, line)
        raise exceptions.InvalidSpaceException(
            level=self.level, line_number=line, fixed_code=fixed_code, fixed_result=result)

    def error_ask_missing_variable(self, meta, args):
        raise exceptions.MissingVariableException(command='is ask', level=self.level, line_number=meta.line)

    def error_print_nq(self, meta, args):
        words = [str(x[1]).replace('\\\\', '\\') for x in args]  # second half of the list is the word
        text = find_unquoted_segments(' '.join(words))

        raise exceptions.UnquotedTextException(
            level=self.level,
            unquotedtext=text,
            line_number=meta.line
        )

    def error_ask_dep_2(self, meta, args):
        # ask is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1, 'ask', "ask_needs_var", meta.line)

    def error_echo_dep_2(self, meta, args):
        # echo is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1, 'echo', "echo_out", meta.line)

    def error_list_access(self, meta, args):
        raise exceptions.MisspelledAtCommand(command='at', arg1=str(args[1][1]), line_number=meta.line)

    def error_add_missing_to(self, meta, args):
        raise exceptions.MissingAdditionalCommand(command='add', missing_command='to', line_number=meta.line)

    def error_remove_missing_from(self, meta, args):
        raise exceptions.MissingAdditionalCommand(command='remove', missing_command='from', line_number=meta.line)

    def error_non_decimal(self, meta, args):
        raise exceptions.NonDecimalVariable(line_number=meta.line)

    def error_invalid(self, meta, args):
        invalid_command = args[0][1]
        sug_exists, suggestion = closest_command(invalid_command, get_suggestions_for_language(self.lang, self.level))

        if sug_exists is None:  # there is no suggestion
            raise exceptions.MissingCommandException(level=self.level, line_number=meta.line)
        if not sug_exists:  # the suggestion is invalid, i.e. identical to the command
            invalid_command_en = hedy_translation.translate_keyword_to_en(invalid_command, self.lang)
            if invalid_command_en == Command.turn:
                arg = args[1][1]
                raise hedy.exceptions.InvalidArgumentException(
                    command=invalid_command,
                    allowed_types=get_allowed_types(Command.turn, self.level),
                    invalid_argument=arg,
                    line_number=meta.line)
            # clearly the error message here should be better or it should be a different one!
            raise exceptions.ParseException(level=self.level, location=[meta.line, meta.column], found=invalid_command)
        else:  # there is a valid suggestion
            result = None
            fixed_code = self.input_string.replace(invalid_command, suggestion)
            if fixed_code != self.input_string:  # only if we have made a successful fix
                try:
                    fixed_result = transpile_inner(fixed_code, self.level)
                    result = fixed_result
                except exceptions.HedyException:
                    # The fixed code contains another error. Only report the original error for now.
                    pass

        raise exceptions.InvalidCommandException(invalid_command=invalid_command, level=self.level,
                                                 guessed_command=suggestion, line_number=meta.line,
                                                 fixed_code=fixed_code, fixed_result=result)

    def error_unsupported_number(self, meta, args):
        # add in , line=meta.line, column=meta.column
        raise exceptions.UnsupportedFloatException(value=''.join(str(args[0])))

    def error_condition(self, meta, args):
        raise exceptions.UnquotedEqualityCheckException(line_number=meta.line)

    def error_repeat_no_command(self, meta, args):
        raise exceptions.MissingInnerCommandException(command='repeat', level=self.level, line_number=meta.line)

    def error_repeat_no_print(self, meta, args):
        raise exceptions.IncompleteRepeatException(command='print', level=self.level, line_number=meta.line)

    def error_repeat_no_times(self, meta, args):
        raise exceptions.IncompleteRepeatException(command='times', level=self.level, line_number=meta.line)

    def error_repeat_dep_8(self, meta, args):
        # repeat is no longer usable this way, raise!
        raise hedy.exceptions.WrongLevelException(7, 'repeat', "repeat_dep", meta.line)

    def error_text_no_print(self, meta, args):
        raise exceptions.LonelyTextException(level=self.level, line_number=meta.line)

    def error_list_access_at(self, meta, args):
        raise exceptions.InvalidAtCommandException(command='at', level=self.level, line_number=meta.line)

    # flat if no longer allowed in level 8 and up
    def error_ifelse(self, meta, args):
        raise exceptions.WrongLevelException(
            offending_keyword='if',
            working_level=7,
            tip='no_more_flat_if',
            line_number=meta.line)

    def error_else_no_if(self, meta, args):
        raise exceptions.ElseWithoutIfException(meta.line)

    def error_for_missing_in(self, meta, args):
        raise exceptions.MissingAdditionalCommand(command='for', missing_command='in', line_number=meta.line)

    def error_for_missing_to(self, meta, args):
        raise exceptions.MissingAdditionalCommand(command='for', missing_command='to', line_number=meta.line)

    def error_for_missing_command(self, meta, args):
        raise exceptions.IncompleteCommandException(incomplete_command='for', level=self.level, line_number=meta.line)

    def error_assign_list_missing_brackets(self, meta, args):
        raise exceptions.MissingBracketsException(level=self.level, line_number=meta.line)

    def error_nested_define(self, meta, args):
        raise exceptions.NestedFunctionException()

    def error_if_pressed_missing_else(self, meta, args):
        raise exceptions.MissingElseForPressitException(
            command='ifpressed_else', level=self.level, line_number=meta.line)

    def if_pressed_no_colon(self, meta, args):
        raise exceptions.MissingColonException(command=Command.if_, line_number=meta.line)

    def if_pressed_elifs_no_colon(self, meta, args):
        # if_pressed_elifs starts with _EOL, so we need to add +1 to its line
        raise exceptions.MissingColonException(command=Command.elif_, line_number=meta.line + 1)

    def if_pressed_elses_no_colon(self, meta, args):
        # if_pressed_elses starts with _EOL, so we need to add +1 to its line
        raise exceptions.MissingColonException(command=Command.else_, line_number=meta.line + 1)

    def ifs_no_colon(self, meta, args):
        raise exceptions.MissingColonException(command=Command.if_, line_number=meta.line)

    def elifs_no_colon(self, meta, args):
        # elifs starts with _EOL, so we need to add +1 to its line
        raise exceptions.MissingColonException(command=Command.elif_, line_number=meta.line + 1)

    def elses_no_colon(self, meta, args):
        # elses starts with _EOL, so we need to add +1 to its line
        raise exceptions.MissingColonException(command=Command.else_, line_number=meta.line + 1)

    def for_list_no_colon(self, meta, args):
        raise exceptions.MissingColonException(command=Command.for_list, line_number=meta.line)

    def for_loop_no_colon(self, meta, args):
        raise exceptions.MissingColonException(command=Command.for_loop, line_number=meta.line)

    def while_loop_no_colon(self, meta, args):
        raise exceptions.MissingColonException(command=Command.while_, line_number=meta.line)

    def define_no_colon(self, meta, args):
        raise exceptions.MissingColonException(command=Command.define, line_number=meta.line)

    # other rules are inherited from Filter


@v_args(meta=True)
def valid_echo(ast):
    commands = ast.children
    command_names = [x.children[0].data for x in commands]
    no_echo = 'echo' not in command_names

    # no echo is always ok!

    # otherwise, both have to be in the list and echo should come after
    return no_echo or ('echo' in command_names and 'ask' in command_names) and command_names.index(
        'echo') > command_names.index('ask')


@v_args(meta=True)
class IsComplete(Filter):
    def __init__(self, level):
        self.level = level

    # ah so we actually have 2 types of "error productions"!
    # true ones that live in the grammar like error_ask_dep_2
    # and these ones where the parser combines valid and not valid
    # versions, like print: _PRINT (text)?

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


supported_quotes = {
    "'": "'",  # single straight quotation marks
    '"': '"',  # double straight quotation marks
    '‘': '’',  # single curved quotation marks
    "“": "”",  # double curved quotation marks or English quotes
    "„": "“",  # inward double curved quotation marks or German quotes
    "«": "»",  # guillemets or double angular marks or French quotes
}


def is_quoted(s):
    return isinstance(s, str) and len(s) > 1 and s[0] in supported_quotes and s[-1] in supported_quotes[s[0]]


def find_unquoted_segments(s):
    result = ''
    segment = ''
    used_quote = None
    for c in s:
        if not used_quote and c in supported_quotes:
            # if it is a valid opening quote, append the segment to the result and clear the buffer
            used_quote = c
            result += segment
            segment = c
        elif used_quote and c == supported_quotes[used_quote]:
            # if this is a valid closing quote, then empty the buffer as it holds a correctly quoted segment
            used_quote = None
            segment = ''
        else:
            segment += c

    # add a segment with a missing closing quote, if any
    result += segment
    return result


def get_allowed_types(command, level):
    # get only the allowed types of the command for all levels before the requested level
    allowed = [values for key, values in commands_and_types_per_level[command].items() if key <= level]
    # use the allowed types of the highest level available
    return allowed[-1] if allowed else []


def add_sleep_to_command(commands, indent=True, is_debug=False, location="after"):
    if is_debug:
        return commands

    lines = commands.split()
    if lines[-1] == "time.sleep(0.1)":  # we don't sleep double so skip if final line is a sleep already
        return commands

    sleep_command = "time.sleep(0.1)" if indent is False else "  time.sleep(0.1)"
    if location == "after":
        return commands + "\n" + sleep_command
    else:  # location is before
        return sleep_command + "\n" + commands


class BaseValue:
    """ Used to preserve localization information, such as numeral system, during transpilation. It has the following
    properties:
      - data holds the already transpiled Python value, e.g. 1, -50.5, 'Hedy', True, 'sum * 15'
      - num_sys keeps the used numeral system, e.g. 'Latin', 'Arabic'
      - booleans holds the actual keywords used to create the boolean value, e.g. {True: 'вярно', False: 'невярно'}"""

    def __init__(self, data, num_sys, booleans):
        self.data = data
        self.num_sys = num_sys
        self.booleans = booleans

    def __str__(self):
        return f"{self.__class__.__name__}({self.data}, {self.num_sys}, {self.booleans})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data}, {self.num_sys}, {self.booleans})"


class LiteralValue(BaseValue):
    """ Used to transpile numbers, booleans and texts. The `data` property contains the already transpiled value,
    e.g. 1, -50.5, 'Hedy', True, false. Note that in some cases variable access is parsed to a text node instead
    of a var_access and gets converted to a LiteralValue. If you need to check for variables, always assume they
    could come as plain strings or LiteralValues, i.e. 'variable' or LiteralValue('variable'). """

    def __init__(self, data, num_sys=None, booleans=None):
        super().__init__(data, num_sys, booleans)


class ExpressionValue(BaseValue):
    """ Used to transpile expressions. The data property contains the already transpiled expression,
    e.g. '5 * a', 'sum_with_error(a, b, get_error('error_name'))'. """

    def __init__(self, data, num_sys=None, bools=None):
        super().__init__(data, num_sys, bools)


# decorator used to store each class in the lookup table
def hedy_transpiler(level, microbit=False):
    def decorator(c):
        if not microbit:
            TRANSPILER_LOOKUP[level] = c
        else:
            MICROBIT_TRANSPILER_LOOKUP[level] = c
        c.level = level
        return c

    return decorator


@v_args(meta=True)
class ConvertToPython(Transformer):
    def __init__(self, lookup, language="en", is_debug=False):
        super().__init__()
        self.lookup = lookup
        self.language = language
        self.is_debug = is_debug

    def add_debug_breakpoint(self):
        if self.is_debug:
            return f" # __BREAKPOINT__"
        else:
            return ""

    def get_fresh_var(self, name):
        while self.is_variable(name):
            name = '_' + name
        return name

    def get_var_lookup_entries(self, var):
        """ Returns the lookup entries that match the provided variable name. Note that in the lookup table, variables
        are escaped but functions are not. In other words, the variable `sum` is stored as `_sum`, but the function
        `sum` is stored as `sum()`. When calling this method, don't escape func names. """
        def escape(arg):
            arg = str(arg)
            letter_or_underscore = r"[\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]"
            letter_or_numeral = r"[\p{Mn}\p{Mc}\p{Nd}\p{Pc}·]"
            var_regex = fr"{letter_or_underscore}({letter_or_underscore}|{letter_or_numeral})*"
            function_regex = fr"{var_regex}\("
            if regex.match(function_regex, arg):
                return escape_var(arg.split('(')[0])
            return escape_var(arg)

        return [entry for entry in self.lookup if escape(entry.name) == escape(var)]

    def is_var_defined_before_access(self, var, access_line, var_to_escape=''):
        """ Returns true if a variable is defined before being accessed. The `var_to_escape` parameter allows
        the ask command to force the left-hand-side variable to not be defined on the same line."""
        def is_before(entry, line):
            if entry.name != var_to_escape:
                return entry.definition_line <= line
            else:
                return entry.definition_line < line

        matching_lookup_entries = self.get_var_lookup_entries(var)
        return any([e for e in matching_lookup_entries if is_before(e, access_line)])

    def is_variable(self, arg, access_line=100):
        """ Checks whether the argument is a variable. However, this method DOES NOT require a var definition and should
        be used in places where the unquoted text can be interpreted also as a literal string. For example, in
        `add value to list` the arg `value` could be a variable or the literal string `value`. If the argument turns out
        to be a variable (and not an expression, a number or a quoted string):
         - its access will be registered in the lookup table
         - an exception will be raised if it is accessed before definition. Note that the default for access line is
         max lines of Hedy code. So, if it is not provided, there is no check on whether the var is defined."""
        # Unpacking is needed because sometimes a var reference is parsed as 'text' and transpiled to a LiteralValue
        var = self.unpack(arg)
        entries = self.get_var_lookup_entries(var)
        if entries:
            if not self.is_var_defined_before_access(var, access_line):
                raise hedy.exceptions.AccessBeforeAssignException(var, access_line, entries[0].definition_line)

            for e in entries:  # vars can be defined multiple times, access validates all of them
                e.access_line = access_line

        return entries != []

    def try_register_variable_access(self, var_name, access_line):
        """ Identical to is_variable() but used in places where no return value is needed (thus, the different name)"""
        self.is_variable(var_name, access_line)

    def is_variable_with_definition(self, arg, access_line=100):
        """ In case the arguments is an unquoted string, this method checks if it is correct variable usage with
        definition. This method should be used in places where an unquoted text CANNOT be interpreted as a literal
        string. For example, in `print 'Answer is ' answer` the arg `answer` must be a variable defined before the print
        statement. If the argument turns out to be a variable (and not an expression, a number or a quoted string):
         - its access will be registered in the lookup table
         - an exception will be raised if the variable is not defined, or it is accessed before definition."""
        value = self.unpack(arg)
        # expressions and trees are excluded from the check because they are not variables.
        # note that we need to unpack to do the boolean, number and quoted checks.
        is_var_candidate = not isinstance(arg, Tree) and \
            not isinstance(arg, ExpressionValue) and \
            not self.is_bool(value) and \
            not self.is_int(value) and \
            not self.is_float(value) and \
            not is_quoted(value)

        if is_var_candidate and not self.is_variable(arg, access_line):
            raise exceptions.UndefinedVarException(name=value, line_number=access_line)

        return is_var_candidate

    def has_variable_with_definition(self, args, access_line=100):
        """ Checks whether the unquoted text arguments are correct variable usages with definitions.
        Returns True if at least one of the provided arguments is a variable."""
        return any([self.is_variable_with_definition(a, access_line) for a in args])

    def check_variable_usage_and_definition(self, args, access_line=100):
        """ Identical to has_variable_with_definition() but used in places where no return value is needed
        Thus, the different name"""
        self.has_variable_with_definition(args, access_line)

    def merge_localization_info(self, args):
        """ Merges the localization information of all arguments. Currently, it works in the following manner:
            - take the numeral system of the first argument. If the arg is a LV or EV, return its numeral system.
              If it is a variable, determine the numeral system at runtime.
            - take the boolean representation of the first LV or EV argument that has booleans stored.
              Unfortunately, at this point we don't have a way to determine the boolean representation at runtime."""

        num_sys, bools = None, None
        if args:
            num_sys = args[0].num_sys if isinstance(args[0], BaseValue) else f'get_num_sys({args[0]})'
            bools = next((a.booleans for a in args if isinstance(a, BaseValue) and a.booleans is not None), None)
        return num_sys, bools

    def get_localization_info_from_arg(self, arg, access_line):
        if self.is_variable(arg, access_line):
            return f'get_num_sys({escape_var(arg)})'
        elif isinstance(arg, BaseValue):
            return f"'{arg.num_sys}'"
        else:
            return f'get_num_sys({arg})'

    def process_arg_for_data_access(self, arg, access_line=100, use_var_value=True):
        if self.is_variable(arg, access_line):
            return escape_var(arg)
        if is_quoted(arg):
            arg = arg[1:-1]
        return f"'{process_characters_needing_escape(arg)}'"

    def process_arg_for_fstring(self, arg, access_line=100, var_to_escape=''):
        """ Returns an argument prepared for a fstring. Note that it has a custom is_variable check. This is required,
        because until level 3 variables are sometimes interpreted as literal strings in fstrings. For example, consider:
           color = red, blue, yellow
           print What is your favorite color?
        In the print statement, `color` is not a var reference, but the literal string 'color'"""

        matching_entries = self.get_var_lookup_entries(arg)
        is_list = [e for e in matching_entries if e.type_ == HedyType.list and '[' not in e.name]
        is_var = not is_list and self.is_var_defined_before_access(arg, access_line, var_to_escape)

        if is_var:
            self.try_register_variable_access(arg, access_line)
            return "{" + escape_var(arg) + "}"
        else:
            return process_characters_needing_escape(arg)

    #
    # static methods
    #

    @staticmethod
    def check_if_error_skipped(tree):
        return hasattr(IsValid, tree.data)

    @staticmethod
    def is_int(n):
        try:
            int(n)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_float(n):
        try:
            float(n)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_random(s):
        return isinstance(s, str) and 'random.choice' in s

    @staticmethod
    def is_bool(s):
        return s in ['True', 'False']

    @staticmethod
    def is_list(s):
        return isinstance(s, str) and '[' in s and ']' in s

    @staticmethod
    def indent(s, spaces_amount=2):
        lines = s.split('\n')
        return '\n'.join([' ' * spaces_amount + line for line in lines])

    @staticmethod
    def unpack(arg):
        if isinstance(arg, Tree):
            # colors come as Tree('red', []), so we need get the Tree data
            return arg.data
        if isinstance(arg, BaseValue):
            return arg.data
        return arg

    @staticmethod
    def unpack_if_literal(arg):
        if isinstance(arg, LiteralValue):
            return arg.data
        return arg


@v_args(meta=True)
@hedy_transpiler(level=1)
@source_map_transformer(source_map)
class ConvertToPython_1(ConvertToPython):

    def __init__(self, lookup, language, is_debug):
        super().__init__(lookup, language, is_debug)
        __class__.level = 1

    def program(self, meta, args):
        return '\n'.join([str(c) for c in args])

    def command(self, meta, args):
        return args[0]

    def text(self, meta, args):
        return LiteralValue(''.join([str(c) for c in args]))

    def integer(self, meta, args):
        input_text = args[0].replace(' ', '')  # remove whitespaces
        return LiteralValue(int(input_text), num_sys=get_num_sys(input_text))

    def number(self, meta, args):
        input_text = ''.join([x for x in args])
        return LiteralValue(int(args[0]), num_sys=get_num_sys(input_text))

    def NEGATIVE_NUMBER(self, meta, args):
        input_text = ''.join([x for x in args])
        return LiteralValue(int(args[0]), num_sys=get_num_sys(input_text))

    def print(self, meta, args):
        argument = process_characters_needing_escape(self.unpack(args[0]))
        return f"print('{argument}'){self.add_debug_breakpoint()}"

    def ask(self, meta, args):
        argument = process_characters_needing_escape(self.unpack(args[0]))
        return f"answer = input('{argument}'){self.add_debug_breakpoint()}"

    def echo(self, meta, args):
        if not args:
            return f"print(answer){self.add_debug_breakpoint()}"  # no arguments, just print answer

        argument = process_characters_needing_escape(self.unpack(args[0]))
        return f"print('{argument} '+answer){self.add_debug_breakpoint()}"

    def play(self, meta, args):
        if not args:
            return self.make_play('C4', meta)

        note = self.unpack(args[0]).upper()  # will we also support multiple notes at once?
        return self.make_play(note, meta)

    def comment(self, meta, args):
        return f"#{''.join(args)}"

    def empty_line(self, meta, args):
        return ''

    def forward(self, meta, args):
        if not args:
            return add_sleep_to_command(f't.forward(50){self.add_debug_breakpoint()}',
                                        indent=False, is_debug=self.is_debug, location="after")
        return self.make_forward(int(self.unpack(args[0])))

    def color(self, meta, args):
        if not args:
            return f"t.pencolor('black'){self.add_debug_breakpoint()}"  # no arguments defaults to black ink

        arg = self.unpack(args[0])
        if arg in command_make_color_local(self.language):
            return f"t.pencolor('{arg}'){self.add_debug_breakpoint()}"
        else:
            # the TypeValidator should protect against reaching this line:
            raise exceptions.InvalidArgumentTypeException(command=Command.color, invalid_type='', invalid_argument=arg,
                                                          allowed_types=get_allowed_types(Command.color, self.level),
                                                          line_number=meta.line)

    def turn(self, meta, args):
        if not args:
            return f"t.right(90){self.add_debug_breakpoint()}"  # no arguments defaults to a right turn

        arg = args[0].data
        if arg == 'left':
            return f"t.left(90){self.add_debug_breakpoint()}"
        elif arg == 'right':
            return f"t.right(90){self.add_debug_breakpoint()}"
        else:
            # the TypeValidator should protect against reaching this line:
            raise exceptions.InvalidArgumentTypeException(command=Command.turn, invalid_type='', invalid_argument=arg,
                                                          allowed_types=get_allowed_types(Command.turn, self.level),
                                                          line_number=meta.line)

    def make_turn(self, parameter):
        return self.make_turtle_command(parameter, Command.turn, 'right', False, HedyType.integer)

    def make_forward(self, parameter):
        return self.make_turtle_command(parameter, Command.forward, 'forward', True, HedyType.integer)

    def make_play(self, note, meta):
        ex = make_value_error(Command.play, 'suggestion_note', self.language)

        return textwrap.dedent(f"""\
                play(note_with_error(localize('{note}'), {ex}))
                time.sleep(0.5)""") + self.add_debug_breakpoint()

    def make_play_var(self, note, meta):
        self.is_variable_with_definition(note, meta.line)
        chosen_note = note.children[0] if isinstance(note, Tree) else note
        ex = make_value_error(Command.play, 'suggestion_note', self.language)

        return textwrap.dedent(f"""\
                play(note_with_error({chosen_note}, {ex}))
                time.sleep(0.5)""") + self.add_debug_breakpoint()

    def make_turtle_command(self, parameter, command, command_text, add_sleep, target_type):
        list_index_exception = self.make_index_error_check_if_list([parameter]) if isinstance(parameter, str) else ''
        variable = self.get_fresh_var('__trtl')
        func = 'int_with_error' if target_type == HedyType.integer else 'number_with_error'
        ex = make_value_error(command, 'suggestion_number', self.language)
        transpiled = list_index_exception + textwrap.dedent(f"""\
            {variable} = {func}({parameter}, {ex})
            t.{command_text}(min(600, {variable}) if {variable} > 0 else max(-600, {variable})){self.add_debug_breakpoint()}""")
        if add_sleep and not self.is_debug:
            return add_sleep_to_command(transpiled, False, self.is_debug, location="after")
        return transpiled

    def make_turtle_color_command(self, parameter, command, command_text, language):
        both_colors = command_make_color_local(language)
        variable = self.get_fresh_var('__trtl')

        # we translate the color value to English at runtime, since it might be decided at runtime
        # coming from a random list or ask

        color_dict = {hedy_translation.translate_keyword_from_en(x, language): x for x in english_colors}
        ex = make_value_error(command, 'suggestion_color', self.language, parameter)
        return textwrap.dedent(f"""\
            {variable} = f'{parameter}'
            color_dict = {color_dict}
            if {variable} not in {both_colors}:
              raise Exception(f{ex})
            else:
              if not {variable} in {english_colors}:
                {variable} = color_dict[{variable}]
            t.{command_text}({variable}){self.add_debug_breakpoint()}""")

    def make_index_error_check_if_list(self, args):
        list_args = {}
        # List usage comes in indexation and random choice
        var_regex = r"([\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+|[\p{Mn}\p{Mc}\p{Nd}\p{Pc}·]+)(\.data)?"
        list_access_with_int_cast = fr"(({var_regex})+\[int\(({var_regex})\)-1\])"
        list_access_without_cast = fr"(({var_regex})+\[({var_regex})-1\])"
        list_access_random = fr"(random\.choice\(({var_regex})\))"
        list_regex = f"{list_access_with_int_cast}|{list_access_without_cast}|{list_access_random}"
        for arg in args:
            # arg could be a literal value, expression value or a tree, so unpack it
            arg = str(self.unpack(arg))
            for group in regex.findall(list_regex, arg):
                match = [e for e in group if e][:2]
                # match[0] is the access, e.g. animals[int(1)-1]; match[2] is the list name, e.g. animals
                list_args[match[0]] = match[1]

        errors = [self.make_index_error(list_access, list_name) for list_access, list_name in list_args.items()]
        return ''.join(errors)

    def make_index_error(self, code, list_name):
        exception_text = make_error_text(exceptions.RuntimeIndexException(name=list_name), self.language)
        return textwrap.dedent(f"""\
            try:
              {code}
            except IndexError:
              raise Exception({exception_text})
            """)


@v_args(meta=True)
@hedy_transpiler(level=2)
@source_map_transformer(source_map)
class ConvertToPython_2(ConvertToPython_1):
    def color(self, meta, args):
        if not args:
            return f"t.pencolor('black'){self.add_debug_breakpoint()}"

        value = self.unpack(args[0])
        value = self.process_arg_for_fstring(value)

        return self.make_turtle_color_command(value, Command.color, 'pencolor', self.language)

    def turn(self, meta, args):
        if not args:
            return f"t.right(90){self.add_debug_breakpoint()}"  # no arguments defaults to a right turn
        arg = self.unpack(args[0])
        if self.is_variable(arg, meta.line):
            return self.make_turn(escape_var(arg))
        # if not a variable, then the arg is an int
        return self.make_turn(arg)

    def forward(self, meta, args):
        if not args:
            return add_sleep_to_command(f't.forward(50){self.add_debug_breakpoint()}',
                                        indent=False, is_debug=self.is_debug, location="after")
        arg = self.unpack(args[0])
        if not self.is_variable(arg, meta.line):
            arg = int(arg)  # if not a variable, then the arg is an int
        return self.make_forward(escape_var(arg))

    def var(self, meta, args):
        name = args[0]
        return escape_var(name)

    def var_access(self, meta, args):
        name = args[0]
        self.is_variable_with_definition(name, meta.line)
        return escape_var(name)

    def var_access_print(self, meta, args):
        return self.var_access(meta, args)

    def print(self, meta, args):
        argument_string = self.process_print_ask_args(args, meta)
        exception = self.make_index_error_check_if_list(args)
        return exception + f"print(f'{argument_string}'){self.add_debug_breakpoint()}"

    def ask(self, meta, args):
        var = args[0]
        argument_string = self.process_print_ask_args(args[1:], meta, var)
        exception = self.make_index_error_check_if_list(args)
        return exception + f"{var} = input(f'{argument_string}'){self.add_debug_breakpoint()}"

    def process_print_ask_args(self, args, meta, var_to_escape=''):
        # list access has been already rewritten since it occurs lower in the tree
        # so when we encounter it as a child of print it will not be a subtree, but
        # transpiled code (for example: random.choice(dieren))
        # therefore we should not process it anymore and treat it as a variable:
        # we set the line number to 100 so there is never an issue with variable access before
        # assignment (regular code will not work since random.choice(dieren) is never defined as var as such)
        result = []
        for arg in args:
            arg = self.unpack(arg)
            if self.is_random(arg) or self.is_list(arg):
                result.append(self.process_arg_for_fstring(arg, meta.line, var_to_escape))
            else:
                # this regex splits words from non-letter characters, such that name! becomes [name, !]
                p = (r"[·\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}\p{Mn}\p{Mc}\p{Nd}\p{Pc}]+|"
                     r"[^·\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}]+")
                words = regex.findall(p, arg)
                result.append(''.join([self.process_arg_for_fstring(w, meta.line, var_to_escape) for w in words]))
        return ' '.join(result)

    def play(self, meta, args):
        if not args:
            return self.make_play('C4', meta)

        note = escape_var(self.unpack(args[0]))
        if present_in_notes_mapping(note):  # this is a supported note
            return self.make_play(note.upper(), meta)

        if not self.is_variable_with_definition(note, meta.line):
            note = f"'{note}'"

        ex = make_value_error(Command.play, 'suggestion_note', self.language)
        return textwrap.dedent(f"""\
                play(note_with_error(localize({note}), {ex}))
                time.sleep(0.5)""") + self.add_debug_breakpoint()

    def assign(self, meta, args):
        var_name = args[0]
        value = self.unpack(args[1])

        exception = self.make_index_error_check_if_list([value])
        if self.is_variable(value, meta.line):
            # if the assigned value is a variable, this is a reassign
            value = escape_var(value)
        else:
            # if it is not a variable, put it in single quotes and escape them
            value = f"'{process_characters_needing_escape(value)}'"
        return f"{exception}{var_name} = {value}{self.add_debug_breakpoint()}"

    def sleep(self, meta, args):
        if not args:
            return f"time.sleep(1){self.add_debug_breakpoint()}"

        value = escape_var(self.unpack(args[0]))
        value = f'"{value}"' if self.is_int(value) else value
        self.try_register_variable_access(value, meta.line)
        index_exception = self.make_index_error_check_if_list(args)
        ex = make_value_error(Command.sleep, 'suggestion_number', self.language)
        return f"{index_exception}time.sleep(int_with_error({value}, {ex})){self.add_debug_breakpoint()}"


@v_args(meta=True)
@hedy_transpiler(level=3)
@source_map_transformer(source_map)
class ConvertToPython_3(ConvertToPython_2):
    def assign_list(self, meta, args):
        parameter = self.unpack(args[0])
        values = [f"'{process_characters_needing_escape(str(self.unpack(a)))}'" for a in args[1:]]
        return f"{parameter} = [{', '.join(values)}]{self.add_debug_breakpoint()}"

    def list_access(self, meta, args):
        args = [escape_var(str(self.unpack(a))) for a in args]
        # filter the word `random` since it has a special meaning here and is not excluded in the check var usage
        vars_to_check = [a for a in args if a != 'random']
        self.check_variable_usage_and_definition(vars_to_check, meta.line)

        list_name = args[0]
        index = args[1]
        if index == 'random':
            return f'random.choice({list_name})'
        else:
            return f'{list_name}[int({index})-1]'

    def add(self, meta, args):
        value = self.process_add_to_remove_from_list_argument(self.unpack(args[0]), meta)
        list_name = self.unpack(args[1])

        # both sides have been used now
        self.try_register_variable_access(value, meta.line)
        self.try_register_variable_access(list_name, meta.line)
        return f"{list_name}.append({value}){self.add_debug_breakpoint()}"

    def remove(self, meta, args):
        value = self.process_add_to_remove_from_list_argument(self.unpack(args[0]), meta)
        list_name = self.unpack(args[1])

        # both sides have been used now
        self.try_register_variable_access(value, meta.line)
        self.try_register_variable_access(list_name, meta.line)

        return textwrap.dedent(f"""\
        try:
          {list_name}.remove({value}){self.add_debug_breakpoint()}
        except:
          pass""")

    def process_add_to_remove_from_list_argument(self, arg, meta):
        # only call process_variable if arg is a string, else keep as is (ie.
        # don't change 5 into '5', my_list[1] into 'my_list[1]')
        if self.is_list(arg):
            list_name = arg.split('[')[0]
            self.try_register_variable_access(list_name, meta.line)
            before_index, after_index = arg.split(']', 1)
            return before_index + '-1' + ']' + after_index  # account for 1-based indexing
        else:
            return self.process_arg_for_data_access(arg, meta.line)


@v_args(meta=True)
@hedy_transpiler(level=4)
@source_map_transformer(source_map)
class ConvertToPython_4(ConvertToPython_3):
    def process_arg_for_fstring(self, name, access_line=100, var_to_escape=''):
        name = escape_var(self.unpack(name))

        if self.is_variable(name):
            return f"{{{name}}}"

        if is_quoted(name):
            name = name[1:-1]

        # at level 4 backslashes are escaped in preprocessing, so we escape only '
        escaped_single_quotes = name.replace("'", "\\'")
        return escaped_single_quotes

    def var_access(self, meta, args):
        name = args[0]
        return escape_var(name)

    def var_access_print(self, meta, args):
        return self.var_access(meta, args)

    def process_print_ask_args(self, args, meta, var_to_escape=''):
        self.check_variable_usage_and_definition(args, meta.line)
        return ''.join([self.process_arg_for_fstring(a, meta.line) for a in args])

    def print(self, meta, args):
        argument_string = self.process_print_ask_args(args, meta)
        ex = self.make_index_error_check_if_list(args)
        return f"{ex}print(f'{argument_string}'){self.add_debug_breakpoint()}"

    def ask(self, meta, args):
        var = args[0]
        argument_string = self.process_print_ask_args(args[1:], meta)
        ex = self.make_index_error_check_if_list(args)
        return f"{ex}{var} = input(f'{argument_string}'){self.add_debug_breakpoint()}"

    def error_print_nq(self, meta, args):
        return ConvertToPython_2.print(self, meta, args)

    def clear(self, meta, args):
        command = textwrap.dedent(f"""\
        extensions.clear(){self.add_debug_breakpoint()}
        try:
            # If turtle is being used, reset canvas
            t.hideturtle()
            turtle.resetscreen()
            t.left(90)
            t.showturtle()
        except NameError:
            pass""")

        # add two sleeps, one is a bit brief
        command = add_sleep_to_command(command, False, self.is_debug, "before")
        command = add_sleep_to_command(command, False, self.is_debug, "before")

        return command


@v_args(meta=True)
@hedy_transpiler(level=5)
@source_map_transformer(source_map)
class ConvertToPython_5(ConvertToPython_4):
    def ifs(self, meta, args):  # might be worth asking if we want a debug breakpoint here
        return f"""if {args[0]}:{self.add_debug_breakpoint()}
{ConvertToPython.indent(args[1])}"""

    def ifelse(self, meta, args):
        return f"""if {args[0]}:{self.add_debug_breakpoint()}
{ConvertToPython.indent(args[1])}
else:{self.add_debug_breakpoint()}
{ConvertToPython.indent(args[2])}"""

    def condition(self, meta, args):
        return ' and '.join(args)

    def condition_spaces(self, meta, args):
        arg0 = self.process_arg_for_data_access(self.unpack(args[0]), meta.line)
        arg1 = self.process_arg_for_data_access(' '.join([self.unpack(a) for a in args[1:]]))
        return f"localize({arg0}) == localize({arg1})"

    def equality_check(self, meta, args):
        lhs = self.process_arg_for_data_access(str(self.unpack(args[0])), meta.line)
        rhs = self.process_arg_for_data_access(str(self.unpack(args[1])).strip(), meta.line)
        # In level 5 the values of variables are always strings (numbers are added in level 6)
        # So, to compare numbers of diff numeral systems, we use localize()
        return f"localize({lhs}) == localize({rhs})"

    def in_list_check(self, meta, args):
        arg0 = self.process_arg_for_data_access(self.unpack(args[0]), meta.line)
        arg1 = self.process_arg_for_data_access(self.unpack(args[1]), meta.line)
        # In level 5 the values of variables are always strings (numbers are added in level 6)
        # So, to check if a number is in a list of numbers with diff numeral system, we use localize()
        return f"localize({arg0}) in [localize(__la) for __la in {arg1}]"

    def not_in_list_check(self, meta, args):
        arg0 = self.process_arg_for_data_access(self.unpack(args[0]), meta.line)
        arg1 = self.process_arg_for_data_access(self.unpack(args[1]), meta.line)
        # In level 5 the values of variables are always strings (numbers are added in level 6)
        # So, to check if a number is not in a list of numbers with diff numeral system, we use localize()
        return f"localize({arg0}) not in [localize(__la) for __la in {arg1}]"

    def assign_button(self, meta, args):
        button_name = self.process_arg_for_data_access(args[0], meta.line)
        return f"""create_button({button_name})"""

    def make_function_name(self, key_name):
        return f"if_pressed_{key_name}_"

    def make_function(self, function_name, body):
        return (
            f'def {function_name}():' + '\n' +
            ConvertToPython.indent(body)
        )

    def clear_key_mapping(self):
        return 'if_pressed_mapping = {"else": "if_pressed_default_else"}'

    def add_if_key_mapping(self, key, function_name):
        return f"if_pressed_mapping['{key}'] = '{function_name}'"

    def add_else_key_mapping(self, function_name):
        return f"if_pressed_mapping['else'] = '{function_name}'"

    def make_extension_call(self):
        return 'extensions.if_pressed(if_pressed_mapping)'

    def if_pressed_without_else(self, meta, args):
        raise exceptions.MissingElseForPressitException(
            command='if_pressed_else', level=self.level, line_number=meta.line
        )

    def if_pressed_else(self, meta, args):
        self.process_arg_for_data_access(args[0], meta.line)
        key = args[0]

        if_code = args[1]
        if_function_name = self.make_function_name(key)

        else_code = args[2]
        else_function_name = self.make_function_name('else')

        return (
            self.clear_key_mapping() + '\n' +
            self.add_if_key_mapping(key, if_function_name) + '\n' +
            self.add_else_key_mapping(else_function_name) + '\n' +
            self.make_function(if_function_name, if_code) + '\n' +
            self.make_function(else_function_name, else_code) + '\n' +
            self.make_extension_call()
        )


@v_args(meta=True)
@hedy_transpiler(level=6)
@source_map_transformer(source_map)
class ConvertToPython_6(ConvertToPython_5):
    def turn(self, meta, args):
        if not args:
            return "t.right(90)" + self.add_debug_breakpoint()  # no arguments defaults to a right turn
        arg = args[0]
        if self.is_variable_with_definition(arg, meta.line):
            value = f'{escape_var(self.unpack(arg))}.data'
        else:
            value = f'{self.unpack(arg)}'
        return self.make_turn(value)

    def forward(self, meta, args):
        if not args:
            return add_sleep_to_command('t.forward(50)' + self.add_debug_breakpoint(), indent=False,
                                        is_debug=self.is_debug, location="after")
        arg = args[0]
        if self.is_variable_with_definition(arg, meta.line):
            value = f'{escape_var(self.unpack(arg))}.data'
        else:
            value = f'{self.unpack(arg)}'
        return self.make_forward(value)

    def sleep(self, meta, args):
        if not args:
            return "time.sleep(1)"

        arg = args[0]
        if type(arg) is Tree and self.check_if_error_skipped(arg):
            raise hedy.exceptions.InvalidErrorSkippedException

        if self.is_variable_with_definition(arg, meta.line):
            value = f'{escape_var(self.unpack(arg))}.data'
        else:
            value = f'"{self.unpack(arg)}"'
        index_exception = self.make_index_error_check_if_list(args)
        ex = make_value_error(Command.sleep, 'suggestion_number', self.language)
        return index_exception + textwrap.dedent(f"time.sleep(int_with_error({value}, {ex}))")

    def ask(self, meta, args):
        var = args[0]
        argument_string = self.process_print_ask_args(args[1:], meta)
        ex = self.make_index_error_check_if_list(args)
        return ex + textwrap.dedent(f"""\
            {var} = input(f'{argument_string}'){self.add_debug_breakpoint()}
            __ns = get_num_sys({var})
            {var} = Value({var}, num_sys=__ns)""")

    def play(self, meta, args):
        if not args:
            return self.make_play('C4', meta)

        arg = args[0]
        note = escape_var(self.unpack(arg))
        if present_in_notes_mapping(note):  # this is a supported note
            return self.make_play(note.upper(), meta)

        if self.is_variable_with_definition(arg, meta.line):
            arg = f'{escape_var(self.unpack(arg))}.data'
        elif isinstance(arg, LiteralValue):
            arg = f"{arg.data}" if is_quoted(arg.data) else f"'{arg.data}'"
        elif isinstance(arg, ExpressionValue):
            arg = arg.data
        else:
            # We end up here in case of list access, e.g. 'random.choice[animals]'
            arg = f"{arg}.data"

        ex = make_value_error(Command.play, 'suggestion_note', self.language)
        return textwrap.dedent(f"""\
                play(note_with_error(localize({arg}), {ex}))
                time.sleep(0.5)""") + self.add_debug_breakpoint()

    def process_arg_for_fstring(self, name, access_line=100, var_to_escape=''):
        if self.is_variable(name) or self.is_list(name) or self.is_random(name):
            return f"{{{escape_var(self.unpack(name))}}}"
        elif isinstance(name, LiteralValue):
            return self.process_literal_for_fstring(name)
        elif isinstance(name, ExpressionValue):
            return self.process_expression_for_fstring(name)
        elif is_quoted(name):
            name = name[1:-1]
            return name.replace("'", "\\'")
        elif not ConvertToPython.is_int(name) and not ConvertToPython.is_float(name):
            # We end up here with colors
            return name.replace("'", "\\'")
        return str(name)

    def equality_check(self, meta, args):
        left_hand_side = self.process_arg_for_data_access(args[0], meta.line)
        right_hand_side = self.process_arg_for_data_access(args[1], meta.line)

        # Until level 12 numbers are often represented as strings, e.g. `a = Value('10')`. Thus, when checking for
        # equality, we convert all args to string and to the default numeral system and then compare the result.
        return f"localize({left_hand_side}) == localize({right_hand_side})"

    def process_arg_for_data_access(self, arg, access_line=100, use_var_value=True):
        if self.is_variable(arg, access_line):
            # In some cases, we don't need to use the data of a variable, e.g. `for a in animals`
            data_part = '.data' if use_var_value else ''
            var_name = escape_var(self.unpack(arg))
            return f"{var_name}{data_part}"
        elif isinstance(arg, LiteralValue):
            val = arg.data[1:-1] if is_quoted(arg.data) else arg.data
            # equality does not have an f string and requires quotes to be added manually
            return f"'{process_characters_needing_escape(str(val))}'"
        elif self.is_random(arg) or self.is_list(arg):
            return f'{arg}.data'
        else:
            # We end up here when if-pressed receives a Token(LETTER_OR_NUMBER, 'x')
            # We also en up here when equality deals with an arg with spaces. We need to unpack, join them and pass it.
            # And since equality does not have an f string and requires quotes to be added manually
            val = arg[1:-1] if is_quoted(arg) else arg
            return f"'{process_characters_needing_escape(str(val))}'"

    def assign(self, meta, args):
        left_hand_side = args[0]
        right_hand_side = args[1]

        if self.is_variable(right_hand_side, meta.line):
            var = escape_var(self.unpack(right_hand_side))
            if self.is_list(var) or self.is_random(var):
                exception = self.make_index_error_check_if_list([var])
                return f"{exception}{left_hand_side} = {var}{self.add_debug_breakpoint()}"
            else:
                return f"{left_hand_side} = {var}"
        else:
            value = self.process_assign_argument(right_hand_side, escape_quotes=True)
            return f"{left_hand_side} = {value}{self.add_debug_breakpoint()}"

    def assign_list(self, meta, args):
        parameter = args[0]
        arguments = [self.process_assign_argument(v, escape_quotes=True) for v in args[1:]]

        return f"{parameter} = Value([{', '.join(arguments)}]){self.add_debug_breakpoint()}"

    def process_assign_argument(self, arg, escape_quotes=False):
        if isinstance(arg, LiteralValue):
            return self.process_literal_to_value(arg, escape=escape_quotes)
        elif isinstance(arg, ExpressionValue):
            return self.process_expression_to_value(arg)
        else:
            return arg

    def list_access(self, meta, args):
        args = [escape_var(a) for a in args]
        # filter the word `random` since it has a special meaning here and is not excluded in the check var usage
        vars_to_check = [a for a in args if a != 'random']
        self.check_variable_usage_and_definition(vars_to_check, meta.line)

        list_name = str(args[0])
        list_index = args[1]
        if str(list_index) == 'random':
            return f'random.choice({list_name}.data)'

        if self.is_variable_with_definition(list_index, meta.line):
            value = f'{escape_var(self.unpack(list_index))}.data'
        else:
            value = self.unpack(list_index)
        return f'{list_name}.data[int({value})-1]'

    def add(self, meta, args):
        value = self.process_add_to_remove_from_list_argument(args[0], meta)
        list_name = self.unpack(args[1])
        self.try_register_variable_access(list_name, meta.line)

        return f"{list_name}.data.append({value}){self.add_debug_breakpoint()}"

    def remove(self, meta, args):
        value = self.process_add_to_remove_from_list_argument(args[0], meta)
        list_name = self.unpack(args[1])
        self.try_register_variable_access(list_name, meta.line)

        return textwrap.dedent(f"""\
        try:
          {list_name}.data.remove({value}){self.add_debug_breakpoint()}
        except:
          pass""")

    def process_add_to_remove_from_list_argument(self, arg, meta):
        if self.is_variable(arg, meta.line):
            return f'{escape_var(self.unpack(arg))}'
        elif isinstance(arg, LiteralValue):
            return self.process_literal_to_value(arg)
        elif isinstance(arg, ExpressionValue):
            return self.process_expression_to_value(arg)
        else:
            return f"{arg}"

    def in_list_check(self, meta, args):
        arg0 = self.process_arg_for_data_access(self.unpack(args[0]), meta.line)
        arg1 = self.process_arg_for_data_access(self.unpack(args[1]), meta.line)
        # In level 6 the values of variables could be either a number or a string, e.g. 5 or '5'.
        # So, to check if a number is in a list of numbers with diff numeral system, we use localize()
        return f"localize({arg0}) in [localize(__la.data) for __la in {arg1}]"

    def not_in_list_check(self, meta, args):
        arg0 = self.process_arg_for_data_access(self.unpack(args[0]), meta.line)
        arg1 = self.process_arg_for_data_access(self.unpack(args[1]), meta.line)
        # In level 6 the values of variables could be either a number or a string, e.g. 5 or '5'.
        # So, to check if a number is not in a list of numbers with diff numeral system, we use localize()
        return f"localize({arg0}) not in [localize(__la.data) for __la in {arg1}]"

    def addition(self, meta, args):
        return self.process_calculation(args, '+', meta)

    def subtraction(self, meta, args):
        return self.process_calculation(args, '-', meta)

    def multiplication(self, meta, args):
        return self.process_calculation(args, '*', meta)

    def division(self, meta, args):
        return self.process_calculation(args, '//', meta)

    def process_calculation(self, args, operator, meta):
        lhs = self.unpack(args[0])
        rhs = self.unpack(args[1])
        self.check_variable_usage_and_definition(args, meta.line)
        num_sys, bools = self.merge_localization_info(args)

        only_literal_values = all([isinstance(a, LiteralValue) for a in args])
        if only_literal_values:
            value = f'{lhs} {operator} {rhs}'
        else:
            exception_text = make_value_error(operator, 'suggestion_number', self.language)
            value = f'number_with_error({lhs}, {exception_text}) {operator} number_with_error({rhs}, {exception_text})'
        return ExpressionValue(value, num_sys, bools)

    def process_literal_to_value(self, lv, escape=False):
        """ Transpiles a Literal Value to a Value instance, which exists in prefixes. For example,
        LiteralValue(1, num_sys='Arabic') is converted to Value(1, num_sys='Arabic'). """
        arg = lv.data
        data = f"'{process_characters_needing_escape(str(arg))}'"
        num_sys = f", num_sys='{lv.num_sys}'" if lv.num_sys else ''
        booleans = f', bools={lv.booleans}' if lv.booleans else ''
        return f"Value({data}{num_sys}{booleans})"

    def process_expression_to_value(self, ev):
        """ Transpiles an Expression Value instance to a Value instance, which exists in prefixes.
        For example, ExpressionValue('100 / 2', num_sys='Arabic') is converted to Value(100 / 2, num_sys='Arabic'). """
        # The data of the expression value is exactly as it would be transpiled, so quotes must already be in it.
        data = ev.data
        num_sys_value = ev.num_sys if ev.num_sys and 'get_num_sys' in ev.num_sys else f"'{ev.num_sys}'"
        num_sys = f", num_sys={num_sys_value}" if ev.num_sys else ''
        booleans = f', bools={ev.booleans}' if ev.booleans else ''
        return f"Value({data}{num_sys}{booleans})"

    def process_literal_for_fstring(self, lv):
        value = lv.data
        if is_quoted(value):
            value = value[1:-1].replace("'", "\\'")
        if (lv.num_sys is None or lv.num_sys == 'Latin') and lv.booleans is None:
            return str(value)
        num_sys_part = f', num_sys="{lv.num_sys}"' if lv.num_sys else ''
        bools_part = f', bools={lv.booleans}' if lv.booleans else ''
        return f"{{localize({value}{num_sys_part}{bools_part})}}"

    def process_expression_for_fstring(self, ev):
        num_sys_value = ev.num_sys if ev.num_sys and 'get_num_sys' in ev.num_sys else f'"{ev.num_sys}"'
        num_sys = f", num_sys={num_sys_value}" if ev.num_sys else ''
        booleans = f', bools={ev.booleans}' if ev.booleans else ''
        return f"{{localize({ev.data}{num_sys}{booleans})}}"


@v_args(meta=True)
@hedy_transpiler(level=7)
@source_map_transformer(source_map)
class ConvertToPython_7(ConvertToPython_6):
    def repeat(self, meta, args):
        return self.make_repeat(meta, args, multiline=False)

    def make_repeat(self, meta, args, multiline):
        var_name = self.get_fresh_var('__i')
        times = self.process_arg_for_data_access(args[0], meta.line)

        # In level 7, repeat can only have 1 line in its body
        if not multiline:
            body = self.indent(args[1])
        # In level 8 and up, repeat can have multiple lines in its body
        else:
            body = "\n".join([self.indent(x) for x in args[1:]])

        body = add_sleep_to_command(body, indent=True, is_debug=self.is_debug, location="after")
        ex = make_value_error(Command.repeat, 'suggestion_number', self.language)
        return f"for {var_name} in range(int_with_error({times}, {ex})):{self.add_debug_breakpoint()}\n{body}"


@v_args(meta=True)
@hedy_transpiler(level=8)
@v_args(meta=True)
@hedy_transpiler(level=9)
@source_map_transformer(source_map)
class ConvertToPython_8_9(ConvertToPython_7):
    def command(self, meta, args):
        return "".join(args)

    def repeat(self, meta, args):
        return self.make_repeat(meta, args, multiline=True)

    def ifs(self, meta, args):
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        return "if " + args[0] + ":" + self.add_debug_breakpoint() + "\n" + "\n".join(all_lines)

    def if_pressed(self, meta, args):
        self.process_arg_for_data_access(args[0], meta.line)
        args = [a for a in args if a != ""]  # filter out in|dedent tokens

        key = args[0]

        if_code = '\n'.join([x for x in args[1:]])
        if_code = ConvertToPython.indent(if_code)
        if_function_name = self.make_function_name(key)

        return (
            self.clear_key_mapping() + '\n' +
            self.add_if_key_mapping(key, if_function_name) + '\n' +
            self.make_function(if_function_name, if_code) + '\n'
        )

    def if_pressed_elses(self, met, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        else_code = '\n'.join([x for x in args[0:]])
        else_code = ConvertToPython.indent(else_code)
        else_function_name = self.make_function_name('else')

        return (
            self.add_else_key_mapping(else_function_name) + '\n' +
            self.make_function(else_function_name, else_code) + '\n' +
            self.make_extension_call()
        )

    def elses(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args]

        return "\nelse:\n" + "\n".join(all_lines)


@v_args(meta=True)
@hedy_transpiler(level=10)
@source_map_transformer(source_map)
class ConvertToPython_10(ConvertToPython_8_9):
    def for_list(self, meta, args):
        times = self.process_arg_for_data_access(args[0], meta.line, use_var_value=False)
        list_name = self.process_arg_for_data_access(args[1], meta.line, use_var_value=True)

        body = "\n".join([ConvertToPython.indent(x) for x in args[2:]])
        body = add_sleep_to_command(body, True, self.is_debug, location="after")

        return f"for {times} in {list_name}:{self.add_debug_breakpoint()}\n{body}"


@v_args(meta=True)
@hedy_transpiler(level=11)
@source_map_transformer(source_map)
class ConvertToPython_11(ConvertToPython_10):
    def for_loop(self, meta, args):
        iterator = escape_var(args[0])
        # iterator is always a used variable
        self.try_register_variable_access(iterator, meta.line)

        step = self.get_fresh_var('__step')
        step_begin = self.process_for_loop_args(args[1], meta, runtime_error=True)
        step_end = self.process_for_loop_args(args[2], meta, runtime_error=True)
        num_sys = self.get_localization_info_from_arg(args[1], meta.line)
        range_var = self.get_fresh_var("__rv")
        range_begin = self.process_for_loop_args(args[1], meta)
        range_end = self.process_for_loop_args(args[2], meta)
        range_part = (f'[Value({range_var}, num_sys={num_sys}) '
                      f'for {range_var} in range({range_begin}, {range_end} + {step}, {step})]')
        body = "\n".join([ConvertToPython.indent(x) for x in args[3:]])
        body = add_sleep_to_command(body, indent=True, is_debug=self.is_debug, location="after")
        # Adding runtime errors, i.e. int_with_error(arg, 'Very long error message'), can bloat the code a lot.
        # To overcome this, we only add the runtime error the first time the arg is accessed - in the step definition.
        # In later uses, such as the range definition, we use regular int() cast.
        return textwrap.dedent(f"""\
            {step} = 1 if {step_begin} < {step_end} else -1
            for {iterator} in {range_part}:{self.add_debug_breakpoint()}
            """) + body

    def process_for_loop_args(self, arg, meta, runtime_error=False):
        if self.is_variable(arg, meta.line):
            var = escape_var(arg)
            if runtime_error:
                ex = make_value_error(Command.sleep, 'suggestion_number', self.language)
                return f'int_with_error({var}.data, {ex})'
            else:
                return f'int({var}.data)'
        return f'int({self.unpack(arg)})'


@v_args(meta=True)
@hedy_transpiler(level=12)
@source_map_transformer(source_map)
class ConvertToPython_12(ConvertToPython_11):
    def text_in_quotes(self, meta, args):
        # We need to re-add the quotes, so that the Python code becomes name = 'Jan' or "Jan's"
        if args:
            text = args[0].data
            text_in_quotes = f'"{text}"' if "'" in text else f"'{text}'"
        else:
            text_in_quotes = "''"
        return LiteralValue(text_in_quotes)

    def number(self, meta, args):
        # try converting to ints
        try:
            value = ''.join([str(int(x)) for x in args])
            value = int(value)
        except Exception:
            # if it does not work, convert to floats
            value = ''.join([str(float(x)) for x in args])
            value = float(value)
        input_text = ''.join([x for x in args])
        return LiteralValue(value, num_sys=get_num_sys(input_text))

    def true(self, meta, args):
        booleans = self.extract_booleans(args[0], True)
        return LiteralValue(True, booleans=booleans)

    def false(self, meta, args):
        booleans = self.extract_booleans(args[0], False)
        return LiteralValue(False, booleans=booleans)

    def extract_booleans(self, value, boolean):
        def get_boolean_values(val, used_key, language, true_key, false_key):
            if KEYWORDS[language][used_key] == val:
                return KEYWORDS[language][true_key], KEYWORDS[language][false_key]
            return None, None

        booleans = ['true', 'True'] if boolean else ['false', 'False']
        for lang in [self.language, 'en']:
            keyword_true, keyword_false = get_boolean_values(value, booleans[0], lang, 'true', 'false')
            if keyword_true:
                return {True: keyword_true, False: keyword_false}

            keyword_true, keyword_false = get_boolean_values(value, booleans[1], lang, 'True', 'False')
            if keyword_true:
                return {True: keyword_true, False: keyword_false}

    def is_variable_with_definition(self, arg, access_line=100):
        # This method should be used from level 12 and up where quotes around strings are required
        # The arg is valid if it is either an int, a float, the 'random' operator, a quoted string,
        # or a variable. If the arg is an unquoted string which is not in the lookup table, an
        # UnquotedAssignTextException is raised. Most likely the real is that the kid forgot to add quotes.
        # args = arg if type(arg) is list else [arg]
        try:
            return super().is_variable_with_definition(arg, access_line)
        except exceptions.UndefinedVarException:
            a = self.unpack(arg)
            if not (self.is_int(a) or
                    self.is_float(a) or
                    self.is_random(a) or
                    self.is_bool(a)):
                raise exceptions.UnquotedAssignTextException(text=a, line_number=access_line)
        return False

    def play(self, meta, args):
        if not args:
            return self.make_play('C4', meta)

        arg = args[0]
        note = self.unpack(arg)
        if present_in_notes_mapping(note):  # this is a supported note
            return self.make_play(note.upper(), meta)

        if self.is_variable_with_definition(arg, meta.line):
            arg = f'{escape_var(self.unpack(arg))}.data'
        elif isinstance(arg, LiteralValue):
            arg = f"{arg.data}" if is_quoted(arg.data) else f"'{arg.data}'"
        elif isinstance(arg, ExpressionValue):
            arg = arg.data
        else:
            # We end up here in case of list access, e.g. 'random.choice[animals]'
            arg = f"{arg}.data"

        ex = make_value_error(Command.play, 'suggestion_note', self.language)
        return textwrap.dedent(f"""\
                play(note_with_error(localize({arg}), {ex}))
                time.sleep(0.5)""") + self.add_debug_breakpoint()

    def addition(self, meta, args):
        lhs = self.unpack(args[0])
        rhs = self.unpack(args[1])
        num_sys, bools = self.merge_localization_info(args)

        if self.has_variable_with_definition(args, meta.line):
            ex_text = make_values_error(Command.addition, 'suggestion_numbers_or_strings', self.language)
            value = f'sum_with_error({lhs}, {rhs}, {ex_text})'
        else:
            value = f'{lhs} + {rhs}'
        return ExpressionValue(value, num_sys, bools)

    def division(self, meta, args):
        return self.process_calculation(args, '/', meta)

    def sleep(self, meta, args):
        if not args:
            return "time.sleep(1)"

        if type(args[0]) is Tree and self.check_if_error_skipped(args[0]):
            raise hedy.exceptions.InvalidErrorSkippedException

        if self.is_variable_with_definition(args[0], meta.line):
            value = f'{escape_var(self.unpack(args[0]))}.data'
        else:
            value = f'{self.unpack(args[0])}'

        index_exception = self.make_index_error_check_if_list(args)
        ex = make_value_error(Command.sleep, 'suggestion_number', self.language)
        return index_exception + textwrap.dedent(f"time.sleep(int_with_error({value}, {ex}))")

    def turn(self, meta, args):
        if not args:
            return "t.right(90)" + self.add_debug_breakpoint()  # no arguments defaults to a right turn

        if self.is_variable_with_definition(args[0], meta.line):
            return self.make_turn(f'{escape_var(self.unpack(args[0]))}.data')

        value = f'{self.unpack(args[0])}'
        return self.make_turn(value)

    def forward(self, meta, args):
        if not args:
            command = f't.forward(50){self.add_debug_breakpoint()}'
            return add_sleep_to_command(command, False, self.is_debug)

        if self.is_variable_with_definition(args[0], meta.line):
            return self.make_forward(f'{escape_var(self.unpack(args[0]))}.data')

        value = f'{self.unpack(args[0])}'
        return self.make_forward(value)

    def make_turn(self, parameter):
        return self.make_turtle_command(parameter, Command.turn, 'right', False, HedyType.float)

    def make_forward(self, parameter):
        return self.make_turtle_command(parameter, Command.forward,
                                        'forward', True, HedyType.float)

    def assign(self, meta, args):
        left_hand_side = args[0]
        right_hand_side = args[1]

        self.is_variable_with_definition(right_hand_side, meta.line)

        right_hand_side = self.process_assign_argument(right_hand_side)
        # we no longer escape quotes here because they are now needed
        exception = self.make_index_error_check_if_list([right_hand_side])
        return exception + left_hand_side + " = " + right_hand_side + self.add_debug_breakpoint()

    def print(self, meta, args):
        argument_string = self.process_print_ask_args(args, meta)
        exception = self.make_index_error_check_if_list(args)
        return exception + f"print(f'''{argument_string}''')" + self.add_debug_breakpoint()

    def ask(self, meta, args):
        var = args[0]
        argument_string = self.process_print_ask_args(args[1:], meta)
        exception = self.make_index_error_check_if_list(args)
        return exception + textwrap.dedent(f"""\
            {var} = input(f'''{argument_string}'''){self.add_debug_breakpoint()}
            __ns = get_num_sys({var})
            try:
              {var} = int({var})
            except ValueError:
              try:
                {var} = float({var})
              except ValueError:
                pass
            {var} = Value({var}, num_sys=__ns)""")  # no number? leave as string

    def process_print_ask_args(self, args, meta, var_to_escape=''):
        result = super().process_print_ask_args(args, meta)
        if "'''" in result:
            raise exceptions.UnsupportedStringValue(invalid_value="'''")
        return result

    def process_arg_for_fstring(self, name, access_line=100, var_to_escape=''):
        if self.is_variable(name) or self.is_list(name) or self.is_random(name):
            return f"{{{escape_var(self.unpack(name))}}}"
        elif isinstance(name, LiteralValue):
            return self.process_literal_for_fstring(name)
        elif isinstance(name, ExpressionValue):
            return self.process_expression_for_fstring(name)
        elif is_quoted(name):
            name = name[1:-1]
            return name.replace("'", "\\'")
        elif not ConvertToPython.is_int(name) and not ConvertToPython.is_float(name):
            # We end up here with colors
            name = name if self.is_bool(name) else escape_var(name.replace("'", "\\'"))
            name = '"' + name + '"'
        return str(name)

    def list_access(self, meta, args):
        args = [escape_var(a) for a in args]
        # filter the word `random` since it has a special meaning here and is not excluded in the check var usage
        vars_to_check = [a for a in args if str(a) != 'random']
        self.check_variable_usage_and_definition(vars_to_check, meta.line)

        list_name = str(args[0])
        list_index = args[1]

        if str(list_index) == 'random':
            return f'random.choice({list_name}.data)'

        if self.is_variable_with_definition(list_index, meta.line):
            value = f'{escape_var(list_index)}.data'
        else:
            value = self.unpack(list_index)
        return f'{list_name}.data[int({value})-1]'

    def ifs(self, meta, args):
        all_lines = [self.indent(x) for x in args[1:]]
        exception = self.make_index_error_check_if_list([args[0]])
        return exception + "if " + args[0] + ":" + self.add_debug_breakpoint() + "\n" + "\n".join(all_lines)

    def add(self, meta, args):
        value = self.process_add_to_remove_from_list_argument(args[0], meta)
        list_name = args[1]

        # both sides have been used now
        self.try_register_variable_access(value, meta.line)
        self.try_register_variable_access(list_name, meta.line)
        return f"{list_name}.data.append({value}){self.add_debug_breakpoint()}"

    def remove(self, meta, args):
        value = self.process_add_to_remove_from_list_argument(args[0], meta)
        list_name = args[1]

        # both sides have been used now
        self.try_register_variable_access(value, meta.line)
        self.try_register_variable_access(list_name, meta.line)

        return textwrap.dedent(f"""\
            try:
              {list_name}.data.remove({value}){self.add_debug_breakpoint()}
            except:
              pass""")

    def process_add_to_remove_from_list_argument(self, arg, meta):
        if self.is_variable_with_definition(arg, meta.line):
            return f'{escape_var(self.unpack(arg))}'
        elif isinstance(arg, LiteralValue):
            return self.process_literal_to_value(arg)
        elif isinstance(arg, ExpressionValue):
            return self.process_expression_to_value(arg)
        else:
            return f"{arg}"

    def in_list_check(self, meta, args):
        self.check_variable_usage_and_definition(args, meta.line)

        value = self.process_assign_argument(args[0])
        list_name = args[1]
        return f"{value} in {list_name}.data"

    def not_in_list_check(self, meta, args):
        self.check_variable_usage_and_definition(args, meta.line)

        value = self.process_assign_argument(args[0])
        list_name = args[1]
        return f"{value} not in {list_name}.data"

    def equality_check(self, meta, args):
        left_hand_side = self.process_arg_for_data_access(args[0], meta.line)
        right_hand_side = self.process_arg_for_data_access(args[1], meta.line)

        # From level 12 we work only with the real values (e.g. int, floats, booleans), no string conversion is needed
        return f"{left_hand_side} == {right_hand_side}"

    def for_list(self, meta, args):
        times = self.process_arg_for_data_access(args[0], meta.line, use_var_value=False)
        list_name = escape_var(args[1])
        # add the list to the lookup table, this used now too
        self.try_register_variable_access(list_name, meta.line)

        body = "\n".join([ConvertToPython.indent(x) for x in args[2:]])
        body = add_sleep_to_command(body, is_debug=self.is_debug)
        return f"for {times} in {list_name}.data:{self.add_debug_breakpoint()}\n{body}"

    def for_loop(self, meta, args):
        iterator = escape_var(args[0])
        # iterator is always a used variable
        self.try_register_variable_access(iterator, meta.line)

        body = "\n".join([ConvertToPython.indent(x) for x in args[3:]])
        body = add_sleep_to_command(body, is_debug=self.is_debug)
        step_var_name = self.get_fresh_var('__step')

        begin = self.process_arg_for_data_access(args[1], meta.line)
        end = self.process_arg_for_data_access(args[2], meta.line)
        num_sys = self.get_localization_info_from_arg(args[1], meta.line)
        range_var = self.get_fresh_var("__rv")
        range_part = (f'[Value({range_var}, num_sys={num_sys}) '
                      f'for {range_var} in range({begin}, {end} + {step_var_name}, {step_var_name})]')

        return textwrap.dedent(f"""\
            {step_var_name} = 1 if {begin} < {end} else -1
            for {iterator} in {range_part}:{self.add_debug_breakpoint()}
            """) + body

    def process_arg_for_data_access(self, arg, access_line=100, use_var_value=True):
        if self.is_variable(arg, access_line):
            # In some cases, we don't need to use the data of a variable, e.g. `for a in animals`
            data_part = '.data' if use_var_value else ''
            var_name = escape_var(self.unpack(arg))
            return f"{var_name}{data_part}"
        elif isinstance(arg, LiteralValue):
            if is_quoted(arg.data):
                return f"'{process_characters_needing_escape(arg.data[1:-1])}'"
            return arg.data
        elif self.is_random(arg) or self.is_list(arg):
            return f'{arg}.data'
        else:
            # We end up here when if-pressed receives a Token(LETTER_OR_NUMBER, 'x')
            return f"{arg}"

    def process_literal_to_value(self, lv, escape=False):
        """ Transpiles a Literal Value to a Value instance, which exists in prefixes. For example,
        LiteralValue(1, num_sys='Arabic') is converted to Value(1, num_sys='Arabic'). """
        # The data of the literal value is exactly as it would be transpiled, so quotes must already be in it.
        # However, in some cases we need to strip quotes and re-add them as single quotes.
        if escape and isinstance(lv.data, str):
            arg = lv.data[1:-1] if is_quoted(lv.data) else lv.data
            data = f"'{process_characters_needing_escape(arg)}'"
        else:
            data = lv.data
        num_sys = f", num_sys='{lv.num_sys}'" if lv.num_sys else ''
        booleans = f', bools={lv.booleans}' if lv.booleans else ''
        return f"Value({data}{num_sys}{booleans})"

    def process_literal_for_fstring(self, lv):
        value = lv.data
        if is_quoted(value):
            value = value[1:-1].replace("'", "\\'")
        if (lv.num_sys is None or lv.num_sys == 'Latin') and lv.booleans is None:
            return str(value)
        # In level 12, the f string uses ''', so we keep the status quo and use single quotes for the numeral system
        num_sys_part = f", num_sys='{lv.num_sys}'" if lv.num_sys else ''
        bools_part = f', bools={lv.booleans}' if lv.booleans else ''
        return f"{{localize({value}{num_sys_part}{bools_part})}}"

    def process_expression_for_fstring(self, ev):
        num_sys_value = ev.num_sys if ev.num_sys and 'get_num_sys' in ev.num_sys else f"'{ev.num_sys}'"
        num_sys = f", num_sys={num_sys_value}" if ev.num_sys else ''
        booleans = f', bools={ev.booleans}' if ev.booleans else ''
        return f"{{localize({ev.data}{num_sys}{booleans})}}"

    def define(self, meta, args):
        function_name = self.unpack(args[0])
        has_args = isinstance(args[1], Tree) and args[1].data == "arguments"
        args_str = ", ".join(str(x) for x in args[1].children) if has_args else ""

        body_start = 2 if has_args else 1
        body = "\n".join(ConvertToPython.indent(line) for line in args[body_start:])

        return f"def {function_name}({args_str}):\n{body}"

    def call(self, meta, args):
        function_name = self.unpack(args[0])
        self.try_register_variable_access(function_name, meta.line)

        function_tree = [e.tree for e in self.lookup if e.name == function_name + "()"]
        tree_arguments = [c for c in function_tree[0].children if c.data == 'arguments']

        number_of_defined_arguments = 0 if tree_arguments == [] else len(tree_arguments[0].children)
        number_of_used_arguments = 0 if len(args) == 1 else len(args[1].children)

        if number_of_used_arguments != number_of_defined_arguments:
            raise hedy.exceptions.WrongNumberofArguments(
                name=function_name,
                defined_number=number_of_defined_arguments,
                used_number=number_of_used_arguments,
                line_number=meta.line)

        if len(args) > 1:
            flat_args = [x.children[0] if isinstance(x, Tree) else x for x in args[1].children]
            args_str = ", ".join([self.process_assign_argument(a) for a in flat_args])
            for a in args[1].children:
                self.try_register_variable_access(str(self.unpack(a)), meta.line)
        else:
            args_str = ""

        return f"{function_name}({args_str})"

    def returns(self, meta, args):
        args_str = self.process_print_ask_args(args, meta)
        exception = self.make_index_error_check_if_list(args)
        return exception + textwrap.dedent(f"""\
            try:
              return Value(int(f'''{args_str}'''), num_sys=get_num_sys(f'''{args_str}'''))
            except ValueError:
              try:
                return Value(float(f'''{args_str}'''), num_sys=get_num_sys(f'''{args_str}'''))
              except ValueError:
                return Value(f'''{args_str}''')""")


@v_args(meta=True)
@hedy_transpiler(level=13)
@source_map_transformer(source_map)
class ConvertToPython_13(ConvertToPython_12):
    def and_condition(self, meta, args):
        return ' and '.join(args)

    def or_condition(self, meta, args):
        return ' or '.join(args)


@v_args(meta=True)
@hedy_transpiler(level=14)
@source_map_transformer(source_map)
class ConvertToPython_14(ConvertToPython_13):
    def process_comparison(self, meta, args, operator):
        arg0 = self.process_variable_for_comparisons(args[0], meta)
        arg1 = self.process_variable_for_comparisons(args[1], meta)

        return f"{arg0}{operator}{arg1}"

    def process_variable_for_comparisons(self, arg, meta):
        if self.is_variable(arg, meta.line):
            return f"{escape_var(arg)}.data"
        else:
            return f'{self.unpack(arg)}'

    def equality_check_dequals(self, meta, args):
        return self.equality_check(meta, args)

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
@source_map_transformer(source_map)
class ConvertToPython_15(ConvertToPython_14):
    def while_loop(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        body = "\n".join(all_lines)
        body = add_sleep_to_command(body, True, self.is_debug, location="after")
        exception = self.make_index_error_check_if_list([args[0]])
        return exception + "while " + args[0] + ":" + self.add_debug_breakpoint() + "\n" + body

    def if_pressed_without_else(self, meta, args):
        code = args[0]

        return (
            code + self.make_extension_call()
        )


@v_args(meta=True)
@hedy_transpiler(level=16)
@source_map_transformer(source_map)
class ConvertToPython_16(ConvertToPython_15):
    def change_list_item(self, meta, args):
        name = self.unpack(args[0])
        index = self.unpack(args[1])
        self.check_variable_usage_and_definition(args[0:3], meta.line)

        index = f'{index}.data' if self.is_variable(args[1]) else index
        left_side = f'{name}.data[int({index})-1]'
        right_side = self.process_literal_to_value(args[2]) if isinstance(args[2], LiteralValue) else args[2]

        exception = self.make_index_error_check_if_list([left_side])
        return exception + left_side + ' = ' + right_side + self.add_debug_breakpoint()


@v_args(meta=True)
@hedy_transpiler(level=17)
@source_map_transformer(source_map)
class ConvertToPython_17(ConvertToPython_16):
    def elifs(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        return "\nelif " + args[0] + ":" + self.add_debug_breakpoint() + "\n" + "\n".join(all_lines)

    def if_pressed_elifs(self, meta, args):
        self.process_arg_for_data_access(args[0], meta.line)
        args = [a for a in args if a != ""]  # filter out in|dedent tokens

        key = args[0]

        elif_code = '\n'.join([x for x in args[1:]])
        elif_code = self.indent(elif_code)
        elif_function_name = self.make_function_name(key)

        return (
            self.add_if_key_mapping(key, elif_function_name) + '\n' +
            self.make_function(elif_function_name, elif_code) + '\n'
        )


@v_args(meta=True)
@hedy_transpiler(level=18)
@source_map_transformer(source_map)
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


@v_args(meta=True)
@hedy_transpiler(level=1, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_1(ConvertToPython_1):
    def print(self, meta, args):
        # escape needed characters
        argument = process_characters_needing_escape(self.unpack(args[0]))
        return f"display.scroll('{argument}')"


@v_args(meta=True)
@hedy_transpiler(level=2, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_2(MicrobitConvertToPython_1, ConvertToPython_2):

    def print(self, meta, args):
        argument_string = self.process_print_ask_args(args, meta)
        return f"display.scroll({argument_string})"

    def process_print_ask_args(self, args, meta, var_to_escape=''):
        return ' '.join([self.unpack(a) if self.is_variable(a, meta.line) else f"'{self.unpack(a)}'" for a in args])

    def assign(self, meta, args):
        variable_name = args[0]
        value = self.unpack(args[1])

        exception = self.make_index_error_check_if_list([value])
        if self.is_variable(value, meta.line):
            # if the assigned value is a variable, this is a reassign
            value = escape_var(value)
        elif not self.is_int(value) and not self.is_float(value):
            # if it is not a variable and not a number, add quotes
            value = f"'{process_characters_needing_escape(value)}'"

        return exception + variable_name + " = " + value + self.add_debug_breakpoint()

    def sleep(self, meta, args):
        if not args:
            return f"sleep(1000){self.add_debug_breakpoint()}"  # Default 1-second sleep in milliseconds

        variable = self.unpack(args[0])
        if self.is_int(variable):
            # Direct conversion of seconds to milliseconds
            milliseconds = int(variable) * 1000
        else:
            milliseconds = f"{variable} * 1000"
            self.try_register_variable_access(variable, meta.line)
        return f"sleep({milliseconds}){self.add_debug_breakpoint()}"


@v_args(meta=True)
@hedy_transpiler(level=3, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_3(MicrobitConvertToPython_2, ConvertToPython_3):
    pass


@v_args(meta=True)
@hedy_transpiler(level=4, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_4(MicrobitConvertToPython_3, ConvertToPython_4):

    def process_print_ask_args(self, args, meta, var_to_escape=''):
        return ''.join([self.unpack(a) if self.is_variable(a, meta.line) else f'{self.unpack(a)}' for a in args])

    def print(self, meta, args):
        argument_string = self.process_print_ask_args(args, meta)
        return f"display.scroll({argument_string})"

    def clear(self, meta, args):
        return f"display.clear()"


@v_args(meta=True)
@hedy_transpiler(level=5, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_5(MicrobitConvertToPython_4, ConvertToPython_5):
    pass


@v_args(meta=True)
@hedy_transpiler(level=6, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_6(MicrobitConvertToPython_5, ConvertToPython_6):
    pass


@v_args(meta=True)
@hedy_transpiler(level=7, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_7(MicrobitConvertToPython_6, ConvertToPython_7):
    pass


@v_args(meta=True)
@hedy_transpiler(level=8, microbit=True)
@hedy_transpiler(level=9, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_8_9(MicrobitConvertToPython_7, ConvertToPython_8_9):
    pass


@v_args(meta=True)
@hedy_transpiler(level=10, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_10(MicrobitConvertToPython_8_9, ConvertToPython_10):
    pass


@v_args(meta=True)
@hedy_transpiler(level=11, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_11(MicrobitConvertToPython_10, ConvertToPython_11):
    pass


@v_args(meta=True)
@hedy_transpiler(level=12, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_12(MicrobitConvertToPython_11, ConvertToPython_12):
    pass
    # def print(self, meta, args):
    #     argument_string = self.process_print_ask_args(args, meta)
    #     return f"display.scroll('{argument_string}')"


@v_args(meta=True)
@hedy_transpiler(level=13, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_13(MicrobitConvertToPython_12, ConvertToPython_13):
    pass


@v_args(meta=True)
@hedy_transpiler(level=14, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_14(MicrobitConvertToPython_13, ConvertToPython_14):
    pass


@v_args(meta=True)
@hedy_transpiler(level=15, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_15(MicrobitConvertToPython_14, ConvertToPython_15):
    pass


@v_args(meta=True)
@hedy_transpiler(level=16, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_16(MicrobitConvertToPython_15, ConvertToPython_16):
    pass


@v_args(meta=True)
@hedy_transpiler(level=17, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_17(MicrobitConvertToPython_16, ConvertToPython_17):
    pass


@v_args(meta=True)
@hedy_transpiler(level=18, microbit=True)
@source_map_transformer(source_map)
class MicrobitConvertToPython_18(MicrobitConvertToPython_17, ConvertToPython_18):
    pass


def _get_parser_cache_directory():
    # TODO we should maybe store this to .test-cache so we can
    # re-use them in github actions caches for faster CI.
    # We can do this after #4574 is merged.
    return tempfile.gettempdir()


def _save_parser_to_file(lark, pickle_file):
    # Store the parser to a file, a bit hacky because it is not
    # pickle-able out of the box
    # See https://github.com/lark-parser/lark/issues/1348

    # Note that if Lark ever implements the cache for Earley parser
    # or if we switch to a LALR parser we don't need this hack anymore

    full_path = os.path.join(_get_parser_cache_directory(), pickle_file)

    # These attributes can not be pickled as they are a module
    lark.parser.parser.lexer_conf.re_module = None
    lark.parser.lexer_conf.re_module = None

    try:
        with atomic_write_file(full_path) as fp:
            pickle.dump(lark, fp)
    except OSError:
        # Ignore errors if another process already moved the file
        # or if the destination already exist.
        # These scenarios can happen under concurrent execution.
        pass

    # Restore the unpickle-able bits.
    # Keep this in sync with the restore method!
    lark.parser.parser.lexer_conf.re_module = regex
    lark.parser.lexer_conf.re_module = regex


def _restore_parser_from_file_if_present(pickle_file):
    full_path = os.path.join(_get_parser_cache_directory(), pickle_file)
    if os.path.isfile(full_path):
        try:
            with open(full_path, "rb") as fp:
                lark = pickle.load(fp)
            # Restore the unpickle-able bits.
            # Keep this in sync with the save method!
            lark.parser.parser.lexer_conf.re_module = regex
            lark.parser.lexer_conf.re_module = regex
            return lark
        except Exception:
            # If anything goes wrong try to remove the file
            # and we will try again in the next cycle
            try:
                os.unlink(full_path)
            except Exception:
                pass
    return None


@lru_cache(maxsize=0 if utils.is_production() else 100)
def get_parser(level, lang="en", keep_all_tokens=False, skip_faulty=False):
    """Return the Lark parser for a given level.
    Parser generation takes about 0.5 seconds depending on the level so
    we want to cache it, or we have latency of 500ms on the calculations
    and a high server load, and CI runs of 5+ hours.

    We used to cache this to RAM but because of all the permutations we
    had 1000s of parsers and got into out-of-memory issue in the
    production environment.

    Now we cache a limited number of the parsers to RAM, but introduce
    a second tier of cache to disk.

    This is not implemented by Lark natively for the Earley parser.
    See https://github.com/lark-parser/lark/issues/1348.
    """
    grammar = hedy_grammar.create_grammar(level, lang, skip_faulty)
    parser_opts = {
        "regex": True,
        "propagate_positions": True,
        "keep_all_tokens": keep_all_tokens,
    }
    unique_parser_hash = hashlib.sha1("_".join((
        grammar,
        str(sys.version_info[:2]),
        str(parser_opts),
    )).encode()).hexdigest()

    cached_parser_file = f"cached-parser-{level}-{lang}-{unique_parser_hash}.pkl"

    use_cache = True
    parser = None
    if use_cache:
        parser = _restore_parser_from_file_if_present(cached_parser_file)
    if parser is None:
        parser = Lark(grammar, **parser_opts)  # ambiguity='explicit'
        if use_cache:
            _save_parser_to_file(parser, cached_parser_file)

    return parser


ParseResult = namedtuple('ParseResult', ['code', 'source_map', 'has_turtle',
                                         'has_pressed', 'has_clear', 'has_music', 'has_sleep', 'commands',
                                         'roles_of_variables'])


def transpile_inner_with_skipping_faulty(input_string, level, lang="en", unused_allowed=True):
    def skipping_faulty(meta, args):
        return [True]

    defined_errors = [method for method in dir(IsValid) if method.startswith('error')]
    defined_errors_original = dict()

    def set_error_to_allowed():
        # override IsValid methods to always be valid & store original
        for error in defined_errors:
            defined_errors_original[error] = getattr(IsValid, error)
            setattr(IsValid, error, skipping_faulty)

    def set_errors_to_original():
        # revert IsValid methods to original
        for error in defined_errors:
            setattr(IsValid, error, defined_errors_original[error])

    try:
        set_error_to_allowed()
        transpile_result = transpile_inner(
            input_string, level, lang, populate_source_map=True, unused_allowed=unused_allowed
        )
    finally:
        # make sure to always revert IsValid methods to original
        set_errors_to_original()

    # If transpiled successfully while allowing errors, transpile mapped code again to get original error
    # If none is found, raise error so that original error will be returned
    at_least_one_error_found = False

    for hedy_source_code, python_source_code in source_map.map.copy().items():
        if hedy_source_code.error is not None or python_source_code.code == 'pass':
            try:
                transpile_inner(hedy_source_code.code, source_map.level, source_map.language)
            except Exception as e:
                hedy_source_code.error = e

            if hedy_source_code.error is not None:
                at_least_one_error_found = True

    if not at_least_one_error_found:
        raise Exception('Could not find original error for skipped code')

    return transpile_result


def transpile(input_string, level, lang="en", skip_faulty=True, is_debug=False, unused_allowed=False, microbit=False):
    """
    Function that transpiles the Hedy code to Python

    The first time we try to transpile the code without skipping faulty code
    If an exception is caught (the Hedy code contains faults) an exception is raised

    The second time, after the non-skipping approach raised an exception,
    we try transpile the code with skipping faulty code, if skip_faulty is True.
    After that either the partial program is returned or the original error
    """

    try:
        source_map.set_skip_faulty(False)
        transpile_result = transpile_inner(input_string, level, lang, populate_source_map=True,
                                           is_debug=is_debug, unused_allowed=unused_allowed, microbit=microbit)

    except Exception as original_error:
        hedy_amount_lines = len(input_string.strip().split('\n'))

        if getenv('ENABLE_SKIP_FAULTY', False) and skip_faulty and hedy_amount_lines > 1:
            if isinstance(original_error, source_map.exceptions_not_to_skip):
                raise original_error
            try:
                source_map.set_skip_faulty(True)
                transpile_result = transpile_inner_with_skipping_faulty(input_string, level, lang)
            except Exception:
                raise original_error  # we could not skip faulty code, raise original exception
        else:
            raise original_error

    return transpile_result


def translate_characters(s):
    # this method is used to make it more clear to kids what is meant in error messages
    # for example ' ' is hard to read, space is easier
    commas = [',', "،", "，", "、"]
    if s == ' ':
        return 'space'
    elif s in commas:
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
            raise hedy.exceptions.CodePlaceholdersPresentException(line_number=line_number + 1)

        leading_spaces = find_indent_length(line)

        line_number += 1

        # ignore whitespace-only lines
        if leading_spaces == len(line):
            processed_code.append('')
            continue

        # ignore lines that contain only a comment
        comment_reg_ex = r' *\#[^\n]*'
        if regex.fullmatch(comment_reg_ex, line):
            processed_code.append(line)
            continue

        # first encounter sets indent size for this program
        if not indent_size_adapted and leading_spaces > 0:
            indent_size = leading_spaces
            indent_size_adapted = True

        # there is inconsistent indentation, not sure if that is too much or too little!
        if (leading_spaces % indent_size) != 0:
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            if leading_spaces < current_number_of_indents * indent_size:
                raise_too_few_indents_error(line_number, leading_spaces, indent_size, fixed_code, level)
            else:
                raise_too_many_indents_error(line_number, leading_spaces, indent_size, fixed_code, level)

        # happy path, indentation is consistent, i.e. multiple of 2 or 4:
        current_number_of_indents = leading_spaces // indent_size
        if current_number_of_indents > 1 and level == hedy.LEVEL_STARTING_INDENTATION:
            raise hedy.exceptions.TooManyIndentsStartLevelException(line_number=line_number,
                                                                    leading_spaces=leading_spaces)

        if current_number_of_indents > previous_number_of_indents and not next_line_needs_indentation:
            # we are indenting, but this line is not following* one that even needs indenting, raise
            # * note that we have not yet updated the value of 'next line needs indenting' so if refers to this line!
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            raise_too_many_indents_error(line_number, leading_spaces, indent_size, fixed_code, level)

        if next_line_needs_indentation and current_number_of_indents <= previous_number_of_indents:
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            raise_too_few_indents_error(line_number, leading_spaces, indent_size, fixed_code, level)

        if current_number_of_indents - previous_number_of_indents > 1:
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            raise_too_many_indents_error(line_number, leading_spaces, indent_size, fixed_code, level)

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


def raise_too_many_indents_error(line_number, leading_spaces, indent_size, fixed_code, level):
    if level == hedy.LEVEL_STARTING_INDENTATION:
        raise hedy.exceptions.TooManyIndentsStartLevelException(line_number=line_number, leading_spaces=leading_spaces,
                                                                fixed_code=fixed_code)
    else:
        raise hedy.exceptions.IndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                   indent_size=indent_size, fixed_code=fixed_code)


def raise_too_few_indents_error(line_number, leading_spaces, indent_size, fixed_code, level):
    if level == hedy.LEVEL_STARTING_INDENTATION:
        raise hedy.exceptions.TooFewIndentsStartLevelException(line_number=line_number, leading_spaces=leading_spaces,
                                                               fixed_code=fixed_code)
    else:
        raise hedy.exceptions.NoIndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                     indent_size=indent_size, fixed_code=fixed_code)


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
        keywords_in_lang = KEYWORDS.get(lang, KEYWORDS['en'])
        repeat_plus_translated = ['repeat', keywords_in_lang.get('repeat')]
        times_plus_translated = ['times', keywords_in_lang.get('times')]

        if len(elements_in_line) > 2 and elements_in_line[0] in repeat_plus_translated and elements_in_line[
                2] in times_plus_translated:
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
            if not command == '=':
                command_plus_translated_command = [command, KEYWORDS[lang].get(command)]
            else:
                command_plus_translated_command = [command]
            for c in command_plus_translated_command:
                if c in line:
                    return True
            return False
        else:
            return command in line

    def contains_two(command, line):
        if lang in ALL_KEYWORD_LANGUAGES:
            command_plus_translated_command = [command, KEYWORDS[lang].get(command)]
            for c in command_plus_translated_command:
                if line.count(
                        ' ' + c + ' ') >= 2:  # surround in spaces since we dont want to mathc something like 'dishwasher is sophie'
                    return True
            return False

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

    def next_non_empty_line(lines, start_line_number):
        if start_line_number > len(lines):
            return ''  # end of code, return empty so that starts_with doesnt find anything
        else:
            for i in range(start_line_number + 1, len(lines)):
                if lines[i] == '':
                    continue
                else:
                    return lines[i]

        return ''  # nothing found? return empty so that starts_with doesnt find anything

    for i in range(len(lines) - 1):
        line = lines[i]

        # if this line starts with if but does not contain an else, and the next non-empty line too is not an else.
        if (starts_with('if', line) or starts_with_after_repeat('if', line)) and (
                not starts_with('else', next_non_empty_line(lines, i))) and (not contains('else', line)):
            # is this line just a condition and no other keyword (because that is no problem)
            commands = ["print", "ask", "forward", "turn", "play"]
            excluded_commands = ["pressed"]

            if (
                (contains_any_of(commands, line) or contains_two('is', line)
                 or (contains('is', line) and contains('=', line)))
                and not contains_any_of(excluded_commands, line)
            ):
                # a second command, but also no else in this line -> check next line!

                # no else in next line?
                # add a nop (like 'Pass' but we just insert a meaningless assign)
                line = line + " else x__x__x__x is 5"

        processed_code.append(line)
    processed_code.append(lines[-1])  # always add the last line (if it has if and no else that is no problem)
    return "\n".join(processed_code)


def location_of_first_blank(code_snippet):
    # returns 0 if the code does not contain _
    # otherwise returns the first location (line) of the blank
    lines = code_snippet.split('\n')
    for i in range(len(lines)):
        code = lines[i]
        if len(code) > 0:
            if (" _" in code) or ("_ " in code) or (code[-1] == "_"):
                return i + 1
    return 0


def check_program_size_is_valid(input_string):
    number_of_lines = input_string.count('\n')
    # parser is not made for huge programs!
    if number_of_lines > MAX_LINES:
        raise exceptions.InputTooBigException(lines_of_code=number_of_lines, max_lines=MAX_LINES)


def process_input_string(input_string, level, lang, preprocess_ifs_enabled=True):
    result = input_string.replace('\r\n', '\n')

    location = location_of_first_blank(result)
    if location > 0:
        raise exceptions.CodePlaceholdersPresentException(line_number=location)

    if level >= 4:
        result = result.replace("\\", "\\\\")

    # In levels 5 to 7 we do not allow if without else, we add an empty print to make it possible in the parser
    if level >= 5 and level < 8 and preprocess_ifs_enabled:
        result = preprocess_ifs(result, lang)

    # In level 8 we add indent-dedent blocks to the code before parsing
    if level >= hedy.LEVEL_STARTING_INDENTATION:
        result = preprocess_blocks(result, level, lang)

    return result


def parse_input(input_string, level, lang):
    parser = get_parser(level, lang, skip_faulty=source_map.skip_faulty)
    try:
        parse_result = parser.parse(input_string + '\n')
        return parse_result.children[0]  # getting rid of the root could also be done in the transformer would be nicer
    except lark.UnexpectedEOF:
        lines = input_string.split('\n')
        last_line = len(lines)
        raise exceptions.UnquotedEqualityCheckException(line_number=last_line)
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
    # IsValid raises the appropriate exception when an error production (starting with error_)
    # is found in the parse tree
    IsValid(level, lang, input_string).transform(program_root)


def repair_leading_space(input_string, lang, level, line):
    fixed_code = program_repair.remove_leading_spaces(input_string)
    result = None
    if fixed_code != input_string:  # only if we have made a successful fix
        try:
            fixed_result = transpile_inner(fixed_code, level, lang)
            result = fixed_result
            raise exceptions.InvalidSpaceException(
                level=level, line_number=line, fixed_code=fixed_code, fixed_result=result)
        except exceptions.HedyException as E:
            if type(E) is not exceptions.InvalidSpaceException:
                transpile_inner(fixed_code, level)
                # The fixed code contains another error. Only report the original error for now.
    return fixed_code, result


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


def create_AST(input_string, level, lang="en"):
    program_root = parse_input(input_string, level, lang)

    # checks whether any error production nodes are present in the parse tree
    is_program_valid(program_root, input_string, level, lang)
    abstract_syntax_tree = ExtractAST().transform(program_root)
    is_program_complete(abstract_syntax_tree, level)

    if not valid_echo(abstract_syntax_tree):
        raise exceptions.LonelyEchoException()

    lookup_table = create_lookup_table(abstract_syntax_tree, level, lang, input_string)
    commands = AllCommands(level).transform(program_root)
    # FH, dec 2023. I don't love how AllCommands works on program root and not on AST,
    # but his will do for now. One day we should really start to clean up our AST!

    return abstract_syntax_tree, lookup_table, commands


def determine_roles(lookup, input_string, level, lang):
    all_vars = all_variables(input_string, level, lang)
    roles_dictionary = {}
    for var in all_vars:
        assignments = [x for x in lookup if x.name == var]

        if (assignments[0].tree.data == 'for_list'):
            roles_dictionary[var] = gettext('walker_variable_role')
        elif (assignments[0].tree.data == 'for_loop'):
            roles_dictionary[var] = gettext('stepper_variable_role')
        elif (assignments[0].type_ == 'list'):
            roles_dictionary[var] = gettext('list_variable_role')
        elif (len(assignments) == 1):
            if (assignments[0].type_ == 'input'):
                roles_dictionary[var] = gettext('input_variable_role')
            else:
                roles_dictionary[var] = gettext('constant_variable_role')
        else:
            roles_dictionary[var] = gettext('unknown_variable_role')

    return roles_dictionary


def transpile_inner(input_string, level, lang="en", populate_source_map=False, is_debug=False, unused_allowed=False,
                    microbit=False):
    check_program_size_is_valid(input_string)
    input_string = process_input_string(input_string, level, lang)

    level = int(level)
    if level > HEDY_MAX_LEVEL:
        raise Exception(f'Levels over {HEDY_MAX_LEVEL} not implemented yet')

    if populate_source_map:
        source_map.clear()
        source_map.set_level(level)
        source_map.set_language(lang)
        source_map.set_hedy_input(input_string)

    try:
        abstract_syntax_tree, lookup_table, commands = create_AST(input_string, level, lang)

        # grab the right transpiler from the lookup
        convertToPython = MICROBIT_TRANSPILER_LOOKUP[level] if microbit else TRANSPILER_LOOKUP[level]
        python = convertToPython(lookup_table, lang, is_debug).transform(abstract_syntax_tree)

        has_clear = "clear" in commands
        has_turtle = "forward" in commands or "turn" in commands or "color" in commands
        has_pressed = "if_pressed" in commands or "if_pressed_else" in commands or "assign_button" in commands
        has_music = "play" in commands
        has_sleep = "sleep" in commands

        roles_of_variables = determine_roles(lookup_table, input_string, level, lang)

        parse_result = ParseResult(python, source_map, has_turtle, has_pressed,
                                   has_clear, has_music, has_sleep, commands, roles_of_variables)

        if populate_source_map:
            source_map.set_python_output(python)

        if not unused_allowed:
            for x in lookup_table:
                if isinstance(x.name, str) and x.access_line is None and x.name != 'x__x__x__x':
                    x.name = re.sub(r'^_', '', x.name)
                    raise hedy.exceptions.UnusedVariableException(
                        level, x.definition_line, x.name, fixed_code=python, fixed_result=parse_result)

        return parse_result
    except VisitError as E:
        if isinstance(E, VisitError):
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


def transpile_and_return_python(input_string, level):
    python = transpile(input_string, level, microbit=True)
    return str(python.code)
