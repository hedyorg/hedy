from lark import Transformer, Tree
import hedy
import yaml 
import os 

TRANSPILER_LOOKUP = {}


def keywords_to_dict(to_lang="nl"):
    """"Return a dictionary of keywords from language of choice. Key is english value is lang of choice"""
    keywords_path = './coursedata/keywords/'
    yaml_filesname_with_path = os.path.join(keywords_path, to_lang + '.yaml')
    
    with open(yaml_filesname_with_path, 'r') as stream:
      command_combinations = yaml.safe_load(stream)

    return command_combinations

def translate_keywords(input_string, from_lang="nl", to_lang="nl", level=1):
    """"Return code with keywords translated to language of choice in level of choice"""
    parser = hedy.get_parser(level, from_lang)

    punctuation_symbols = ['!', '?', '.']

    keywordDict = keywords_to_dict(to_lang)
    program_root = parser.parse(input_string + '\n').children[0]
    abstract_syntaxtree = hedy.ExtractAST().transform(program_root)
    translator = TRANSPILER_LOOKUP[level]
    abstract_syntaxtree = translator(keywordDict, punctuation_symbols).transform(program_root)

    return abstract_syntaxtree


def hedy_translator(level):
    def decorating(c):
        TRANSPILER_LOOKUP[level] = c
        c.level = level
        return c

    return decorating


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

    def invalid_space(self, args):
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

    def invalid(self, args):
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
            # escape quotes if kids accidentally use them at level 2
            argument = hedy.process_characters_needing_escape(argument)

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

        return all_parameters[0] + " " + self.keywords["is"] + " " + self.keywords["ask"] + " " + ''.join(all_parameters[1:])

    def ask_dep_2(self, args):
        return self.keywords["ask"] + " " + ''.join([str(c) for c in args])

    def echo_dep_2(self, args):
        return self.keywords["echo"] + " " + ''.join([str(c) for c in args])
