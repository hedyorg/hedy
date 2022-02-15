import textwrap

import hedy
from test_level_01 import HedyTester
import hedy_translation

    # tests should be ordered as follows:
    # * Translation from English to Dutch
    # * Translation from Dutch to English
    # * Translation to several languages
    # * Error handling

class TestsTranslationLevel4(HedyTester):
    level = 4

    def test_print(self):
        code = "print 'Hello welcome to Hedy.'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print 'Hello welcome to Hedy.'"

        self.assertEqual(expected, result)

    def test_assign(self):
        code = "name is Hedy"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "name is Hedy"

        self.assertEqual(expected, result)

    def test_print_assign(self):
        code = "print 'my name is ' name"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "print 'my name is ' name"

        self.assertEqual(expected, result)

    def test_ask(self):
        code = "color is ask 'What is your favorite color?'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "color is vraag 'What is your favorite color?'"

        self.assertEqual(expected, result)

    def test_ask_vraag_var_name(self):
        code = "vraag is ask 'What is your favorite color?'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "vraag is vraag 'What is your favorite color?'"

        self.assertEqual(expected, result)

    def test_ask_vraag_var_name_reverse(self):
        code = "ask is ask 'What is your favorite color?'"

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = "ask is vraag 'What is your favorite color?'"

        self.assertEqual(expected, result)

    def test_ask_vraag_var_name_reverse(self):
        code = textwrap.dedent("""\
        print 'Im Hedy the fortune teller!'
        ask is ask 'What do you want to know?'
        print 'This is your question: ' question
        answers is yes, no, maybe
        print 'My crystal ball says...'
        sleep 2
        print answers at random""")

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = textwrap.dedent("""\
        print 'Im Hedy the fortune teller!'
        ask is vraag 'What do you want to know?'
        print 'This is your question: ' question
        answers is yes, no, maybe
        print 'My crystal ball says...'
        slaap 2
        print answers op willekeurig""")

        self.assertEqual(expected, result)

    def test_print_nl_en(self):
        code = "print 'Hello welcome to Hedy.'"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print 'Hello welcome to Hedy.'"

        self.assertEqual(expected, result)

    def test_assign_nl_en(self):
        code = "name is Hedy"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "name is Hedy"

        self.assertEqual(expected, result)

    def test_print_assign_nl_en(self):
        code = "print 'my name is ' name"

        result = hedy_translation.translate_keywords(code, "nl", "en", self.level)
        expected = "print 'my name is ' name"

        self.assertEqual(expected, result)

    def test_add_remove_en_nl(self):
        code = textwrap.dedent("""\
        dieren is koe, kiep
        add muis to dieren
        remove koe from dieren
        print dieren at random""")

        result = hedy_translation.translate_keywords(code, "en", "nl", self.level)
        expected = textwrap.dedent("""\
        dieren is koe, kiep
        voeg muis toe aan dieren
        verwijder koe uit dieren
        print dieren op willekeurig""")

        self.assertEqual(expected, result)