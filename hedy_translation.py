from collections import namedtuple
from lark import Visitor, Token
import hedy
import operator
import yaml
from os import path
import hedy_content

KEYWORD_LANGUAGES = list(hedy_content.ALL_KEYWORD_LANGUAGES.keys())

# Holds the token that needs to be translated, its line number, start and end indexes and its value (e.g. ", ").
Rule = namedtuple("Rule", "keyword line start end value")


def keywords_to_dict(to_lang="nl"):
    """"Return a dictionary of keywords from language of choice. Key is english value is lang of choice"""
    base = path.abspath(path.dirname(__file__))

    keywords_path = 'coursedata/keywords/'
    yaml_filesname_with_path = path.join(base, keywords_path, to_lang + '.yaml')

    with open(yaml_filesname_with_path, 'r', encoding='UTF-8') as stream:
        command_combinations = yaml.safe_load(stream)

    return command_combinations


def all_keywords_to_dict():
    """Return a dictionary where each key is a list of the translations of that keyword. Used for testing"""    
    keyword_list = []
    for lang in KEYWORD_LANGUAGES:
        commands = keywords_to_dict(lang)
        keyword_list.append(commands)

    #gets the translation but defaults to the key k (in En) when it is not present
    all_translations = {k: [d.get(k, k) for d in keyword_list] for k in keyword_list[0]}
    return all_translations


def translate_keywords(input_string_, from_lang="en", to_lang="nl", level=1):
    """"Return code with keywords translated to language of choice in level of choice"""

    processed_input = hedy.process_input_string(input_string_, level)

    parser = hedy.get_parser(level, from_lang, True)
    keyword_dict_from = keywords_to_dict(from_lang)
    keyword_dict_to = keywords_to_dict(to_lang)

    program_root = parser.parse(processed_input + '\n').children[0]

    translator = Translator(processed_input)
    translator.visit(program_root)
    ordered_rules = reversed(sorted(translator.rules, key=operator.attrgetter("line", "start")))

    # FH Feb 2022 TODO trees containing invalid nodes are happily translated, should be stopped here!

    result = processed_input
    for rule in ordered_rules:
        if rule.keyword in keyword_dict_from and rule.keyword in keyword_dict_to:
            lines = result.splitlines()
            line = lines[rule.line-1]
            replaced_line = replace_token_in_line(line, rule, keyword_dict_from[rule.keyword], keyword_dict_to[rule.keyword])
            result = replace_line(lines, rule.line-1, replaced_line)

    # For now the needed post processing is only removing the 'end-block's added during pre-processing
    result = '\n'.join([line for line in result.splitlines() if not line.startswith('end-block')])

    return result


def replace_line(lines, index, line):
    before = '\n'.join(lines[0:index])
    after = '\n'.join(lines[index+1:])
    if len(before) > 0:
        before = before + '\n'
    if len(after) > 0:
        after = '\n' + after
    return ''.join([before, line, after])


def replace_token_in_line(line, rule, original, target):
    """Replaces a token in a line from the user input with its translated equivalent"""
    before = '' if rule.start == 0 else line[0:rule.start]
    after = '' if rule.end == len(line)-1 else line[rule.end+1:]
    # Note that we need to replace the target value in the original value because some
    # grammar rules have ambiguous length and value, e.g. _COMMA: _SPACES* (latin_comma | arabic_comma) _SPACES*
    return before + rule.value.replace(original, target) + after


def find_command_keywords(input_string, lang, level, keywords, start_line, end_line, start_column, end_column):
    parser = hedy.get_parser(level, lang, True)
    program_root = parser.parse(input_string).children[0]

    translator = Translator(input_string)
    translator.visit(program_root)

    return {k: find_keyword_in_rules(translator.rules, k, start_line, end_line, start_column, end_column) for k in keywords}


def find_keyword_in_rules(rules, keyword, start_line, end_line, start_column, end_column):
    for rule in rules:
        if rule.keyword == keyword and rule.line == start_line and rule.start >= start_column:
            if rule.line < end_line or (rule.line == end_line and rule.end <= end_column):
                return rule.value
    return None


