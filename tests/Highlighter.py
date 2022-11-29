import regex as re
import json
import os
import unittest

# Transcription of the used tokens into a symbol (a letter) in order to apply a coloring
TOKEN_CODE = {
    "text": 'T',  # normal
    "keyword": 'K',
    "comment": 'C',
    "variable": 'N',
    "constant.character": 'S',
    "invalid": 'I',
}

# for the caractere SPACE, all this highlights are equals
SAME_COLOR_FOR_SPACE = ['T', 'K', 'C', 'N', 'S']

ABBREVIATION = {
    "text": "T",
    "uncolor": "T",
    "txt": "T",
    "white": "T",
    "T": "T",

    "keyword": "K",
    "kw": "K",
    "red": "K",
    "K": "K",

    "comment": "C",
    "cmt": "C",
    "grey": "C",
    "C": "C",

    "variable": "N",
    "number": "N",
    "green": "N",
    "N": "N",

    "constant.character": "S",
    "string": "S",
    "str": "S",
    "blue": "S",
    "S": "S",

    "invalid": "I",
    "inv": "I",
    "pink": "I",
    "I": "I",
}


class HighlightTester(unittest.TestCase):

    def assert_highlighted_chr(
            self,
            code,
            expected,
            level,
            lang="en",
            start_token="start",
            last_state="start",
            intermediate_tests=True):
        """Test if the code has the expected coloring on one line

        Arguments :
            - code : str, Ex: "print Welcome to Hedy!"
            - expected : str, Ex: "KKKKK TTTTTTTTTTTTTTTT"
            - level : str, between "level1" and "level18"
            - lang : str, code of language
            - start_token : str, token for beginning of the highlighting
            - last_token : str, token for the end of the highlighting
                                if last_token == None, ignore the end state test
            - intermediate_tests : boolean, execution of tests on the consistency
                                            of the input word by word or not
        """
        state_machine = self.get_state_machine(level, lang)
        self.check(code + "\n", expected + "\n", state_machine, start_token, last_state)
        if intermediate_tests:
            self.checkInter(code, expected, state_machine, start_token)

    def assert_highlighted_chr_multi_line(
            self,
            *args,
            level,
            lang="en",
            start_token="start",
            last_state="start",
            intermediate_tests=True):
        """Test if the code has the expected coloring on several lines

        Arguments :
            - *args : list of str, With alternating code and syntax highlighting Ex:
                "name is ask 'what is your name?'",
                "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
                "if name is Hedy print 'nice' else print 'boo!'",
                "KK TTTT KK TTTT KKKKK SSSSSS KKKK KKKKK SSSSSS",
            - level : str, between "level1" and "level18"
            - lang : str, code of language
            - start_token : str, token for beginning of the highlighting
            - last_token : str, token for the end of the highlighting
                                if last_token == None, ignore the end state test
            - intermediate_tests : boolean, execution of tests on the consistency
                                            of the input word by word or not
        """
        if len(args) % 2 != 0:
            raise RuntimeError(
                f'Pass an even number of strings to assert_highlighted_chr_multi_line\
                  (alternatingly code and highlighting). Got: {args}')

        code = '\n'.join(line for i, line in enumerate(args) if i % 2 == 0)
        expected = '\n'.join(line for i, line in enumerate(args) if i % 2 != 0)

        self.assert_highlighted_chr(
            code,
            expected,
            level,
            lang,
            start_token,
            last_state,
            intermediate_tests)

    def assert_highlighted(
            self,
            code_coloration,
            level,
            lang="en",
            start_token="start",
            last_state="start",
            intermediate_tests=True):
        """Test if the code has the expected coloring on one line

        Arguments :
            - code_coloration : str, Ex: "{print|kw} {Welcome to Hedy!|txt}"
            - level : str, between "level1" and "level18"
            - lang : str, code of language
            - start_token : str, token for beginning of the highlighting
            - last_token : str, token for the end of the highlighting
                                if last_token == None, ignore the end state test
            - intermediate_tests : boolean, execution of tests on the consistency
                                            of the input word by word or not
        """
        code, expected = self.convert(code_coloration)
        self.assert_highlighted_chr(
            code,
            expected,
            level,
            lang,
            start_token,
            last_state,
            intermediate_tests)

    def assert_highlighted_multi_line(
            self,
            *args,
            level,
            lang="en",
            start_token="start",
            last_state="start",
            intermediate_tests=True):
        """Test if the code has the expected coloring on several lines

        Arguments :
            - *args : list of str, Ex: "{print|kw} {Welcome to Hedy!|txt}"
            - level : str, between "level1" and "level18"
            - lang : str, code of language
            - start_token : str, token for beginning of the highlighting
            - last_token : str, token for the end of the highlighting
                                if last_token == None, ignore the end state test
            - intermediate_tests : boolean, execution of tests on the consistency
                                            of the input word by word or not
        """
        code_coloration = "\n".join(args)
        code, expected = self.convert(code_coloration)
        self.assert_highlighted_chr(
            code,
            expected,
            level,
            lang,
            start_token,
            last_state,
            intermediate_tests)

    def checkInter(self, code, expected, state_machine, start_token="start"):
        """Check the highlighting on the intermediate states

        check intermediate tests, word by word, to make
        sure that the highlighting when typing the code will be consistent.

        Arguments :
            - code : str, The code you want to color
            - expected : str, The expected coloring, character by character,
                with the code described here TOKEN_CODE
            - state_machine : a state_machine
            - start_token : str, token for beginning of the highlighting
        """

        listCode, listExpected = genInterTest(code, expected)

        for n in range(len(listCode)):
            self.check(listCode[n], listExpected[n], state_machine, start_token, None)

    def check(self, code, expected, state_machine, start_token="start", last_state='start'):
        """Apply state_machine on code and check if the result is valid

        Arguments :
            - code : str, The code you want to color
            - expected : str, The expected coloring, character by character,
                with the code described here TOKEN_CODE
            - state_machine : a state_machine
            - start_token : str, token for beginning of the highlighting
            - last_token : str, token for the end of the highlighting
                                if last_token == None, ignore the end state test

        Computes the syntax highlighting of the code from the state_machine,
        and compares with the expected highlighting.
        """
        simulator = SimulatorAce(state_machine)
        result, last_state_result = simulator.highlight(code, start_token)

        result = list(result)
        expected = list(expected)

        # check if they are same length
        self.assertEqual(len(result), len(expected))

        # replacement of space by result coloration
        for i in range(len(result)):
            if code[i] == " ":
                # coloration in space are same
                self.assertIn(result[i], SAME_COLOR_FOR_SPACE)
                result[i] = expected[i]

        result = "".join(result)
        expected = "".join(expected)

        # test between two coloration
        self.assertEqual(result, expected)

        # test for last state
        if last_state is not None:
            self.assertEqual(last_state, last_state_result)

    def get_state_machine(self, level, lang="en"):
        """Recovery of syntax coloring rules.

        Recovery of syntax coloring rules from `highlighting-trad.json`
        and `highlighting.json` files and mixes

        Arguments :
            - level : str, between "level1" and "level18"
            - lang : str, code of language

        Returns a state machine.
        """
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        trad_file = os.path.normpath(root_dir + '/highlighting/highlighting-trad.json')

        # get traduction
        with open(trad_file, 'r', encoding='utf-8') as file_regex_trad:
            data_regex_trad = json.load(file_regex_trad)

        if lang not in data_regex_trad.keys():
            lang = 'en'

        regex_trad = data_regex_trad[lang]

        # get state_machine
        sm_file = os.path.normpath(root_dir + '/highlighting/highlighting.json')
        with open(sm_file, 'r', encoding='utf-8') as file_regex:
            data_regex = json.load(file_regex)

        # apply translation of keywords
        for lvl_rules in data_regex:
            for state in lvl_rules["rules"]:
                for rule in lvl_rules["rules"][state]:
                    for key in regex_trad:
                        rule['regex'] = rule['regex'].replace("__" + key + "__", regex_trad[key])

        # get state_machine for the level
        state_machine = [item for item in data_regex if item['name'] == level]
        if len(state_machine) != 1:
            raise RuntimeError(f'Expected exactly 1 rule with {level}, got {len(state_machine)}')
        else:
            state_machine = state_machine[0]['rules']
        return state_machine

    def convert(self, code_coloration):
        """Conversion of the test specification format.

        The description of the codes is provided in the variable ABBREVIATION

        Arguments :
            - code_coloration : str, Ex: "{print|kw} {Welcome to Hedy!|txt}"

        Returns (code, coloration):
            - code       : str, Ex : "print Welcome to Hedy!",
            - coloration : str, Ex : "KKKKK TTTTTTTTTTTTTTTT",
        """

        code = []
        coloring = []
        TEXT, CODE, KEYWORD = range(3)
        state = TEXT
        for ch in code_coloration:
            if ch == "{":
                state = CODE

                tmp_code = []
                tmp_coloring = []
            elif ch == "}":
                state = TEXT

                code.append("".join(tmp_code))
                coloring.append(ABBREVIATION["".join(tmp_coloring)] * len(tmp_code))

            elif ch == "|" and state == CODE:
                state = KEYWORD

            else:  # not a special symbol

                if state == CODE:
                    tmp_code.append(ch)
                elif state == KEYWORD:
                    tmp_coloring.append(ch)

                else:  # state == TEXT
                    if ch == "\n":
                        code.append("\n")
                        coloring.append("\n")
                    else:
                        code.append(ch)
                        coloring.append(" ")

        return "".join(code), "".join(coloring)


