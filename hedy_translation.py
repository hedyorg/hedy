from lark import Transformer, Tree
from hedy import get_keywords_for_language, ExtractAST, get_parser


TRANSPILER_LOOKUP = {}


def keywords_to_dict(to_lang="nl"):
    """"Return a dictionary of keywords from language of choice. Key is english value is lang of choice"""
    keywords = {}
    keywords_from = get_keywords_for_language("en").replace("\n\n", "\n").splitlines()

    keywords_to = get_keywords_for_language(to_lang).replace("\n\n", "\n").splitlines()
    keywords_from_withoutlvl = []
    for line in keywords_from:
        if line[0] != '/':
            keywords_from_withoutlvl.append(line)

    keywords_to_withoutlvl = []
    for line in keywords_to:
        if line[0] != '/':
            keywords_to_withoutlvl.append(line)

    for line in range(len(keywords_from_withoutlvl)):
        keywords[(keywords_from_withoutlvl[line].split('"'))[1]] = keywords_to_withoutlvl[line].split('"')[1]

    return keywords


def translate_keywords(input_string, from_lang="nl", to_lang="nl", level=1):
    """"Return code with keywords translated to language of choice in level of choice"""
    parser = get_parser(level, from_lang)

    punctuation_symbols = ['!', '?', '.']

    keywordDict = keywords_to_dict(to_lang)
    program_root = parser.parse(input_string + '\n').children[0]
    abstract_syntaxtree = ExtractAST().transform(program_root)
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
