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

    def assert_highlighted_chr(self,code,expected,level,lang="en"):
        
        rules  = self._get_rules(level,lang)

        result = self.apply_rules(rules,code)

        valid, ind_error = self.check(result,expected)
        if not valid:

            st = 0
            ind = ind_error
            if ind_error >= 40 :
                st = ind_error - 40
                ind = 40
            end = len(code)
            if len(code) >= ind_error + 40:
                end = ind_error + 40


            print("ERROR in level {} in {}:".format(level, lang))
            print("In this code :",code.replace("\n","\\n")[st:end])
            print("We want      :",expected.replace("\n","\\n")[st:end])
            print("We have      :",result.replace("\n","\\n")[st:end])
            print("At           :"," " * ind + "^")
        self.assertTrue(valid)


    def assert_highlighted_chr_multi_line(self,*args,level,lang="en"):
        if len(args)%2 != 0:
            raise("*args must be even (alternating lines of code and lines of highlighting)")

        code = []
        expected = []
        for i,line in enumerate(args):
            if i%2 == 0: code.append(line)
            else: expected.append(line)

        code = "\n".join(code)
        expected = "\n".join(expected)

        self.assert_highlighted_chr(code,expected,level,lang)


    def assert_highlighted(self,code_col,level,lang="en"):
        
        code,expected = self._transforme(code_col)

        self.assert_highlighted_chr(code,expected,level,lang)


    def assert_highlighted_multi_line(self,*args,level,lang="en"):
        code_col = "\n".join(args)

        code,expected = self._transforme(code_col)

        self.assert_highlighted_chr(code,expected,level,lang)


    def _get_rules(self,level,lang="en"):
        os.chdir(os.path.dirname(__file__) +"/..")

        file_regex_trad = open('highlighting/highlighting-trad.json')
        data_regex_trad = json.load(file_regex_trad)
        file_regex_trad.close()

        if lang not in data_regex_trad.keys():
            lang = 'en'

        regex_trad = data_regex_trad[lang]


        # open data for regex
        file_regex = open('highlighting/highlighting.json')
        data_regex = json.load(file_regex)
        file_regex.close()

        for lvl_rules in data_regex:
            for state in lvl_rules["rules"]:
                for rule in lvl_rules["rules"][state]:
                    for key in regex_trad:
                        rule['regex'] = rule['regex'].replace("(__"+key+"__)", regex_trad[key])

        # get rules for the level
        rules = [item for item in data_regex if item['name']==level]
        if len(rules) != 1 : exit()
        else : rules = rules[0]['rules']
        return rules


    def _transforme(self,code_col):
        code = ""
        colo = ""

        flag = False
        flag2 = False

        for ch in code_col:
            if ch == "{" :
                flag = True
                flag2 = False
                tmp_code = ""
                tmp_colo = ""
            elif ch == "}":
                flag = False
                flag2 = False

                code += tmp_code
                colo += ABBREVIATION[tmp_colo] * len(tmp_code)

            elif flag:
                if ch == "|":
                    flag2 = True
                elif not flag2:
                    tmp_code += ch
                elif flag2:
                    tmp_colo += ch

            elif not flag:
                if ch == "\n":
                    colo += "\n"
                    code += "\n"
                else:
                    colo += " "
                    code += ch

        return code,colo


    #######################################################################################
    ##                     This part concerns the simulation by Ace                      ##
    #######################################################################################

    # This function simulates the operation of Ace on a
    # string provided as input, and "colors" it using the variable TOKEN_CODE.

    def apply_rules_line(self,rules,code,start_token="start"):
        # Initialisation output
        output = " " * len(code)

        # Initialisation variables
        current_state = start_token
        current_position = 0


        flag = False
        while not flag:

            # search for the transition that we will use
            current_match = None
            NEXT = {"rule":{},"match":None}
            FIND = False
            next_pos = len(code) + 42
            for rule in rules[current_state]:

                regex_compile = re.compile(rule['regex'], re.MULTILINE)
                match = regex_compile.search(code, current_position)

                if match:
                    if match.start() < next_pos :
                        next_pos = match.start()
                        NEXT["rule"] = rule
                        NEXT["match"] = match
                        FIND = True


            if FIND :

                # Application of coloring on the code
                current_rule,current_match = NEXT["rule"],NEXT["match"]

                if "token" not in current_rule:
                    raise ValueError("We need a token in all rules !")
        
                if type(current_rule['token']) == str :
                    current_rule['token'] = [current_rule['token']]
        
                if re.compile(current_rule['regex'], re.MULTILINE).groups == 0:
                    tok = current_rule['token'][0]
                    start = current_match.start()
                    length = current_match.end() - current_match.start()
                    output = output[:start] + TOKEN_CODE[tok] * length + output[start + length:]

                else:
                    pos = current_match.start()
                    for i,submatch in enumerate(current_match.groups()):    
                        tok = current_rule['token'][i%len(current_rule['token'])]        
                        output = output[:pos] + TOKEN_CODE[tok] * len(submatch) + output[pos + len(submatch):]
                        pos += len(submatch)

                current_position = current_match.end()

                if 'next' in current_rule:
                    current_state = current_rule['next']

                if current_position ==len(code):
                    flag = True


            else:
                flag = True

        output = output.replace(" ","T")
        return output,current_state


    def apply_rules(self,rules,code):
        outputs = []
        token = "start"
        for line in code.split("\n"):
            output,token = self.apply_rules_line(rules,line,token)
            print("next",token)
            outputs.append(output)
        return "\n".join(outputs)



    # This function allows to check 2 syntactic colorations one desired
    # and the other obtained, and manages some special cases

    # Returns a boolean and a value:
    # - If the 2 highlights are consistent, the boolean will be true and the value unused
    # - if there is an error in the highlight, the boolean will be false and
    #   the value will be the number of the 1st character where there is an inconsistency
    def check(self,result,expected):
        if len(result) != len(expected):
            raise ValueError("The desired highlight and the obtained highlight do not have the same length !")
        cpt = 0
        for i in range(len(expected)):
            ch_wanted,ch_result = expected[i],result[i]

            if ch_wanted == ch_result:
                pass # if they are the same, no problem 
            elif ch_wanted == " " and ch_result in ['T','K','C','N','S']:
                pass # if it was not fixed at the beginning, everything is tolerated except the pink highlighting
            else:
                # in all other cases, an error is returned indicating the number of the problematic character
                return False,cpt

            cpt += 1
            if result[i] == "\n" : cpt += 1

        return True,-1



    #######################################################################################
    #######################################################################################
    #######################################################################################
