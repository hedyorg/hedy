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

        result = self.simulateRulesWithToken(rules,code)

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






    def simulateRulesWithToken(self,Rules,code):
        T = Tokenizer(Rules)
        Outputs = []
        token = "start"
        for line in code.split("\n"):
            output,token = T.getLineHighlight(Rules,line,token)
            Outputs.append(output)
        return "\n".join(Outputs)



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


class Tokenizer:
    """docstring for Tokenizer"""
    def __init__(self, rules):
        self.states = rules
        self.regExps = {}
        self.matchMappings = {}

        for key in self.states:

            state = self.states[key]
            ruleRegExps = []
            matchTotal = 0
            mapping = {"defaultToken": "text"}
            self.matchMappings[key] = {"defaultToken": "text"}
            
            flag = "g"

            splitterRurles = []
            for i in range(len(state)):
                rule = state[i]
                if rule.get('defaultToken',False) :
                    mapping['defaultToken'] = rule['defaultToken']
                if rule.get('caseInsensitive',False) and "i" not in flag:
                    flag += "i"
                if rule.get('unicode',False) and "u" not in flag:
                    flag += "u"
                # if (rule.regex == null)
                #     continue


                # Count number of matching groups. 2 extra groups from the full match
                # And the catch-all on the end (used to force a match)
                adjustedregex = rule["regex"]
                matchcount = re.compile(adjustedregex).groups
                if type(rule['token']) == list:
                    if len(rule['token']) == 1 or matchcount == 1:
                        rule['token'] = rule['token'][0]
                    elif 

                if (matchcount > 1) {
                    if (/\\\d/.test(rule.regex)) {
                        # Replace any backreferences and offset appropriately.
                        adjustedregex = rule.regex.replace(/\\([0-9]+)/g, function(match, digit) {
                            return "\\" + (parseInt(digit, 10) + matchTotal + 1)
                        })
                    } else {
                        matchcount = 1
                        adjustedregex = self.removeCapturingGroups(rule.regex)
                    }
                    if (!rule.splitRegex && typeof rule.token != "string")
                        splitterRurles.push(rule); # flag will be known only at the very end
                }

                mapping[matchTotal] = i
                matchTotal += matchcount

                ruleRegExps.push(adjustedregex)

                # makes property access faster
                if (!rule.onMatch)
                    rule.onMatch = null
            

            if (!ruleRegExps.length) {
                mapping[0] = 0
                ruleRegExps.push("$")
            }

            splitterRurles.forEach(function(rule) {
                rule.splitRegex = self.createSplitterRegexp(rule.regex, flag)
            }, this)
            console.log('Create Nex Regex')
            self.regExps[key] = new RegExp("(" + ruleRegExps.join(")|(") + ")|($)", flag)
        


    def getLineTokens(self,line,startState="start"):
        pass

    def getLineHighlight(self,line,startState="start"):
        pass