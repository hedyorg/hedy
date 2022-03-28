import textwrap

import lark
from lark import Lark
from lark.exceptions import LarkError, UnexpectedEOF, UnexpectedCharacters, VisitError
from lark import Tree, Transformer, visitors, v_args
from os import path, environ

import warnings
import hedy
import hedy_translation
import utils
from collections import namedtuple
import hashlib
import re
from dataclasses import dataclass, field
import exceptions
import program_repair
import yaml
import sys

# Some useful constants
HEDY_MAX_LEVEL = 18
MAX_LINES = 100
LEVEL_STARTING_INDENTATION = 8

# Boolean variables to allow code which is under construction to not be executed
local_keywords_enabled = True

# dictionary to store transpilers
TRANSPILER_LOOKUP = {}

# Python keywords need hashing when used as var names
reserved_words = ['and', 'except', 'lambda', 'with', 'as', 'finally', 'nonlocal', 'while', 'assert', 'False', 'None', 'yield', 'break', 'for', 'not', 'class', 'from', 'or', 'continue', 'global', 'pass', 'def', 'if', 'raise', 'del', 'import', 'return', 'elif', 'in', 'True', 'else', 'is', 'try']

# Define and load all available language data
ALL_LANGUAGES = {
    'en': 'English',
    'nl': 'Nederlands',
    'es': 'Español',
    'fr': 'Français',
    'nb_NO': 'Norsk',
    'pt_pt': 'Português(pt)',
    'pt_br': 'Português(br)',
    'de': 'Deutsch',
    'it': 'Italiano',
    'sw': 'Swahili',
    'hu': 'Magyar',
    'el': 'Ελληνικά',
    'zh': "简体中文",
    'cs': 'Čeština',
    'bg': 'Български',
    'bn': 'বাংলা',
    'hi': 'हिंदी',
    'id': 'Bahasa Indonesia',
    'fy': 'Frysk',
    'ar': 'عربى',
    'tr': 'Türk'
}
# Define fall back languages for adventures
FALL_BACK_ADVENTURE = {
    'fy': 'nl',
    'pt_br': 'pt_pt'
}

ALL_KEYWORD_LANGUAGES = {
    'en': 'EN',
    'nl': 'NL',
    'ar': 'AR',
    'fr': 'FR',
    'hi': 'HI',
    'es': 'ES'
}


class Command:
    print = 'print'
    ask = 'ask'
    echo = 'echo'
    turn = 'turn'
    forward = 'forward'
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


