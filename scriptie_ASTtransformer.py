from lark import Lark
from lark.exceptions import VisitError, LarkError, UnexpectedEOF
from lark import Tree, Transformer, Visitor
from lark.indenter import Indenter
import hedy
import sys
import scriptie_unparser as unparser

# Doel Transformer:
# Het transformeren van hedy code naar een nieuw level met zo min mogelijk
# moeite voor programmeurs van toekomstige levels.
# Droom: volledig automatisch
#        anders met strikte opstel eissen
#        worst case bestand met veranderingen tussen Grammars


level = 0

def get_changes_in_grammar():
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
    return result


def get_changes_in_used_grammar(AST):
    start = get_changes_in_grammar()
    result = []
    for line in start:
        parts = line.split(':')
        name = parts[0]
        if str(AST).find("Tree('"+name) == -1:
            True
        else:
            result.append(line)
    return result

class transformer(Transformer):
    def start (self, args):
        return Tree('start', args)

def execute(AST, lvl):
    global level
    level = int(lvl)
    changes = get_changes_in_used_grammar(AST)
    if changes == "":
        return AST
    AST = transformer().transform(AST)
    return AST
