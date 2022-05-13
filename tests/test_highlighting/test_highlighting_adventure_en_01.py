from tests.Highlighter import HighlightTester

class HighlighterTestLeveL1(HighlightTester):


    def test_1(self):
        self.assert_highlighted_chr(
            "print hello world!",
            "KKKKK TTTTTTTTTTTT",
            level="level1",lang='en')


    def test_2(self):
        self.assert_highlighted_chr_multi_line(
            "print Hello!",
            "KKKKK TTTTTT",
            "print Welcome to Hedy!",
            "KKKKK TTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_3(self):
        self.assert_highlighted_chr_multi_line(
            "ask What is your name?",
            "KKK TTTTTTTTTTTTTTTTTT",
            "echo hello",
            "KKKK TTTTT",
            level="level1",lang='en')


    def test_4(self):
        self.assert_highlighted_chr(
            "print Your story starts here",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_5(self):
        self.assert_highlighted_chr(
            "ask who is the star in your story?",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_6(self):
        self.assert_highlighted_chr_multi_line(
            "ask The main character of this story is",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print The main character is now going to walk in the forest",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo He's a bit scared,",
            "KKKK TTTTTTTTTTTTTTTTTT",
            "print He hears crazy noises everywhere",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print He's afraid this is a haunted forest",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_7(self):
        self.assert_highlighted_chr(
            "print Im Hedy the parrot",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_8(self):
        self.assert_highlighted_chr_multi_line(
            "print Im Hedy the parrot",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "ask whats your name?",
            "KKK TTTTTTTTTTTTTTTT",
            "echo",
            "KKKK",
            "echo",
            "KKKK",
            level="level1",lang='en')


    def test_9(self):
        self.assert_highlighted_chr_multi_line(
            "forward 50",
            "KKKKKKK TT",
            "turn left",
            "KKKK KKKK",
            level="level1",lang='en')


    def test_10(self):
        self.assert_highlighted_chr_multi_line(
            "turn right",
            "KKKK KKKKK",
            "forward 50",
            "KKKKKKK TT",
            "turn left",
            "KKKK KKKK",
            "forward 50",
            "KKKKKKK TT",
            level="level1",lang='en')


    def test_11(self):
        self.assert_highlighted_chr(
            "print Welcome to your own rock scissors paper!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_12(self):
        self.assert_highlighted_chr_multi_line(
            "print what do you choose?",
            "KKKKK TTTTTTTTTTTTTTTTTTT",
            "ask choose from rock, paper or scissors",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo so your choice was:",
            "KKKK TTTTTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_13(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level1",lang='en')


    def test_14(self):
        self.assert_highlighted_chr_multi_line(
            "print Hello, I'm Hedy the fortune teller!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "ask Who are you?",
            "KKK TTTTTTTTTTTT",
            "print Let me take a look in my crystal ball",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print I see... I see...",
            "KKKKK TTTTTTTTTTTTTTTTT",
            "echo Your name is",
            "KKKK TTTTTTTTTTTT",
            level="level1",lang='en')


    def test_15(self):
        self.assert_highlighted_chr_multi_line(
            "print Welcome to Hedy's restaurant 🍟",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "ask What would you like to order?",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo So you would like to order",
            "KKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Thanks you for your order!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print It's on its way!",
            "KKKKK TTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_16(self):
        self.assert_highlighted_chr(
            "print How did I get here?",
            "KKKKK TTTTTTTTTTTTTTTTTTT",
            level="level1",lang='en')


    def test_17(self):
        self.assert_highlighted_chr_multi_line(
            "print How did I get here?",
            "KKKKK TTTTTTTTTTTTTTTTTTT",
            "print I remember my friend telling me to go into the old mansion...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print and suddenly everything went black.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print But how did I end up on the floor...?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print My head hurts like Ive been hit by a baseball bat!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print What's that sound?",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "print Oh no! I feel like Im not alone in this house!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print I need to get out of here!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print There are 3 doors in front of me..",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "ask Which door should i pick?",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo I choose door",
            "KKKK TTTTTTTTTTTTT",
            "print ...?",
            "KKKKK TTTT",
            level="level1",lang='en')


    def test_18(self):
        self.assert_highlighted_chr(
            "print Let's go!",
            "KKKKK TTTTTTTTT",
            level="level1",lang='en')


    def test_19(self):
        self.assert_highlighted_chr_multi_line(
            "print Welcome at Hedy's",
            "KKKKK TTTTTTTTTTTTTTTTT",
            "ask What would you like to eat?",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo So you want ",
            "KKKK TTTTTTTTTTTT",
            "ask what would you like to drink?",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo So you want ",
            "KKKK TTTTTTTTTTTT",
            level="level1",lang='en')
