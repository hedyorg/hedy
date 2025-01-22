from collections import namedtuple, defaultdict
from lark import Token, Transformer, v_args
from lark.exceptions import VisitError
import hedy
from os import path
import hedy_content
from website.yaml_file import YamlFile
import copy
import re

# Holds the token that needs to be translated, its line number, start and
# end indexes and its value (e.g. ", ").
Rule = namedtuple("Rule", "keyword line start end value")


def keywords_to_dict(lang="nl"):
    """ "Return a dictionary of keywords from language of choice. Key is english value is lang of choice"""
    base = path.abspath(path.dirname(__file__))

    keywords_path = "content/keywords/"
    yaml_filesname_with_path = path.join(base, keywords_path, lang + ".yaml")

    # as we mutate this dict, we have to make a copy
    # as YamlFile re-uses the yaml contents
    command_combinations = copy.deepcopy(
        YamlFile.for_file(yaml_filesname_with_path).to_dict()
    )
    for k, v in command_combinations.items():
        words = v.split("|")
        # Sort the keywords by length descending. This is important for the substitution logic later
        command_combinations[k] = list(sorted(words, key=len, reverse=True))

    return command_combinations


def keywords_to_dict_single_choice(lang):
    command_combinations = keywords_to_dict(lang)
    return {k: v[0] for (k, v) in command_combinations.items()}


def all_keywords_to_dict():
    """Return a dictionary where each value is a list of the translations of that keyword (key). Used for testing"""
    keyword_dict = {}
    for lang in hedy_content.ALL_KEYWORD_LANGUAGES:
        commands = keywords_to_dict_single_choice(lang)
        keyword_dict[lang] = commands

    all_translations = {k: [v.get(k, k) for v in keyword_dict.values()] for k in keyword_dict["en"]}
    return all_translations


def translate_keyword_from_en(keyword, lang="en"):
    # translated the keyword to a local lang
    local_keywords = keywords_to_dict(lang)
    if keyword in local_keywords.keys():
        local_keyword = local_keywords[keyword][0]
    else:
        local_keyword = keyword
    return local_keyword


def translate_keyword_to_en(keyword, lang):
    # translated the keyword to from a local lang
    original_keywords = keywords_to_dict(lang)
    for k, v in original_keywords.items():
        if keyword in v:
            return k
    return keyword


def get_target_keyword(keyword_dict, keyword):
    if keyword in keyword_dict.keys():
        return keyword_dict[keyword][0]
    else:
        return keyword


MATCH_EDGE_WHITESPACE = re.compile(r'^(\s*).+?(\s*)$')

def make_keyword_string_with_whitespace(matched_substring: str, new_keyword: str):
    """Make a new keyword string based on the matched substring.

    We retain all whitespace characters at the edge of the source string.
    """
    return MATCH_EDGE_WHITESPACE.sub(f'\\1{new_keyword}\\2', matched_substring)


def translate_keywords(input_string, from_lang="en", to_lang="nl", level=1):
    """ "Return code with keywords translated to language of choice in level of choice"""

    if input_string == "":
        return ""

    # remove leading spaces.
    # FH, dec 23. This creates a bit of a different version of translation but that seems ok to me
    # putting it back in seems overkill
    input_string = input_string.lstrip()

    try:
        processed_input = hedy.process_input_string(input_string, level, from_lang, preprocess_ifs_enabled=False)

        hedy.source_map.clear()
        hedy.source_map.set_skip_faulty(False)

        parser = hedy.get_parser(level, from_lang, True, hedy.source_map.skip_faulty)
        keyword_dict_from = keywords_to_dict(from_lang)
        keyword_dict_to = keywords_to_dict(to_lang)

        program_root = parser.parse(processed_input + "\n").children[0]

        translator = Translator(processed_input)
        translator.transform(program_root)

        # Build a list of textual substitutions, one per line
        # { line -> [(start, end, replacement)] }
        substitutions = defaultdict(list)

        lines = processed_input.splitlines()
        for rule in translator.rules:
            if rule.keyword in keyword_dict_from and rule.keyword in keyword_dict_to:
                # Sometimes the rule matches just a keyword, sometimes it matches a keyword
                # with spaces.
                line0 = rule.line - 1
                source_substring = lines[line0][rule.start:rule.end + 1]
                replaced_substring = make_keyword_string_with_whitespace(source_substring, get_target_keyword(keyword_dict_to, rule.keyword))

                substitutions[line0].append((rule.start, rule.end + 1, replaced_substring))

        # Do the actual replacements, taking care to do them back-to-front
        for line0, subs in sorted(substitutions.items(), reverse=True):
            for start, end, replacement in sorted(subs, reverse=True):
                lines[line0] = lines[line0][:start] + replacement + lines[line0][end:]

        result = "\n".join(lines)
        result = result.replace("#ENDBLOCK", "")

        # we have to reverse escaping or translating and retranslating will add an unlimited number of slashes
        if level >= 4:
            result = result.replace("\\\\", "\\")

        return result
    except VisitError as E:
        if isinstance(E, VisitError):
            # Exceptions raised inside visitors are wrapped inside VisitError. Unwrap it if it is a
            # HedyException to show the intended error message.
            if isinstance(E.orig_exc, hedy.exceptions.HedyException):
                raise E.orig_exc
            else:
                raise E
    except Exception as E:
        raise E


