import unittest
import re
import json
import os



# Transcription of the used tokens into a symbol (a letter) in order to apply a coloring
TOKEN_CODE = {
    "text" :               'T', # normal
    "keyword" :            'K', # 
    "comment" :            'C',
    "variable" :           'N',
    "constant.character" : 'S',
    "invalid" :            'I',
}


ABBREVIATION = {
    "text"                : "T",
    "uncolor"             : "T",
    "txt"                 : "T",
    "white"               : "T",
    "T"                   : "T",

    "keyword"             : "K",
    "kw"                  : "K",
    "red"                 : "K",
    "K"                   : "K",

    "comment"             : "C",
    "cmt"                 : "C",
    "grey"                : "C",
    "C"                   : "C",

    "variable"            : "N",
    "number"              : "N",
    "green"               : "N",
    "N"                   : "N",

    "constant.character"  : "S",
    "string"              : "S",
    "str"                 : "S",
    "blue"                : "S",
    "S"                   : "S",

    "invalid"             : "I",
    "inv"                 : "I",
    "pink"                : "I",
    "I"                   : "I",
}


class HighlightTester(unittest.TestCase):

    def assert_highlighted_chr(self, code, expected, level, lang="en"):
        rules  = self.get_rules(level, lang)
        self.check(code, expected, rules)


    def assert_highlighted_chr_multi_line(self, *args, level, lang="en"):
        if len(args)%2 != 0:
            raise RuntimeError(f'Pass an even number of strings to assert_highlighted_chr_multi_line (alternatingly code and highlighting). Got: {args}')

        code = []
        expected = []
        for i, line in enumerate(args):
            if i%2 == 0: code.append(line)
            else: expected.append(line)

        code = "\n".join(code)
        expected = "\n".join(expected)

        self.assert_highlighted_chr(code, expected, level, lang)


    def assert_highlighted(self, code_col, level, lang="en"):
        code, expected = self.converts(code_col)
        self.assert_highlighted_chr(code, expected, level, lang)


    def assert_highlighted_multi_line(self, *args, level, lang="en"):
        code_col = "\n".join(args)
        code, expected = self.converts(code_col)
        self.assert_highlighted_chr(code, expected, level, lang)



    # apply rules on code and check if the result is valid
    def check(self, code, expected, rules):
        
        simulator = SimulatorAce(rules)
        result = simulator.highlight(code)

        valid, ind_error = self.compare(result, expected)

        if not valid:

            code_list     = code.split('\n')
            expected_list = expected.split('\n')
            result_list   = result.split('\n')

            line_cpt = 0
            while ind_error >= len(code_list[line_cpt]):
                ind_error -= len(code_list[line_cpt]) +1
                line_cpt += 1

            print("ERROR in this code :")
            print("In this code :", code_list[line_cpt] )
            print("We want      :", expected_list[line_cpt] )
            print("We have      :", result_list[line_cpt] )
            print("At           :", " " * ind_error + "^")

        self.assertTrue(valid)


    # This function allows to compare 2 syntactic colorations one desired
    # and the other obtained, and manages some special cases

    # Returns a boolean and a value:
    # - If the 2 highlights are consistent, the boolean will be true and the value unused
    # - if there is an error in the highlight, the boolean will be false and
    #   the value will be the number of the 1st character where there is an inconsistency
    def compare(self, result, expected):
        if len(result) != len(expected):
            raise ValueError("The desired highlight and the obtained highlight do not have the same length !")

        cpt = 0
        for i in range(len(expected)):
            ch_wanted, ch_result = expected[i], result[i]

            if ch_wanted == ch_result:
                pass # if they are the same, no problem 
            elif ch_wanted == " " and ch_result in ['T', 'K', 'C', 'N', 'S']:
                pass # if it was not fixed at the beginning, everything is tolerated except the pink highlighting
            else:
                # in all other cases, an error is returned indicating the number of the problematic character
                return False, cpt

            cpt += 1

        return True, -1



    # get rules from json files
    def get_rules(self, level, lang="en"):
        os.chdir(os.path.dirname(__file__) +"/..")

        # get traduction
        with open('highlighting/highlighting-trad.json') as file_regex_trad:
            data_regex_trad = json.load(file_regex_trad)
    
        if lang not in data_regex_trad.keys():
            lang = 'en'

        regex_trad = data_regex_trad[lang]

        # get rules
        with open('highlighting/highlighting.json') as file_regex:
            data_regex = json.load(file_regex)

        # apply translation of keywords
        for lvl_rules in data_regex:
            for state in lvl_rules["rules"]:
                for rule in lvl_rules["rules"][state]:
                    for key in regex_trad:
                        rule['regex'] = rule['regex'].replace("(__" + key + "__)", regex_trad[key])

        # get rules for the level
        rules = [item for item in data_regex if item['name']==level]
        if len(rules) != 1 :
              raise RuntimeError(f'Expected exactly 1 rule with {level}, got {len(rules)}')
        else :
            rules = rules[0]['rules']
        return rules


    # this fonctions convert :
    #      "{print|kw} {Welcome to Hedy!|txt}"
    # in :
    #      "print Welcome to Hedy!",
    #      "KKKKK TTTTTTTTTTTTTTTT",
    def converts(self, code_col):
        code     = []
        coloring = []


        TEXT, CODE, KEYWORD = range(3)
        
        state = TEXT
        for ch in code_col:
            if ch == "{" :
                state = CODE

                tmp_code     = []
                tmp_coloring = []
            elif ch == "}" :
                state = TEXT

                code.append("".join(tmp_code))
                coloring.append(ABBREVIATION["".join(tmp_coloring)] * len(tmp_code))

            elif ch == "|" and state == CODE :
                state = KEYWORD


            else: # not a special symbol

                if state == CODE:
                    tmp_code.append(ch)
                elif state == KEYWORD:
                    tmp_coloring.append(ch)

                else : # state == TEXT
                    if ch == "\n" :
                        code.append("\n")
                        coloring.append("\n")
                    else:
                        code.append(ch)
                        coloring.append(" ")

        return "".join(code), "".join(coloring)





