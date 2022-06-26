from lark import Lark
from lark.exceptions import VisitError, LarkError, UnexpectedEOF
from lark import Tree, Transformer, Visitor, Token
from lark.indenter import Indenter
import hedy
import sys
import converter_unparser as unparser

varlist = []

# Doel Transformer:
# Het transformeren van hedy code naar een nieuw level met zo min mogelijk
# moeite voor programmeurs van toekomstige levels.
# Droom: volledig automatisch
#        anders met strikte opstel eissen
#        worst case bestand met veranderingen tussen Grammars

def get_changes_in_grammar(level):
    #current grammar
    current = hedy.create_grammar(level)
    # Grammar additions
    next = hedy.get_additional_rules_for_level(level+1)
    result = []
    rules_current = current.split('\n')
    for cline in rules_current:
        if cline == '' or cline[0] == '/':
            continue
        parts = cline.split(':')
        cname, cdefinition = parts[0], ''.join(parts[1:])
        rules_next = next.split('\n')
        for nline in rules_next:
            if nline == '' or nline[0] == '/':
                continue
            parts = nline.split(':')
            nname, ndefinition = parts[0], ''.join(parts[1]) #why not 1:?
            if cname == nname:
                result.append(nline)
                break
    print("BEGIN CHANGES")
    for line in result:
        print(line)
    print("END CHANGES")
    return result

class transformer_level_1(Transformer):
    def echo(self,args):
        children = []
        for arg in args:
            if isinstance(arg, Token) and arg.type == '_ECHO' :
                children.append(Token('_PRINT', 'print '))
            else:
                children.append(arg)
        children.append(Token('_SPACE', ' '))
        children.append(Tree('text', [Token('__ANON_2', 'var')]))
        return Tree(Token('RULE', 'print'), children)

    def ask(self,args):
        children = []
        for arg in args:
            if isinstance(arg, Token) and arg.type == '_ASK':
                children.append(Tree(Token('RULE', 'var'), [Token('NAME', 'var')]))
                children.append(Token('_IS', ' is '))
                children.append(Token('_ASK', 'ask '))
            else:
                children.append(arg)
        return Tree(Token('RULE', 'ask'), children)

class transformer_level_3(Transformer):
    def var(self,args):
        for arg in args:
            if arg in varlist:
                return Tree(Token('RULE', 'var'), args)
            varlist.append(arg.value)
            return Tree(Token('RULE', 'var'), args)

    def text(self,args):
        for arg in args:
            if arg in varlist:
                return Tree(Token('RULE', 'var_access'), [Token('NAME', arg.value)])
        return Tree(Token('__ANON_1','text'), args)

    def print(self,args):
        children = [Token('_PRINT', 'print ')]
        temp = "'"
        for arg in args[1:]:
            if isinstance(arg, Tree) and (arg.data == "text" or arg.data == "punctuation"):
                temp = temp + self._contents_getter(arg.data, arg.children)
            elif isinstance(arg, Token):
                temp = temp + arg.value
            else:
                if temp != "'":
                    temp = temp+"' "
                    children.append(Tree('text',[Token('__ANON_1', temp)]))
                    temp = "'"
                children.append(arg)
        if temp != "'":
            temp = temp+"' "
            children.append(Tree('text',[Token('__ANON_1', temp)]))
        return Tree('print', children)

    def ask(self,args):
        children = []
        temp = "'"
        for arg in args[1:]:
            if isinstance(arg, Tree) and (arg.data == "text" or arg.data == "punctuation"):
                temp = temp + self._contents_getter(arg.data, arg.children)
            elif isinstance(arg, Token):
                temp = temp + arg.value
            else:
                if temp != "'":
                    temp = temp+"' "
                    children.append(Tree('text',[Token('__ANON_1', temp)]))
                    temp = "'"
                children.append(arg)
        if temp != "'":
            temp = temp+"' "
            children.append(Tree('text',[Token('__ANON_1', temp)]))
        return Tree('ask', children)

    def _contents_getter(self, name, args):
        return self._get_contents(args)

    def _get_contents(self, args):
        return ''.join([x for x in args])

class transformer_level_7(Transformer):
    def ifs (self, args):
        children = []
        grandchildren = []
        first = True

        for arg in args:
            if isinstance(arg, Token) and (arg.type == '_SPACE' or arg.type == '_EOL'):
                if first:
                    first = False
                    children.append(Token('_EOL', '\n'))
                    children.append(Token('_SPACE', '    '))
            else:
                if first: children.append(arg)
                else: grandchildren.append(arg)
        children.append(Tree(Token('RULE', 'command'), grandchildren))
        children.append(Token('_EOL', '\n'))
        children.append(Token('_END_BLOCK', 'end-block'))
        return Tree(Token('RULE', 'ifs'), children)

    def condition_spaces (self, args):
        return Tree(Token('RULE', 'condition'), [Tree(Token('RULE', 'equality_check'), args)])

    def repeat (self, args):
        children = []
        for arg in args:
            if isinstance(arg, Token) and arg.type == '_SPACE':
                children.append(Token('_EOL', '\n'))
                children.append(Token('_SPACE', '    '))
            else:
                children.append(arg)
        children.append(Token('_EOL', '\n'))
        children.append(Token('_END_BLOCK', 'end-block'))
        return Tree(Token('RULE', 'repeat'), children)

