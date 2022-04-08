import json
from highlighter import simulateRulesWithoutToken

# open data for regex
file = open('data.json') 
dataRegex = json.load(file)
file.close()

# open data for tests
file = open('tests.json') 
dataTests = json.load(file)
file.close()



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
        print("WORK :")
        print("In this Code :",Code.replace("\n","\\n"))
        print("We want      :",Expected.replace("\n","\\n"))
        print("We have      :",Result.replace("\n","\\n"))
        print("")



for test in dataTests:
    run(test)