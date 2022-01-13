import textwrap
from os.path import dirname

from lark import Transformer, Tree
import hedy
import yaml
from os import path

TRANSLATOR_LOOKUP = {}

KEYWORD_LANGUAGES = ['en', 'nl', 'es']

def keywords_to_dict(to_lang="nl"):
    """"Return a dictionary of keywords from language of choice. Key is english value is lang of choice"""
    base = path.abspath(path.dirname(__file__))

    keywords_path = 'coursedata/keywords/'
    yaml_filesname_with_path = path.join(base, keywords_path, to_lang + '.yaml')

    with open(yaml_filesname_with_path, 'r') as stream:
        command_combinations = yaml.safe_load(stream)

    return command_combinations

def all_keywords_to_dict():
    """Return a dictionary where each key is a list of the translations of that keyword. Used for testing"""    
    keyword_list = []
    for lang in KEYWORD_LANGUAGES:
        commands = keywords_to_dict(lang)
        keyword_list.append(commands)
    all_translations = {k: [d[k] for d in keyword_list] for k in keyword_list[0]}
    return all_translations

def translate_keywords(input_string, from_lang="en", to_lang="nl", level=1):
    """"Return code with keywords translated to language of choice in level of choice"""
    punctuation_symbols = ['!', '?', '.']

    input_string = hedy.process_input_string(input_string, level)

    parser = hedy.get_parser(level, from_lang)
    keyword_dict = keywords_to_dict(to_lang)

    program_root = parser.parse(input_string + '\n').children[0]

    translated_program = TRANSLATOR_LOOKUP[level](keyword_dict, punctuation_symbols).transform(program_root)

    return translated_program


def hedy_translator(level):
    def decorating(c):
        TRANSLATOR_LOOKUP[level] = c
        c.level = level
        return c

    return decorating


def indent(s):
    new_indent = ""
    for line in s:
        lines = line.split('\n')
        new_indent += ''.join(['\n    ' + l for l in lines])
    return new_indent

@hedy_translator(level=1)
class ConvertToLang1(Transformer):

    def __init__(self, keywords, punctuation_symbols):
        self.keywords = keywords
        self.punctuation_symbols = punctuation_symbols
        __class__.level = 1

    def command(self, args):
        return args[0]

    def program(self, args):
        return '\n'.join([str(c) for c in args])

    def text(self, args):
        return ''.join([str(c) for c in args])

    def error_invalid_space(self, args):
        return " " + ''.join([str(c) for c in args])

    def print(self, args):
        return self.keywords["print"] + " " + "".join([str(c) for c in args])

    def echo(self, args):
        all_args = self.keywords["echo"]
        if args:
            all_args += " "
        return all_args + "".join([str(c) for c in args])

    def ask(self, args):
        return self.keywords["ask"] + " " + "".join([str(c) for c in args])

    def turn(self, args):
        return self.keywords["turn"] + " " + "".join([str(c) for c in args])

    def forward(self, args):
        return self.keywords["forward"] + " " + "".join([str(c) for c in args])

    def random(self, args):
        return self.keywords["random"] + "".join([str(c) for c in args])

    def error_invalid(self, args):
        return ' '.join([str(c) for c in args])

    def __default__(self, data, children, meta):
        return Tree(data, children, meta)


@hedy_translator(level=2)
class ConvertToLang2(ConvertToLang1):

    def assign(self, args):
        return args[0] + " " + self.keywords["is"] + " " + ''.join([str(c) for c in args[1:]])

    def print(self, args):

        argument_string = ""
        i = 0

        for argument in args:
            # final argument and punctuation arguments do not have to be separated with a space, other do
            if i == len(args) - 1 or args[i + 1] in self.punctuation_symbols:
                space = ''
            else:
                space = " "

            argument_string += argument + space

            i = i + 1

        return self.keywords["print"] + " " + argument_string

    def punctuation(self, args):
        return ''.join([str(c) for c in args])

    def var(self, args):
        var = args[0]
        all_parameters = ["'" + hedy.process_characters_needing_escape(a) + "'" for a in args[1:]]
        return var + ''.join(all_parameters)

    def ask(self, args):
        var = args[0]
        all_parameters = [hedy.process_characters_needing_escape(a) for a in args]

        return all_parameters[0] + " " + self.keywords["is"] + " " + self.keywords["ask"] + " " + ''.join(
            all_parameters[1:])

    def error_ask_dep_2(self, args):
        return self.keywords["ask"] + " " + ''.join([str(c) for c in args])

    def error_echo_dep_2(self, args):
        return self.keywords["echo"] + " " + ''.join([str(c) for c in args])


