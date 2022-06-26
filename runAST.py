import sys
from lark import Lark
from lark.exceptions import VisitError, LarkError, UnexpectedEOF
from lark import Tree, Transformer, Visitor
from lark.indenter import Indenter
import hedy
import converter_ASTtransformer as ASTtransformer
import converter_unparser as unparser

def parser(input_string, level, keep_all_tokens = False, lang = "en"):
    input_string = hedy.process_input_string(input_string, level)
    parser = hedy.get_parser(level, keep_all_tokens = keep_all_tokens, lang = lang)
#    print(parser.parse(input_string+ '\n').pretty())
    return parser.parse(input_string+ '\n')

def printHelp():
    print("Usage: python hedy.py [--help] <filename> [--level <level (1-8)>]\n\nTo specify a level, add #level <level> to the top of your file or use the --level <level> argument.")
    sys.exit(1)

def unparser_tester(input, level, lang = "en"):
    AST = parser(input,level, keep_all_tokens = True, lang=lang)
    if not valid_and_complete(input, level, lang=lang): return input
    unparsed = unparser.execute(AST, level, keep_all_tokens = True, lang=lang)
    print(unparsed[0:-1])
    return unparsed[0:-1]

def complete_tester(input, level):
    AST = parser(input,level, keep_all_tokens = True)
    if level < 18: AST = ASTtransformer.execute(AST, level)
    print(AST)
    unparsed = unparser.execute(AST, level+1, keep_all_tokens = True)
    print(unparsed)
    return unparsed

def valid_and_complete(program, level, lang="en"):
    AST = parser(program,level, lang)
    try:
        hedy.is_program_valid(AST, program, level, lang)
        hedy.is_program_complete(AST, level)
    except:
        return False
    return True

def converter(program, level, lang="en"):
    No_Changes = [2, 4, 5, 6, 8, 9, 10, 12, 13, 14]

    #is the input program valid and complete
    if not valid_and_complete(program, level, lang="en"): return ""
    if level in No_Changes: return program

    #Parse
    AST = parser(program,level, keep_all_tokens = True)

    #Transform
    if level < 18: AST = ASTtransformer.execute(AST, level)
    else: print("level too high to Transform")

    #Unparse
    unparsed = unparser.execute(AST, level+1, keep_all_tokens = True)

    #is the output program valid and complete
    if not valid_and_complete(unparsed, level+1, lang="en"): return ""
    return unparsed

def main():
    # python3 hedy.py <filename(0)> [levelargument(1)] [level(2)]

    args = sys.argv[1:]
    args_length = len(args)

    if args_length == 0 or args[0] == "-h" or args[0] == "--help":
        printHelp()

    level = 0 # Set level to 0 by default so we can check later if the level already has been set
    filename = args[0] # Set filename to args[0]

    if not args_length == 1:
        if args_length == 3:
            if args[1] == "--level" or args[1] == "-l":
                try:
                    level = int(args[2])
                    if level > 18:
                        print("Level has been set to 8, because the value specified was to high")
                        level = 18
                except ValueError:
                    print("Level argument is not an integer, skipping argument.")

    lines = ""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if level == 0:
        if lines[0].lower().startswith('#level'):
            parts = lines[0].split(' ')
            if len(parts) >= 2:
                level = int(parts[1])
                if level > 18:
                    print("Level has been set to 8, because the value specified was to high")
                    level = 18

    program = ''.join([line
        for line in lines
        if not line.startswith('#')])

#    result = converter(program, level)
#    print(result[0:-1])
    AST = parser(program,level, keep_all_tokens = True)
    print(AST)
    unparsed = unparser.execute(AST, level, keep_all_tokens = True)
    print(unparsed)
    #Test
    #print("Converting...")
    #python = hedy.transpile_inner(unparsed, level)
    #print("Conversion result:")
    #print(python.code)
    #print("Running code:")
    #exec(python.code)

if __name__ == '__main__':
    main()
