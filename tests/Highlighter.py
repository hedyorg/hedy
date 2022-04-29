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


class HighlightTester(unittest.TestCase):

    def assertHighlightedChr(self,code,expected,level,lang="en"):
        
        rules  = self._getRules(level,lang)

        result = self._simulateRulesWithToken(rules,code)

        valid, indError = self.check(result,expected)
        if not valid:

            st = 0
            ind = indError
            if indError >= 40 :
                st = indError - 40
                ind = 40
            end = len(code)
            if len(code) >= indError + 40:
                end = indError + 40


            print("ERROR in level {} in {}:".format(level, lang))
            print("In this code :",code.replace("\n","\\n")[st:end])
            print("We want      :",expected.replace("\n","\\n")[st:end])
            print("We have      :",result.replace("\n","\\n")[st:end])
            print("At           :"," " * ind + "^")
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


    def _getRules(self,level,lang="en"):

        # open data for regex
        os.chdir(os.path.dirname(__file__) +"/..")
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

    def _simulateRulesWithToken(self,Rules,code):
        # Initialisation Output
        Output = ""
        for c in code:
            if c == "\n": Output += "\n"
            else: Output += " "

        # Initialisation variables
        currentState = "start"
        currentPosition = 0

        flag = False
        while not flag:

            # search for the transition that we will use
            currentMatch = None
            NEXT = {"rule":None,"match":None}
            FIND = False
            nextPos = len(code) + 42
            for rule in Rules[currentState]:

                regexCompile = re.compile(rule['regex'], re.MULTILINE)
                match = regexCompile.search(code,currentPosition)

                if match:
                    if match.start() < nextPos :
                        nextPos = match.start()
                        NEXT["rule"] = rule
                        NEXT["match"] = match
                        FIND = True


            if FIND :

                # Application of coloring on the code
                currentRule,currentMatch = NEXT["rule"],NEXT["match"]
        
                if type(currentRule['token']) == str :
                    currentRule['token'] = [currentRule['token']]
        
                if re.compile(currentRule['regex'], re.MULTILINE).groups == 0:
                    tok = currentRule['token'][0]
                    start = currentMatch.start()
                    length = currentMatch.end() - currentMatch.start()
                    Output = Output[:start] + Tokencode[tok] * length + Output[start + length:]

                else:
                    pos = currentMatch.start()
                    for i,submatch in enumerate(currentMatch.groups()):    
                        tok = currentRule['token'][i%len(currentRule['token'])]        
                        Output = Output[:pos] + Tokencode[tok] * len(submatch) + Output[pos + len(submatch):]
                        pos += len(submatch)

                currentPosition = currentMatch.end()
                currentState = currentRule['next']

            else:
                flag = True

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



    #######################################################################################
    #######################################################################################
    #######################################################################################