@hedy_translator(level=3)
class ConvertToLang3(ConvertToLang2):
    def ask(self, args):
        var = args[0]
        remaining_args = args[1:]
        return var + " " + self.keywords["is"] + " " + self.keywords["ask"] + " " + ''.join(remaining_args)

    def var_access(self, args):
        return ''.join([str(c) for c in args])

    def assign_list(self, args):
        return args[0] + " " + self.keywords["is"] + " " + ', '.join([str(c) for c in args[1:]])

    def list_access(self, args):
        return args[0] + " " + self.keywords["at"] + " " + ''.join([str(c) for c in args[1:]])


@hedy_translator(level=4)
class ConvertToLang4(ConvertToLang3):

    def print(self, args):
        i = 0
        #    self.check_args_type_allowed(args, 'print', self.level)
        argument_string = ""
        for argument in args:
            if i == len(args) or args[i] in self.punctuation_symbols:
                space = ''
            else:
                space = " "
            argument_string += space + argument
            i += 1
        return self.keywords["print"] + argument_string

    def print_nq(self, args):
        return ConvertToLang2.print(self, args)


@hedy_translator(level=5)
class ConvertToLang5(ConvertToLang4):
    def ifs(self, args):
        return self.keywords["if"] + " " + ''.join([str(c) for c in args])

    def ifelse(self, args):
        return self.keywords["if"] + " " + args[0] + args[1] + " " + self.keywords["else"] + " " + args[2]

    def condition(self, args):
        return ' and '.join(args)

    def equality_check(self, args):
        return args[0] + " " + self.keywords["is"] + " " + " ".join([str(c) for c in args[1:]]) + " "

    def in_list_check(self, args):
        return args[0] + " " + self.keywords["in"] + " " + ''.join([str(c) for c in args[1:]]) + " "


@hedy_translator(level=6)
class ConvertToLang6(ConvertToLang5):

    def addition(self, args):
        return args[0] + " + " + args[1]

    def subtraction(self, args):
        return args[0] + " - " + args[1]

    def multiplication(self, args):
        return args[0] + " * " + args[1]

    def division(self, args):
        return args[0] + " / " + args[1]

    def assign_equals(self, args):
        return args[0] + " = " + ''.join([str(c) for c in args[1:]])

    def assign_is(self, args):
        return args[0] + " "+ self.keywords["is"] + " " + ''.join([str(c) for c in args[1:]])

    def ask_equals(self, args):
        var = args[0]
        remaining_args = args[1:]
        return var + " = " + self.keywords["ask"] + " " + ''.join(remaining_args)

    def ask_is(self, args):
        var = args[0]
        remaining_args = args[1:]
        return var + " " + self.keywords["is"] + " " + self.keywords["ask"] + " " + ''.join(remaining_args)

    def assign_list_is(self, args):
        return args[0] + " " + self.keywords["is"] + " " + ', '.join([str(c) for c in args[1:]])
    
    def assign_list_equals(self, args):
        return args[0] + " " + " = " + " " + ', '.join([str(c) for c in args[1:]])

    def list_access_var_equals(self, args):
        var = args[0]
        var_list = args[1]
        return var + " = " + var_list + " " + self.keywords["at"] + " " + args[2]
    
    def list_access_var_is(self, args):
        var = args[0]
        var_list = args[1]
        return var + " " + self.keywords["is"] + " " + var_list + " " + self.keywords["at"]  + " " + args[2]
    
    def equality_check_is(self, args):
        return args[0] + " " + self.keywords["is"] + " " + " ".join([str(c) for c in args[1:]]) + " "

    def equality_check_equals(self, args):
        return args[0] + " = ".join([str(c) for c in args[1:]]) + " "

@hedy_translator(level=7)
class ConvertToLang7(ConvertToLang6):
    def repeat(self, args):
        return self.keywords["repeat"] + " " + args[0] + " " + self.keywords["times"] + " " + args[1]


@hedy_translator(level=8)
class ConvertToLang8(ConvertToLang7):
    def command(self, args):
        return '\n'.join([str(c) for c in args])

    def repeat(self, args):
        return self.keywords["repeat"] + " " + args[0] + " " + self.keywords["times"] + indent(args[1:])

    def ifs(self, args):
        return self.keywords["if"] + " " + args[0] + indent(args[1:])

    def elses(self, args):
        return self.keywords["else"] + indent(args[0:])

    def equality_check_is(self, args):
        return args[0] + " " + self.keywords["is"] + " " + " ".join([str(c) for c in args[1:]])

    def equality_check_equals(self, args):
        return args[0] + " = " + " ".join([str(c) for c in args[1:]])

    def end_block(self, args):
        return args


