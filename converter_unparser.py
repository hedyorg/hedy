from lark import Lark
from lark.exceptions import VisitError, LarkError, UnexpectedEOF
from lark import Tree, Transformer, Visitor, Token
from lark.indenter import Indenter
import hedy
import sys

#==============================================================================
#   UTILITY functions
#==============================================================================

# This function will, for a given rule, group it based on the given seperators.
def get_groupings(rule, seperators):
    group = ['/', '"', '(', '[']
    sets = {"(" : ")", "[" : "]"}
    group_symbol = []
    groupings = []
    start = 0
    current = 0

    while (current < len(rule)):
        while current < len(rule) and rule[current] == '\\': #escape character
            current += 2
        if (current >= len(rule)): break

        if (group_symbol == []): # currently not in group
            if (rule[current] in group):
                group_symbol.append(rule[current])
            elif (rule[current] in seperators):
                if (start != current):
                    groupings.append(rule[start:current+1])
                start = current + 1
        else: # currently in group
            if (rule[current] == group_symbol[-1]):
                if (group_symbol[-1] not in sets):
                    group_symbol.pop()
                else:
                    group_symbol.append(rule[current])
            elif group_symbol[-1] in sets and rule[current] == sets[group_symbol[-1]]:
                group_symbol.pop()
        current += 1

    if (start != current):
        groupings.append(rule[start:current])

    return groupings

# This function should for a given rule tell if it contains elements
# Which cam create trees.
# top level:
#   - line of one or more elements
# non final elements:
#   - _rules <- call creates_tree for rule
#   - (something in)
#   - [something in]
#   - *,+,?
# Core elements:
#   - rules <- creates tree
#   - "text" <- doesn't create tree
#   - /reggex/ <- creates tree
def creates_tree(grammar, group):
    options = get_groupings(group.strip(), [' ', '+', '?', '*', '|'])
    optionz = []
    for option in options:
        if option[-1] == "|":
            option = option[0:-1]
        optionz.append(option.strip())

    for option in optionz:
        #call creates_tree for section with *,+,?
        if (option[-1] == '*' or option[-1] == '+' or option[-1] == '?'):
            if (creates_tree(grammar, option[0:-1])):
                return True
        # call creates_tree for groupings () and []
        elif (option[0] == "(" or option[0] == "["):
            if (creates_tree(grammar, option[1:-1])):
                return True
        # if it starts with _ not in tree, but should call creates_tree
        elif option[0] == "_":
            new_rule = grammar.get(option)
            if new_rule != None:
                if creates_tree(grammar, new_rule):
                    return True
        # If it isn't "text", it is in tree
        elif option[0] != '"':
            return True

    return False

#==============================================================================
#   GRAMMAR functions
#==============================================================================

# Grammar utility function
def add_option(result, key, addition):
    if key in result:
        result[key] += " | " + addition
    else:
        result[key] = addition
    return result

# On the first pass through the grammar, the following will be done:
# 1. Any comments will be removed
# 2. Unsupported Grammar will be ignored, and a warning will be sent.
# 3. Multiline will be combined into one.

# Haven't tested wether the multiline works yet...
# Since Hedy hasn't been created with the possibility of using it...
def first_pass(grammar):
    temp_line = ""
    temp_grammar = []
    for line in grammar:
        if "//" in line:
            line = line.split("//")[0]
        if line.strip() == "": continue
        # Directives aren't supported
        if line.strip()[0] == "%": continue
        # Templates aren't supported
        if "{" in line.split(":")[0]: continue
        # Priorities aren't supported
        if "." in line.split(".")[0]: continue

        if len(get_groupings(line, [":"])) > 1:
            if temp_line.strip() != "":
                temp_grammar.append(temp_line)
            temp_line = line
        elif temp_line.strip() != "":
            temp_line += " " + line
    if temp_line.strip() != "":
        temp_grammar.append(temp_line)
    return temp_grammar