def genInterTest(code, expected):
    """generates intermediate tests, word by word,
    to check that the highlighting when
    typing the code will be consistent."""
    C, E = [], []
    codes = [k.split(' ') for k in code.split("\n")]

    currentCode = []

    for nbLine in range(len(codes)):
        currentLine = []

        for nbMot in range(len(codes[nbLine])):
            currentLine.append(codes[nbLine][nbMot])

            # add
            current = "\n".join([" ".join(k) for k in currentCode + [currentLine]])
            C.append(current)
            E.append(expected[:len(current)])

        currentCode.append(currentLine)

    return C, E


class SimulatorAce:

    # constructor of SimulatorAce with check on state_machine
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self._precompile_regexes()

    def _precompile_regexes(self):
        """Initialization and verification of the provided state_machine.

        The provided state_machine must have the following format:
        state_machine = [
            state(string) : list of rules,
            ...
        ]

        And the format of the rules (or transition) is as follows:
        {
            "regex" : str, the regex describing the transition
            "token" : Syntactic colorations, str if regex as no groups. list if regex has 1 or more groups
            "next" : str (optional),
            "default_token" : str (optional),

            # And this method adds:
            "regex_compile" : Regex Object (see : https://docs.python.org/3/library/re.html#regular-expression-objects)
            "nb_groups" : int, number of groups in regex
        }
        """
        for state in self.state_machine:
            for rule in self.state_machine[state]:

                if "token" not in rule:
                    raise ValueError("We need a token in all rules !")

                rule["regex_compile"] = re.compile(rule['regex'], re.MULTILINE)
                rule["nb_groups"] = rule["regex_compile"].groups

                if rule["nb_groups"] == 0:
                    if not isinstance(rule["token"], str):
                        raise ValueError(
                            f"if regex has no groups, token must be a string. In this rule : {rule}!")

                else:
                    if not isinstance(rule["token"], list):
                        raise ValueError(
                            f"if regex has groups, token must be a list. In this rule : {rule}!")

                    else:
                        if rule["nb_groups"] != len(rule["token"]):
                            raise ValueError(
                                f"The number of groups in the regex is different from the number of tokens.\
                                  In this rule : {rule}!")

    def highlight(self, code, start_token="start"):
        """Simulates the application of syntax highlighting state_machine on a code.

        Arguments:
            - code (string): code on which syntax highlighting will be applied.
            - start_token (string) : first token for the beginning of the line

        Returns :
            - string, a character by character coloring, according to the coloring code specified in TOKEN_CODE
            - string, final token for the code
        """
        outputs = []
        token = start_token
        for line in code.split("\n"):
            output, token = self.highlight_rules_line(line, token)
            outputs.append(output)
        return "\n".join(outputs), token

    def highlight_rules_line(self, code, start_token="start"):
        """Simulates the application of syntax highlighting state_machine on a line of code.

        Arguments:
            - code (string): code on which syntax highlighting will be applied.
            - start_token (string): token with which to start the analysis of the line

        Returns :
            - string, a character by character coloring, according to the coloring code specified in TOKEN_CODE
            - string : token for the next line
        """

        # Initialisation output
        output = []

        # Initialisation variables
        current_state = start_token
        current_position = 0

        default_token = "text"

        find_transition, next_transition = self.find_match(code, current_position, current_state)
        while find_transition:

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
                tok = current_rule['token']
                length = current_match.end() - current_match.start()
                output.append(TOKEN_CODE[tok] * length)

            # if rule has only multiples groups
            else:
                pos = current_match.start()
                for i, submatch in enumerate(current_match.groups()):
                    tok = current_rule['token'][i % len(current_rule['token'])]
                    output.append(TOKEN_CODE[tok] * len(submatch))
                    pos += len(submatch)

            # get nexts values
            current_position = current_match.end()

            if 'next' in current_rule:
                current_state = current_rule['next']

            if current_position == len(code):
                find_transition = False
            else:
                find_transition, next_transition = self.find_match(
                    code, current_position, current_state)

        # we color the last characters since the last match with the default coloring
        for c in range(current_position, len(code)):
            output.append(TOKEN_CODE[default_token])

        return "".join(output), current_state

    def find_match(self, code, current_position, current_state):
        """ Find the next matching rule in the given code.

        If there are multiple rules that match the code in the given state,
        returns the one that matches earliest in the source string.

        Arguments:
            - code (string) : the code we're searching
            - current_state (string) : name of the highlight state we are in
            - current_position (int) : index to start searching

        Returns:
            (did_match, transition):
            a tuple of a boolean and a transition dictionary.
            The transition dictionary contains {rule, match} fields and should only be inspected if did_match is True.
        """

        next_transition = {"rule": {}, "match": None}
        find_transition = False

        next_pos = len(code) + 1
        for rule in self.state_machine[current_state]:

            regex_compile = rule["regex_compile"]
            match = regex_compile.search(code, current_position)

            if match:
                if match.start() < next_pos:
                    next_pos = match.start()
                    next_transition["rule"] = rule
                    next_transition["match"] = match
                    find_transition = True

        return find_transition, next_transition