@hedy_translator(level=9)
@hedy_translator(level=10)
class ConvertToLang9_10(ConvertToLang8):

    def repeat_list(self, args):
        return self.keywords["for"] + " " + args[0] + " " + self.keywords["in"] + " " + args[1] + indent(args[2:])


@hedy_translator(level=11)
class ConvertToLang11(ConvertToLang9_10):
    def for_loop(self, args):
        return self.keywords["for"] + " " + args[0] + " " + self.keywords["in"] + " " + \
               self.keywords["range"] + " " + args[1] + " " + self.keywords["to"] + " " + args[2] + indent(args[3:])


@hedy_translator(level=12)
class ConvertToLang12(ConvertToLang11):

    def text_in_quotes(self, args):
        return ''.join(["'" + str(c) + "'" for c in args])


@hedy_translator(level=13)
class ConvertToLang13(ConvertToLang12):

    def andcondition(self, args):
        returnString = args[0]
        for arg in args[1:]:
            returnString += " " + self.keywords["and"] + " " + arg
        return returnString

    def orcondition(self, args):
        returnString = args[0]
        for arg in args[1:]:
            returnString += " " + self.keywords["or"] + " " + arg
        return returnString

    def in_list_check(self, args):
        return args[0] + " " + self.keywords["in"] + " " + ''.join([str(c) for c in args[1:]])


@hedy_translator(level=14)
class ConvertToLang14(ConvertToLang13):

    def equality_check_dequals(self, args):
       return args[0] + " == " + " ".join([str(c) for c in args[1:]])     

    def bigger(self, args):
        return args[0] + " > " + args[1]

    def smaller(self, args):
        return args[0] + " < " + args[1]

    def bigger_equal(self, args):
        return args[0] + " >= " + args[1]

    def smaller_equal(self, args):
        return args[0] + " <= " + args[1]

    def not_equal(self,args):
        return args[0] + " != " + args[1]


@hedy_translator(level=15)
class ConvertToLang15(ConvertToLang14):

    def while_loop(self, args):
        return self.keywords["while"] + " " + args[0] + indent(args[1:])


@hedy_translator(level=16)
class ConvertToLang16(ConvertToLang15):
    
    def assign_list_is(self, args):
        return args[0] + " " + self.keywords["is"] + " " + "[" + ', '.join([str(c) for c in args[1:]]) + "]"
    
    def assign_list_equals(self, args):
        return args[0] + " = [" + ', '.join([str(c) for c in args[1:]]) + "]"

    def list_access(self, args):
        return args[0] + "[" + ''.join([str(c) for c in args[1:]]) + "]"


@hedy_translator(level=17)
class ConvertToLang17(ConvertToLang16):

    def for_loop(self, args):
        return self.keywords["for"] + " " + args[0] + " " + self.keywords["in"] + " " + \
               self.keywords["range"] + " " + args[1] + " " + self.keywords["to"] + " " + args[2] + ":" + indent(args[3:])

    def while_loop(self, args):
        return self.keywords["while"] + " " + args[0] + ":" + indent(args[1:])

    def repeat_list(self, args):
        return self.keywords["for"] + " " + args[0] + " " + self.keywords["in"] + " " + args[1] + ":" + indent(args[2:])

    def ifs(self, args):
        return self.keywords["if"] + " " + args[0] + ":" + indent(args[1:])

    def elses(self, args):
        return self.keywords["else"] + ":" + indent(args[0:])

    def elifs(self, args):
        return self.keywords["elif"] + " " + args[0] + ":" + indent(args[1:])

@hedy_translator(level=18)
class ConvertToLang18(ConvertToLang17):

    def input(self, args):
        var = args[0]
        remaining_args = args[1:]
        return var + " " + self.keywords["is"] + " " + self.keywords["input"] + "(" + ''.join(remaining_args) + ")"

    def for_loop(self, args):
        return self.keywords["for"] + " " + args[0] + " " + self.keywords["in"] + " " + \
               f'{self.keywords["range"]}({args[1]},{args[2]})' + ":" + indent(args[3:])


    def print(self, args):
        argument_string = ''.join(args)
        return f'{self.keywords["print"]}({argument_string})'