# This prepare grammar function handles the alias side of things.
def prep_alias(result, line):
    parts = get_groupings(line, [":"])
    parts[0] = parts[0].split(":",1)[0].strip()
    groups = get_groupings(parts[1], ['|'])
    inline = "!"

    for group in groups:
        if group[-1] == "|":
            group = group[0:-1]
        group = group.strip()

        if "->" in group: # group contains alias
            #inline prep
            if parts[0][0] == "?": inline = parts[0].strip()
            else: inline = "?"+parts[0].strip()

            if "_"+inline[1:] in result: inline = "_"+inline[1:]
            elif prep_inline (group.split("->")[0], inline, inline) != prep_inline (group.split("->")[0], inline[1:], "_"+inline):
                if inline in result:
                    result = add_option(result, "_"+inline[1:], result[inline])
                    del result[inline]
                inline = "_"+inline[1:]

            # add alias to inline
            result = add_option(result, inline, group.split("->")[1].strip())
            # We only need one line for all code with same alias
            result = add_option(result, group.split("->")[1].strip(), group.split("->")[0].strip())
        else: # no alias
            result = add_option(result, parts[0].strip(), group)

    if inline[0] == "_":
        for line in result:
            result[line] = prep_inline (result[line], inline[1:], inline)
    return result

#TODO: bracket stuff can possibly be improved with brackets function
#recursive function to replace inline
def prep_inline(line, replace, replacement):
    operators = ['+', '?', '*']
    temp_group = ""
    for group in get_groupings(line, [' ', '+', '?', '*']):
        group = group.strip()
        if len(get_groupings(group,['|'])) > 1:
            # are we dealing with multiple options?
            temp = ""
            for line_group in get_groupings(group,['|']):
                if line_group[-1] == "|": line_group = line_group[0:-1]
                line_group = line_group.strip()
                line_group = prep_inline(line_group, replace, replacement) #let's go deeper
                if temp == "": temp = line_group
                else: temp += " | " + line_group
            group = temp
        elif group[-1] in operators:
            #haken als nodig <- ?
            group = prep_inline(group[0:-1], replace, replacement) + group[-1]
        elif group == replace:
            # are brackets needed?
            if len(get_groupings(line, [' ', '+', '?', '*'])) == 1 and replacement[0] == "(": group = replacement[1:-1]
            else: group = replacement
        elif group[0] == "(" or group[0] == "[":
            group = group[0] + prep_inline(group[1:-1], replace, replacement) + group[-1]
        if temp_group == "": temp_group = group
        else: temp_group += " " + group
    if temp_group != "": return temp_group
    return line

# calls all relevent prepare grammar functions.
# creates a dictionary containing all rules.
# while dealing with aliases and inline rules.
def prep_grammar(lvl):
    result = {}
    inlines = []

    grammar = hedy.create_grammar(lvl).split('\n')
    grammar = first_pass(grammar)

    for line in grammar:
        if len(get_groupings(line, [":"])) > 1: #add the rules to the dictionary
            if "->" in line: # line contains alias
                result = prep_alias(result, line)
                key = get_groupings(line, [":"])[0].split(":",1)[0].strip()
                if key[0] == "?" or key[0] == "_": test = "_" + key[1:]
                else: test = "_" + key
                if test in result: inlines.append(test)
            else:
                parts = get_groupings(line, [":"])
                key = parts[0].split(":",1)[0].strip()
                result[key] = parts[1].strip()
                for inline in inlines:
                    result[key] = prep_inline (result[key], inline[1:], inline)

    # process inline "?" stuff:
    list = []
    for line in result:
        if line[0] == '?': list.append(line)

    for line in list:
        if len(get_groupings(result[line], ['|'])) > 1:
            replacement = "(" + result[line] + ")"
        else:
            replacement = result[line]
        for line2 in result:
            result[line2] = prep_inline(result[line2], line[1:], replacement)
        del result[line]

    #TODO: Any grammar patterns that can be rewritten should be done here

    return result

#==============================================================================

# simplify grammar utility function
def brackets(symbol, contents):
    comp = {"(":")","[":"]"}
    if symbol not in comp:
        print("ERROR: brackets function received something other than brackets")

    if len(get_groupings(contents, [' ', '+', '?', '*'])) < 2:
        return contents.strip()
    else:
        return symbol + contents.strip() + comp[symbol]

# Processes rules to simplify the grammar
# This will remove portions of rules if it might not create a tree.
def process_rule(grammar, rule):
    operators = ['+', '?', '*']
    result = []

    # This needs to be added to handle the indents
    if "_END_BLOCK" in rule:
        if rule.split(" ")[0] == "_EOL":
            temp = "_EOL _START_BLOCK" + ''.join([" " + str(c) for c in rule.split(" ")[1:]])
            rule = temp
        else:
            rule = "_START_BLOCK " + rule

    for group in get_groupings(rule, [' ', '+', '?', '*']):
        group = group.strip()
        if (group != "" and (group[0] == "(" or group[0] == "[")):
            # dealing with a group, process content
            if (group[-1] == ")" or group[-1] == "]"):
                group = brackets(group[0], process_split(grammar, group[1:-1]))
            else:
                group = brackets(group[0], process_split(grammar, group[1:-2]))+group[-1]

        if group == "": continue # needs to be here because of the group part
        if group[-1] not in operators: result.append(group + " ")
        else:
            #let's handle the operators
            if (not creates_tree(grammar, group)):
                if group[-1] == "+": result.append(group[0:-1] + " ")
            else: result.append(group + " ")

    if (result != []): result[-1] = result[-1].strip()

    return ''.join([str(c) for c in result])

