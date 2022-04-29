import unittest
import re
import json
import os



# Transcription of the used tokens into a symbol (a letter) in order to apply a coloring
Tokencode = {
    "text" :               'T', # normal
    "keyword" :            'K', # 
    "comment" :            'C',
    "variable" :           'N',
    "constant.character" : 'S',
    "invalid" :            'I',
}


Abbreviation = {
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

os.chdir(os.path.dirname(__file__) +"/..")




class HighlightTester(unittest.TestCase):

    def assertHighlightedChr(self,code,expected,level,lang="en"):
        
        rules  = self.getRules(level,lang)

        result = self.simulateRulesWithoutToken(rules,code)

        valid, indError = self.check(result,expected)
        if not valid:
            print("ERROR in level {} in {}:".format(level, lang))
            print("In this code :",code.replace("\n","\\n"))
            print("We want      :",expected.replace("\n","\\n"))
            print("We have      :",result.replace("\n","\\n"))
            print("At           :"," "* indError + "^")
        self.assertTrue(valid)


    def assertHighlightedChrMultiLine(self,*args,level,lang="en"):
        if len(args)%2 != 0:
            raise("*args must be even (alternating lines of code and lines of highlighting)")

        code = []
        expected = []
        for i,line in enumerate(args):
            if i%2 == 0: code.append(line)
            else: expected.append(line)

        code = "\n".join(code)
        expected = "\n".join(expected)

        self.assertHighlightedChr(code,expected,level,lang)


    def assertHighlighted(self,codeCol,level,lang="en"):
        
        code,expected = self._transforme(codeCol)

        self.assertHighlightedChr(code,expected,level,lang)


    def assertHighlightedMultiLine(self,*args,level,lang="en"):
        codeCol = "\n".join(args)

        code,expected = self._transforme(codeCol)

        self.assertHighlightedChr(code,expected,level,lang)


    def getRules(self,level,lang="en"):

        # open data for regex
        file = open('highlighting/highlightingRules/highlighting-'+lang+'.json') 
        dataRegex = json.load(file)
        file.close()

        # get rules for the level
        Rules = [item for item in dataRegex if item['name']==level]
        if len(Rules) != 1 : exit()
        else : Rules = Rules[0]['rules']
        return Rules


    def _transforme(self,codeCol):
        Code = ""
        Colo = ""

        flag = False
        flag2 = False

        for ch in codeCol:
            if ch == "{" :
                flag = True
                flag2 = False
                tmpCode = ""
                tmpColo = ""
            elif ch == "}":
                flag = False
                flag2 = False

                Code += tmpCode
                Colo += Abbreviation[tmpColo] * len(tmpCode)

            elif flag:
                if ch == "|":
                    flag2 = True
                elif not flag2:
                    tmpCode += ch
                elif flag2:
                    tmpColo += ch

            elif not flag:
                if ch == "\n":
                    Colo += "\n"
                    Code += "\n"
                else:
                    Colo += " "
                    Code += ch

        return Code,Colo


    #######################################################################################
    ##                     This part concerns the simulation by Ace                      ##
    #######################################################################################

    # This function simulates the operation of Ace on a
    # string provided as input, and "colors" it using the variable Tokencode.

    # Be careful, this function only works when the coloring
    # uses only one state in its automaton (`start`)

    def simulateRulesWithoutToken(self,rules,code):
        # we initialize the result variable
        Output = ""
        for c in code:
            if c == "\n": Output += "\n"
            else: Output += " "

        # We go through all the rules 
        regRule = rules["start"]
        for reg in regRule:

            # for each rule, we create the regex
            regComp = re.compile(reg["regex"], re.MULTILINE)

            # In case the rule does not use several groups
            if type(reg['token']) == str or len(reg['token']) == 1:

                # we get the type of the syntactic coloring
                if  type(reg['token']) == str : Tokcode = Tokencode[reg['token']]
                else: Tokcode = Tokencode[reg['token'][0]]


                for match in regComp.finditer(code):
                    # For each match, we see if this sequence has already been used
                    if self._notYetUsed(Output[match.start():match.end()]):

                        start  = match.start()
                        length = match.end() - start

                        # we replace in the output spaces by the token
                        Output = Output[:start] + Tokcode * length + Output[start + length:]


            else: # In case the rule uses several groups

                for match in regComp.finditer(code):
                    # For each match, we see if this sequence has already been used
                    if self._notYetUsed(Output[match.start():match.end()]):

                        pos = match.start()
                        for i,submatch in enumerate(match.groups()):
                            # For each of the subgroups of the match
                            # we replace the spaces by the coloring code
                            tok = reg['token'][i%len(reg['token'])]
                            Output = Output[:pos] + Tokencode[tok] * len(submatch) + Output[pos + len(submatch):]
                            pos += len(submatch)

        return Output


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
            chWanted,chresult = expected[i],result[i]

            if chWanted == chresult:
                pass # if they are the same, no problem 
            elif chWanted == " " and chresult in ['T','K','C','N','S']:
                pass # if it was not fixed at the beginning, everything is tolerated except the pink highlighting
            elif chWanted == "T" and chresult == " ":
                pass # If we wanted text, but we don't get syntactic coloring, then we tolerate
            else:
                # in all other cases, an error is returned indicating the number of the problematic character
                return False,cpt

            cpt += 1
            if result[i] == "\n" : cpt += 1

        return True,-1




    # Returns whether a portion of the string has already been " highlighted ".
    def _notYetUsed(self,string):
        for c in string:
            if c not in [" ","\n"]:
                return False
        return True

    #######################################################################################
    #######################################################################################
    #######################################################################################