import hedy
from Tester import HedyTester
import hedy_translation
import textwrap
from parameterized import parameterized

    # tests should be ordered as follows:
    # * Translation from English to Dutch
    # * Translation from Dutch to English
    # * Translation to several languages
    # * Error handling


class TestsTranslationLevel5(HedyTester):
    level = 5
    keywords_from = hedy_translation.keywords_to_dict('en')
    keywords_to = hedy_translation.keywords_to_dict('nl')
    all_keywords = hedy_translation.all_keywords_to_dict()
    
    def test_print_english_dutch(self):
        code = "print 'Hallo welkom bij Hedy!'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "print 'Hallo welkom bij Hedy!'"

        self.assertEqual(expected, result)

    def test_print2_english_dutch(self):
        code = "print Hallo 'welkom bij Hedy!'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "print Hallo 'welkom bij Hedy!'"

        self.assertEqual(expected, result)

    def test_ask_assign_english_dutch(self):
        code = "answer is ask 'What is 10 plus 10?'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "answer is vraag 'What is 10 plus 10?'"

        self.assertEqual(expected, result)

    def test_if_else_english_dutch(self):
        code = "if answer is far forward 100 else forward 5"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "als answer is far vooruit 100 anders vooruit 5"

        self.assertEqual(expected, result)

    def test_in_list_english_dutch(self):
        code = "if color in pretty_colors print 'pretty!'"

        result = hedy_translation.translate_keywords(code, from_lang="en", to_lang="nl", level=self.level)
        expected = "als color in pretty_colors print 'pretty!'"

        self.assertEqual(expected, result)


    def test_print_dutch_english(self):
        code = "print 'Hallo welkom bij Hedy!'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "print 'Hallo welkom bij Hedy!'"

        self.assertEqual(expected, result)

    def test_print2_dutch_english(self):
        code = "print Hallo 'welkom bij Hedy!'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "print Hallo 'welkom bij Hedy!'"

        self.assertEqual(expected, result)

    def test_ask_assign_dutch_english(self):
        code = "answer is vraag 'What is 10 plus 10?'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "answer is ask 'What is 10 plus 10?'"

        self.assertEqual(expected, result)

    def test_2116(self):
        code = textwrap.dedent("""\
            people is mom, dad, Emma, Sophie
            dishwasher is people op willekeurig
            als dishwasher is Sophie
            print 'too bad I have to do the dishes'
            anders
            print 'luckily no dishes because' dishwasher 'is already washing up'""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
            people is mom, dad, Emma, Sophie
            dishwasher is people at random
            if dishwasher is Sophie
            print 'too bad I have to do the dishes'
            else
            print 'luckily no dishes because' dishwasher 'is already washing up'""")

        self.assertEqual(expected, result)

    def test_if_else_dutch_english(self):
        code = textwrap.dedent("als answer is far vooruit 100 anders vooruit 5")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "if answer is far forward 100 else forward 5"

        self.assertEqual(expected, result)

    def test_ifelse_should_go_before_assign(self):
        code = textwrap.dedent("""\
            kleur is geel
            als kleur is groen antwoord is ok anders antwoord is stom
            print antwoord""")

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = textwrap.dedent("""\
            kleur is geel
            if kleur is groen antwoord is ok else antwoord is stom
            print antwoord""")

        self.assertEqual(expected, result)

    def test_in_list_dutch_english(self):
        code = "als hond in dieren print 'Cute!'"

        result = hedy_translation.translate_keywords(code, from_lang="nl", to_lang="en", level=self.level)
        expected = "if hond in dieren print 'Cute!'"

        self.assertEqual(expected, result)

    @parameterized.expand(HedyTester.as_list_of_tuples(all_keywords["if"], all_keywords["print"], all_keywords["is"], all_keywords["else"],hedy_translation.KEYWORD_LANGUAGES))
    def test_print_if_is_else_all_lang(self, if_keyword, print_keyword, is_kwrd, else_kwrd, lang):
        code = f"{if_keyword} name {is_kwrd} Hedy {print_keyword} 'Great!' {else_kwrd} {print_keyword} 'Oh no'"

        result = hedy_translation.translate_keywords(code, from_lang=lang, to_lang="en", level=self.level)
        expected = "if name is Hedy print 'Great!' else print 'Oh no'"

        self.assertEqual(expected, result)

    @parameterized.expand([('en', 'is'), ('es', 'es'), ('es', 'is')])
    def test_equality_type_error_translates_command(self, lang, is_):
        code = textwrap.dedent(f"""\
            letters is a, b, c
            if letters {is_} '10' print 'wrong!'""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=7,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(is_)
        )

    @parameterized.expand([('en', 'in'), ('es', 'en'), ('es', 'in')])
    def test_in_list_type_error_translates_command(self, lang, in_):
        code = textwrap.dedent(f"""\
            letters is 'test'
            if 10 {in_} letters print 'wrong!'""")

        self.multi_level_tester(
            lang=lang,
            code=code,
            max_level=7,
            exception=hedy.exceptions.InvalidArgumentTypeException,
            extra_check_function=self.exception_command(in_)
        )