# Processes rule(sections) with multiple options
# should have one option which doesn't create a tree
# example: turning rule | _rule | _other into rule | _rule
def process_split(grammar, rule):
    has_alternative = False
    options = get_groupings(rule, ['|'])
    if len(options) > 1:
        value = ""
        for option in options:
            if option[-1] == "|": option = option[0:-1]
            option = option.strip()
            #process rules
            if (creates_tree(grammar, option)):
                option = process_rule(grammar, option)
            elif has_alternative: continue
            else:
                has_alternative = True
                temp_option = process_rule(grammar, option)
                if (temp_option.strip() == ""): option = "\"\""
                else: option = temp_option
            if (option.strip() == ""): continue
            #put them all back together
            if not (value == ""): value += " | "
            value += option
    else: value = process_rule(grammar, rule)
    return value

# This function processes all rules in dict to simplify them if possible
def simp_grammar(grammar):
    for key in grammar:
        value = grammar.get(key)
        grammar[key] = process_split(grammar, value)
    return grammar

# Before we really begin with unparsing we first:
# - Prepare the grammar, to make it easier to deal with certain functionalities
#   (like handling the aliases)
# - Simplify the grammar, to remove any unnecesary portions of the grammar
#   which would only slow down the programs
def start_unparsing(Tree, lvl):
    #process grammar
    grammar = prep_grammar(lvl)
    grammar = simp_grammar(grammar)
    #print("\nresult:")
    #for key in grammar: print (key + " : " + grammar[key])
    #print("\n")
    #start unparsing
    return unparsing(Tree, grammar, 0)

#==============================================================================
#   UNPARSING functions
#==============================================================================

# If we have one "word" we will handle it here,
# but will otherwise "send" us to the right function
# if result is empty, it means there is no fit in the given Templates
def simple_format(Tree, grammar, Templates, rule):
    result = [] # if empty: functions as a False
    group = ["(", "["]
    not_in_tree = ['_', '"']
    do_not_process = ["_START_BLOCK", "_END_BLOCK", "_EOL", "_SPACE"]

    for possibility in Templates:
        template = possibility[0]
        nr_child = possibility[1]
        if (rule[0] in group): # this needs to be handled by get_group_format
            result += get_group_format(Tree, grammar, [possibility], rule[1:-1])
        elif (rule[0] in not_in_tree and len(get_groupings(rule, [' ', '+', '?', '*', '|'])) == 1):
            new_rule = grammar.get(rule)
            if new_rule == None or rule in do_not_process:
                # No processing neccesary, add to result
                result.append((str(template) + " " + str(rule), nr_child))
            else:
                # New _rule to go through
                result += get_format(Tree, grammar, Templates, new_rule)
        else:
            if (nr_child >= len(Tree.children)): continue
            elif (len(get_groupings(rule, [' ', '+', '?', '*', '|'])) > 1):
                result += get_op_format(Tree, grammar, Templates, rule)
            elif (isinstance(Tree.children[nr_child], Token)):
                #check if what's in rule is also a token
                if (not rule in grammar.keys()) or (rule.isupper()):
                    result.append((str(template) + " " + str(rule), nr_child+1))
            else:
                #does the child match what's expected in rule?
                if (Tree.children[nr_child].data == rule):
                    result.append((str(template) + " " + str(rule), nr_child+1))
    return result

# Grammar format requirements: <- requirements need to be rechecked if still necessary
# The options in a rule with | should only include rules or a group
#
# This function handles all possible options seperated by "|" in a rule.
# Current version takes the first not in tree if the tree options don't work <- Happens indirectly in unparsing
def get_options_format(Tree, grammar, Templates, rule):
    result = []
    #Get the options of this rule
    for option in get_groupings(rule, ['|']):
        if option[-1] == "|":
            option = option[0:-1]
        result += simple_format(Tree, grammar, Templates, option.strip())

    return result