def replace_line(lines, index, line):
    before = "\n".join(lines[0:index])
    after = "\n".join(lines[index + 1:])
    if len(before) > 0:
        before = before + "\n"
    if len(after) > 0:
        after = "\n" + after
    return "".join([before, line, after])


def replace_token_in_line(line, rule, original, target):
    """Replaces a token in a line from the user input with its translated equivalent"""
    before = "" if rule.start == 0 else line[0: rule.start]
    after = "" if rule.end == len(line) - 1 else line[rule.end + 1:]
    # Note that we need to replace the target value in the original value because some
    # grammar rules have ambiguous length and value, e.g. _COMMA: _SPACES*
    # (latin_comma | arabic_comma) _SPACES*
    return before + rule.value.replace(original, target) + after


def find_command_keywords(
    input_string, lang, level, keywords, start_line, end_line, start_column, end_column
):
    parser = hedy.get_parser(level, lang, True, hedy.source_map.skip_faulty)
    program_root = parser.parse(input_string).children[0]

    translator = Translator(input_string)
    translator.transform(program_root)

    return {
        k: find_keyword_in_rules(
            translator.rules, k, start_line, end_line, start_column, end_column
        )
        for k in keywords
    }


def find_keyword_in_rules(rules, keyword, start_line, end_line, start_column, end_column):
    for rule in rules:
        if rule.keyword == keyword and rule.line == start_line and rule.start >= start_column:
            if rule.line < end_line or (rule.line == end_line and rule.end <= end_column):
                return rule.value
    return None


