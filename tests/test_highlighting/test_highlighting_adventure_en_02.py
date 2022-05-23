from tests.Highlighter import HighlightTester

class HighlighterTestLeveL2(HighlightTester):


    def test_1(self):
        self.assert_highlighted_chr(
            "print hello world!",
            "KKKKK TTTTTTTTTTTT",
            level="level2", lang='en')


    def test_2(self):
        self.assert_highlighted_chr_multi_line(
            "name is Hedy",
            "TTTT KK TTTT",
            "age is 15",
            "TTT KK TT",
            "print name is age years old",
            "KKKKK TTTTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_3(self):
        self.assert_highlighted_chr_multi_line(
            "answer is ask What is your name?",
            "TTTTTT KK KKK TTTTTTTTTTTTTTTTTT",
            "print Hello answer",
            "KKKKK TTTTTTTTTTTT",
            level="level2", lang='en')


    def test_4(self):
        self.assert_highlighted_chr_multi_line(
            "print My favorite colour is...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTT",
            "sleep 2",
            "KKKKK T",
            "print green!",
            "KKKKK TTTTTT",
            level="level2", lang='en')


    def test_5(self):
        self.assert_highlighted_chr(
            "print Your story",
            "KKKKK TTTTTTTTTT",
            level="level2", lang='en')


    def test_6(self):
        self.assert_highlighted_chr_multi_line(
            "name is ask What is the name of the main character?",
            "TTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print name is now going to run in the woods",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print name is a bit scared",
            "KKKKK TTTTTTTTTTTTTTTTTTTT",
            "print Suddenly he hears a crazy noise...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "sleep",
            "KKKKK",
            "print name is afraid this is a haunted forest",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_7(self):
        self.assert_highlighted_chr(
            "print Im Hedy the parrot!",
            "KKKKK TTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_8(self):
        self.assert_highlighted_chr_multi_line(
            "print Im Hedy the parrot",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "name is ask whats your name?",
            "TTTT KK KKK TTTTTTTTTTTTTTTT",
            "print name",
            "KKKKK TTTT",
            "sleep",
            "KKKKK",
            "print squawk",
            "KKKKK TTTTTT",
            "sleep",
            "KKKKK",
            "print name",
            "KKKKK TTTT",
            level="level2", lang='en')


    def test_9(self):
        self.assert_highlighted_chr_multi_line(
            "print Turtle race!",
            "KKKKK TTTTTTTTTTTT",
            "hoek is 90",
            "TTTT KK TT",
            "turn hoek",
            "KKKK TTTT",
            "forward 25",
            "KKKKKKK TT",
            level="level2", lang='en')


    def test_10(self):
        self.assert_highlighted_chr_multi_line(
            "print Drawing figures",
            "KKKKK TTTTTTTTTTTTTTT",
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
            level="level2", lang='en')


    def test_11(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level2", lang='en')


    def test_12(self):
        self.assert_highlighted_chr_multi_line(
            "choice is _",
            "TTTTTT KK T",
            "print I choose choice",
            "KKKKK TTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_13(self):
        self.assert_highlighted_chr_multi_line(
            "print Welcome to Hedy's restaurant!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Today we're serving pizza or lasagna.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "food is ask What would you like to eat?",
            "TTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Great choice! The food is my favorite!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "topping is ask Would you like meat or veggies on that?",
            "TTTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print food with topping is on its way!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "drinks is ask What would you like to drink with that?",
            "TTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Thank you for your order.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Your food and drinks will be right there!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_14(self):
        self.assert_highlighted_chr(
            "monster1 is _",
            "TTTTTTTT KK T",
            level="level2", lang='en')


    def test_15(self):
        self.assert_highlighted_chr_multi_line(
            "monster_1 is 👻",
            "TTTTTTTTT KK T",
            "monster_2 is 🤡",
            "TTTTTTTTT KK T",
            "monster_3 is 👶",
            "TTTTTTTTT KK T",
            "print You enter the haunted house.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Suddenly you see a monster_1",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print You run into the other room, but a monster_2 is waiting there for you!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Oh no! Quickly get to the kitchen.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print But as you enter monster_3 attacks you!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_16(self):
        self.assert_highlighted_chr(
            "print Let's go to the next level!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')
