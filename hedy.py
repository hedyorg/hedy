import textwrap
from functools import lru_cache, cache

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

HEDY_MAX_LEVEL = 18
HEDY_MAX_LEVEL_SKIPPING_FAULTY = 5
MAX_LINES = 100
LEVEL_STARTING_INDENTATION = 8

# Boolean variables to allow code which is under construction to not be executed
local_keywords_enabled = True

# dictionary to store transpilers
TRANSPILER_LOOKUP = {}

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
    commands[level] = [c for c in commands[level-1] if c not in remove] + add


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
        16: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.list]
    },
    Command.ask: {
        1: [HedyType.string, HedyType.integer, HedyType.input, HedyType.list],
        4: [HedyType.string, HedyType.integer, HedyType.input],
        12: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float],
        16: [HedyType.string, HedyType.integer, HedyType.input, HedyType.float, HedyType.list]
    },
    Command.turn: {1: command_turn_literals,
                   2: [HedyType.integer, HedyType.input],
                   12: [HedyType.integer, HedyType.input, HedyType.float]
                   },
    Command.color: {1: [english_colors, HedyType.list],
                    2: [english_colors, HedyType.string, HedyType.input, HedyType.list]},
    Command.forward: {1: [HedyType.integer, HedyType.input],
                      12: [HedyType.integer, HedyType.input, HedyType.float]
                      },
    Command.sleep: {1: [HedyType.integer, HedyType.input],
                    12: [HedyType.integer, HedyType.input, HedyType.float]
                    },
    Command.list_access: {1: [HedyType.list]},
    Command.in_list: {1: [HedyType.list]},
    Command.not_in_list: {1: [HedyType.list]},
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
        if isinstance(args[1], Tree):
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

        if production_rule_name in commands_per_level[self.level] or production_rule_name in operators or production_rule_name == 'if_pressed_else':
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
        words = [str(x[1]) for x in args]  # second half of the list is the word
        text = ' '.join(words)

        raise exceptions.UnquotedTextException(
            level=self.level,
            unquotedtext=text,
            line_number=meta.line
        )

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
        raise exceptions.MissingColonException(command=Command.elif_, line_number=meta.line+1)

    def if_pressed_elses_no_colon(self, meta, args):
        # if_pressed_elses starts with _EOL, so we need to add +1 to its line
        raise exceptions.MissingColonException(command=Command.else_, line_number=meta.line+1)

    def ifs_no_colon(self, meta, args):
        raise exceptions.MissingColonException(command=Command.if_, line_number=meta.line)

    def elifs_no_colon(self, meta, args):
        # elifs starts with _EOL, so we need to add +1 to its line
        raise exceptions.MissingColonException(command=Command.elif_, line_number=meta.line+1)

    def elses_no_colon(self, meta, args):
        # elses starts with _EOL, so we need to add +1 to its line
        raise exceptions.MissingColonException(command=Command.else_, line_number=meta.line+1)

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
    def __init__(self, lookup, language="en", numerals_language="Latin", is_debug=False, microbit=False):
        self.lookup = lookup
        self.language = language
        self.numerals_language = numerals_language
        self.is_debug = is_debug
        self.microbit = microbit

    def add_debug_breakpoint(self):
        if self.is_debug:
            return f" # __BREAKPOINT__"
        else:
            return ""

    def is_var_in_lookup(self, variable_name):
        all_names = [a.name for a in self.lookup]
        return variable_name in all_names

    # The var_to_escape parameter allows the ask command to force the variable defined
    # by itself, i.e. the left-hand-side var, to not be defined on the same line
    def is_var_defined_before_access(self, variable_name, access_line_number, var_to_escape=''):
        def is_before(entry, line):
            return entry.definition_line <= line if entry.name != var_to_escape else entry.definition_line < line

        all_names_before_access_line = [entry.name for entry in self.lookup if is_before(entry, access_line_number)]
        return variable_name in all_names_before_access_line

    # In level 3, a list name without index or random should be treated as a literal string, e.g.
    #   color = red, blue, yellow
    #   print What is your favorite color? <- color is not a var reference here, but the text 'color'
    def is_unreferenced_list(self, variable_name):
        for entry in self.lookup:
            if entry.name == escape_var(variable_name):
                return entry.type_ == HedyType.list and '[' not in variable_name
        return False

    # default for line number is max lines so if it is not given, there
    # is no check on whether the var is defined
    def is_variable(self, variable_name, access_line_number=100):
        if self.is_var_in_lookup(variable_name) and not self.is_var_defined_before_access(variable_name,
                                                                                          access_line_number):
            definition_line_number = [a.definition_line for a in self.lookup if a.name == variable_name][0]
            raise hedy.exceptions.AccessBeforeAssignException(
                name=variable_name,
                access_line_number=access_line_number,
                definition_line_number=definition_line_number)

        # valid use, store!
        self.add_variable_access_location(variable_name, access_line_number)

        all_names_before_access_line = [a.name for a in self.lookup if a.definition_line <= access_line_number]
        if escape_var(variable_name) in all_names_before_access_line:
            return True

        if isinstance(variable_name, str):
            pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\('
            match = re.match(pattern, variable_name)
            is_function = match and [a.name for a in self.lookup if match.group(1) + "()" == a.name]
            return is_function

        return False

    def process_variable(self, arg, access_line_number=100):
        # processes a variable by hashing and escaping when needed
        if self.is_variable(arg, access_line_number):
            # add this access line to the lookup table
            self.add_variable_access_location(arg, access_line_number)
            return escape_var(arg)
        if ConvertToPython.is_quoted(arg):
            arg = arg[1:-1]
        return f"'{process_characters_needing_escape(arg)}'"

    def process_variable_without_quotes(self, arg, access_line_number=100):
        if self.is_variable(arg, access_line_number):
            # add this access line to the lookup table
            self.add_variable_access_location(arg, access_line_number)
            return escape_var(arg)
        return arg

    def process_variable_for_fstring(self, variable_name, access_line_number=100, var_to_escape=''):

        if (self.is_var_defined_before_access(variable_name, access_line_number, var_to_escape) and
                not self.is_unreferenced_list(variable_name)):
            self.add_variable_access_location(variable_name, access_line_number)
            return "{" + escape_var(variable_name) + "}"
        else:
            return process_characters_needing_escape(variable_name)

    def add_variable_access_location(self, variable_name, access_line_number):
        # store the line of access (or string value) in the lookup table
        # so we know what variable is used where
        if isinstance(variable_name, str):
            vars = [a for a in self.lookup if isinstance(a.name, str) and a.name[:len(variable_name)] == variable_name]
            for v in vars:  # vars can be defined multiple times, access validates all of them
                corresponding_lookup_entry = v
                corresponding_lookup_entry.access_line = access_line_number

    def process_variable_for_comparisons(self, name):
        # used to transform variables in comparisons
        if self.is_variable(name):
            return f"convert_numerals('{self.numerals_language}', {escape_var(name)})"
        elif ConvertToPython.is_float(name):
            return f"convert_numerals('{self.numerals_language}', {name})"
        elif ConvertToPython.is_quoted(name):
            return f"{name}"

    def get_fresh_var(self, name):
        while self.is_variable(name):
            name = '_' + name
        return name

    def check_var_usage(self, args, var_access_linenumber=100):
        # This function should be used up until level 11 where quotes around strings are NOT required
        # It succeeds if all args are valid. An arg is valid if it is either quoted or a variable
        # If an unquoted arg is not present in the lookup table, an UndefinedVarException is raised

        def is_var_candidate(arg) -> bool:
            return not isinstance(arg, Tree) and \
                not ConvertToPython.is_int(arg) and \
                not ConvertToPython.is_float(arg)

        args_to_process = [a for a in args if is_var_candidate(a)]  # we do not check trees (calcs) they are always ok

        unquoted_args = [a for a in args_to_process if not ConvertToPython.is_quoted(a)]
        unquoted_in_lookup = [self.is_variable(a, var_access_linenumber) for a in unquoted_args]

        if unquoted_in_lookup == [] or all(unquoted_in_lookup):

            # # all good? store location
            for a in args:
                self.add_variable_access_location(str(a), var_access_linenumber)
            # return for further processing
            return args
        else:
            # return first name with issue
            for index, a in enumerate(unquoted_args):
                current_arg = unquoted_in_lookup[index]
                if current_arg is None:
                    first_unquoted_var = a
                    raise exceptions.UndefinedVarException(name=first_unquoted_var, line_number=var_access_linenumber)

    def check_var_usage_when_quotes_are_required(self, arg, meta):
        # This method should be used from level 12 and up where quotes around strings are required
        # The arg is valid if it is either an int, a float, the 'random' operator, a quoted string,
        # or a variable. If the arg is an unquoted string which is not in the lookup table, an
        # UnquotedAssignTextException is raised. Most likely the real is that the kid forgot to add quotes.
        try:
            self.check_var_usage([arg], meta.line)
        except exceptions.UndefinedVarException:
            if not (ConvertToPython.is_int(arg) or
                    ConvertToPython.is_float(arg) or
                    ConvertToPython.is_random(arg)):
                raise exceptions.UnquotedAssignTextException(text=arg, line_number=meta.line)

    # static methods

    @staticmethod
    def check_if_error_skipped(tree):
        return hasattr(IsValid, tree.data)

    @staticmethod
    def is_quoted(s):
        opening_quotes = ['‘', "'", '"', "“", "«", "„"]
        closing_quotes = ['’', "'", '"', "”", "»", "“"]
        return len(s) > 1 and (s[0] in opening_quotes and s[-1] in closing_quotes)

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
@source_map_transformer(source_map)
class ConvertToPython_1(ConvertToPython):

    def __init__(self, lookup, language, numerals_language, is_debug, microbit=False):
        self.numerals_language = numerals_language
        self.language = language
        self.lookup = lookup
        self.is_debug = is_debug
        self.microbit = microbit
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
        if not self.microbit:
            return f"print('" + argument + "')" + self.add_debug_breakpoint()
        else:
            return textwrap.dedent(f"""\
                display.scroll('{argument}')""")

    def ask(self, meta, args):
        argument = process_characters_needing_escape(args[0])
        return "answer = input('" + argument + "')" + self.add_debug_breakpoint()

    def echo(self, meta, args):
        if len(args) == 0:
            return f"print(answer){self.add_debug_breakpoint()}"  # no arguments, just print answer

        argument = process_characters_needing_escape(args[0])
        return "print('" + argument + " '+answer)" + self.add_debug_breakpoint()

    def play(self, meta, args):
        if len(args) == 0:
            return self.make_play('C4', meta) + self.add_debug_breakpoint()

        note = args[0].upper()  # will we also support multiple notes at once?
        return self.make_play(note, meta) + self.add_debug_breakpoint()

    def comment(self, meta, args):
        return f"#{''.join(args)}"

    def empty_line(self, meta, args):
        return ''

    def forward(self, meta, args):
        if len(args) == 0:
            return add_sleep_to_command(f't.forward(50){self.add_debug_breakpoint()}', False, self.is_debug,
                                        location="after")
        return self.make_forward(int(args[0]))

    def color(self, meta, args):
        if len(args) == 0:
            return f"t.pencolor('black'){self.add_debug_breakpoint()}"  # no arguments defaults to black ink

        arg = args[0].data
        if arg in command_make_color_local(self.language):
            return f"t.pencolor('{arg}'){self.add_debug_breakpoint()}"
        else:
            # the TypeValidator should protect against reaching this line:
            raise exceptions.InvalidArgumentTypeException(command=Command.color, invalid_type='', invalid_argument=arg,
                                                          allowed_types=get_allowed_types(Command.color, self.level),
                                                          line_number=meta.line)

    def turn(self, meta, args):
        if len(args) == 0:
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
                play(note_with_error('{note}', {ex}))
                time.sleep(0.5)""")

    def make_play_var(self, note, meta):
        self.check_var_usage([note], meta.line)
        chosen_note = note.children[0] if isinstance(note, Tree) else note
        ex = make_value_error(Command.play, 'suggestion_note', self.language)

        return textwrap.dedent(f"""\
                play(note_with_error({chosen_note}, {ex}))
                time.sleep(0.5)""")

    def make_color(self, parameter, language):
        return self.make_turtle_color_command(parameter, Command.color, 'pencolor', language)

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
        lists_names = []
        list_args = []
        # List usage comes in indexation and random choice
        var_regex = r"[\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+|[\p{Mn}\p{Mc}\p{Nd}\p{Pc}·]+"
        list_access_with_int_cast = fr"(({var_regex})+\[int\(({var_regex})\)-1\])"
        list_access_without_cast = fr"(({var_regex})+\[({var_regex})-1\])"
        list_access_random = fr"(random\.choice\(({var_regex})\))"
        list_regex = f"{list_access_with_int_cast}|{list_access_without_cast}|{list_access_random}"
        for arg in args:
            # Expressions come inside a Tree object, so unpack them
            if isinstance(arg, Tree):
                arg = arg.children[0]
            for group in regex.findall(list_regex, arg):
                match = [e for e in group if e][:2]
                list_args.append(match[0])
                lists_names.append(match[1])

        errors = [self.make_index_error(list_args[i], list_name) for i, list_name in enumerate(lists_names)]
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

    # ->>> why doesn't this live in isvalid? refactor now that isvalid is cleaned up!
    def error_ask_dep_2(self, meta, args):
        # ask is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1, 'ask', "ask_needs_var", meta.line)

    def error_echo_dep_2(self, meta, args):
        # echo is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1, 'echo', "echo_out", meta.line)

    def color(self, meta, args):
        if len(args) == 0:
            return f"t.pencolor('black'){self.add_debug_breakpoint()}"
        arg = args[0]
        if not isinstance(arg, str):
            arg = arg.data

        arg = self.process_variable_for_fstring(arg)

        return self.make_color(arg, self.language)

    def turn(self, meta, args):
        if len(args) == 0:
            return f"t.right(90){self.add_debug_breakpoint()}"  # no arguments defaults to a right turn
        arg = args[0]
        if self.is_variable(arg, meta.line):
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
        args_new = [self.make_print_ask_arg(a, meta) for a in args]
        argument_string = ' '.join(args_new)
        if not self.microbit:
            exception = self.make_index_error_check_if_list(args)
            return exception + f"print(f'{argument_string}'){self.add_debug_breakpoint()}"
        else:
            return f"""display.scroll('{argument_string}')"""

    def ask(self, meta, args):
        var = args[0]
        args_new = [self.make_print_ask_arg(a, meta, var) for a in args[1:]]
        argument_string = ' '.join(args_new)
        exception = self.make_index_error_check_if_list(args)
        return exception + f"{var} = input(f'{argument_string}'){self.add_debug_breakpoint()}"

    def make_print_ask_arg(self, arg, meta, var_to_escape=''):
        # list access has been already rewritten since it occurs lower in the tree
        # so when we encounter it as a child of print it will not be a subtree, but
        # transpiled code (for example: random.choice(dieren))
        # therefore we should not process it anymore and thread it as a variable:
        # we set the line number to 100 so there is never an issue with variable access before
        # assignment (regular code will not work since random.choice(dieren) is never defined as var as such)
        if "random.choice" in arg or "[" in arg:
            return self.process_variable_for_fstring(arg, meta.line, var_to_escape)

        # this regex splits words from non-letter characters, such that name! becomes [name, !]
        p = r"[·\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}\p{Mn}\p{Mc}\p{Nd}\p{Pc}]+|[^·\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}]+"
        res = regex.findall(p, arg)
        return ''.join([self.process_variable_for_fstring(x, meta.line, var_to_escape) for x in res])

    def forward(self, meta, args):
        if len(args) == 0:
            return add_sleep_to_command(f't.forward(50){self.add_debug_breakpoint()}', False, self.is_debug,
                                        location="after")

        if ConvertToPython.is_int(args[0]):
            parameter = int(args[0])
        else:
            # if not an int, then it is a variable
            parameter = args[0]
            self.add_variable_access_location(parameter, meta.line)

        return self.make_forward(parameter)

    def play(self, meta, args):
        if len(args) == 0:
            return self.make_play('C4', meta) + self.add_debug_breakpoint()

        # if ConvertToPython.is_int(args[0]): #handig ff laten staan als ik nog integers ga ondersteunen in this PR or the next
        #     parameter = int(args[0])
        # else:
        # if not an int, then it is a variable

        note = args[0]
        if isinstance(note, str):
            if present_in_notes_mapping(note):  # this is a supported note
                return self.make_play(note.upper(), meta) + self.add_debug_breakpoint()

        # no note? it must be a variable!
        self.add_variable_access_location(note, meta.line)
        return self.make_play_var(note, meta) + self.add_debug_breakpoint()

    def assign(self, meta, args):
        variable_name = args[0]
        value = args[1]

        if self.is_random(value) or self.is_list(value):
            exception = self.make_index_error_check_if_list([value])
            return exception + variable_name + " = " + value + self.add_debug_breakpoint()
        else:
            if self.is_variable(value, meta.line):  # if the value is a variable, this is a reassign
                value = self.process_variable(value, meta.line)
                return variable_name + " = " + value + self.add_debug_breakpoint()
            else:
                # if the assigned value is not a variable and contains single quotes, escape them
                value = process_characters_needing_escape(value)
                return variable_name + " = '" + value + "'" + self.add_debug_breakpoint()

    def sleep(self, meta, args):
        if not args:
            return f"time.sleep(1){self.add_debug_breakpoint()}"
        else:
            value = f'"{args[0]}"' if self.is_int(args[0]) else args[0]
            if not self.is_int(args[0]):
                self.add_variable_access_location(value, meta.line)
            index_exception = self.make_index_error_check_if_list(args)
            ex = make_value_error(Command.sleep, 'suggestion_number', self.language)
            code = index_exception + \
                textwrap.dedent(f"time.sleep(int_with_error({value}, {ex})){self.add_debug_breakpoint()}")
            return code


@v_args(meta=True)
@hedy_transpiler(level=3)
@source_map_transformer(source_map)
class ConvertToPython_3(ConvertToPython_2):
    def assign_list(self, meta, args):
        parameter = args[0]
        values = [f"'{process_characters_needing_escape(a)}'" for a in args[1:]]
        return f"{parameter} = [{', '.join(values)}]{self.add_debug_breakpoint()}"

    def list_access(self, meta, args):
        args = [escape_var(a) for a in args]
        listname = str(args[0])
        location = str(args[0])

        # check the arguments (except when they are random or numbers, that is not quoted nor a var but is allowed)
        self.check_var_usage([a for a in args if a != 'random' and not a.isnumeric()], meta.line)

        # store locations of both parts (can be list at var)
        self.add_variable_access_location(listname, meta.line)
        self.add_variable_access_location(location, meta.line)

        if args[1] == 'random':
            return 'random.choice(' + listname + ')'
        else:
            return listname + '[int(' + args[1] + ')-1]'

    def process_argument(self, meta, arg):
        # only call process_variable if arg is a string, else keep as is (ie.
        # don't change 5 into '5', my_list[1] into 'my_list[1]')
        if arg.isnumeric() and isinstance(arg, int):  # is int/float
            return arg
        elif (self.is_list(arg)):  # is list indexing
            list_name = arg.split('[')[0]
            self.add_variable_access_location(list_name, meta.line)
            before_index, after_index = arg.split(']', 1)
            return before_index + '-1' + ']' + after_index  # account for 1-based indexing
        else:
            return self.process_variable(arg, meta.line)

    def add(self, meta, args):
        value = self.process_argument(meta, args[0])
        list_var = args[1]

        # both sides have been used now
        self.add_variable_access_location(value, meta.line)
        self.add_variable_access_location(list_var, meta.line)
        return f"{list_var}.append({value}){self.add_debug_breakpoint()}"

    def remove(self, meta, args):
        value = self.process_argument(meta, args[0])
        list_var = args[1]

        # both sides have been used now
        self.add_variable_access_location(value, meta.line)
        self.add_variable_access_location(list_var, meta.line)

        return textwrap.dedent(f"""\
        try:
          {list_var}.remove({value}){self.add_debug_breakpoint()}
        except:
          pass""")


@v_args(meta=True)
@hedy_transpiler(level=4)
@source_map_transformer(source_map)
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
        exceptions = self.make_index_error_check_if_list(args)
        if not self.microbit:
            return exceptions + f"print(f'{argument_string}'){self.add_debug_breakpoint()}"
        else:
            return textwrap.dedent(f"""\
                    display.scroll('{argument_string}')""")

    def ask(self, meta, args):
        var = args[0]
        argument_string = self.print_ask_args(meta, args[1:])
        index_check = self.make_index_error_check_if_list(args)
        return index_check + f"{var} = input(f'{argument_string}'){self.add_debug_breakpoint()}"

    def error_print_nq(self, meta, args):
        return ConvertToPython_2.print(self, meta, args)

    def clear(self, meta, args):
        command = "extensions.clear()"

        # add two sleeps, one is a bit brief
        command = add_sleep_to_command(command, False, self.is_debug, "before")
        command = add_sleep_to_command(command, False, self.is_debug, "before")

        return f"""{command}{self.add_debug_breakpoint()}
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
@source_map_transformer(source_map)
class ConvertToPython_5(ConvertToPython_4):

    def __init__(self, lookup, language, numerals_language, is_debug, microbit):
        super().__init__(lookup, language, numerals_language, is_debug, microbit)

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
        self.process_variable(args[0], meta.line)
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

    def convert_tree_to_number(self, a):
        # takes a calculation tree coming from the process_calculation() method, and turns it into numbers
        # we do that late in the tree to deal with different numeral systems

        if self.numerals_language == "Latin":
            return "{" + a.children[0] + "}"
        else:
            converted = f'convert_numerals("{self.numerals_language}",{a.children[0]})'
            return "{" + converted + "}"

    def sleep(self, meta, args):
        if not args:
            return "time.sleep(1)"
        else:
            if type(args[0]) is Tree:
                if self.check_if_error_skipped(args[0]):
                    raise hedy.exceptions.InvalidErrorSkippedException
                else:
                    args[0] = args[0].children[0]
                    value = f'{args[0]}'
            else:
                value = f'"{args[0]}"' if self.is_int(args[0]) else args[0]
                if not self.is_int(args[0]):
                    self.add_variable_access_location(value, meta.line)

            index_exception = self.make_index_error_check_if_list(args)
            ex = make_value_error(Command.sleep, 'suggestion_number', self.language)
            code = index_exception + textwrap.dedent(f"time.sleep(int_with_error({value}, {ex}))")
            return code

    def print_ask_args(self, meta, args):
        # we only check non-Tree (= non calculation) arguments
        self.check_var_usage(args, meta.line)

        # force all to be printed as strings (since there can not be int arguments)
        args_new = []
        for a in args:
            if isinstance(a, Tree):
                args_new.append(self.convert_tree_to_number(a))
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
            return parameter + " = " + value.children[0] + self.add_debug_breakpoint()
        else:
            if self.is_variable(value, meta.line):
                value = self.process_variable(value, meta.line)
                if self.is_list(value) or self.is_random(value):
                    exception = self.make_index_error_check_if_list([value])
                    return exception + parameter + " = " + value + self.add_debug_breakpoint()
                else:
                    return parameter + " = " + value
            else:
                # if the assigned value is not a variable and contains single quotes, escape them
                value = process_characters_needing_escape(value)
                return parameter + " = '" + value + "'" + self.add_debug_breakpoint()

    def process_token_or_tree(self, argument, meta):
        if type(argument) is Tree:
            return f'{str(argument.children[0])}'
        if argument.isnumeric():
            latin_numeral = int(argument)
            return f'int({latin_numeral})'
        # this is a variable
        self.add_variable_access_location(argument, meta.line)
        return f'int({argument})'

    def process_token_or_tree_for_calculation(self, argument, command, meta):
        if type(argument) is Tree:
            return f'{str(argument.children[0])}'
        if argument.isnumeric():
            latin_numeral = int(argument)
            return f'int({latin_numeral})'
        self.add_variable_access_location(argument, meta.line)
        exception_text = make_value_error(command, 'suggestion_number', self.language)
        return f'int_with_error({argument}, {exception_text})'

    def process_calculation(self, args, operator, meta):
        # arguments of a sum are either a token or a
        # tree resulting from earlier processing
        # for trees we need to grap the inner string
        # for tokens we add int around them

        args = [self.process_token_or_tree_for_calculation(a, operator, meta) for a in args]
        return Tree('sum', [f'{args[0]} {operator} {args[1]}'])

    def addition(self, meta, args):
        return self.process_calculation(args, '+', meta)

    def subtraction(self, meta, args):
        return self.process_calculation(args, '-', meta)

    def multiplication(self, meta, args):
        return self.process_calculation(args, '*', meta)

    def division(self, meta, args):
        return self.process_calculation(args, '//', meta)

    def turn(self, meta, args):
        if len(args) == 0:
            return "t.right(90)" + self.add_debug_breakpoint()  # no arguments defaults to a right turn
        arg = args[0]
        if self.is_variable(arg, meta.line):
            return self.make_turn(escape_var(arg))
        if isinstance(arg, Tree):
            return self.make_turn(arg.children[0])
        return self.make_turn(int(arg))

    def forward(self, meta, args):
        if len(args) == 0:
            return add_sleep_to_command('t.forward(50)' + self.add_debug_breakpoint(), False, self.is_debug,
                                        location="after")
        arg = args[0]
        if self.is_variable(arg, meta.line):
            return self.make_forward(escape_var(arg))
        if isinstance(arg, Tree):
            return self.make_forward(arg.children[0])
        return self.make_forward(int(args[0]))


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


@v_args(meta=True)
@hedy_transpiler(level=7)
@source_map_transformer(source_map)
class ConvertToPython_7(ConvertToPython_6):
    def make_repeat(self, meta, args, multiline):
        var_name = self.get_fresh_var('__i')
        times = self.process_variable(args[0], meta.line)

        # In level 7, repeat can only have 1 line in its body
        if not multiline:
            body = self.indent(args[1])
        # In level 8 and up, repeat can have multiple lines in its body
        else:
            body = "\n".join([self.indent(x) for x in args[1:]])

        body = add_sleep_to_command(body, indent=True, is_debug=self.is_debug, location="after")
        ex = make_value_error(Command.repeat, 'suggestion_number', self.language)
        return f"for {var_name} in range(int_with_error({times}, {ex})):{self.add_debug_breakpoint()}\n{body}"

    def repeat(self, meta, args):
        return self.make_repeat(meta, args, multiline=False)


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
        self.process_variable(args[0], meta.line)
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

    def var_access(self, meta, args):
        if len(args) == 1:  # accessing a var
            return escape_var(args[0])
        else:
            # this is list_access
            return escape_var(args[0]) + "[" + str(escape_var(args[1])) + "]" if type(args[1]
                                                                                      ) is not Tree else "random.choice(" + str(
                escape_var(args[0])) + ")"

    def var_access_print(self, meta, args):
        return self.var_access(meta, args)


@v_args(meta=True)
@hedy_transpiler(level=10)
@source_map_transformer(source_map)
class ConvertToPython_10(ConvertToPython_8_9):
    def for_list(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        times = self.process_variable(args[0], meta.line)

        # add the list to the lookup table, this used now too
        self.add_variable_access_location(args[1], meta.line)

        body = "\n".join([ConvertToPython.indent(x) for x in args[2:]])

        body = add_sleep_to_command(body, True, self.is_debug, location="after")
        return f"for {times} in {args[1]}:{self.add_debug_breakpoint()}\n{body}"


@v_args(meta=True)
@hedy_transpiler(level=11)
@source_map_transformer(source_map)
class ConvertToPython_11(ConvertToPython_10):
    def for_loop(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        iterator = escape_var(args[0])
        # iterator is always a used variable
        self.add_variable_access_location(iterator, meta.line)

        body = "\n".join([ConvertToPython.indent(x) for x in args[3:]])
        body = add_sleep_to_command(body, True, self.is_debug, location="after")
        stepvar_name = self.get_fresh_var('step')
        begin = self.process_token_or_tree(args[1], meta)
        end = self.process_token_or_tree(args[2], meta)
        return f"""{stepvar_name} = 1 if {begin} < {end} else -1
for {iterator} in range({begin}, {end} + {stepvar_name}, {stepvar_name}):{self.add_debug_breakpoint()}
{body}"""


@v_args(meta=True)
@hedy_transpiler(level=12)
@source_map_transformer(source_map)
class ConvertToPython_12(ConvertToPython_11):
    def define(self, meta, args):
        function_name = args[0]
        args_str = ", ".join(str(x) for x in args[1].children) if isinstance(
            args[1], Tree) and args[1].data == "arguments" else ""

        lines = []
        for line in args[1 if args_str == "" else 2:]:
            lines.append(line)
        body = "\n".join(ConvertToPython.indent(x) for x in lines)

        return f"def {function_name}({args_str}):\n{body}"

    def call(self, meta, args):
        args_str = ""
        self.add_variable_access_location(args[0], meta.line)

        function_name = args[0]
        function_tree = [x.tree for x in self.lookup if x.name == function_name + "()"]
        tree_arguments = [x for x in function_tree[0].children if x.data == 'arguments']

        number_of_defined_arguments = 0 if tree_arguments == [] else len(tree_arguments[0].children)
        number_of_used_arguments = 0 if len(args) == 1 else len(args[1].children)

        if number_of_used_arguments != number_of_defined_arguments:
            raise hedy.exceptions.WrongNumberofArguments(
                name=function_name,
                defined_number=number_of_defined_arguments,
                used_number=number_of_used_arguments,
                line_number=meta.line)

        if len(args) > 1:
            args_str = ", ".join(str(x.children[0]) if isinstance(x, Tree) else str(x) for x in args[1].children)
            for x in args[1].children:
                self.add_variable_access_location(str(x), meta.line)

        return f"{function_name}({args_str})"

    def returns(self, meta, args):
        argument_string = self.print_ask_args(meta, args)
        exception = self.make_index_error_check_if_list(args)
        return exception + textwrap.dedent(f"""\
            try:
              return int(f'''{argument_string}''')
            except ValueError:
              try:
                return float(f'''{argument_string}''')
              except ValueError:
                return f'''{argument_string}'''""")

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
        text = args[0] if args else ''
        if "'" in text:
            return f'"{text}"'
        return f"'{text}'"

    def print_ask_args(self, meta, args):
        result = super().print_ask_args(meta, args)
        if "'''" in result:
            raise exceptions.UnsupportedStringValue(invalid_value="'''")
        return result

    def print(self, meta, args):
        argument_string = self.print_ask_args(meta, args)
        exception = self.make_index_error_check_if_list(args)
        if not self.microbit:
            return exception + f"print(f'''{argument_string}''')" + self.add_debug_breakpoint()
        else:
            return textwrap.dedent(f"""\
                    display.scroll('{argument_string}')""")

    def ask(self, meta, args):
        var = args[0]
        argument_string = self.print_ask_args(meta, args[1:])
        exception = self.make_index_error_check_if_list(args)
        return exception + textwrap.dedent(f"""\
            {var} = input(f'''{argument_string}'''){self.add_debug_breakpoint()}
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
        return parameter + " = [" + ", ".join(values) + "]" + self.add_debug_breakpoint()

    def in_list_check(self, meta, args):
        left_hand_side = args[0]
        right_hand_side = args[1]
        self.check_var_usage_when_quotes_are_required(left_hand_side, meta)
        self.check_var_usage_when_quotes_are_required(right_hand_side, meta)
        return f"{left_hand_side} in {right_hand_side}"

    def not_in_list_check(self, meta, args):
        left_hand_side = args[0]
        right_hand_side = args[1]
        self.check_var_usage_when_quotes_are_required(left_hand_side, meta)
        self.check_var_usage_when_quotes_are_required(right_hand_side, meta)
        return f"{left_hand_side} not in {right_hand_side}"

    def assign(self, meta, args):
        right_hand_side = args[1]
        left_hand_side = args[0]

        self.check_var_usage_when_quotes_are_required(right_hand_side, meta)

        if isinstance(right_hand_side, Tree):
            exception = self.make_index_error_check_if_list([right_hand_side.children[0]])
            return exception + left_hand_side + " = " + right_hand_side.children[0] + self.add_debug_breakpoint()
        else:
            # we no longer escape quotes here because they are now needed
            exception = self.make_index_error_check_if_list([right_hand_side])
            return exception + left_hand_side + " = " + right_hand_side + "" + self.add_debug_breakpoint()

    def var(self, meta, args):
        name = args[0]
        # self.check_var_usage(args, meta.line)
        return escape_var(name)

    def turn(self, meta, args):
        if len(args) == 0:
            return "t.right(90)" + self.add_debug_breakpoint()  # no arguments defaults to a right turn
        arg = args[0]
        if self.is_variable(arg, meta.line):
            return self.make_turn(escape_var(arg))
        if isinstance(arg, Tree):
            return self.make_turn(arg.children[0])
        return self.make_turn(float(arg))

    def forward(self, meta, args):
        if len(args) == 0:
            return add_sleep_to_command('t.forward(50)' + self.add_debug_breakpoint(), False, self.is_debug,
                                        location="after")
        arg = args[0]
        if self.is_variable(arg, meta.line):
            return self.make_forward(escape_var(arg))
        if isinstance(arg, Tree):
            return self.make_forward(arg.children[0])
        return self.make_forward(float(args[0]))

    def make_turn(self, parameter):
        return self.make_turtle_command(parameter, Command.turn, 'right', False, HedyType.float)

    def make_forward(self, parameter):
        return self.make_turtle_command(parameter, Command.forward,
                                        'forward', True, HedyType.float)

    def process_token_or_tree(self, argument, meta):
        if isinstance(argument, Tree):
            return f'{str(argument.children[0])}'
        else:
            # this is a variable, add to the table
            self.add_variable_access_location(argument, meta.line)
            return argument

    def process_token_or_tree_for_calculation(self, argument, command, meta):
        if type(argument) is Tree:
            return f'{str(argument.children[0])}'
        else:
            # this is a variable, add to the table
            self.add_variable_access_location(argument, meta.line)
            exception_text = make_value_error(command, 'suggestion_number', self.language)
            return f'number_with_error({argument}, {exception_text})'

    # From level 12 concatenation should also work, so the args could be either numbers or strings
    def addition(self, meta, args):
        args = [self.process_token_or_tree(a, meta) for a in args]
        if all([self.is_int(a) or self.is_float(a) for a in args]):
            return Tree('sum', [f'{args[0]} + {args[1]}'])
        else:
            ex_text = make_values_error(Command.addition, 'suggestion_numbers_or_strings', self.language)
            return Tree('sum', [f'sum_with_error({args[0]}, {args[1]}, {ex_text})'])

    def division(self, meta, args):
        return self.process_calculation(args, '/', meta)


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
@source_map_transformer(source_map)
class ConvertToPython_15(ConvertToPython_14):
    def while_loop(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        body = "\n".join(all_lines)
        body = add_sleep_to_command(body, True, self.is_debug, location="after")
        exceptions = self.make_index_error_check_if_list([args[0]])
        return exceptions + "while " + args[0] + ":" + self.add_debug_breakpoint() + "\n" + body

    def if_pressed_without_else(self, meta, args):
        code = args[0]

        return (
            code + self.make_extension_call()
        )

    def if_pressed(self, meta, args):
        self.process_variable(args[0], meta.line)
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


@v_args(meta=True)
@hedy_transpiler(level=16)
@source_map_transformer(source_map)
class ConvertToPython_16(ConvertToPython_15):
    def assign_list(self, meta, args):
        parameter = args[0]
        values = [a for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]" + self.add_debug_breakpoint()

    def change_list_item(self, meta, args):
        left_side = args[0] + '[' + args[1] + '-1]'
        right_side = args[2]

        self.add_variable_access_location(args[0], meta.line)
        self.add_variable_access_location(args[1], meta.line)
        self.add_variable_access_location(args[2], meta.line)

        exception = self.make_index_error_check_if_list([left_side])
        return exception + left_side + ' = ' + right_side + self.add_debug_breakpoint()

    def ifs(self, meta, args):
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        exceptions = self.make_index_error_check_if_list([args[0]])
        return exceptions + "if " + args[0] + ":" + self.add_debug_breakpoint() + "\n" + "\n".join(all_lines)


@v_args(meta=True)
@hedy_transpiler(level=17)
@source_map_transformer(source_map)
class ConvertToPython_17(ConvertToPython_16):
    def elifs(self, meta, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        return "\nelif " + args[0] + ":" + self.add_debug_breakpoint() + "\n" + "\n".join(all_lines)

    def if_pressed_elifs(self, meta, args):
        self.process_variable(args[0], meta.line)
        args = [a for a in args if a != ""]  # filter out in|dedent tokens

        key = args[0]

        elif_code = '\n'.join([x for x in args[1:]])
        elif_code = ConvertToPython.indent(elif_code)
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


# this is only a couple of MB in total, safe to cache
@cache
def create_grammar(level, lang, skip_faulty):
    # start with creating the grammar for level 1
    merged_grammars = get_full_grammar_for_level(1)

    # then keep merging new grammars in
    for i in range(2, level + 1):
        grammar_text_i = get_additional_rules_for_level(i)
        merged_grammars = hedy_grammar.merge_grammars(merged_grammars, grammar_text_i)

    # keyword and other terminals never have mergable rules, so we can just add them at the end
    keywords = get_keywords_for_language(lang)
    terminals = get_terminals()
    merged_grammars = merged_grammars + '\n' + keywords + '\n' + terminals

    # Change the grammar if skipping faulty is enabled
    if skip_faulty:
        # Make sure to change the meaning of error_invalid
        # this way more text will be 'catched'
        error_invalid_rules = re.findall(r'^error_invalid.-100:.*?\n', merged_grammars, re.MULTILINE)
        if len(error_invalid_rules) > 0:
            error_invalid_rule = error_invalid_rules[0]
            error_invalid_rule_changed = 'error_invalid.-100: textwithoutspaces _SPACE* text?\n'
            merged_grammars = merged_grammars.replace(error_invalid_rule, error_invalid_rule_changed)

        # from level 12:
        # Make sure that all keywords in the language are added to the rules:
        # textwithspaces & textwithoutspaces, so that these do not fall into the error_invalid rule
        if level > 12:
            textwithspaces_rules = re.findall(r'^textwithspaces:.*?\n', merged_grammars, re.MULTILINE)
            if len(textwithspaces_rules) > 0:
                textwithspaces_rule = textwithspaces_rules[0]
                textwithspaces_rule_changed = r'textwithspaces: /(?:[^#\n،,，、 ]| (?!SKIP1))+/ -> text' + '\n'
                merged_grammars = merged_grammars.replace(textwithspaces_rule, textwithspaces_rule_changed)

            textwithoutspaces_rules = re.findall(r'^textwithoutspaces:.*?\n', merged_grammars, re.MULTILINE)
            if len(textwithoutspaces_rules) > 0:
                textwithoutspaces_rule = textwithoutspaces_rules[0]
                textwithoutspaces_rule_changed = (
                    r'textwithoutspaces: /(?:[^#\n،,，、 *+\-\/eiіиలేไamfnsbअ否אو]|SKIP2)+/ -> text' + '\n'
                )
                merged_grammars = merged_grammars.replace(textwithoutspaces_rule, textwithoutspaces_rule_changed)

            non_allowed_words = re.findall(r'".*?"', keywords)
            non_allowed_words = list(set(non_allowed_words))

            non_allowed_words = [x.replace('"', '') for x in non_allowed_words]
            non_allowed_words_with_space = '|'.join(non_allowed_words)
            merged_grammars = merged_grammars.replace('SKIP1', non_allowed_words_with_space)

            letters_done = []
            string_words = ''

            for word in non_allowed_words:
                # go through all words and add them in groups by their first letter
                first_letter = word[0]
                if first_letter not in letters_done:
                    string_words += f'|{first_letter}(?!{word[1:]})'
                    letters_done.append(first_letter)
                else:
                    string_words = string_words.replace(f'|{word[0]}(?!', f'|{word[0]}(?!{word[1:]}|')

            string_words = string_words.replace('|)', ')')  # remove empty regex expressions
            string_words = string_words[1:]  # remove first |

            merged_grammars = merged_grammars.replace('SKIP2', string_words)

        # Make sure that the error_invalid is added to the command rule
        # to function as a 'bucket' for faulty text
        command_rules = re.findall(r'^command:.*?\n', merged_grammars, re.MULTILINE)
        if len(command_rules) > 0:
            command_rule = command_rules[0]
            command_rule_with_error_invalid = command_rule.replace('\n', '') + " | error_invalid\n"
            merged_grammars = merged_grammars.replace(command_rule, command_rule_with_error_invalid)

        # Make sure that the error_invalid is added to the if_less_command rule
        # to function as a 'bucket' for faulty if body commands
        if_less_command_rules = re.findall(r'^_if_less_command:.*?\n', merged_grammars, re.MULTILINE)
        if len(if_less_command_rules) > 0:
            if_less_command_rule = if_less_command_rules[0]
            if_less_command_rule_with_error_invalid = if_less_command_rule.replace('\n', '') + " | error_invalid\n"
            merged_grammars = merged_grammars.replace(if_less_command_rule, if_less_command_rule_with_error_invalid)

        # Make sure that the _non_empty_program rule does not contain error_invalid rules
        # so that all errors will be catches by error_invalid instead of _non_empty_program_skipping
        non_empty_program_rules = re.findall(r'^_non_empty_program:.*?\n', merged_grammars, re.MULTILINE)
        if len(non_empty_program_rules) > 0:
            non_empty_program_rule = non_empty_program_rules[0]
            non_empty_program_rule_changed = (
                '_non_empty_program: _EOL* (command) _SPACE* (_EOL+ command _SPACE*)* _EOL*\n'
            )
            merged_grammars = merged_grammars.replace(non_empty_program_rule, non_empty_program_rule_changed)

    # ready? Save to file to ease debugging
    # this could also be done on each merge for performance reasons
    save_total_grammar_file(level, merged_grammars, lang)
    return merged_grammars


def save_total_grammar_file(level, grammar, lang_):
    write_file(grammar, 'grammars-Total', f'level{level}.{lang_}-Total.lark')


def get_additional_rules_for_level(level):
    return read_file('grammars', f'level{level}-Additions.lark')


def get_full_grammar_for_level(level):
    return read_file('grammars', f'level{level}.lark')


def get_keywords_for_language(language):
    if not local_keywords_enabled:
        language = 'en'
    try:
        return read_file('grammars', f'keywords-{language}.lark')
    except FileNotFoundError:
        return read_file('grammars', f'keywords-en.lark')


def get_terminals():
    return read_file('grammars', 'terminals.lark')


def read_file(*paths):
    script_dir = path.abspath(path.dirname(__file__))
    path_ = path.join(script_dir, *paths)
    with open(path_, "r", encoding="utf-8") as file:
        return file.read()


def write_file(content, *paths):
    script_dir = path.abspath(path.dirname(__file__))
    path_ = path.join(script_dir, *paths)
    with open(path_, "w", encoding="utf-8") as file:
        file.write(content)


PARSER_CACHE = {}


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
    grammar = create_grammar(level, lang, skip_faulty)
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
    lark = None
    if use_cache:
        lark = _restore_parser_from_file_if_present(cached_parser_file)
    if lark is None:
        lark = Lark(grammar, **parser_opts)  # ambiguity='explicit'
        if use_cache:
            _save_parser_to_file(lark, cached_parser_file)

    return lark


ParseResult = namedtuple('ParseResult', ['code', 'source_map', 'has_turtle',
                                         'has_pressed', 'has_clear', 'has_music', 'commands'])


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
            raise hedy.exceptions.CodePlaceholdersPresentException(line_number=line_number + 1)

        leading_spaces = find_indent_length(line)

        line_number += 1

        # ignore whitespace-only lines
        if leading_spaces == len(line):
            processed_code.append('')
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

    # FH, May 2022. for now, we just output arabic numerals when the language is ar
    # this can be changed into a profile setting or could be detected
    # in usage of programs
    if lang == "ar":
        numerals_language = "Arabic"
    else:
        numerals_language = "Latin"

    try:
        abstract_syntax_tree, lookup_table, commands = create_AST(input_string, level, lang)

        # grab the right transpiler from the lookup
        convertToPython = TRANSPILER_LOOKUP[level]
        python = convertToPython(lookup_table, lang, numerals_language, is_debug,
                                 microbit).transform(abstract_syntax_tree)

        has_clear = "clear" in commands
        has_turtle = "forward" in commands or "turn" in commands or "color" in commands
        has_pressed = "if_pressed" in commands or "if_pressed_else" in commands or "assign_button" in commands
        has_music = "play" in commands

        parse_result = ParseResult(python, source_map, has_turtle, has_pressed, has_clear, has_music, commands)

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
