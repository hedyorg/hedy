from tests.Highlighter import HighlightTester

class HighlighterTestLeveL8(HighlightTester):

    def test_1(self):
        self.assertHighlightedChrMultiLine(
            "repeat 5 times",
            "KKKKKK N KKKKK",
            "print 'Hello folks'",
            "KKKKK SSSSSSSSSSSSS",
            "print 'This will be printed 5 times'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8",lang='en')


    def test_2(self):
        self.assertHighlightedChrMultiLine(
            "repeat 5 times",
            "KKKKKK N KKKKK",
            "print 'Hello everyone'",
            "KKKKK SSSSSSSSSSSSSSSS",
            "print 'This is all repeated 5 times'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8",lang='en')


    def test_3(self):
        self.assertHighlightedChrMultiLine(
            "print 'OH NO! The T-rex is closing in!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "end = ask 'Do you want a happy or a sad ending?'",
            "TTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if end is happy",
            "KK TTT KK TTTTT",
            "print 'Just in time Richard jumps back into the time machine!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Michael types in the code and...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print '💥ZAP!💥'",
            "KKKKK SSSSSSSS",
            "print 'They are back in their garage'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Michael yells COME ON RICHARD! RUN FASTER!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'But Richard is too slow...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'The T-rex closes in and eats him in one big bite!🦖'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8",lang='en')


    def test_4(self):
        self.assertHighlightedChr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level8",lang='en')


    def test_5(self):
        self.assertHighlightedChrMultiLine(
            "verse = 99",
            "TTTTT K NN",
            "repeat 99 times",
            "KKKKKK NN KKKKK",
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
            level="level8",lang='en')


    def test_6(self):
        self.assertHighlightedChrMultiLine(
            "angle = 90",
            "TTTTT K NN",
            "repeat 10 times",
            "KKKKKK NN KKKKK",
            "turn angle",
            "KKKK TTTTT",
            "forward 50",
            "KKKKKKK NN",
            level="level8",lang='en')


    def test_7(self):
        self.assertHighlightedChrMultiLine(
            "angles = ask 'How many angles should I draw?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "angle = 360 / angles",
            "TTTTT K NNN K TTTTTT",
            "repeat angle times",
            "KKKKKK TTTTT KKKKK",
            "turn _",
            "KKKK I",
            "forward _",
            "KKKKKKK I",
            level="level8",lang='en')


    def test_8(self):
        self.assertHighlightedChr(
            "hoeken = ask 'How many angles should I draw?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8",lang='en')


    def test_9(self):
        self.assertHighlightedChrMultiLine(
            "print 'Welcome to Hedys restaurant!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "people = ask 'How many people will be joining us today?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Great!'",
            "KKKKK SSSSSSSS",
            "repeat people times",
            "KKKKKK TTTTTT KKKKK",
            "food = ask 'What would you like to order?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print food",
            "KKKKK TTTT",
            "print 'Thank you for ordering!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Enjoy your meal!'",
            "KKKKK SSSSSSSSSSSSSSSSSS",
            level="level8",lang='en')


    def test_10(self):
        self.assertHighlightedChrMultiLine(
            "print 'I am Hedy the fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You can ask me 3 questions.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "answers = yes, no, maybe",
            "TTTTTTT K TTTK TTK TTTTT",
            "repeat 3 times",
            "KKKKKKNNKKKKKK",
            "question = ask 'What do you want to know?'",
            "TTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print question",
            "KKKKK TTTTTTTT",
            "sleep",
            "KKKKK",
            "print 'My crystal ball says...' answers at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTT KK KKKKKK",
            level="level8",lang='en')


    def test_11(self):
        self.assertHighlightedChrMultiLine(
            "answer = ask 'Would you like to go to the next level?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if answer is yes",
            "KK TTTTTT KK TTT",
            "print 'Great! You can use the repeat commando in the if command!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Hooray!'",
            "KKKKK SSSSSSSSS",
            "print 'Hooray!'",
            "KKKKK SSSSSSSSS",
            "print 'Hooray!'",
            "KKKKK SSSSSSSSS",
            "else",
            "KKKK",
            "print 'Okay, you can stay here for a little longer!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8",lang='en')


    def test_12(self):
        self.assertHighlightedChr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8",lang='en')