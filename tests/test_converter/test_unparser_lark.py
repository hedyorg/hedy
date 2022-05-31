from tests.Tester import HedyTester
import converter_unparser as unparser

# In this testfile the tests are based on Lark. This will give a clearer view
# of what is possible in grammars, and what isn't.
# The contents of this testfile can therefore be seen as unit tests. where
# small sections of code are tested.

class TestsUnparserLark(HedyTester):
    def test_multi(self):
        input = "rule : thing \n | other".split('\n')
        expected = ["rule : thing   | other"]
        output = unparser.first_pass(input)
        self.assertEqual(expected, output)

    #foo | _bar | _this => foo | _bar hasn't been implemented, it caused errors.
    def test_simplify(self):
        input = {"plus":"_foo+", "question":"_foo?", "star":"_foo*", "options":"foo | _bar?"}
        expected = {"plus":"_foo", "question":"", "star":"", "options":"foo | \"\""}
        output = unparser.simp_grammar(input)
        self.assertEqual(expected, output)