class Translator(Visitor):
    """The visitor finds tokens that must be translated and stores information about their exact position
       in the user input string and original value. The information is later used to replace the token in
       the original user input with the translated token value."""

    def __init__(self, input_string):
        self.input_string = input_string
        self.rules = []

    def print(self, tree):
        self.add_rule('_PRINT', 'print', tree)

    def print_empty_brackets(self, tree):
        self.print(tree)

    def ask(self, tree):
        self.add_rule('_IS', 'is', tree)
        self.add_rule('_ASK', 'ask', tree)

    def echo(self, tree):
        self.add_rule('_ECHO', 'echo', tree)

    def forward(self, tree):
        self.add_rule('_FORWARD', 'forward', tree)

    def turn(self, tree):
        self.add_rule('_TURN', 'turn', tree)

    def left(self, tree):
        token = tree.children[0]
        rule = Rule('left', token.line, token.column - 1, token.end_column - 2, token.value)
        self.rules.append(rule)

    def right(self, tree):
        token = tree.children[0]
        rule = Rule('right', token.line, token.column - 1, token.end_column - 2, token.value)
        self.rules.append(rule)

    def assign_list(self, tree):
        self.add_rule('_IS', 'is', tree)
        commas = self.get_keyword_tokens('_COMMA', tree)
        for comma in commas:
            rule = Rule('comma', comma.line, comma.column - 1, comma.end_column - 2, comma.value)
            self.rules.append(rule)

    def assign(self, tree):
        self.add_rule('_IS', 'is', tree)

    def sleep(self, tree):
        self.add_rule('_SLEEP', 'sleep', tree)

    def add(self, tree):
        self.add_rule('_ADD_LIST', 'add', tree)
        self.add_rule('_TO_LIST', 'to_list', tree)

    def remove(self, tree):
        self.add_rule('_REMOVE', 'remove', tree)
        self.add_rule('_FROM', 'from', tree)

    def random(self, tree):
        token = tree.children[0]
        rule = Rule('random', token.line, token.column - 1, token.end_column - 2, token.value)
        self.rules.append(rule)

    def ifs(self, tree):
        self.add_rule('_IF', 'if', tree)

    def ifelse(self, tree):
        self.add_rule('_IF', 'if', tree)
        self.add_rule('_ELSE', 'else', tree)

    def elifs(self, tree):
        self.add_rule('_ELIF', 'elif', tree)

    def elses(self, tree):
        self.add_rule('_ELSE', 'else', tree)

    def condition_spaces(self, tree):
        self.add_rule('_IS', 'is', tree)

    def equality_check_is(self, tree):
        self.equality_check(tree)

    def equality_check(self, tree):
        self.add_rule('_IS', 'is', tree)
        self.add_rule('_EQUALS', '=', tree)
        self.add_rule('_DOUBLE_EQUALS', '==', tree)

    def in_list_check(self, tree):
        self.add_rule('_IN', 'in', tree)

    def list_access(self, tree):
        self.add_rule('_AT', 'at', tree)

    def list_access_var(self, tree):
        self.add_rule('_IS', 'is', tree)
        self.add_rule('_AT', 'at', tree)

    def repeat(self, tree):
        self.add_rule('_REPEAT', 'repeat', tree)
        self.add_rule('_TIMES', 'times', tree)

    def for_list(self, tree):
        self.add_rule('_FOR', 'for', tree)
        self.add_rule('_IN', 'in', tree)

    def for_loop(self, tree):
        self.add_rule('_FOR', 'for', tree)
        self.add_rule('_IN', 'in', tree)
        self.add_rule('_RANGE', 'range', tree)
        self.add_rule('_TO', 'to', tree)

    def while_loop(self, tree):
        self.add_rule('_WHILE', 'while', tree)

    def andcondition(self, tree):
        self.add_rule('_AND', 'and', tree)

    def orcondition(self, tree):
        self.add_rule('_OR', 'or', tree)

    def input(self, tree):
        self.add_rule('_IS', 'is', tree)
        self.add_rule('_INPUT', 'input', tree)

    def input_empty_brackets(self, tree):
        self.add_rule('_IS', 'is', tree)
        self.add_rule('_INPUT', 'input', tree)

    def add_rule(self, token_name, token_keyword, tree):
        token = self.get_keyword_token(token_name, tree)
        if token:
            rule = Rule(token_keyword, token.line, token.column - 1, token.end_column - 2, token.value)
            self.rules.append(rule)

    def get_keyword_token(self, token_type, node):
        for c in node.children:
            if type(c) is Token and c.type == token_type:
                return c
        return None

    def get_keyword_tokens(self, token_type, node):
        return [c for c in node.children if type(c) is Token and c.type == token_type]