translatable_commands = {Command.print: ['print'],
                         Command.ask: ['ask'],
                         Command.echo: ['echo'],
                         Command.turn: ['turn'],
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
    1 :['print', 'ask', 'echo', 'turn', 'forward'],
    2 :['print', 'ask', 'is', 'turn', 'forward', 'sleep'],
    3 :['ask', 'is', 'print', 'forward', 'turn', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from'],
    4 :['ask', 'is', 'print', 'forward', 'turn', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from'],
    5 :['ask', 'is', 'print', 'forward', 'turn', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else'],
    6 :['ask', 'is', 'print', 'forward', 'turn', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else'],
    7 :['ask', 'is', 'print', 'forward', 'turn', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'repeat', 'times'],
    8 :['ask', 'is', 'print', 'forward', 'turn', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'repeat', 'times'],
    9 :['ask', 'is', 'print', 'forward', 'turn', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'repeat', 'times'],
    10 :['ask', 'is', 'print', 'forward', 'turn', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'repeat', 'times', 'for'],
    11 :['ask', 'is', 'print', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'for', 'range'],
    12 :['ask', 'is', 'print', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'for', 'range'],
    13 :['ask', 'is', 'print', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'for', 'range', 'and', 'or'],
    14 :['ask', 'is', 'print', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'for', 'range', 'and', 'or'],
    15 :['ask', 'is', 'print', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'for', 'range', 'and', 'or', 'while'],
    16 :['ask', 'is', 'print', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'for', 'range', 'and', 'or', 'while'],
    17 :['ask', 'is', 'print', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'for', 'range', 'and', 'or', 'while', 'elif'],
    18 :['is', 'print', 'sleep', 'at', 'random', 'add', 'to', 'remove', 'from', 'in', 'if', 'else', 'for', 'range', 'and', 'or', 'while', 'elif', 'input'],
}

command_turn_literals = ['right', 'left']

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
                   2: [HedyType.integer, HedyType.input]},
    Command.forward: {1: [HedyType.integer, HedyType.input]},
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
    Command.not_equal: {14: [HedyType.integer, HedyType.float, HedyType.string, HedyType.input, HedyType.list]}
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
    path_keywords = dir + "/coursedata/keywords"

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


def hash_needed(var):
    # this function now sometimes gets a str and sometimes - a LookupEntry
    # not pretty but it will all be removed once we no longer need hashing (see issue #959) so ok for now

    # some elements are not names but processed names, i.e. random.choice(dieren)
    # they should not be hashed
    # these are either of type assignment and operation or already processed and then contain ( or [
    if (type(var) is LookupEntry and var.skip_hashing) or (isinstance(var, str) and ('[' in var or '(' in var)):
        return False

    var_name = var.name if type(var) is LookupEntry else var

    return var_name in reserved_words or character_skulpt_cannot_parse.search(var_name) is not None


def hash_var(var):
    var_name = var.name if type(var) is LookupEntry else var
    if hash_needed(var):
        # hash "illegal" var names
        # being reserved keywords
        # or non-latin vars to comply with Skulpt, which does not implement PEP3131 :(
        # prepend with v for when hash starts with a number
        hash_object = hashlib.md5(var_name.encode())
        return "v" + hash_object.hexdigest()
    else:
        return var_name

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


def style_closest_command(command):
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

    def NEGATIVE_NUMBER(self, args):
        return Tree('number', [str(args)])

    #level 2
    def var(self, meta, args):
        return Tree('var', [''.join([str(c) for c in args])], meta)

    def punctuation(self, meta, args):
        return Tree('punctuation', [''.join([str(c) for c in args])], meta)

    def list_access(self, meta, args):
        if type(args[1]) == Tree:
            if "random" in args[1].data:
                return Tree('list_access', [args[0], 'random'], meta)
            else:
                return Tree('list_access', [args[0], args[1].children[0]], meta)
        else:
            return Tree('list_access', [args[0], args[1]], meta)

    #level 5
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
            self.add_to_lookup(tree.children[0].children[0], tree)

    def input_empty_brackets(self, tree):
        self.input(tree)

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
        position_name = hash_var(tree.children[1])
        if position_name == 'random':
            name = f'random.choice({list_name})'
        else:
            # We want list access to be 1-based instead of 0-based, hence the -1
            name = f'{list_name}[{position_name}-1]'
        self.add_to_lookup(name, tree, True)

    def list_access_var(self, tree):
        self.add_to_lookup(tree.children[0].children[0], tree)
    def change_list_item(self, tree):
        self.add_to_lookup(tree.children[0].children[0], tree, True)

    def for_list(self, tree):
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
        entry = LookupEntry(name, tree, skip_hashing)
        hashed_name = hash_var(entry)
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

    def turn(self, tree):
        if tree.children:
            name = tree.children[0].data
            if self.level > 1 or name not in command_turn_literals:
                self.validate_args_type_allowed(Command.turn, tree.children, tree.meta)
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

        list_name = hash_var(tree.children[0].children[0])
        if tree.children[1] == 'random':
            name = f'random.choice({list_name})'
        else:
            # We want list access to be 1-based instead of 0-based, hence the -1
            name = f'{list_name}[{tree.children[1]}-1]'
        self.save_type_to_lookup(name, HedyType.any)

        return self.to_typed_tree(tree, HedyType.any)

    def list_access_var(self, tree):
        self.save_type_to_lookup(tree.children[0].children[0], HedyType.any)
        return self.to_typed_tree(tree)

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

    def punctuation(self, tree):
        return self.to_typed_tree(tree, HedyType.string)

    def text_in_quotes(self, tree):
        return self.to_typed_tree(tree.children[0], HedyType.string)

    def var_access(self, tree):
        return self.to_typed_tree(tree, HedyType.string)

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
                result = hedy_translation.find_command_keywords(self.input_string, self.lang, self.level, keywords,
                                                                meta.line, meta.end_line, meta.column-1, meta.end_column-2)
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
                raise hedy.exceptions.UndefinedVarException(name=var_name)

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
            if entry.name == hash_var(name):
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
        matches = [entry for entry in self.lookup if entry.name == hash_var(name)]
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
@v_args(meta=True)
class Filter(Transformer):
    def __default__(self, data, children, meta):
        result, args = are_all_arguments_true(children)
        return result, args, meta

    def program(self, meta, args):
        bool_arguments = [x[0] for x in args]
        if all(bool_arguments):
            return [True] #all complete
        else:
            for a in args:
                if not a[0]:
                    return False, a[1]

    #leafs are treated differently, they are True + their arguments flattened
    def var(self, meta, args):
        return True, ''.join([str(c) for c in args]), meta

    def random(self, meta, args):
        return True, 'random', meta

    def punctuation(self, meta, args):
        return True, ''.join([c for c in args]), meta

    def number(self, meta, args):
        return True, ''.join([c for c in args]), meta

    def NEGATIVE_NUMBER(self, args):
        return True, ''.join([c for c in args]), None

    def text(self, meta, args):
        return all(args), ''.join([c for c in args]), meta


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

    def NEGATIVE_NUMBER(self, args):
        return False

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
        if keyword == 'orcondition':
            return 'or'
        if keyword == 'andcondition':
            return 'and'
        if keyword == 'while_loop':
            return 'while'
        if keyword == 'in_list_check':
            return 'in'
        if keyword == 'input_empty_brackets':
            return 'input'
        if keyword == 'print_empty_brackets':
            return 'print'
        return keyword

    def __default__(self, args, children, meta):
        # if we are matching a rule that is a command
        production_rule_name = self.translate_keyword(args)
        leaves = flatten_list_of_lists_to_list(children)
        operators = ['addition', 'subtraction', 'multiplication', 'division'] # for the achievements we want to be able to also detct which operators were used by a kid

        if production_rule_name in commands_per_level[self.level] or production_rule_name in operators:
            return [production_rule_name] + leaves
        else:
            return leaves # 'pop up' the children


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

    def NEGATIVE_NUMBER(self, args):
        return []

    def text(self, args):
        return []


def all_commands(input_string, level, lang='en'):
    input_string = process_input_string(input_string, level)
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
            return leaves # 'pop up' the children

    def program(self, args):
        return flatten_list_of_lists_to_list(args)

    # somehow tokens are not picked up by the default rule so they need their own rule
    def INT(self, args):
        return []

    def NAME(self, args):
        return []

    def NUMBER(self, args):
        return []

    def NEGATIVE_NUMBER(self, args):
        return []

    def text(self, args):
        return ''.join(args)



def all_print_arguments(input_string, level, lang='en'):
    input_string = process_input_string(input_string, level)
    program_root = parse_input(input_string, level, lang)

    return AllPrintArguments(level).transform(program_root)


@v_args(meta=True)
class IsValid(Filter):
    # all rules are valid except for the "Invalid" production rule
    # this function is used to generate more informative error messages
    # tree is transformed to a node of [Bool, args, command number]

    # def program(self, meta, args):
    #     if len(args) == 0:
    #         return False, InvalidInfo("empty program")
    #     return super().program(meta, args)

    def error_invalid_space(self, meta, args):
        # return space to indicate that line starts in a space
        return False, InvalidInfo(" ", line=args[0][2].line, column=args[0][2].column), meta

    def error_print_nq(self, meta, args):
        # return error source to indicate what went wrong
        return False, InvalidInfo("print without quotes", line=args[0][2].line, column=args[0][2].column), meta

    def error_invalid(self, meta, args):
        # TODO: this will not work for misspelling 'at', needs to be improved!

        error = InvalidInfo('invalid command', args[0][1], [a[1] for a in args[1:]], meta.line, meta.column)
        return False, error, meta

    def error_unsupported_number(self, meta, args):
        error = InvalidInfo('unsupported number', arguments=[str(args[0])], line=meta.line, column=meta.column)
        return False, error, meta



    #other rules are inherited from Filter

def valid_echo(ast):
    commands = ast.children
    command_names = [x.children[0].data for x in commands]
    no_echo = not 'echo' in command_names

    #no echo is always ok!

    #otherwise, both have to be in the list and echo shold come after
    return no_echo or ('echo' in command_names and 'ask' in command_names) and command_names.index('echo') > command_names.index('ask')

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
        #echo may miss an argument
        return True, ('echo', meta.line)

    #other rules are inherited from Filter

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

class ConvertToPython(Transformer):
    def __init__(self, punctuation_symbols, lookup):
        self.lookup = lookup

    def is_variable(self, name):
        all_names = [a.name for a in self.lookup]
        return hash_var(name) in all_names

    def process_variable(self, arg):
        #processes a variable by hashing and escaping when needed
        if self.is_variable(arg):
            return hash_var(arg)
        elif ConvertToPython.is_quoted(arg): #sometimes kids accidentally quote strings, then we do not want them quoted again
            return f"{arg}"
        else:
            return f"'{arg}'"

    def process_variable_for_fstring(self, name):
        if self.is_variable(name):
            return "{" + hash_var(name) + "}"
        else:
            return name

    def process_variable_for_fstring_padded(self, name):
        # used to transform variables in comparisons
        if self.is_variable(name):
            return f"str({hash_var(name)}).zfill(100)"
        elif ConvertToPython.is_float(name):
            return f"str({name}).zfill(100)"
        elif ConvertToPython.is_quoted(name):
            return f"{name}.zfill(100)"
        else:
            raise hedy.exceptions.UndefinedVarException(name)

    def make_f_string(self, args):
        argument_string = ''
        for argument in args:
            if self.is_variable(argument):
                # variables are placed in {} in the f string
                argument_string += "{" + hash_var(argument) + "}"
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

    def check_var_usage(self, args):
        # this function checks whether arguments are valid
        # we can proceed if all arguments are either quoted OR all variables

        args_to_process = [a for a in args if not isinstance(a, Tree)]#we do not check trees (calcs) they are always ok

        unquoted_args = [a for a in args_to_process if not ConvertToPython.is_quoted(a)]
        unquoted_in_lookup = [self.is_variable(a) for a in unquoted_args]

        if unquoted_in_lookup == [] or all(unquoted_in_lookup):
            # all good? return for further processing
            return args
        else:
            # return first name with issue
            # note this is where issue #832 can be addressed by checking whether
            # first_unquoted_var ius similar to something in the lookup list
            first_unquoted_var = unquoted_args[0]
            raise exceptions.UndefinedVarException(name=first_unquoted_var)

    # static methods
    @staticmethod
    def is_quoted(s):
        return (s[0] == "'" and s[-1] == "'") or (s[0] == '"' and s[-1] == '"')

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
    def indent(s):
        lines = s.split('\n')
        return '\n'.join(['  ' + l for l in lines])



@hedy_transpiler(level=1)
class ConvertToPython_1(ConvertToPython):

    def __init__(self, punctuation_symbols, lookup):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup
        __class__.level = 1

    def program(self, args):
        return '\n'.join([str(c) for c in args])
    def command(self, args):
        return args[0]

    def text(self, args):
        return ''.join([str(c) for c in args])

    def integer(self, args):
        return str(args[0])

    def number(self, args):
        return str(args[0])

    def NEGATIVE_NUMBER(self, args):
        return str(args[0])

    def print(self, args):
        # escape needed characters
        argument = process_characters_needing_escape(args[0])
        return "print('" + argument + "')"

    def ask(self, args):
        argument = process_characters_needing_escape(args[0])
        return "answer = input('" + argument + "')"

    def echo(self, args):
        if len(args) == 0:
            return "print(answer)" #no arguments, just print answer

        argument = process_characters_needing_escape(args[0])
        return "print('" + argument + " '+answer)"

    def comment(self, args):
        return f"#{''.join(args)}"

    def forward(self, args):
        if len(args) == 0:
            return sleep_after('t.forward(50)', False)
        return self.make_forward(int(args[0]))

    def turn(self, args):
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
        return self.make_turtle_command(parameter, Command.turn, 'right', False)

    def make_forward(self, parameter):
        return self.make_turtle_command(parameter, Command.forward, 'forward', True)

    def make_turtle_command(self, parameter, command, command_text, add_sleep):
        variable = self.get_fresh_var('trtl')
        transpiled = textwrap.dedent(f"""\
            {variable} = {parameter}
            try:
              {variable} = int({variable})
            except ValueError:
              raise Exception(f'While running your program the command {style_closest_command(command)} received the value {style_closest_command('{'+variable+'}')} which is not allowed. Try changing the value to a number.')
            t.{command_text}(min(600, {variable}) if {variable} > 0 else max(-600, {variable}))""")
        if add_sleep:
            return sleep_after(transpiled, False)
        return transpiled



@hedy_transpiler(level=2)
class ConvertToPython_2(ConvertToPython_1):

    def error_ask_dep_2(self, args):
        # ask is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1, 'ask', "ask_needs_var")
    def error_echo_dep_2(self, args):
        # echo is no longer usable this way, raise!
        # ask_needs_var is an entry in lang.yaml in texts where we can add extra info on this error
        raise hedy.exceptions.WrongLevelException(1,  'echo', "echo_out")

    def turn(self, args):
        if len(args) == 0:
            return "t.right(90)"  # no arguments defaults to a right turn
        arg = args[0]
        if self.is_variable(arg):
            return self.make_turn(hash_var(arg))
        if arg.lstrip("-").isnumeric():
            return self.make_turn(arg)

    def punctuation(self, args):
        return ''.join([str(c) for c in args])
    def var(self, args):
        name = args[0]
        self.check_var_usage(args)
        return hash_var(name)
    def var_access(self, args):
        name = args[0]
        return hash_var(name)
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

            argument_string += self.process_variable_for_fstring(argument) + space

            i = i + 1

        return f"print(f'{argument_string}')"

    def ask(self, args):
        var = args[0]
        all_parameters = ["'" + process_characters_needing_escape(a) + "'" for a in args[1:]]
        return f'{var} = input(' + '+'.join(all_parameters) + ")"

    def forward(self, args):
        if len(args) == 0:
            return sleep_after('t.forward(50)', False)

        if ConvertToPython.is_int(args[0]):
            parameter = int(args[0])
        else:
            # if not an int, then it is a variable
            parameter = args[0]

        return self.make_forward(parameter)

    def assign(self, args):
        parameter = args[0]
        value = args[1]
        if self.is_random(value):
            return parameter + " = " + value
        else:
            if self.is_variable(value):
                value = self.process_variable(value)
                return parameter + " = " + value
            else:
                # if the assigned value is not a variable and contains single quotes, escape them
                value = process_characters_needing_escape(value)
                return parameter + " = '" + value + "'"


    def sleep(self, args):
        if args == []:
            return "time.sleep(1)"
        else:
            return f"time.sleep({args[0]})"


@hedy_transpiler(level=3)
class ConvertToPython_3(ConvertToPython_2):
    def assign_list(self, args):
        parameter = args[0]
        values = ["'" + a.replace("'", "\\'") + "'" for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

    def list_access(self, args):
        args = [hash_var(a) for a in args]

        # check the arguments (except when they are random or numbers, that is not quoted nor a var but is allowed)
        self.check_var_usage(a for a in args if a != 'random' and not a.isnumeric())


        if args[1] == 'random':
            return 'random.choice(' + args[0] + ')'
        else:
            return args[0] + '[' + args[1] + '-1]'

    def add(self, args):
        var = self.process_variable(args[0])
        list = args[1]
        return f"{list}.append({var})"
    def remove(self, args):
        var = self.process_variable(args[0])
        list = args[1]
        return textwrap.dedent(f"""\
        try:
            {list}.remove({var})
        except:
           pass""")


#TODO: punctuation chars not be needed for level2 and up anymore, could be removed
@hedy_transpiler(level=4)
class ConvertToPython_4(ConvertToPython_3):

    def var_access(self, args):
        name = args[0]
        return hash_var(name)

    def print_ask_args(self, args):
        args = self.check_var_usage(args)
        result = ''
        for argument in args:
            argument = self.process_variable_for_fstring(argument)
            argument = argument.replace("'", '').replace('"', '')  # no quotes needed in fstring
            result += argument
        return result

    def print(self, args):
        argument_string = self.print_ask_args(args)
        return f"print(f'{argument_string}')"

    def ask(self, args):
        var = args[0]
        argument_string = self.print_ask_args(args[1:])
        return f"{var} = input(f'{argument_string}')"

    def error_print_nq(self, args):
        return ConvertToPython_2.print(self, args)


@hedy_transpiler(level=5)
class ConvertToPython_5(ConvertToPython_4):
    def list_access_var(self, args):
        var = hash_var(args[0])
        if args[2].data == 'random':
            return var + ' = random.choice(' + args[1] + ')'
        else:
            return var + ' = ' + args[1] + '[' + args[2].children[0] + '-1]'

    def ifs(self, args):
        return f"""if {args[0]}:
{ConvertToPython.indent(args[1])}"""

    def ifelse(self, args):
        return f"""if {args[0]}:
{ConvertToPython.indent(args[1])}
else:
{ConvertToPython.indent(args[2])}"""

    def condition(self, args):
        return ' and '.join(args)

    def condition_spaces(self, args):
        result = args[0] + " == '" + ' '.join(args[1:]) + "'"
        return result


    def equality_check(self, args):
        arg0 = self.process_variable(args[0])
        remaining_text = ' '.join(args[1:])
        arg1 = self.process_variable(remaining_text)
        return f"{arg0} == {arg1}"
        #TODO, FH 2021: zelfde change moet ik ook nog ff maken voor equal. check in hogere levels

    def in_list_check(self, args):
        arg0 = self.process_variable(args[0])
        arg1 = self.process_variable(args[1])
        return f"{arg0} in {arg1}"

@hedy_transpiler(level=6)
class ConvertToPython_6(ConvertToPython_5):

    def print_ask_args(self, args):
        # we only check non-Tree (= non calculation) arguments
        self.check_var_usage(args)

        #force all to be printed as strings (since there can not be int arguments)
        args_new = []
        for a in args:
            if isinstance(a, Tree):
                args_new.append("{" + a.children[0] + "}")
            else:
                a = a.replace("'", "").replace('"', '')  # no quotes needed in fstring
                args_new.append(self.process_variable_for_fstring(a))

        return ''.join(args_new)

    def equality_check(self, args):
        arg0 = self.process_variable(args[0])
        remaining_text = ' '.join(args[1:])
        arg1 = self.process_variable(remaining_text)

        return f"str({arg0}) == str({arg1})"

    def assign(self, args):
        parameter = args[0]
        value = args[1]
        if type(value) is Tree:
            return parameter + " = " + value.children[0]
        else:
            if self.is_variable(value):
                value = self.process_variable(value)
                return parameter + " = " + value
            else:
                # if the assigned value is not a variable and contains single quotes, escape them
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

        args = [self.process_token_or_tree(a) for a in args]
        return Tree('sum', [f'{args[0]} {operator} {args[1]}'])

    def addition(self, args):
        return self.process_calculation(args, '+')

    def subtraction(self, args):
        return self.process_calculation(args, '-')

    def multiplication(self, args):
        return self.process_calculation(args, '*')

    def division(self, args):
        return self.process_calculation(args, '//')

def sleep_after(commands, indent=True):
    lines = commands.split()
    if lines[-1] == "time.sleep(0.1)": #we don't sleep double so skip if final line is a sleep already
        return commands

    sleep_command = "time.sleep(0.1)" if indent is False else "  time.sleep(0.1)"
    return commands + "\n" + sleep_command

@hedy_transpiler(level=7)
class ConvertToPython_7(ConvertToPython_6):
    def repeat(self, args):
        var_name = self.get_fresh_var('i')
        times = self.process_variable(args[0])
        command = args[1]
        # in level 7, repeats can only have 1 line as their arguments
        command = sleep_after(command, False)
        return f"""for {var_name} in range(int({str(times)})):
{ConvertToPython.indent(command)}"""

@hedy_transpiler(level=8)
@hedy_transpiler(level=9)
class ConvertToPython_8_9(ConvertToPython_7):
    def __init__(self, punctuation_symbols, lookup):
        self.punctuation_symbols = punctuation_symbols
        self.lookup = lookup

    def command(self, args):
        return "".join(args)

    def repeat(self, args):
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        body = "\n".join(all_lines)
        body = sleep_after(body)

        return "for i in range(int(" + str(args[0]) + ")):\n" + body

    def ifs(self, args):
        args = [a for a in args if a != ""] # filter out in|dedent tokens

        all_lines = [ConvertToPython.indent(x) for x in args[1:]]

        return "if " + args[0] + ":\n" + "\n".join(all_lines)

    def elses(self, args):
        args = [a for a in args if a != ""] # filter out in|dedent tokens

        all_lines = [ConvertToPython.indent(x) for x in args]

        return "\nelse:\n" + "\n".join(all_lines)

    def var_access(self, args):
        if len(args) == 1: #accessing a var
            return hash_var(args[0])
        else:
        # this is list_access
            return hash_var(args[0]) + "[" + str(hash_var(args[1])) + "]" if type(args[1]) is not Tree else "random.choice(" + str(hash_var(args[0])) + ")"

@hedy_transpiler(level=10)
class ConvertToPython_10(ConvertToPython_8_9):
    def for_list(self, args):
      args = [a for a in args if a != ""]  # filter out in|dedent tokens

      body = "\n".join([ConvertToPython.indent(x) for x in args[2:]])

      body = sleep_after(body, True)

      return f"for {args[0]} in {args[1]}:\n{body}"

@hedy_transpiler(level=11)
class ConvertToPython_11(ConvertToPython_10):
    def for_loop(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        iterator = hash_var(args[0])
        body = "\n".join([ConvertToPython.indent(x) for x in args[3:]])
        body = sleep_after(body)
        stepvar_name = self.get_fresh_var('step')
        return f"""{stepvar_name} = 1 if int({args[1]}) < int({args[2]}) else -1
for {iterator} in range(int({args[1]}), int({args[2]}) + {stepvar_name}, {stepvar_name}):
{body}"""




@hedy_transpiler(level=12)
class ConvertToPython_12(ConvertToPython_11):
    def number(self, args):
        return ''.join(args)

    def NEGATIVE_NUMBER(self, args):
        return ''.join(args)

    def text_in_quotes(self, args):
        # We need to re-add the quotes, so that the Python code becomes name = 'Jan'
        # Even though the quotes could be single or double, we could always use the same ones here
        text = args[0]
        return "'" + text + "'"

    def process_token_or_tree(self, argument):
        if isinstance(argument, Tree):
            return f'{str(argument.children[0])}'
        else:
            # If the string is quoted, we have to use " instead of ' to avoid f-str illegal syntax
            if "'" in argument:  # Check only for single quotes because text_in_quotes re-adds single quotes only
                return '"' + argument.replace("'", '').replace('"', '') + '"'
            return f'{argument}'

    def ask(self, args):
        var = args[0]
        assign = super().ask(args)

        return textwrap.dedent(f"""\
        {assign}
        try:
          {var} = int({var})
        except ValueError:
          try:
            {var} = float({var})
          except ValueError:
            pass""")  # no number? leave as string

    def assign_list(self, args):
        parameter = args[0]
        values = args[1:]
        return parameter + " = [" + ", ".join(values) + "]"

    def assign(self, args):
        right_hand_side = args[1]
        left_hand_side = args[0]

        # we now need to check if the right hand side of te assign is
        # either a var or quoted, if it is not (and undefined var is raised)
        # the real issue is probably that the kid forgot quotes
        try:
            self.check_var_usage([right_hand_side]) #check_var_usage expects a list of arguments so place this one in a list.
        except exceptions.UndefinedVarException as E:
            # is the text a number? then no quotes are fine. if not, raise maar!

            if not (ConvertToPython.is_int(right_hand_side) or ConvertToPython.is_float(right_hand_side) or ConvertToPython.is_random(right_hand_side)):
                raise exceptions.UnquotedAssignTextException(text = args[1])

        if isinstance(right_hand_side, Tree):
            return left_hand_side + " = " + right_hand_side.children[0]
        else:
            # we no longer escape quotes here because they are now needed
            return left_hand_side + " = " + right_hand_side + ""

    def var(self, args):
        name = args[0]
        self.check_var_usage(args)
        return hash_var(name)

@hedy_transpiler(level=13)
class ConvertToPython_13(ConvertToPython_12):
    def andcondition(self, args):
        return ' and '.join(args)
    def orcondition(self, args):
        return ' or '.join(args)

@hedy_transpiler(level=14)
class ConvertToPython_14(ConvertToPython_13):
    def process_comparison(self, args, operator):

        # we are generating an fstring now
        arg0 = self.process_variable_for_fstring_padded(args[0])
        arg1 = self.process_variable_for_fstring_padded(args[1])

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

    def equality_check_dequals(self, args):
        return super().equality_check(args)

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

@hedy_transpiler(level=15)
class ConvertToPython_15(ConvertToPython_14):
    def while_loop(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        body = "\n".join(all_lines)
        body = sleep_after(body)
        return "while " + args[0] + ":\n" + body

@hedy_transpiler(level=16)
class ConvertToPython_16(ConvertToPython_15):
    def assign_list(self, args):
        parameter = args[0]
        values = [a for a in args[1:]]
        return parameter + " = [" + ", ".join(values) + "]"

    def change_list_item(self, args):
        return args[0] + '[' + args[1] + '-1] = ' + args[2]

@hedy_transpiler(level=17)
class ConvertToPython_17(ConvertToPython_16):
    def elifs(self, args):
        args = [a for a in args if a != ""]  # filter out in|dedent tokens
        all_lines = [ConvertToPython.indent(x) for x in args[1:]]
        return "\nelif " + args[0] + ":\n" + "\n".join(all_lines)

@hedy_transpiler(level=18)
class ConvertToPython_18(ConvertToPython_17):
    def input(self, args):
        return self.ask(args)

    def input_is(self, args):
        return self.input(args)

    def input_equals(self, args):
        return self.input(args)

    def input_empty_brackets(self, args):
        return self.input(args)
    
    def print_empty_brackets(self, args):
        return self.print(args)

def merge_grammars(grammar_text_1, grammar_text_2, level):
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
                if definition_1.strip() == definition_2.strip():
                    warn_message = f"The rule {name_1} is duplicated on level {level}. Please check!"
                    warnings.warn(warn_message)
                # Check if the rule is adding or substracting new rules                
                has_add_op  = definition_2.startswith('+=') 
                has_sub_op = has_add_op and '-='  in definition_2
                has_last_op = has_add_op and '>'  in definition_2
                if has_sub_op:
                    # Get the rules we need to substract
                    part_list = definition_2.split('-=')
                    add_list, sub_list =  (part_list[0], part_list[1]) if has_sub_op else (part_list[0], '')
                    add_list = add_list[3:]  
                    # Get the rules that need to be last
                    sub_list = sub_list.split('>')  
                    sub_list, last_list = (sub_list[0], sub_list[1]) if has_last_op  else (sub_list[0], '')
                    sub_list = sub_list + '|' + last_list
                    result_cmd_list = get_remaining_rules(definition_1, sub_list)
                elif has_add_op:
                     # Get the rules that need to be last
                    part_list = definition_2.split('>')
                    add_list, sub_list =  (part_list[0], part_list[1]) if has_last_op else (part_list[0], '')
                    add_list = add_list[3:]
                    last_list = sub_list
                    result_cmd_list = get_remaining_rules(definition_1, sub_list)
                else:
                    result_cmd_list = definition_1

                if has_last_op:
                    new_rule = f"{name_1}: {result_cmd_list} | {add_list} | {last_list}"
                elif has_add_op:
                    new_rule = f"{name_1}: {result_cmd_list} | {add_list}"
                else:
                    new_rule = line_2
                #Already procesed so remove it
                remaining_rules_grammar_2.remove(line_2)
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

def get_remaining_rules(orig_def, sub_def):
    orig_cmd_list     = [command.strip() for command in orig_def.split('|')]                    
    unwanted_cmd_list = [command.strip() for command in sub_def.split('|')]                    
    result_cmd_list   = [cmd for cmd in orig_cmd_list if cmd not in unwanted_cmd_list]                    
    result_cmd_list   = ' | '.join(result_cmd_list) # turn the result list into a string
    return result_cmd_list

def create_grammar(level, lang="en"):
    # start with creating the grammar for level 1
    result = get_full_grammar_for_level(1)
    keys = get_keywords_for_language(lang)
    result = merge_grammars(result, keys, 1)
    # then keep merging new grammars in
    for i in range(2, level+1):
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
    try:
        if not local_keywords_enabled:
            raise FileNotFoundError("Local keywords are not enabled")
        filename = "keywords-" + str(language) + ".lark"
        with open(path.join(script_dir, "grammars", filename), "r", encoding="utf-8") as file:
            grammar_text = file.read()
    except FileNotFoundError:
        filename = "keywords-en.lark"
        with open(path.join(script_dir, "grammars", filename), "r", encoding="utf-8") as file:
            grammar_text = file.read()
    return grammar_text

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
    ret = Lark(grammar, regex=True, propagate_positions=True, keep_all_tokens=keep_all_tokens) #ambiguity='explicit'
    PARSER_CACHE[key] = ret
    return ret

ParseResult = namedtuple('ParseResult', ['code', 'has_turtle'])

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

def needs_indentation(code):
    keywords_requiring_indentation = ['if', 'als', 'si', 'for', 'repeat', 'répète', 'repete', 'herhaal']
    # this is done a bit half-assed, clearly *parsing* the one line would be superior
    # because now a line like
    # repeat is 5 would also require indentation!
    all_words = code.split()
    if len(all_words) == 0:
        return False

    first_keyword = all_words[0]
    return first_keyword in keywords_requiring_indentation



def preprocess_blocks(code, level):
    processed_code = []
    lines = code.split("\n")
    current_number_of_indents = 0
    previous_number_of_indents = 0
    indent_size = 4 # set at 4 for now
    indent_size_adapted = False
    line_number = 0
    next_line_needs_indentation = False
    for line in lines:
        leading_spaces = find_indent_length(line)

        line_number += 1

        # first encounter sets indent size for this program
        if indent_size_adapted == False and leading_spaces > 0:
            indent_size = leading_spaces
            indent_size_adapted = True

        # ignore whitespace-only lines
        if leading_spaces == len(line):
            continue

        #calculate nuber of indents if possible
        if indent_size != None:
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

            current_number_of_indents = leading_spaces // indent_size
            if current_number_of_indents > 1 and level == hedy.LEVEL_STARTING_INDENTATION:
                raise hedy.exceptions.LockedLanguageFeatureException(concept="nested blocks")

        if next_line_needs_indentation and current_number_of_indents <= previous_number_of_indents:
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            raise hedy.exceptions.NoIndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                                         indent_size=indent_size, fixed_code=fixed_code)

        if needs_indentation(line):
            next_line_needs_indentation = True
        else:
            next_line_needs_indentation = False

        if current_number_of_indents - previous_number_of_indents > 1:
            fixed_code = program_repair.fix_indent(code, line_number, leading_spaces, indent_size)
            raise hedy.exceptions.IndentationException(line_number=line_number, leading_spaces=leading_spaces,
                                            indent_size=indent_size, fixed_code=fixed_code)



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

    # In level 8 we add indent-dedent blocks to the code before parsing
    if level >= hedy.LEVEL_STARTING_INDENTATION:
        result = preprocess_blocks(result, level)

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
            characters_expected = str(e.allowed) #not yet in use, could be used in the future (when our parser rules are better organize, now it says ANON*__12 etc way too often!)
            character_found = beautify_parse_error(e.char)
            # print(e.args[0])
            # print(location, character_found, characters_expected)
            fixed_code = program_repair.remove_unexpected_char(input_string, location[0], location[1])
            raise exceptions.ParseException(level=level, location=location, found=character_found, fixed_code=fixed_code) from e
        except UnexpectedEOF:
            # this one can't be beautified (for now), so give up :)
            raise e


def is_program_valid(program_root, input_string, level, lang):
    # IsValid returns (True,) or (False, args)
    instance = IsValid()
    instance.level = level # TODO: could be done in a constructor once we are sure we will go this way
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
            if fixed_code != input_string: #only if we have made a successful fix
                try:
                    fixed_result = transpile_inner(fixed_code, level, lang)
                    result = fixed_result
                    raise exceptions.InvalidSpaceException(level=level, line_number=line, fixed_code=fixed_code, fixed_result=result)
                except exceptions.HedyException:
                    invalid_info.error_type = None
                    transpile_inner(fixed_code, level)
                    # The fixed code contains another error. Only report the original error for now.
                    pass
            raise exceptions.InvalidSpaceException(level=level, line_number=line, fixed_code=fixed_code, fixed_result=result)
        elif invalid_info.error_type == 'print without quotes':
            # grammar rule is agnostic of line number so we can't easily return that here
            raise exceptions.UnquotedTextException(level=level)
        elif invalid_info.error_type == 'empty program':
            raise exceptions.EmptyProgramException()
        elif invalid_info.error_type == 'unsupported number':
            raise exceptions.UnsupportedFloatException(value=''.join(invalid_info.arguments))
        else:
            invalid_command = invalid_info.command
            closest = closest_command(invalid_command, get_suggestions_for_language(lang, level))

            if closest == 'keyword':  # we couldn't find a suggestion
                if invalid_command == Command.turn:
                    arg = ''.join(invalid_info.arguments).strip()
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

        lookup_table = create_lookup_table(abstract_syntax_tree, level, lang, input_string)

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