class SimulatorAce:

    # constructor of SimulatorAce with check on rules
    def __init__(self, rules):
        self.rules = rules
        self._precompile_regexes()

    # check and precompile regexes
    def _precompile_regexes(self):
        for state in self.rules:
            for rule in self.rules[state]:

                if "token" not in rule :
                    raise ValueError("We need a token in all rules !")

                rule["regex_compile"] =  re.compile(rule['regex'], re.MULTILINE)
                rule["nb_groups"] = rule["regex_compile"].groups


                if rule["nb_groups"] == 0:
                    if type(rule["token"]) != str:
                        raise ValueError(f"if regex has no groups, token must be a string. In this rule : {rule}!")

                else:
                    if type(rule["token"]) != list :
                        raise ValueError(f"if regex has groups, token must be a list. In this rule : {rule}!")

                    else:
                        if rule["nb_groups"] != len(rule["token"]):
                            raise ValueError(f"The number of groups in the regex is different from the number of tokens. In this rule : {rule}!")

    # apply rules on code
    def highlight(self, code):
        outputs = []
        token = "start"
        for line in code.split("\n"):
            output, token = self.highlight_rules_line(line, token)
            outputs.append(output)
        return "\n".join(outputs)

    # apply rule in one line of code
    def highlight_rules_line(self, code, start_token="start"):
        # Initialisation output
        output = []

        # Initialisation variables
        current_state = start_token
        current_position = 0

        default_token = "text"

        end_of_search = False
        while not end_of_search:

            find_transition, next_transition = self.find_match(code, current_state, current_position)

            if find_transition :
                # Application of coloring on the code

                # get match
                current_rule, current_match = next_transition["rule"], next_transition["match"]

                # we color the characters since the last match with the default coloring
                for c in range(current_position, current_match.start()):
                    output.append(TOKEN_CODE[default_token])

                # we recover the next default coloring
                if "defaultToken" in current_rule:
                    default_token = current_rule["defaultToken"]
                else:
                    default_token = "text"

        
                # if rule has only one groups
                if current_rule["nb_groups"] == 0:
                    tok    = current_rule['token']
                    start  = current_match.start()
                    length = current_match.end() - current_match.start()
                    output.append(TOKEN_CODE[tok] * length)

                # if rule has only multiples groups
                else:
                    pos = current_match.start()
                    for i, submatch in enumerate(current_match.groups()):    
                        tok = current_rule['token'][i%len(current_rule['token'])]        
                        output.append(TOKEN_CODE[tok] * len(submatch))
                        pos += len(submatch)

                current_position = current_match.end()

                if 'next' in current_rule:
                    current_state = current_rule['next']


                if current_position == len(code):
                    end_of_search = True

            else:
                end_of_search = True

        # we color the last characters since the last match with the default coloring
        for c in range(current_position, len(code)):
            output.append(TOKEN_CODE[default_token])

        return "".join(output), current_state

    # find next match
    def find_match(self, code, current_state, current_position):
        # search for the transition that we will use

        current_match = None
        next_transition = {"rule":{}, "match":None}
        find_transition = False

        next_pos = len(code) + 1
        for rule in self.rules[current_state]:

            regex_compile = rule["regex_compile"]
            match = regex_compile.search(code, current_position)

            if match:
                if match.start() < next_pos :
                    next_pos = match.start()
                    next_transition["rule"] = rule
                    next_transition["match"] = match
                    find_transition = True

        return find_transition, next_transition