# This function checks if we are dealing with a group,
# and if so, deals with it appropriately.
def get_group_format(Tree, grammar, Templates, rule):
    result = []
    if rule[0] == "(" or rule[0] == "[":
        # we are in a group
        if len(get_groupings(rule[1:-1], ['|'])) > 1:
            result += get_options_format(Tree, grammar, Templates, rule[1:-1])
        else:
            temp_list = Templates
            for group in get_groupings(rule[1:-1], [' ', '+', '?', '*', '|']):
                temp_list = get_op_format(Tree, grammar, temp_list, group)
            result += temp_list
    else:
        # we're not in a group, so let's go to the next step!
        result += get_options_format(Tree, grammar, Templates, rule)
    return result

# This function deals with the operators in the top level of a rule.
def get_op_format(Tree, grammar, Templates, rule):
    result = []
    correct = []
    prog = []
    groups = get_groupings(rule, [' ', '+', '?', '*', '|'])
    none = ["?", "*"]
    more = ["+", "*"]

    for i in range(len(groups)):
        prog = []
        group = groups[i].strip()

        # none if: ?, *
        if (group[-1] in none): prog += Templates

        # more if: +, *
        if (group[-1] in more):
            temp_list = Templates
            loop = True
            while loop:
                for template in temp_list:
                    correct = []
                    list = get_group_format(Tree, grammar, [template], group[0:-1])
                    # check to make sure we won't keep looping non tree items
                    for thing in list:
                        if (template[0] == ""): test = thing[0]
                        else: test = thing[0][len(template[0]):].strip()
                        if creates_tree(grammar, test): correct.append(thing)
                temp_list = correct
                prog += temp_list
                if temp_list == []: loop = False

        # one if not: +, *
        if (group[-1] not in more):
            if group[-1] in none:
                prog += get_group_format(Tree, grammar, Templates, group[0:-1])
            else:
                prog += get_group_format(Tree, grammar, Templates, group)

        #next round prep
        Templates = prog

    return prog

# This function will look at the rule, and "sends" us to the correct function;
# get_options_format if on the top level, we have multiple options we can choose
# get_op_format if we have a single option which we need to work through
def get_format(Tree, grammar, Templates, rule):
    if len(get_groupings(rule, ['|'])) > 1:
        return get_options_format(Tree, grammar, Templates, rule)
    else:
        return get_op_format(Tree, grammar, Templates, rule)

# onderdelen rule stapgeweis afhandelen
def get_result(Tree, grammar, number_of_indents, rule):
    result = []
    count = 0
    indent_size = 4
    last_word = ""

    for word in rule.split(" "):
        if word == "": continue
        elif word[0] == "_":
            #specific fixes for hedy
            if (word == "_START_BLOCK"): number_of_indents += 1
            elif (word == "_END_BLOCK"): number_of_indents -= 1
            elif (word == "_SPACE" and last_word == "_EOL"): True
            elif (word == "_EOL"):
                result.append("\n")
                for i in range(number_of_indents): result.append("    ")
            #end of specific fixes
            else:
                temp = grammar.get(word)
                if '"' == temp[0]: temp = temp[1:-1]
                result.append(temp)
        elif word[0] == '"': result.append(word.split('"')[1])
        else:
            if count < len(Tree.children):
                result.append(unparsing(Tree.children[count],grammar, number_of_indents))
                count += 1
            else: print("There is a problem with the format")
        last_word = word

    return ''.join([str(c) for c in result])

# This function will start the unparsing.
def unparsing(Tree, grammar, number_of_indents):
    # Templates is used to collect possible correct results.
    Templates = [("", 0)]
    #is this a leaf? if so:
    if (isinstance(Tree, Token)): return Tree.value

    #find rule in grammar & process
    rule = grammar.get(Tree.data)
    if (rule == None): return "Error: Rule not in Grammar"

    # Werk regels uit om naar de juiste format te werken
    # kijk hierbij naar de kinderen
    temp = []
    for possibility in get_format(Tree, grammar, Templates, rule):
        if (possibility[1] == len(Tree.children)):
            temp.append(possibility)

    if temp == []:
        print("\nThere is an error during Unparsing, get_format returned empty \n\n", Tree.data,"\n", grammar.get(Tree.data),"\n",Tree)
        return ''

    rule = temp[0][0]
    #TODO: add check to see if it went ok + error code

    #zo ja: rule = opsplitsing

    #onderdelen rule stapgeweis afhandelen
    result = get_result(Tree, grammar, number_of_indents, rule)

    return result

#==============================================================================
#   USE and TEST functions
#==============================================================================

#used to run the unparser
def execute(Tree, lvl):
    return start_unparsing(Tree,lvl)
