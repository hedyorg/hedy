from tests.Highlighter import HighlightTester

class HighlighterTestLeveL6(HighlightTester):


    def test_1(self):
        self.assertHighlightedChr(
            "print '5 times 5 is ' 5 * 5",
            "KKKKK SSSSSSSSSSSSSSS N K N",
            level="level6",lang='en')


    def test_2(self):
        self.assertHighlightedChrMultiLine(
            "print '5 plus 5 is ' 5 + 5",
            "KKKKK SSSSSSSSSSSSSS N K N",
            "print '5 minus 5 is ' 5 - 5",
            "KKKKK SSSSSSSSSSSSSSS N K N",
            "print '5 times 5 is ' 5 * 5",
            "KKKKK SSSSSSSSSSSSSSS N K N",
            level="level6",lang='en')


    def test_3(self):
        self.assertHighlightedChrMultiLine(
            "name = Hedy",
            "TTTT K TTTT",
            "answer = 20 + 4",
            "TTTTTT K NN K N",
            level="level6",lang='en')


    def test_4(self):
        self.assertHighlightedChrMultiLine(
            "verse = 99",
            "TTTTT K NN",
            "print verse ' bottles of beer on the wall'",
            "KKKKK TTTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print verse ' bottles of beer'",
            "KKKKK TTTTT SSSSSSSSSSSSSSSSSS",
            "print 'Take one down, pass it around'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "verse = verse - 1",
            "TTTTT K TTTTT K N",
            "print verse ' bottles of beer on the wall'",
            "KKKKK TTTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_5(self):
        self.assertHighlightedChr(
            "print 'Baby shark'",
            "KKKKK SSSSSSSSSSSS",
            level="level6",lang='en')


    def test_6(self):
        self.assertHighlightedChrMultiLine(
            "angles = ask 'How many angles do you want?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "angle = 360 / angles",
            "TTTTT K NNN K TTTTTT",
            "forward 50",
            "KKKKKKK NN",
            "turn angle",
            "KKKK TTTTT",
            "forward 50",
            "KKKKKKK NN",
            "turn angle",
            "KKKK TTTTT",
            "forward 50",
            "KKKKKKK NN",
            "turn angle",
            "KKKK TTTTT",
            "forward 50",
            "KKKKKKK NN",
            "turn angle",
            "KKKK TTTTT",
            "forward 50",
            "KKKKKKK NN",
            "turn angle",
            "KKKK TTTTT",
            "forward 50",
            "KKKKKKK NN",
            "turn angle",
            "KKKK TTTTT",
            level="level6",lang='en')


    def test_7(self):
        self.assertHighlightedChr(
            "print 'Drawing figures'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_8(self):
        self.assertHighlightedChrMultiLine(
            "people = mom, dad, Emma, Sophie",
            "TTTTTT K TTTK TTTK TTTTK TTTTTT",
            "emma_washes = 0",
            "TTTTTTTTTTT K N",
            "dishwasher = people at random",
            "TTTTTTTTTT K TTTTTT KK KKKKKK",
            "print 'The dishwasher is' dishwasher",
            "KKKKK SSSSSSSSSSSSSSSSSSS TTTTTTTTTT",
            "if dishwasher is Emma emma_washes = emma_washes + 1",
            "KK TTTTTTTTTT KK TTTT TTTTTTTTTTT K TTTTTTTTTTT K N",
            "print 'Emma will do the dishes this week' emma_washes 'times'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTTTTTT SSSSSSS",
            level="level6",lang='en')


    def test_9(self):
        self.assertHighlightedChrMultiLine(
            "people = mom, dad, Emma, Sophie",
            "TTTTTT K TTTK TTTK TTTTK TTTTTT",
            "dishwasher = people at random",
            "TTTTTTTTTT K TTTTTT KK KKKKKK",
            "print 'Monday the dishes are done by: ' dishwasher",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTTTTT",
            "remove dishwasher from people",
            "KKKKKK TTTTTTTTTT KKKK TTTTTT",
            "dishwasher = people at random",
            "TTTTTTTTTT K TTTTTT KK KKKKKK",
            "print 'Tuesday the dishes are done by: ' dishwasher",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS           ",
            "remove dishwasher from people",
            "KKKKKK TTTTTTTTTT KKKK TTTTTT",
            "dishwasher = people at random",
            "TTTTTTTTTT K TTTTTT KK KKKKKK",
            level="level6",lang='en')


    def test_10(self):
        self.assertHighlightedChr(
            "print 'Who does the dishes?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_11(self):
        self.assertHighlightedChrMultiLine(
            "choices = 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT K NK NK NK NK NK TTTTTTTTT",
            "points = 0",
            "TTTTTT K N",
            "throw = choices at random",
            "TTTTT K TTTTTTT KK KKKKKK",
            "print 'you threw' throw",
            "KKKKK SSSSSSSSSSS TTTTT",
            "if throw is earthworm points = points + 5 else points = points + throw",
            "KK TTTTT KK TTTTTTTTT TTTTTT K TTTTTT K N KKKK TTTTTT K TTTTTT K TTTTT",
            "print 'those are' points ' point'",
            "KKKKK SSSSSSSSSSS TTTTTT SSSSSSSS",
            level="level6",lang='en')


    def test_12(self):
        self.assertHighlightedChr(
            "print 'What will the die indicate this time?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_13(self):
        self.assertHighlightedChrMultiLine(
            "correct_answer = 11 * 27",
            "TTTTTTTTTTTTTT K NN K NN",
            "answer = ask 'How much is 11 times 27?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if answer is correct_answer print 'good job!'",
            "KK TTTTTT KK TTTTTTTTTTTTTT KKKKK SSSSSSSSSSS",
            "else print 'Wrong! It was ' correct_answer",
            "KKKK KKKKK SSSSSSSSSSSSSSSS TTTTTTTTTTTTTT",
            level="level6",lang='en')


    def test_14(self):
        self.assertHighlightedChrMultiLine(
            "tables = 4, 5, 6, 8",
            "TTTTTT K NK NK NK N",
            "numbers = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
            "TTTTTTT K NK NK NK NK NK NK NK NK NK NN",
            "table = tables at random",
            "TTTTT K TTTTTT KK KKKKKK",
            "number = numbers at random",
            "TTTTTT K TTTTTTT KK KKKKKK",
            "correct_answer = table * number",
            "TTTTTTTTTTTTTT K TTTTT K TTTTTT",
            "answer = ask 'how much is ' table ' times ' number '?'",
            "TTTTTT K KKK SSSSSSSSSSSSSS TTTTT SSSSSSSSS TTTTTT SSS",
            "if answer is correct_answer print 'okay'",
            "KK TTTTTT KK TTTTTTTTTTTTTT KKKKK SSSSSS",
            "else print 'mistake! it was ' correct_answer",
            "KKKK KKKKK SSSSSSSSSSSSSSSSSS TTTTTTTTTTTTTT",
            level="level6",lang='en')


    def test_15(self):
        self.assertHighlightedChr(
            "print 'Welcome to this calculator!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_16(self):
        self.assertHighlightedChrMultiLine(
            "print 'Welcome to Hedys restaurant'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Here is our menu:'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            "print 'Our main courses are pizza, lasagne, or spaghetti'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "main = ask 'Which main course would you like?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "price = 0",
            "TTTTT K N",
            "if main is pizza price = 10",
            "KK TTTT KK TTTTT TTTTT K NN",
            "if main is lasagne price = 12",
            "KK TTTT KK TTTTTTT TTTTT K NN",
            "if main is spaghetti price = 8",
            "KK TTTT KK TTTTTTTTT TTTTT K N",
            "print 'You have ordered ' main",
            "KKKKK SSSSSSSSSSSSSSSSSSS TTTT",
            "print 'That will be ' price ' dollars, please'",
            "KKKKK SSSSSSSSSSSSSSS TTTTT SSSSSSSSSSSSSSSSSS",
            "print 'Thank you, enjoy your meal!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_17(self):
        self.assertHighlightedChrMultiLine(
            "print 'Welcome to Hedys restaurant'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Here is our menu:'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            "print 'Our starters are salad, soup, or carpaccio'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Our main courses are pizza, lasagne, or spaghetti'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Our desserts are brownie, icecream, or milkshake'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "starter = ask 'Which starter would you like to have?'",
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "main = ask 'Which main course would you like?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "dessert = ask 'Which dessert do you pick?'",
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "price = 0",
            "TTTTT K N",
            "if starter is soup price = price + 6 else price = price + 7",
            "KK TTTTTTT KK TTTT TTTTT K TTTTT K N KKKK TTTTT K TTTTT K N",
            "if main is pizza price = price + 10",
            "KK TTTT KK TTTTT TTTTT K TTTTT K NN",
            "if main is lasagne price = price + 12",
            "KK TTTT KK TTTTTTT TTTTT K TTTTT K NN",
            "if main is spaghetti price = price + 8",
            "KK TTTT KK TTTTTTTTT TTTTT K TTTTT K N",
            "if dessert is brownie price = price + 7",
            "KK TTTTTTT KK TTTTTTT TTTTT K TTTTT KNN",
            "if dessert is icecream price = price + 5",
            "KK TTTTTTT KK TTTTTTTT TTTTT K TTTTT K N",
            "if dessert is milkshake price = price + 4",
            "KK TTTTTTT KK TTTTTTTTT TTTTT K TTTTT K N",
            "print 'You have ordered ' starter ' , ' main ' and ' dessert",
            "KKKKK SSSSSSSSSSSSSSSSSSS TTTTTTT SSSSS TTTT SSSSSSS TTTTTTT",
            "print 'That will be ' price ' dollars, please'",
            "KKKKK SSSSSSSSSSSSSSS TTTTT SSSSSSSSSSSSSSSSSS",
            "print 'Thank you, enjoy your meal!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_18(self):
        self.assertHighlightedChr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level6",lang='en')


    def test_19(self):
        self.assertHighlightedChrMultiLine(
            "print 'I am Hedy the fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I can predict how many kids youll get when you grow up!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "age = ask 'How old are you?'",
            "TTT K KKK SSSSSSSSSSSSSSSSSS",
            "siblings = ask 'How many siblings do you have?'",
            "TTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "length = ask 'How tall are you in centimetres?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "kids = length / age",
            "TTTT K TTTTTT K TTT",
            "kids = kids - siblings",
            "TTTT K TTTT K TTTTTTTT",
            "print 'You will get ...'",
            "KKKKK SSSSSSSSSSSSSSSSSS",
            "sleep",
            "KKKKK",
            "print kids ' kids!'",
            "KKKKK TTTT SSSSSSSS",
            "print 'Im Hedy the silly fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I will predict how smart you are!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "football = ask 'On a scale 1-10 how much do you love football?'",
            "TTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "bananas = ask 'How many bananas did you eat this week?'",
            "TTTTTTT KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "hygiene = ask 'How many times did you wash your hands today?'",
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "result = bananas + hygiene",
            "TTTTTT K TTTTTTT K TTTTTTT",
            "result = result * football",
            "TTTTTT K TTTTTT K TTTTTTTT",
            "print 'You are ' result ' percent smart.'",
            "KKKKK SSSSSSSSSS TTTTTT SSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_20(self):
        self.assertHighlightedChrMultiLine(
            "print 'happy birthday to you'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            "print 'happy birthday to you'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            "print 'happy birthday dear Hedy'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'happy birthday to you'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            level="level6",lang='en')


    def test_21(self):
        self.assertHighlightedChr(
            "print 'On to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            level="level6",lang='en')