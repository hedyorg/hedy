
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
    for reg in regRule:
        regComp = re.compile(reg["regex"], re.MULTILINE)
        for match in regComp.finditer(Code):
            pos = match.start()
            for i,submatch in enumerate(match.groups()):
                tok = reg['token'][i%len(reg['token'])]
                Output = Output[:pos] + TokenCode[tok] * len(submatch) + Output[pos + len(submatch):]
                pos += len(submatch)

    return Output