@v_args(tree=True)
class Translator(Transformer):
    """The translator finds tokens that must be translated and stores information about their exact position
    in the user input string and original value. The information is later used to replace the token in
    the original user input with the translated token value. Please note that it is a transformer
    instead of a visitor because we need tokens to be visited too."""

    def __init__(self, input_string):
        super().__init__()
        self.input_string = input_string
        self.rules = []

    def define(self, tree):
        self.add_rule_for_grammar_token("_DEFINE", "define", tree)

    def defs(self, tree):
        self.add_rule_for_grammar_token("_DEF", "def", tree)

    def call(self, tree):
        self.add_rule_for_grammar_token("_CALL", "call", tree)

    def withs(self, tree):
        self.add_rule_for_grammar_token("_WITH", "with", tree)

    def returns(self, tree):
        self.add_rule_for_grammar_token("_RETURN", "return", tree)

    def print(self, tree):
        self.add_rule_for_grammar_token("_PRINT", "print", tree)

    def print_empty_brackets(self, tree):
        self.print(tree)

    def ask(self, tree):
        self.add_rule_for_grammar_token("_IS", "is", tree)
        self.add_rule_for_grammar_token("_ASK", "ask", tree)

    def echo(self, tree):
        self.add_rule_for_grammar_token("_ECHO", "echo", tree)

    def color(self, tree):
        self.add_rule_for_grammar_token("_COLOR", "color", tree)

    def forward(self, tree):
        self.add_rule_for_grammar_token("_FORWARD", "forward", tree)

    def turn(self, tree):
        self.add_rule_for_grammar_token("_TURN", "turn", tree)

    def left(self, tree):
        self.add_rule_for_grammar_rule("left", tree)

    def right(self, tree):
        self.add_rule_for_grammar_rule("right", tree)

    def black(self, tree):
        self.add_rule_for_grammar_rule("black", tree)

    def blue(self, tree):
        self.add_rule_for_grammar_rule("blue", tree)

    def brown(self, tree):
        self.add_rule_for_grammar_rule("brown", tree)

    def gray(self, tree):
        self.add_rule_for_grammar_rule("gray", tree)

    def green(self, tree):
        self.add_rule_for_grammar_rule("green", tree)

    def orange(self, tree):
        self.add_rule_for_grammar_rule("orange", tree)

    def pink(self, tree):
        self.add_rule_for_grammar_rule("pink", tree)

    def yellow(self, tree):
        self.add_rule_for_grammar_rule("yellow", tree)

    def purple(self, tree):
        self.add_rule_for_grammar_rule("purple", tree)

    def white(self, tree):
        self.add_rule_for_grammar_rule("white", tree)

    def red(self, tree):
        self.add_rule_for_grammar_rule("red", tree)

    def clear(self, tree):
        self.add_rule_for_grammar_rule("clear", tree)

    def TRUE(self, token):
        name = 'True' if token and token[0].isupper() else 'true'
        rule = Rule(name, token.line, token.column - 1, token.end_column - 2, token)
        self.rules.append(rule)

    def FALSE(self, token):
        name = 'False' if token and token[0].isupper() else 'false'
        rule = Rule(name, token.line, token.column - 1, token.end_column - 2, token)
        self.rules.append(rule)

    def assign_list(self, tree):
        self.add_rule_for_grammar_token("_IS", "is", tree)
        commas = self.get_keyword_tokens("_COMMA", tree)
        for comma in commas:
            rule = Rule("comma", comma.line, comma.column - 1, comma.end_column - 2, comma.value)
            self.rules.append(rule)

    def assign(self, tree):
        self.add_rule_for_grammar_token("_IS", "is", tree)

    def sleep(self, tree):
        self.add_rule_for_grammar_token("_SLEEP", "sleep", tree)

    def add(self, tree):
        self.add_rule_for_grammar_token("_ADD_LIST", "add", tree)
        self.add_rule_for_grammar_token("_TO_LIST", "to_list", tree)

    def remove(self, tree):
        self.add_rule_for_grammar_token("_REMOVE", "remove", tree)
        self.add_rule_for_grammar_token("_FROM", "from", tree)

    def random(self, tree):
        self.add_rule_for_grammar_rule("random", tree)

    def error_ask_dep_2(self, tree):
        self.add_rule_for_grammar_token("_ASK", "ask", tree)

    def error_echo_dep_2(self, tree):
        self.add_rule_for_grammar_token("_ECHO", "echo", tree)

    def ifs(self, tree):
        self.add_rule_for_grammar_token("_IF", "if", tree)

    def ifelse(self, tree):
        self.add_rule_for_grammar_token("_IF", "if", tree)
        self.add_rule_for_grammar_token("_ELSE", "else", tree)

    def elifs(self, tree):
        self.add_rule_for_grammar_token("_ELIF", "elif", tree)

    def elses(self, tree):
        self.add_rule_for_grammar_token("_ELSE", "else", tree)

    def condition_spaces(self, tree):
        self.add_rule_for_grammar_token("_IS", "is", tree)

    def equality_check_is(self, tree):
        self.equality_check(tree)

    def equality_check(self, tree):
        self.add_rule_for_grammar_token("_IS", "is", tree)
        self.add_rule_for_grammar_token("_EQUALS", "=", tree)
        self.add_rule_for_grammar_token("_DOUBLE_EQUALS", "==", tree)

    def in_list_check(self, tree):
        self.add_rule_for_grammar_token("_IN", "in", tree)

    def list_access(self, tree):
        self.add_rule_for_grammar_token("_AT", "at", tree)

    def list_access_var(self, tree):
        self.add_rule_for_grammar_token("_IS", "is", tree)
        self.add_rule_for_grammar_token("_AT", "at", tree)

    def repeat(self, tree):
        self.add_rule_for_grammar_token("_REPEAT", "repeat", tree)
        self.add_rule_for_grammar_token("_TIMES", "times", tree)

    def for_list(self, tree):
        self.add_rule_for_grammar_token("_FOR", "for", tree)
        self.add_rule_for_grammar_token("_IN", "in", tree)

    def for_loop(self, tree):
        self.add_rule_for_grammar_token("_FOR", "for", tree)
        self.add_rule_for_grammar_token("_IN", "in", tree)
        self.add_rule_for_grammar_token("_RANGE", "range", tree)
        self.add_rule_for_grammar_token("_TO", "to", tree)

    def while_loop(self, tree):
        self.add_rule_for_grammar_token("_WHILE", "while", tree)

    def and_condition(self, tree):
        self.add_rule_for_grammar_token("_AND", "and", tree)

    def or_condition(self, tree):
        self.add_rule_for_grammar_token("_OR", "or", tree)

    def input(self, tree):
        self.add_rule_for_grammar_token("_IS", "is", tree)
        self.add_rule_for_grammar_token("_INPUT", "input", tree)

    def input_empty_brackets(self, tree):
        self.add_rule_for_grammar_token("_IS", "is", tree)
        self.add_rule_for_grammar_token("_INPUT", "input", tree)

    def pressed(self, tree):
        self.add_rule_for_grammar_token("_PRESSED", "pressed", tree)

    def add_rule_for_grammar_rule(self, rule_name, tree):
        """Creates a translation rule for a rule defined in the lark grammar which
        could have multiple children tokens, e.g. left, random, red"""
        # somehow for some Arabic rules (left, right, random) the parser returns separate tokens instead of one!
        token_start = tree.children[0]
        token_end = tree.children[-1]
        value = ''.join(tree.children)
        rule = Rule(rule_name, token_start.line, token_start.column - 1, token_end.end_column - 2, value)
        self.rules.append(rule)

    def add_rule_for_grammar_token(self, token_name, token_keyword, tree):
        """Creates a translation rule for a token defined in the lark grammar, e.g. _DEFINE, _FOR, _TURN"""
        token = self.get_keyword_token(token_name, tree)
        if token:
            rule = Rule(
                token_keyword, token.line, token.column - 1, token.end_column - 2, token.value
            )
            self.rules.append(rule)

    def get_keyword_token(self, token_type, node):
        for c in node.children:
            if type(c) is Token and c.type == token_type:
                return c
        return None

    def get_keyword_tokens(self, token_type, node):
        return [c for c in node.children if type(c) is Token and c.type == token_type]
