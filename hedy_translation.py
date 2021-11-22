from lark import Transformer, Tree
import hedy


TRANSPILER_LOOKUP = {}


def keywords_to_dict(to_lang="nl"):
    """"Return a dictionary of keywords from language of choice. Key is english value is lang of choice"""
    keywords = {}
    keywords_from = hedy.get_keywords_for_language("en").replace("\n\n", "\n").splitlines()

    keywords_to = hedy.get_keywords_for_language(to_lang).replace("\n\n", "\n").splitlines()
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
        return self.keywords["ask"] + ''.join([str(c) for c in args])

    def assign_list(self, args):
        return args[0] + " " + self.keywords["is"] + " " + ', '.join([str(c) for c in args[1:]])

    def list_access(self, args):
        return args[0] + " " + self.keywords["at"] + " " + ''.join([str(c) for c in args[1:]])

@hedy_translator(level=3)
class ConvertToLang3(ConvertToLang2):

    def check_print_arguments(self, args):
        # this function checks whether arguments of a print are valid
        # we can print if all arguments are either quoted OR they are all variables

        quoted_args=[a for a in args if hedy.is_quoted(a)]
        unquoted_args = [a for a in args if not hedy.is_quoted(a)]
        unquoted_in_lookup = [hedy.is_variable(a, self.lookup) for a in unquoted_args]

        if unquoted_in_lookup == [] or all(unquoted_in_lookup):
            # all good? return for further processing
            return args
        else:
            # return first name with issue
            # note this is where issue #832 can be addressed by checking whether
            # first_unquoted_var ius similar to something in the lookup list
            first_unquoted_var = unquoted_args[0]
            raise hedy.exceptions.UndefinedVarException(name=first_unquoted_var)

    def print(self, args):
        i=0
   #    self.check_args_type_allowed(args, 'print', self.level)
        argument_string = ""
        for argument in args:
            if i==len(args) or args[i] in self.punctuation_symbols:
                space=''
            else:
                space=" "
            argument_string += space + argument
            i+=1
        return self.keywords["print"] + argument_string

    def print_nq(self, args):
        return ConvertToLang2.print(self, args)

    def ask(self, args):
        var = args[0]
        remaining_args = args[1:]
        return var + " " + self.keywords["is"] + " " + self.keywords["ask"] + " " + ''.join(remaining_args)

    def var_access(self, args):
        return ''.join([str(c) for c in args])

@hedy_translator(level=4)
class ConvertToLang4(ConvertToLang3):

    def ifs(self, args):
        return self.keywords["if"] + " " + ''.join([str(c) for c in args])

    def  ifelse(self, args):
        return self.keywords["else"] + " " + ''.join([str(c) for c in args])

    def condition(self, args):
        return ' and '.join(args)

    def equality_check(self, args):
        return args[0] + " " +  self.keywords["is"] + " " + " ".join([str(c) for c in args[1:]]) + " "

    def in_list_check(self, args):
        return args[0] + " " + self.keywords["in"] + " " + ''.join([str(c) for c in args[1:]]) + " "

@hedy_translator(level=5)
class ConvertToLang5(ConvertToLang4):

    def addition(self, args):
        return args[0] + " + " + args[1]

    def substraction(self, args):
        return args[0] + " - " + args[1]

    def multiplication(self, args):
        return args[0] + " * " + args[1]

    def division(self, args):
        return args[0] + " / " + args[1]

@hedy_translator(level=6)
class ConvertToLang6(ConvertToLang5):
    def repeat(self, args):
        return self.keywords["repeat"] + " " + args[0] + " " + self.keywords["times"] + " " + args[1]
    
    
translate_keywords("naam is papa, mama, oma\nif papa in naam print 'ho'", "en", "nl", level=4)
