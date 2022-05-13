from tests.Highlighter import HighlightTester

class HighlighterTestLeveL7(HighlightTester):


    def test_1(self):
        self.assert_highlighted_chr(
            "repeat 3 times print 'Hedy is fun!'",
            "KKKKKK N KKKKK KKKKK SSSSSSSSSSSSSS",
            level="level7",lang='en')


    def test_2(self):
        self.assert_highlighted_chr_multi_line(
            "print 'The prince kept calling for help'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "repeat 5 times print 'Help!'",
            "KKKKKK N KKKKK KKKKK SSSSSSS",
            "print 'Why is nobody helping me?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7",lang='en')


    def test_3(self):
        self.assert_highlighted_chr(
            "repeat 5 times print 'Help!'",
            "KKKKKK N KKKKK KKKKK SSSSSSS",
            level="level7",lang='en')


    def test_4(self):
        self.assert_highlighted_chr_multi_line(
            "repeat _ _ print 'Baby Shark tututudutudu'",
            "KKKKKK I I KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Baby Shark'",
            "KKKKK SSSSSSSSSSSS",
            level="level7",lang='en')


    def test_5(self):
        self.assert_highlighted_chr(
            "print 'Baby Shark'",
            "KKKKK SSSSSSSSSSSS",
            level="level7",lang='en')


    def test_6(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Draw figures'",
            "KKKKK SSSSSSSSSSSSSS",
            "repeat 3 times forward 10",
            "KKKKKK N KKKKK KKKKKKK NN",
            level="level7",lang='en')


    def test_7(self):
        self.assert_highlighted_chr_multi_line(
            "people = mom, dad, Emma, Sophie",
            "TTTTTT K TTTK TTTK TTTTK TTTTTT",
            "repeat _ _ print 'the dishwasher is' _",
            "KKKKKK I I KKKKK SSSSSSSSSSSSSSSSSSS I",
            level="level7",lang='en')


    def test_8(self):
        self.assert_highlighted_chr(
            "print 'Who does the dishes?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level7",lang='en')


    def test_9(self):
        self.assert_highlighted_chr_multi_line(
            "choices = 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT K NK NK NK NK NK TTTTTTTTT",
            "repeat _ _ print _ _ _",
            "KKKKKK I I KKKKK I I I",
            level="level7",lang='en')


    def test_10(self):
        self.assert_highlighted_chr(
            "print 'What will the die indicate this time?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7",lang='en')


    def test_11(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome to Hedys restaurant!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "people = ask 'How many people are joining us today?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "repeat people times food = ask 'What would you like to eat?'",
            "KKKKKK TTTTTT KKKKK TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Thanks for your order! Its coming right up!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7",lang='en')


    def test_12(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level7",lang='en')


    def test_13(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Im Hedy the fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You can ask 3 questions!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "repeat 3 times question = ask 'What do you want to know?'",
            "KKKKKK N KKKKK TTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "answer = yes, no, maybe",
            "TTTTTT K TTTK TTK TTTTT",
            "repeat 3 times print 'My crystal ball says... ' answer at random",
            "KKKKKK N KKKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTT KK KKKKKK",
            level="level7",lang='en')


    def test_14(self):
        self.assert_highlighted_chr(
            "repeat 5 times print 'In the next level you can repeat multiple lines of code at once!'",
            "KKKKKK N KKKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7",lang='en')


    def test_15(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7",lang='en')

