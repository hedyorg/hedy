import json

# open data for regex
file = open('data.json') 
dataRegex = json.load(file)
file.close()

# open data for tests
file = open('tests.json') 
dataTests = json.load(file)
file.close()

#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################

import re


TokenCode = {
    "text" :               'T',
    "keyword" :            'K',
    "comment" :            'C',
    "variable" :           'N',
    "constant.character" : 'S',
    "invalid" :            'I',
}


def simulateRulesWithoutToken(Rules,Code):
    Output = ""
    for c in Code:
        if c == "\n": Output += "\n"
        else: Output += " "
    regRule = Rules["start"][0]
    for reg in regRule[::-1]:

        if type(reg['token']) == str or len(reg['token']) == 1: # case without groups

            if  type(reg['token']) == str : TokCode = TokenCode[reg['token']]
            else: TokCode = TokenCode[reg['token'][0]]

            regComp = re.compile(reg["regex"], re.MULTILINE)
            for match in regComp.finditer(Code):
                start = match.start()
                length = match.end() -start
                Output = Output[:start] + TokCode * length + Output[start + length:]

        else: # case with groups
            regComp = re.compile(reg["regex"], re.MULTILINE)
            for match in regComp.finditer(Code):
                pos = match.start()
                for i,submatch in enumerate(match.groups()):
                    tok = reg['token'][i%len(reg['token'])]
                    Output = Output[:pos] + TokenCode[tok] * len(submatch) + Output[pos + len(submatch):]
                    pos += len(submatch)

    return Output


#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################


def compare(Result,Expected):
    for i,ch in enumerate(Expected):
        if ch not in [" ","\n"]:
            if ch == "T" and Result[i] == " ":
                pass
            elif ch != Result[i]:
                return False
    return True



def run(test):

    # get rules for the level
    Rules = [item for item in dataRegex if item['name']==test['level']]
    if len(Rules) != 1 : exit()
    else : Rules = Rules[0]['rules']

    Code = test['code']
    Expected = test['result']

    Result = simulateRulesWithoutToken(Rules,Code)

    b = compare(Result,Expected)

    if not b:
        print("ERROR :")
        print("In this Code :",Code.replace("\n","\\n"))
        print("We want      :",Expected.replace("\n","\\n"))
        print("We have      :",Result.replace("\n","\\n"))
        exit()
    else:
        pass
        print("WORK :")
        print("In this Code :",Code.replace("\n","\\n"))
        print("We want      :",Expected.replace("\n","\\n"))
        print("We have      :",Result.replace("\n","\\n"))
        print("")



for test in dataTests:
    run(test)

print("Done !")
