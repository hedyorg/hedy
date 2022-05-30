import sys
from lark import Lark
from lark.exceptions import VisitError, LarkError, UnexpectedEOF
from lark import Tree, Transformer, Visitor
from lark.indenter import Indenter
import hedy
import converter_ASTtransformer as ASTtransformer
import converter_unparser as unparser

def parser(input_string, level):
    input_string = hedy.process_input_string(input_string, level)
    parser = hedy.get_parser(level)

#    if level >= 7:
#        input_string = hedy.preprocess_blocks(input_string, level)

    return parser.parse(input_string+ '\n')

def printHelp():
    print("Usage: python hedy.py [--help] <filename> [--level <level (1-8)>]\n\nTo specify a level, add #level <level> to the top of your file or use the --level <level> argument.")
    sys.exit(1)

def unparser_tester(input, level):
    AST = parser(input,level)
    return unparser.execute(AST, level)

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
                    if level > 16:
                        print("Level has been set to 8, because the value specified was to high")
                        level = 16
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
                if level > 16:
                    print("Level has been set to 8, because the value specified was to high")
                    level = 16

    program = '\n'.join([line
        for line in lines
        if not line.startswith('#')])

    #Parse
    print("Input:")
    print(program)
    print("Parsing...")
    AST = parser(program,level)
    print("Parser result:")
    print(AST.pretty())
    #Transform
    print("Transforming...")
    if level < 16:
        AST = ASTtransformer.execute(AST, level)
    #    print("Transformer result:")
    #    print(AST)
    #else:
    #    print("level too high to Transform")
    #Unparse
    print("Unparsing...")
    unparsed = unparser.execute(AST, level)
    #unparser.test_multi()
    print("Unparser result:")
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
