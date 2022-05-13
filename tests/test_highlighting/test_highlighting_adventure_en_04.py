from tests.Highlighter import HighlightTester

class HighlighterTestLeveL4(HighlightTester):


    def test_1(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Hello world'",
            "KKKKK SSSSSSSSSSSSS",
            level="level4",lang='en')


    def test_2(self):
        self.assert_highlighted_chr_multi_line(
            "print 'You need to use quotation marks from now on!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "answer is ask 'What do we need to use from now on?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'We need to use ' answer",
            "KKKKK SSSSSSSSSSSSSSSSS TTTTTT",
            level="level4",lang='en')


    def test_3(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Your story will be printed here!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='en')


    def test_4(self):
        self.assert_highlighted_chr_multi_line(
            "name is Hans",
            "TTTT KK TTTT",
            "print 'The name of the main character is' name",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTT",
            "print name 'is now going to walk in the woods'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print name 'is a bit scared'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSS",
            "animals is 🦔, 🐿, 🦉, 🦇",
            "TTTTTTT KK  K  K  K  ",
            "print 'He hears the sound of an' animals at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTT KK KKKKKK",
            "print name 'is afraid this is a haunted forest'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='en')


    def test_5(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Drawing figures'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "angle is 90",
            "TTTTT KK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            level="level4",lang='en')


    def test_6(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Drawing figures'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "angle is 90",
            "TTTTT KK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            level="level4",lang='en')


    def test_7(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Who does the dishes?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='en')


    def test_8(self):
        self.assert_highlighted_chr_multi_line(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTTK TTTK TTTTK TTTTTT",
            "print _ the dishes are done by _",
            "KKKKK I TTTTTTTTTTTTTTTTTTTTTT I",
            "sleep",
            "KKKKK",
            "print people at _",
            "KKKKK TTTTTT KK I",
            level="level4",lang='en')


    def test_9(self):
        self.assert_highlighted_chr_multi_line(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTTK TTTK TTTTK TTTTTT",
            "print ' the dishes are done by '",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "sleep",
            "KKKKK",
            "print people at random",
            "KKKKK TTTTTT KK KKKKKK",
            level="level4",lang='en')


    def test_10(self):
        self.assert_highlighted_chr_multi_line(
            "print 'What will the die indicate this time?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='en')


    def test_11(self):
        self.assert_highlighted_chr_multi_line(
            "choices is 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT KK TK TK TK TK TK TTTTTTTTT",
            "print _ you threw _",
            "KKKKK I TTTTTTTTT I",
            "print _ _ _ # here you have to program the choice",
            "KKKKK I I I CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            level="level4",lang='en')


    def test_12(self):
        self.assert_highlighted_chr_multi_line(
            "choices is 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT KK TK TK TK TK TK TTTTTTTTT",
            "print ' you threw '",
            "KKKKK SSSSSSSSSSSSS",
            "print choices at random # here you have to program the choice",
            "KKKKK TTTTTTT KK KKKKKK CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            level="level4",lang='en')


    def test_13(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome to your own rock scissors paper!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='en')


    def test_14(self):
        self.assert_highlighted_chr_multi_line(
            "choices is rock, paper, scissors",
            "TTTTTTT KK TTTTK TTTTTK TTTTTTTT",
            "print _ The computer chose: _ _ at _",
            "KKKKK I TTTTTTTTTTTTTTTTTTT I I KK I",
            level="level4",lang='en')


    def test_15(self):
        self.assert_highlighted_chr_multi_line(
            "choices is rock, paper, scissors",
            "TTTTTTT KK TTTTK TTTTTK TTTTTTTT",
            "print ' The computer chose: ' choices at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS TTTTTTT KK KKKKKK",
            level="level4",lang='en')


    def test_16(self):
        self.assert_highlighted_chr_multi_line(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level4",lang='en')


    def test_17(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Im Hedy the fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "question is ask 'What do you want to know?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'This is your question: ' question",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTTT",
            "answers is yes, no, maybe",
            "TTTTTTT KK TTTK TTK TTTTT",
            "print 'My crystal ball says...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "sleep 2",
            "KKKKK T",
            "print answers at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level4",lang='en')


    def test_18(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome to Hedys restaurant!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Today we are serving pizza or lasagna.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "food is ask 'What would you like to eat?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Great choice! The ' food ' is my favorite!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSS TTTT SSSSSSSSSSSSSSSSSS",
            "topping is ask 'Would you like meat or veggies on that?'",
            "TTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print food ' with ' topping ' is on its way!'",
            "KKKKK TTTT SSSSSSSS TTTTTTT SSSSSSSSSSSSSSSSS",
            "drinks is ask 'What would you like to drink with that?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Thank you for your order.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Your ' food ' and ' drinks ' will be right there!'",
            "KKKKK SSSSSSS TTTT SSSSSSS TTTTTT SSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='en')


    def test_19(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Escape from the haunted house!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'There are 3 doors in front of you...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "choice is ask 'Which door do you choose?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You picked door ...' choice",
            "KKKKK SSSSSSSSSSSSSSSSSSSSS TTTTTT",
            "monsters is a zombie, a vampire, NOTHING YOUVE ESCAPED",
            "TTTTTTTT KK TTTTTTTTK TTTTTTTTTK TTTTTTTTTTTTTTTTTTTTT",
            "print 'You see...'",
            "KKKKK SSSSSSSSSSSS",
            "sleep",
            "KKKKK",
            "print monsters at random",
            "KKKKK TTTTTTTT KK KKKKKK",
            level="level4",lang='en')


    def test_20(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='en')


    def test_21(self):
        self.assert_highlighted_chr_multi_line(
            "password is ask 'What is the correct password?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='en')