class transformer_level_11(Transformer):
    def assign_list (self, args):
        children = [args[0]]
        for arg in args[1:]:
            if isinstance(arg, Tree): children.append(self._text(arg))
            else: children.append(arg)
        return Tree('assign_list', children)

    def assign (self, args):
        children = [args[0]]
        for arg in args[1:]:
            if isinstance(arg, Tree): children.append(self._text(arg))
            else: children.append(arg)
        return Tree('assign', children)

    def var (self, args):
        varlist.append(args[0].value)
        return Tree(Token('RULE', 'var'), args)

    def equality_check (self, args):
        children = []
        temp = ""
        children.append(self._text(args[0]))
        children.append(args[1])
        if len(args) == 2: children.append(self._text(args[1]))
        else:
            for arg in args[2:]:
                if isinstance(arg, Tree): temp += arg.children[0]
                else: temp += arg.value
            children.append(self._text(Tree('text', [Token('__ANON_1', temp)])))
        return Tree('equality_check', children)

    def in_list_check (self, args):
        return Tree('in_list_check', [self._text(args[0]), args[1], args[2]])

    def _text(self, arg):
        # ensure this is text
        if isinstance(arg, Token) or arg.data != "text":
            return arg
        # is this a variable?
        if arg.children[0].value in varlist:
            return Tree(Token('RULE','var_access'), [Token('NAME', arg.children[0].value)])
        # is this a number
        if arg.children[0].isnumeric():
            return Token('NUMBER', arg.children[0])
        # else:
        return Tree(Token('RULE','text_in_quotes'), [arg])

    def _contents_getter(self, name, args):
        return self._get_contents(args)

    def _get_contents(self, args):
        return ''.join([x for x in args])

class transformer_level_15(Transformer):
    def assign_list (self, args):
        children = []
        first = True

        for arg in args:
            if isinstance(arg, Tree) and arg.data == 'text_in_quotes':
                if first:
                    first = False
                    children.append(Token('_LEFT_SQUARE_BRACKET', "["))
                children.append(Tree('text', [Token('__ANON_10', "'"+arg.children[1].children[0]+"'")]))
            else:
                children.append(arg)
        children.append(Token('_RIGHT_SQUARE_BRACKET', "]"))
        return Tree(Token('RULE', 'assign_list'), children)

    def list_access (self, args):
        return Tree(Token('RULE', 'list_access'), [args[0], Token('_LEFT_SQUARE_BRACKET', "["), args[2], Token('_RIGHT_SQUARE_BRACKET', "]")])

class transformer_level_16(Transformer):
    def elses (self, args):
        children = []
        for arg in args:
            children.append(arg)
            if isinstance(arg, Token) and arg.type == '_ELSE':
                children.append(Token('_COLON', ':'))

        return Tree(Token('RULE', 'elses'), children)

    def for_list (self, args):
        children = []
        for arg in args:
            children.append(arg)
            if isinstance(arg, Tree) and arg.data == 'var_access':
                children.append(Token('_COLON', ':'))

        return Tree(Token('RULE', 'for_list'), children)

    def for_loop (self, args):
        children = []
        first = True
        for arg in args:
            if isinstance(arg, Token) and arg.type == '_EOL' and first:
                children.append(Token('_COLON', ':'))
                children.append(arg)
                first = False
            else:
                children.append(arg)

        return Tree(Token('RULE', 'for_loop'), children)

    def ifs (self, args):
        children = []
        first = True
        for arg in args:
            if isinstance(arg, Token) and arg.type == '_EOL' and first:
                children.append(Token('_COLON', ':'))
                children.append(arg)
                first = False
            else:
                children.append(arg)

        return Tree(Token('RULE', 'ifs'), children)

    def while_loop (self, args):
        children = []
        first = True
        for arg in args:
            if isinstance(arg, Token) and arg.type == '_EOL' and first:
                children.append(Token('_COLON', ':'))
                children.append(arg)
                first = False
            else:
                children.append(arg)

        return Tree(Token('RULE', 'while_loop'), children)

class transformer_level_17(Transformer):
    def ask (self, args):
        children = []
        for arg in args:
            if isinstance(arg, Token) and arg.type == '_ASK':
                children.append(Token('_INPUT', 'input '))
                children.append(Token('_LEFT_BRACKET', '('))
            elif isinstance(arg, Token) and arg.type == '_COMMA':
                children.append(Token('_COMMA', ','))
            else:
                children.append(arg)
        children.append(Token('_RIGHT_BRACKET', ')'))
        return Tree(Token('RULE', 'input'), children)

    def print (self, args):
        children = [args[0], Token('_LEFT_BRACKET', "(")]
        for arg in args[1:]:
            if isinstance(arg, Token) and arg.type == '_SPACE':
                children.append(Token('_COMMA', ','))
            else:
                children.append(arg)
        children.append(Token('_RIGHT_BRACKET', ")"))
        return Tree(Token('RULE', 'print'), children)

def go_to_transformer(AST, level):
    No_Changes = [2,4,6,8,9,10,12,13,14]

    if level in No_Changes: result = AST
    elif level == 1: result = transformer_level_1().transform(AST)
    elif level == 3: result = transformer_level_3().transform(AST)
    elif level == 7: result = transformer_level_7().transform(AST)
    elif level == 11: result = transformer_level_11().transform(AST)
    elif level == 15: result = transformer_level_15().transform(AST)
    elif level == 16: result = transformer_level_16().transform(AST)
    elif level == 17: result = transformer_level_17().transform(AST)
    else:
        print("Error: level unsupported in transformer")
        result = AST
    return result

def execute(AST, level):
    get_changes_in_grammar(level)

    AST = go_to_transformer(AST, level)
    return AST
