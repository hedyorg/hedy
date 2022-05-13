from tests.Highlighter import HighlightTester

class HighlighterTestLeveL3(HighlightTester):


    def test_1(self):
        self.assert_highlighted_chr_multi_line(
            "print hello world!",
            "KKKKK TTTTTTTTTTTT",
            level="level3",lang='en')


    def test_2(self):
        self.assert_highlighted_chr_multi_line(
            "animals is dog, cat, kangaroo",
            "TTTTTTT KK TTT  TTT  TTTTTTTT",
            "print animals at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_3(self):
        self.assert_highlighted_chr_multi_line(
            "animals is dog, cat, kangaroo",
            "TTTTTTT KK TTT  TTT  TTTTTTTT",
            "add penguin to animals",
            "KKK TTTTTTT KK TTTTTTT",
            "remove cat from animals",
            "KKKKKK TTT KKKK TTTTTTT",
            "print animals at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_4(self):
        self.assert_highlighted_chr_multi_line(
            "print Your story",
            "KKKKK TTTTTTTTTT",
            level="level3",lang='en')


    def test_5(self):
        self.assert_highlighted_chr_multi_line(
            "animals is 🦔, 🐿, 🦉, 🦇",
            "TTTTTTT KK T  T  T  T",
            "print He now hears the sound of an animals at random",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_6(self):
        self.assert_highlighted_chr_multi_line(
            "print He hears a sound",
            "KKKKK TTTTTTTTTTTTTTTT",
            "animals is 🐿, 🦔, 🦇, 🦉",
            "TTTTTTT KK T  T  T  T",
            "animal is ask What do you think it is?",
            "TTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTT",
            "add animal to animals",
            "KKK TTTTTT KK TTTTTTT",
            "print it was a animals at random",
            "KKKKK TTTTTTTTTTTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_7(self):
        self.assert_highlighted_chr_multi_line(
            "print His backpack got way too heavy.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Inside were a bottle of water, a flashlight and a brick.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT  TTTTTTTTTTTTTTTTTTTTTTTTT",
            "bag is water, flashlight, brick",
            "TTT KK TTTTT  TTTTTTTTTT  TTTTT",
            "dump is ask Which item should he dump?",
            "TTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "remove dump from bag",
            "KKKKKK TTTT KKKK TTT",
            level="level3",lang='en')


    def test_8(self):
        self.assert_highlighted_chr_multi_line(
            "words is squawk, Hedy",
            "TTTTT KK TTTTTT  TTTT",
            "print Train your parrot!",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "new_word is ask Which word do you want to teach them?",
            "TTTTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "add new_word to words",
            "KKK TTTTTTTT KK TTTTT",
            "print 🧒 Say new_word , Hedy!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTT",
            "print 🦜 words at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_9(self):
        self.assert_highlighted_chr_multi_line(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level3",lang='en')


    def test_10(self):
        self.assert_highlighted_chr_multi_line(
            "angles is 10, 50, 90, 150, 250",
            "TTTTTT KK TT  TT  TT  TTT  TTT",
            "turn angles at random",
            "KKKK TTTTTT KK KKKKKK",
            "forward 25",
            "KKKKKKK TT",
            level="level3",lang='en')


    def test_11(self):
        self.assert_highlighted_chr_multi_line(
            "print Who does the dishes?",
            "KKKKK TTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='en')


    def test_12(self):
        self.assert_highlighted_chr_multi_line(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTT  TTT  TTTT  TTTTTT",
            "print people at random",
            "KKKKK TTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_13(self):
        self.assert_highlighted_chr_multi_line(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTT  TTT  TTTT  TTTTTT",
            "your_name is ask Who are you?",
            "TTTTTTTTT KK KKK TTTTTTTTTTTT",
            "remove your_name from people",
            "KKKKKK TTTTTTTTT KKKK TTTTTT",
            "print people at random does the dishes",
            "KKKKK TTTTTT KK KKKKKK TTTTTTTTTTTTTTT",
            level="level3",lang='en')


    def test_14(self):
        self.assert_highlighted_chr_multi_line(
            "print What will the die indicate this time?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='en')


    def test_15(self):
        self.assert_highlighted_chr_multi_line(
            "choices is 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT KK T  T  T  T  T  TTTTTTTTT",
            "print choices at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_16(self):
        self.assert_highlighted_chr_multi_line(
            "print Welcome to your own rock scissors paper!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='en')


    def test_17(self):
        self.assert_highlighted_chr_multi_line(
            "choices is rock, paper, scissors",
            "TTTTTTT KK TTTT  TTTTT  TTTTTTTT",
            "print choices at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_18(self):
        self.assert_highlighted_chr_multi_line(
            "print I’m Hedy the fortune teller!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "question is ask What do you want to know?",
            "TTTTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTT",
            "print This is what you want to know: question",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "answers is yes, no, maybe",
            "TTTTTTT KK TTT  TT  TTTTT",
            "print My crystal ball says...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTT",
            "sleep 2",
            "KKKKK T",
            "print answers at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_19(self):
        self.assert_highlighted_chr_multi_line(
            "print Mystery milkshake",
            "KKKKK TTTTTTTTTTTTTTTTT",
            "flavors is strawberry, chocolate, vanilla",
            "TTTTTTT KK TTTTTTTTTT  TTTTTTTTT  TTTTTTT",
            "allergies is ask Are you allergic to any falvors?",
            "TTTTTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "remove allergies from flavors",
            "KKKKKK TTTTTTTTT KKKK TTTTTTT",
            "print You get a flavors at random milkshake",
            "KKKKK TTTTTTTTTTTTTTTTT KK KKKKKK TTTTTTTTT",
            level="level3",lang='en')


    def test_20(self):
        self.assert_highlighted_chr_multi_line(
            "print Welcome to Hedy's Random Restaurant!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print The only restaurant that will randomly choose your meal and its price for you!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "starters is salad, soup, carpaccio",
            "TTTTTTTT KK TTTTT  TTTT  TTTTTTTTT",
            "mains is pizza, brussels sprouts, spaghetti",
            "TTTTT KK TTTTT  TTTTTTTTTTTTTTTT  TTTTTTTTT",
            "desserts is brownies, ice cream, french cheeses",
            "TTTTTTTT KK TTTTTTTT  TTTTTTTTT  TTTTTTTTTTTTTT",
            "drinks is cola, beer, water",
            "TTTTTT KK TTTT  TTTT  TTTTT",
            "prices is 1 dollar, 10 dollars, 100 dollars",
            "TTTTTTTKKTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print You will start with: starters at random",
            "KKKKK                               KK KKKKKK",
            "print Then we'll serve: mains at random",
            "KKKKK                         KK KKKKKK",
            "print And as dessert: desserts at random",
            "KKKKK                          KK KKKKKK",
            "print You will get a drinks at random to drink",
            "KKKKK                       KK KKKKKK         ",
            "print That will be: prices at random",
            "KKKKK                      KK KKKKKK",
            "print Thank you and enjoy your meal!",
            "KKKKK                               ",
            level="level3",lang='en')


    def test_21(self):
        self.assert_highlighted_chr_multi_line(
            "print Escape from the haunted house!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print There are 3 doors in front of you...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "choice is ask Which door do you choose?",
            "TTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTT",
            "print You picked door ... choice",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "monsters is a zombie, a vampire, NOTHING YOUVE ESCAPED",
            "TTTTTTTT KK TTTTTTTT  TTTTTTTTT  TTTTTTTTTTTTTTTTTTTTT",
            "print You see...",
            "KKKKK TTTTTTTTTT",
            "sleep",
            "KKKKK",
            "print monsters at random",
            "KKKKK TTTTTTTT KK KKKKKK",
            level="level3",lang='en')


    def test_22(self):
        self.assert_highlighted_chr_multi_line(
            "name is Sophie",
            "TTTT KK TTTTTT",
            "print My name is name",
            "KKKKK TTTTTTTTTTTTTTT",
            level="level3",lang='en')


    def test_23(self):
        self.assert_highlighted_chr(
            "print Let's go to the next level!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='en')