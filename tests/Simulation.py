from Highlighter import *

def getRules():

    # open data for regex
    os.chdir(os.path.dirname(__file__) +"/..")
    file = open('highlighting/highlightingRules/highlighting-en.json') 
    dataRegex = json.load(file)
    file.close()

    # get rules for the level
    Rules = [item for item in dataRegex if item['name']=="level1"]
    if len(Rules) != 1 : exit()
    else : Rules = Rules[0]['rules']
    return Rules


highlighttester = HighlightTester()

rule = getRules()
print(rule)
code = """qmczqdqaqmcqbadq
grbnorbTestananaeqwswsmsazqdqaqmcqbadqcc
grbnorbTestananaeqwswsmsazqdqaqmcqbadqcc

grbnorbTestananaeqwswsmsbzqdqaqmcqbadqcc
grbnorbTestananaeqwswsmsazqdqaqmcqbadqcc

grbnorbTestananaeqwswsmsbzqdqaqmcqbadqcc"""


out = highlighttester.simulateRulesWithToken(rule,code)

print(code)#.replace("\n","\\n"))
print(out)#.replace("\n","\\n"))