from tests.Highlighter import HighlightTester

class HighlighterTestWebSite(HighlightTester):


    def test_1_1(self):
        self.assert_highlighted_chr(
            "print hello world!",
            "KKKKK TTTTTTTTTTTT",
            level="level1", lang='en')


    def test_1_2(self):
        self.assert_highlighted_chr_multi_line(
            "print Hello!",
            "KKKKK TTTTTT",
            "print Welcome to Hedy!",
            "KKKKK TTTTTTTTTTTTTTTT",
            level="level1", lang='en')


    def test_1_3(self):
        self.assert_highlighted_chr_multi_line(
            "ask What is your name?",
            "KKK TTTTTTTTTTTTTTTTTT",
            "echo hello",
            "KKKK TTTTT",
            level="level1", lang='en')


    def test_1_4(self):
        self.assert_highlighted_chr(
            "print Your story starts here",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='en')


    def test_1_5(self):
        self.assert_highlighted_chr(
            "ask who is the star in your story?",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='en')


    def test_1_6(self):
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
            level="level1", lang='en')


    def test_1_7(self):
        self.assert_highlighted_chr(
            "print Im Hedy the parrot",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            level="level1", lang='en')


    def test_1_8(self):
        self.assert_highlighted_chr_multi_line(
            "print Im Hedy the parrot",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "ask whats your name?",
            "KKK TTTTTTTTTTTTTTTT",
            "echo",
            "KKKK",
            "echo",
            "KKKK",
            level="level1", lang='en')


    def test_1_9(self):
        self.assert_highlighted_chr_multi_line(
            "forward 50",
            "KKKKKKK TT",
            "turn left",
            "KKKK KKKK",
            level="level1", lang='en')


    def test_1_10(self):
        self.assert_highlighted_chr_multi_line(
            "turn right",
            "KKKK KKKKK",
            "forward 50",
            "KKKKKKK TT",
            "turn left",
            "KKKK KKKK",
            "forward 50",
            "KKKKKKK TT",
            level="level1", lang='en')


    def test_1_11(self):
        self.assert_highlighted_chr(
            "print Welcome to your own rock scissors paper!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='en')


    def test_1_12(self):
        self.assert_highlighted_chr_multi_line(
            "print what do you choose?",
            "KKKKK TTTTTTTTTTTTTTTTTTT",
            "ask choose from rock, paper or scissors",
            "KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo so your choice was:",
            "KKKK TTTTTTTTTTTTTTTTTTT",
            level="level1", lang='en')


    def test_1_13(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level1", lang='en')


    def test_1_14(self):
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
            level="level1", lang='en')


    def test_1_15(self):
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
            level="level1", lang='en')


    def test_1_16(self):
        self.assert_highlighted_chr(
            "print How did I get here?",
            "KKKKK TTTTTTTTTTTTTTTTTTT",
            level="level1", lang='en')


    def test_1_17(self):
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
            level="level1", lang='en')


    def test_1_18(self):
        self.assert_highlighted_chr(
            "print Let's go!",
            "KKKKK TTTTTTTTT",
            level="level1", lang='en')


    def test_1_19(self):
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
            level="level1", lang='en')

    def test_2_1(self):
        self.assert_highlighted_chr(
            "print hello world!",
            "KKKKK TTTTTTTTTTTT",
            level="level2", lang='en')


    def test_2_2(self):
        self.assert_highlighted_chr_multi_line(
            "name is Hedy",
            "TTTT KK TTTT",
            "age is 15",
            "TTT KK TT",
            "print name is age years old",
            "KKKKK TTTTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_2_3(self):
        self.assert_highlighted_chr_multi_line(
            "answer is ask What is your name?",
            "TTTTTT KK KKK TTTTTTTTTTTTTTTTTT",
            "print Hello answer",
            "KKKKK TTTTTTTTTTTT",
            level="level2", lang='en')


    def test_2_4(self):
        self.assert_highlighted_chr_multi_line(
            "print My favorite colour is...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTT",
            "sleep 2",
            "KKKKK T",
            "print green!",
            "KKKKK TTTTTT",
            level="level2", lang='en')


    def test_2_5(self):
        self.assert_highlighted_chr(
            "print Your story",
            "KKKKK TTTTTTTTTT",
            level="level2", lang='en')


    def test_2_6(self):
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


    def test_2_7(self):
        self.assert_highlighted_chr(
            "print Im Hedy the parrot!",
            "KKKKK TTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_2_8(self):
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


    def test_2_9(self):
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


    def test_2_10(self):
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


    def test_2_11(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level2", lang='en')


    def test_2_12(self):
        self.assert_highlighted_chr_multi_line(
            "choice is _",
            "TTTTTT KK T",
            "print I choose choice",
            "KKKKK TTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_2_13(self):
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


    def test_2_14(self):
        self.assert_highlighted_chr(
            "monster1 is _",
            "TTTTTTTT KK T",
            level="level2", lang='en')


    def test_2_15(self):
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


    def test_2_16(self):
        self.assert_highlighted_chr(
            "print Let's go to the next level!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2", lang='en')


    def test_3_1(self):
        self.assert_highlighted_chr_multi_line(
            "print hello world!",
            "KKKKK TTTTTTTTTTTT",
            level="level3", lang='en')


    def test_3_2(self):
        self.assert_highlighted_chr_multi_line(
            "animals is dog, cat, kangaroo",
            "TTTTTTT KK TTTT TTTT TTTTTTTT",
            "print animals at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_3(self):
        self.assert_highlighted_chr_multi_line(
            "animals is dog, cat, kangaroo",
            "TTTTTTT KK TTTT TTTT TTTTTTTT",
            "add penguin to animals",
            "KKK TTTTTTT KK TTTTTTT",
            "remove cat from animals",
            "KKKKKK TTT KKKK TTTTTTT",
            "print animals at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_4(self):
        self.assert_highlighted_chr_multi_line(
            "print Your story",
            "KKKKK TTTTTTTTTT",
            level="level3", lang='en')


    def test_3_5(self):
        self.assert_highlighted_chr_multi_line(
            "animals is 🦔, 🐿, 🦉, 🦇",
            "TTTTTTT KK TT TT TT T",
            "print He now hears the sound of an animals at random",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_6(self):
        self.assert_highlighted_chr_multi_line(
            "print He hears a sound",
            "KKKKK TTTTTTTTTTTTTTTT",
            "animals is 🐿, 🦔, 🦇, 🦉",
            "TTTTTTT KK TT TT TT T",
            "animal is ask What do you think it is?",
            "TTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTT",
            "add animal to animals",
            "KKK TTTTTT KK TTTTTTT",
            "print it was a animals at random",
            "KKKKK TTTTTTTTTTTTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_7(self):
        self.assert_highlighted_chr_multi_line(
            "print His backpack got way too heavy.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Inside were a bottle of water, a flashlight and a brick.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT TTTTTTTTTTTTTTTTTTTTTTTTT",
            "bag is water, flashlight, brick",
            "TTT KK TTTTTT TTTTTTTTTTT TTTTT",
            "dump is ask Which item should he dump?",
            "TTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "remove dump from bag",
            "KKKKKK TTTT KKKK TTT",
            level="level3", lang='en')


    def test_3_8(self):
        self.assert_highlighted_chr_multi_line(
            "words is squawk, Hedy",
            "TTTTT KK TTTTTTT TTTT",
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
            level="level3", lang='en')


    def test_3_9(self):
        self.assert_highlighted_chr_multi_line(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level3", lang='en')


    def test_3_10(self):
        self.assert_highlighted_chr_multi_line(
            "angles is 10, 50, 90, 150, 250",
            "TTTTTT KK TTT TTT TTT TTTT TTT",
            "turn angles at random",
            "KKKK TTTTTT KK KKKKKK",
            "forward 25",
            "KKKKKKK TT",
            level="level3", lang='en')


    def test_3_11(self):
        self.assert_highlighted_chr_multi_line(
            "print Who does the dishes?",
            "KKKKK TTTTTTTTTTTTTTTTTTTT",
            level="level3", lang='en')


    def test_3_12(self):
        self.assert_highlighted_chr_multi_line(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTTT TTTT TTTTT TTTTTT",
            "print people at random",
            "KKKKK TTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_13(self):
        self.assert_highlighted_chr_multi_line(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTTT TTTT TTTTT TTTTTT",
            "your_name is ask Who are you?",
            "TTTTTTTTT KK KKK TTTTTTTTTTTT",
            "remove your_name from people",
            "KKKKKK TTTTTTTTT KKKK TTTTTT",
            "print people at random does the dishes",
            "KKKKK TTTTTT KK KKKKKK TTTTTTTTTTTTTTT",
            level="level3", lang='en')


    def test_3_14(self):
        self.assert_highlighted_chr_multi_line(
            "print What will the die indicate this time?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3", lang='en')


    def test_3_15(self):
        self.assert_highlighted_chr_multi_line(
            "choices is 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT KK TT TT TT TT TT TTTTTTTTT",
            "print choices at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_16(self):
        self.assert_highlighted_chr_multi_line(
            "print Welcome to your own rock scissors paper!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3", lang='en')


    def test_3_17(self):
        self.assert_highlighted_chr_multi_line(
            "choices is rock, paper, scissors",
            "TTTTTTT KK TTTTT TTTTTT TTTTTTTT",
            "print choices at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_18(self):
        self.assert_highlighted_chr_multi_line(
            "print I’m Hedy the fortune teller!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "question is ask What do you want to know?",
            "TTTTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTT",
            "print This is what you want to know: question",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "answers is yes, no, maybe",
            "TTTTTTT KK TTTT TTT TTTTT",
            "print My crystal ball says...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTT",
            "sleep 2",
            "KKKKK T",
            "print answers at random",
            "KKKKK TTTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_19(self):
        self.assert_highlighted_chr_multi_line(
            "print Mystery milkshake",
            "KKKKK TTTTTTTTTTTTTTTTT",
            "flavors is strawberry, chocolate, vanilla",
            "TTTTTTT KK TTTTTTTTTTT TTTTTTTTTT TTTTTTT",
            "allergies is ask Are you allergic to any falvors?",
            "TTTTTTTTT KK KKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "remove allergies from flavors",
            "KKKKKK TTTTTTTTT KKKK TTTTTTT",
            "print You get a flavors at random milkshake",
            "KKKKK TTTTTTTTTTTTTTTTT KK KKKKKK TTTTTTTTT",
            level="level3", lang='en')


    def test_3_20(self):
        self.assert_highlighted_chr_multi_line(
            "print Welcome to Hedy's Random Restaurant!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print The only restaurant that will randomly choose your meal and its price for you!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "starters is salad, soup, carpaccio",
            "TTTTTTTT KK TTTTTT TTTTT TTTTTTTTT",
            "mains is pizza, brussels sprouts, spaghetti",
            "TTTTT KK TTTTTT TTTTTTTTTTTTTTTTT TTTTTTTTT",
            "desserts is brownies, ice cream, french cheeses",
            "TTTTTTTT KK TTTTTTTTT TTTTTTTTTT TTTTTTTTTTTTTT",
            "drinks is cola, beer, water",
            "TTTTTT KK TTTTT TTTTT TTTTT",
            "prices is 1 dollar, 10 dollars, 100 dollars",
            "TTTTTTTKKTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print You will start with: starters at random",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT KK KKKKKK",
            "print Then we'll serve: mains at random",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTT KK KKKKKK",
            "print And as dessert: desserts at random",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTT KK KKKKKK",
            "print You will get a drinks at random to drink",
            "KKKKK TTTTTTTTTTTTTTTTTTTTT KK KKKKKK TTTTTTTT",
            "print That will be: prices at random",
            "KKKKK TTTTTTTTTTTTTTTTTTTT KK KKKKKK",
            "print Thank you and enjoy your meal!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3", lang='en')


    def test_3_21(self):
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
            "TTTTTTTT KK TTTTTTTTT TTTTTTTTTT TTTTTTTTTTTTTTTTTTTTT",
            "print You see...",
            "KKKKK TTTTTTTTTT",
            "sleep",
            "KKKKK",
            "print monsters at random",
            "KKKKK TTTTTTTT KK KKKKKK",
            level="level3", lang='en')


    def test_3_22(self):
        self.assert_highlighted_chr_multi_line(
            "name is Sophie",
            "TTTT KK TTTTTT",
            "print My name is name",
            "KKKKK TTTTTTTTTTTTTTT",
            level="level3", lang='en')


    def test_3_23(self):
        self.assert_highlighted_chr(
            "print Let's go to the next level!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3", lang='en')


    def test_4_1(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Hello world'",
            "KKKKK SSSSSSSSSSSSS",
            level="level4", lang='en')


    def test_4_2(self):
        self.assert_highlighted_chr_multi_line(
            "print 'You need to use quotation marks from now on!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "answer is ask 'What do we need to use from now on?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'We need to use ' answer",
            "KKKKK SSSSSSSSSSSSSSSSS TTTTTT",
            level="level4", lang='en')


    def test_4_3(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Your story will be printed here!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4", lang='en')


    def test_4_4(self):
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
            "TTTTTTT KK TK TK TK T",
            "print 'He hears the sound of an' animals at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTT KK KKKKKK",
            "print name 'is afraid this is a haunted forest'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4", lang='en')


    def test_4_5(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Drawing figures'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "angle is 90",
            "TTTTT KK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            level="level4", lang='en')


    def test_4_6(self):
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
            level="level4", lang='en')


    def test_4_7(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Who does the dishes?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level4", lang='en')


    def test_4_8(self):
        self.assert_highlighted_chr_multi_line(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTTK TTTK TTTTK TTTTTT",
            "print _ the dishes are done by _",
            "KKKKK I TTTTTTTTTTTTTTTTTTTTTT I",
            "sleep",
            "KKKKK",
            "print people at _",
            "KKKKK TTTTTT KK I",
            level="level4", lang='en')


    def test_4_9(self):
        self.assert_highlighted_chr_multi_line(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTTK TTTK TTTTK TTTTTT",
            "print ' the dishes are done by '",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "sleep",
            "KKKKK",
            "print people at random",
            "KKKKK TTTTTT KK KKKKKK",
            level="level4", lang='en')


    def test_4_10(self):
        self.assert_highlighted_chr_multi_line(
            "print 'What will the die indicate this time?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4", lang='en')


    def test_4_11(self):
        self.assert_highlighted_chr_multi_line(
            "choices is 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT KK TK TK TK TK TK TTTTTTTTT",
            "print _ you threw _",
            "KKKKK I TTTTTTTTT I",
            "print _ _ _ # here you have to program the choice",
            "KKKKK I I I CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            level="level4", lang='en')


    def test_4_12(self):
        self.assert_highlighted_chr_multi_line(
            "choices is 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT KK TK TK TK TK TK TTTTTTTTT",
            "print ' you threw '",
            "KKKKK SSSSSSSSSSSSS",
            "print choices at random # here you have to program the choice",
            "KKKKK TTTTTTT KK KKKKKK CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            level="level4", lang='en')


    def test_4_13(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome to your own rock scissors paper!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4", lang='en')


    def test_4_14(self):
        self.assert_highlighted_chr_multi_line(
            "choices is rock, paper, scissors",
            "TTTTTTT KK TTTTK TTTTTK TTTTTTTT",
            "print _ The computer chose: _ _ at _",
            "KKKKK I TTTTTTTTTTTTTTTTTTT I I KK I",
            level="level4", lang='en')


    def test_4_15(self):
        self.assert_highlighted_chr_multi_line(
            "choices is rock, paper, scissors",
            "TTTTTTT KK TTTTK TTTTTK TTTTTTTT",
            "print ' The computer chose: ' choices at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS TTTTTTT KK KKKKKK",
            level="level4", lang='en')


    def test_4_16(self):
        self.assert_highlighted_chr_multi_line(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level4", lang='en')


    def test_4_17(self):
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
            level="level4", lang='en')


    def test_4_18(self):
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
            level="level4", lang='en')


    def test_4_19(self):
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
            level="level4", lang='en')


    def test_4_20(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4", lang='en')


    def test_4_21(self):
        self.assert_highlighted_chr_multi_line(
            "password is ask 'What is the correct password?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4", lang='en')


    def test_5_1(self):
        self.assert_highlighted_chr_multi_line(
            "name is ask 'what is your name?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
            "if name is Hedy print 'cool!' else print 'meh'",
            "KK TTTT KK TTTT KKKKK SSSSSSS KKKK KKKKK SSSSS",
            level="level5", lang='en')


    def test_5_2(self):
        self.assert_highlighted_chr_multi_line(
            "name is ask 'what is your name?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
            "if name is Hedy print 'nice' else print 'boo!'",
            "KK TTTT KK TTTT KKKKK SSSSSS KKKK KKKKK SSSSSS",
            level="level5", lang='en')


    def test_5_3(self):
        self.assert_highlighted_chr_multi_line(
            "pretty_colors is green, yellow",
            "TTTTTTTTTTTTT KK TTTTTK TTTTTT",
            "color is ask 'What is your favorite color?'",
            "TTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if color in pretty_colors print 'pretty!'",
            "KK TTTTT KK TTTTTTTTTTTTT KKKKK SSSSSSSSS",
            "else print 'meh'",
            "KKKK KKKKK SSSSS",
            level="level5", lang='en')


    def test_5_4(self):
        self.assert_highlighted_chr_multi_line(
            "name is ask 'what is your name?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
            "if name is Hedy print 'nice'",
            "KK TTTT KK TTTT KKKKK SSSSSS",
            "else print 'boo!'",
            "KKKK KKKKK SSSSSS",
            level="level5", lang='en')


    def test_5_5(self):
        self.assert_highlighted_chr_multi_line(
            "name is ask 'Who is walking in the forest?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print name 'walks through the forest'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print name 'encounter a monster'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSS",
            "end is ask 'Would you like a good or a bad ending?'",
            "TTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if end is good print name 'takes the sword and the monster quickly runs away'",
            "KK TTT KK TTTT KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else print 'The monster eats' name",
            "KKKK KKKKK SSSSSSSSSSSSSSSSSS TTTT",
            level="level5", lang='en')


    def test_5_6(self):
        self.assert_highlighted_chr(
            "print 'Here your story will start!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_7(self):
        self.assert_highlighted_chr_multi_line(
            "words is squawk, Hedy",
            "TTTTT KK TTTTTTK TTTT",
            "print 'Train your parrot!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSS",
            "new_word is ask 'Which word do you want to teach them?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "add new_word to words",
            "KKK TTTTTTTT KK TTTTT",
            "said_word is words at random",
            "TTTTTTTTT KK TTTTT KK KKKKKK",
            "print '🧒 Say ' new_word ', Hedy!'",
            "KKKKK SSSSSSSS TTTTTTTT SSSSSSSSS",
            "print '🦜 ' said_word",
            "KKKKK SSSS TTTTTTTTT",
            "if said_word is new_word print '🧒 Great job, Hedy! 🍪'",
            "KK TTTTTTTTT KK TTTTTTTT KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            "else print '🧒 No, Hedy! Say ' new_word",
            "KKKK KKKKK SSSSSSSSSSSSSSSSSS TTTTTTTT",
            level="level5", lang='en')


    def test_5_8(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level5", lang='en')


    def test_5_9(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Drawing Figures'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "figure is ask 'Do you want a square or a triangle?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if figure is triangle angle is 120",
            "KK TTTTTT KK TTTTTTTT TTTTT KK TTT",
            "else angle is 90",
            "KKKK TTTTT KK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            level="level5", lang='en')


    def test_5_10(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Drawing Figures'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "figure is ask 'Do you want a square or a triangle?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if figure is triangle angle is 120 else angle is 90",
            "KK TTTTTT KK TTTTTTTT TTTTT KK TTT KKKK TTTTT KK TT",
            "turn angle",
            "KKKK TTTTT",
            "forward 25",
            "KKKKKKK TT",
            level="level5", lang='en')

    def test_5_12(self):
        self.assert_highlighted_chr(
            "print 'Who does the dishes?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_13(self):
        self.assert_highlighted_chr_multi_line(
            "choices is 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT KK TK TK TK TK TK TTTTTTTTT",
            "throw is _",
            "TTTTT KK I",
            "print 'you have' _ 'thrown'",
            "KKKKK SSSSSSSSSS I SSSSSSSS",
            "if _ is earthworm print 'You can stop throwing.' _ print 'You have to hear it again!'",
            "KK I KK TTTTTTTTT KKKKK SSSSSSSSSSSSSSSSSSSSSSSS I KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_14(self):
        self.assert_highlighted_chr(
            "print 'What will the die indicate this time?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_15(self):
        self.assert_highlighted_chr_multi_line(
            "options is rock, paper, scissors",
            "TTTTTTT KK TTTTK TTTTTK TTTTTTTT",
            "computer_choice is _",
            "TTTTTTTTTTTTTTT KK I",
            "choice is ask 'What do you choose?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSS",
            "print 'you chose ' _",
            "KKKKK SSSSSSSSSSSS I",
            "print 'computer chose ' _",
            "KKKKK SSSSSSSSSSSSSSSSS I",
            "if _ is _ print 'tie!' else print 'no tie'",
            "KK I KK I KKKKK SSSSSS KKKK KKKKK SSSSSSSS",
            level="level5", lang='en')


    def test_5_16(self):
        self.assert_highlighted_chr(
            "print 'Welcome to your own rock scissors paper!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_17(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome to Hedys restaurant!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "special is ask 'Would you like to hear our specials today?'",
            "TTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if special is yes print 'Todays special is chicken piri piri and rice.' else print 'No problem.'",
            "KK TTTTTTT KK TTT KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS KKKK KKKKK SSSSSSSSSSSSS",
            "food is ask 'What would you like to eat?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'One ' food ', coming right up!'",
            "KKKKK SSSSSS TTTT SSSSSSSSSSSSSSSSSSSS",
            "drink is ask 'What would you like to drink with that?'",
            "TTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if drink is cola print 'Im sorry, we are out of cola!' else print 'Great choice!'",
            "KK TTTTT KK TTTT KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS KKKK KKKKK SSSSSSSSSSSSSSS",
            "anything is ask 'Would you like anything else?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Let me repeat your order...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'One ' food",
            "KKKKK SSSSSS TTTT",
            "if drink is cola print 'and...' else print 'One ' drink",
            "KK TTTTT KK TTTT KKKKK SSSSSSSS KKKK KKKKK SSSSSS TTTTT",
            "if anything is no print 'Thats it!' else print 'One ' anything",
            "KK TTTTTTTT KK TT KKKKK SSSSSSSSSSS KKKK KKKKK SSSSSS TTTTTTTT",
            "print 'Thank you for your order and enjoy your meal!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_18(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Im Hedy the fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I can predict if youll win the lottery tomorrow!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "person is ask 'Who are you?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSS",
            "if person is Hedy print 'You will definitely win!🤩' else print 'Bad luck! Someone else will win!😭'",
            "KK TTTTTT KK TTTT KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS KKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_19(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Im Hedy the fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I can predict if you will win the lottery tomorrow!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "person is ask 'Who are you?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSS",
            "goodanswer is Hurray! You win!, You will definitely win!, We have a winner!",
            "TTTTTTTTTT KK TTTTTTTTTTTTTTTTK TTTTTTTTTTTTTTTTTTTTTTTTK TTTTTTTTTTTTTTTTT",
            "badanswer is Bad luck! Try again!, Another person will win, You lose!",
            "TTTTTTTTT KK TTTTTTTTTTTTTTTTTTTTK TTTTTTTTTTTTTTTTTTTTTTTK TTTTTTTTT",
            "if person is Hedy print goodanswer at random else print badanswer at random",
            "KK TTTTTT KK TTTT KKKKK TTTTTTTTTT KK KKKKKK KKKK KKKKK TTTTTTTTT KK KKKKKK",
            level="level5", lang='en')


    def test_5_20(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Escape from the haunted house!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'There are 3 doors in front of you...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "doors is 1, 2, 3",
            "TTTTT KK TK TK T",
            "monsters is werewolf, mummy, vampire, zombie",
            "TTTTTTTT KK TTTTTTTTK TTTTTK TTTTTTTK TTTTTT",
            "chosen_door is ask 'Which door do you choose?'",
            "TTTTTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You chose door...' chosen_door",
            "KKKKK SSSSSSSSSSSSSSSSSSS TTTTTTTTTTT",
            "sleep",
            "KKKKK",
            "correct_door is doors at random",
            "TTTTTTTTTTTT KK TTTTT KK KKKKKK",
            "if chosen_door is correct_door print 'Great! Youve escaped!'",
            "KK TTTTTTTTTTT KK TTTTTTTTTTTT KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            "else print 'Oh no! You are being eaten by a...' monsters at random",
            "KKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTTT KK KKKKKK",
            level="level5", lang='en')


    def test_5_21(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Learn French!'",
            "KKKKK SSSSSSSSSSSSSSS",
            "cat is ask '🐱'",
            "TTT KK KKK SSS",
            "if cat is chat print 'Terrific!'",
            "KK TTT KK TTTT KKKKK SSSSSSSSSSS",
            "else print 'No, cat is chat'",
            "KKKK KKKKK SSSSSSSSSSSSSSSSS",
            "frog is ask '🐸'",
            "TTTT KK KKK SSS",
            "if frog is grenouille print 'Super!'",
            "KK TTTT KK TTTTTTTTTT KKKKK SSSSSSSS",
            "else print 'No, frog is grenouille'",
            "KKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_22(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome at McHedy'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            "order is ask 'What would you like to eat?'",
            "TTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You would like ' order",
            "KKKKK SSSSSSSSSSSSSSSSS TTTTT",
            "if order is hamburger price is 5",
            "KK TTTTT KK TTTTTTTTT TTTTT KK T",
            "if order is fries price is 2",
            "KK TTTTT KK TTTTT TTTTT KK T",
            "drinks is ask 'What would you like to drink?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You would like ' drinks",
            "KKKKK SSSSSSSSSSSSSSSSS TTTTTT",
            "print 'That will be ' price ' dollars for your ' order ' please'",
            "KKKKK SSSSSSSSSSSSSSS TTTTT SSSSSSSSSSSSSSSSSSSS TTTTT SSSSSSSSS",
            "print 'The drinks are free in this level because Hedy cant calculate the price yet...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')


    def test_5_23(self):
        self.assert_highlighted_chr(
            "print 'On to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            level="level5", lang='en')

    def test_6_1(self):
        self.assert_highlighted_chr(
            "print '5 times 5 is ' 5 * 5",
            "KKKKK SSSSSSSSSSSSSSS N K N",
            level="level6", lang='en')


    def test_6_2(self):
        self.assert_highlighted_chr_multi_line(
            "print '5 plus 5 is ' 5 + 5",
            "KKKKK SSSSSSSSSSSSSS N K N",
            "print '5 minus 5 is ' 5 - 5",
            "KKKKK SSSSSSSSSSSSSSS N K N",
            "print '5 times 5 is ' 5 * 5",
            "KKKKK SSSSSSSSSSSSSSS N K N",
            level="level6", lang='en')


    def test_6_3(self):
        self.assert_highlighted_chr_multi_line(
            "name = Hedy",
            "TTTT K TTTT",
            "answer = 20 + 4",
            "TTTTTT K NN K N",
            level="level6", lang='en')


    def test_6_4(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level6", lang='en')


    def test_6_5(self):
        self.assert_highlighted_chr(
            "print 'Baby shark'",
            "KKKKK SSSSSSSSSSSS",
            level="level6", lang='en')


    def test_6_6(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level6", lang='en')


    def test_6_7(self):
        self.assert_highlighted_chr(
            "print 'Drawing figures'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            level="level6", lang='en')


    def test_6_8(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level6", lang='en')


    def test_6_9(self):
        self.assert_highlighted_chr_multi_line(
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
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTTTTT",
            "remove dishwasher from people",
            "KKKKKK TTTTTTTTTT KKKK TTTTTT",
            "dishwasher = people at random",
            "TTTTTTTTTT K TTTTTT KK KKKKKK",
            level="level6", lang='en')


    def test_6_10(self):
        self.assert_highlighted_chr(
            "print 'Who does the dishes?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level6", lang='en')


    def test_6_11(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level6", lang='en')


    def test_6_12(self):
        self.assert_highlighted_chr(
            "print 'What will the die indicate this time?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level6", lang='en')


    def test_6_13(self):
        self.assert_highlighted_chr_multi_line(
            "correct_answer = 11 * 27",
            "TTTTTTTTTTTTTT K NN K NN",
            "answer = ask 'How much is 11 times 27?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if answer is correct_answer print 'good job!'",
            "KK TTTTTT KK TTTTTTTTTTTTTT KKKKK SSSSSSSSSSS",
            "else print 'Wrong! It was ' correct_answer",
            "KKKK KKKKK SSSSSSSSSSSSSSSS TTTTTTTTTTTTTT",
            level="level6", lang='en')


    def test_6_14(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level6", lang='en')


    def test_6_15(self):
        self.assert_highlighted_chr(
            "print 'Welcome to this calculator!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level6", lang='en')


    def test_6_16(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level6", lang='en')


    def test_6_17(self):
        self.assert_highlighted_chr_multi_line(
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
            "KK TTTTTTT KK TTTTTTT TTTTT K TTTTT K N",
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
            level="level6", lang='en')


    def test_6_18(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level6", lang='en')


    def test_6_19(self):
        self.assert_highlighted_chr_multi_line(
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
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "hygiene = ask 'How many times did you wash your hands today?'",
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "result = bananas + hygiene",
            "TTTTTT K TTTTTTT K TTTTTTT",
            "result = result * football",
            "TTTTTT K TTTTTT K TTTTTTTT",
            "print 'You are ' result ' percent smart.'",
            "KKKKK SSSSSSSSSS TTTTTT SSSSSSSSSSSSSSSSS",
            level="level6", lang='en')


    def test_6_20(self):
        self.assert_highlighted_chr_multi_line(
            "print 'happy birthday to you'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            "print 'happy birthday to you'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            "print 'happy birthday dear Hedy'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'happy birthday to you'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            level="level6", lang='en')


    def test_6_21(self):
        self.assert_highlighted_chr(
            "print 'On to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            level="level6", lang='en')



    def test_7_1(self):
        self.assert_highlighted_chr(
            "repeat 3 times print 'Hedy is fun!'",
            "KKKKKK N KKKKK KKKKK SSSSSSSSSSSSSS",
            level="level7", lang='en')


    def test_7_2(self):
        self.assert_highlighted_chr_multi_line(
            "print 'The prince kept calling for help'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "repeat 5 times print 'Help!'",
            "KKKKKK N KKKKK KKKKK SSSSSSS",
            "print 'Why is nobody helping me?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7", lang='en')


    def test_7_3(self):
        self.assert_highlighted_chr(
            "repeat 5 times print 'Help!'",
            "KKKKKK N KKKKK KKKKK SSSSSSS",
            level="level7", lang='en')


    def test_7_4(self):
        self.assert_highlighted_chr_multi_line(
            "repeat _ _ print 'Baby Shark tututudutudu'",
            "KKKKKK I I KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Baby Shark'",
            "KKKKK SSSSSSSSSSSS",
            level="level7", lang='en')


    def test_7_5(self):
        self.assert_highlighted_chr(
            "print 'Baby Shark'",
            "KKKKK SSSSSSSSSSSS",
            level="level7", lang='en')


    def test_7_6(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Draw figures'",
            "KKKKK SSSSSSSSSSSSSS",
            "repeat 3 times forward 10",
            "KKKKKK N KKKKK KKKKKKK NN",
            level="level7", lang='en')


    def test_7_7(self):
        self.assert_highlighted_chr_multi_line(
            "people = mom, dad, Emma, Sophie",
            "TTTTTT K TTTK TTTK TTTTK TTTTTT",
            "repeat _ _ print 'the dishwasher is' _",
            "KKKKKK I I KKKKK SSSSSSSSSSSSSSSSSSS I",
            level="level7", lang='en')


    def test_7_8(self):
        self.assert_highlighted_chr(
            "print 'Who does the dishes?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level7", lang='en')


    def test_7_9(self):
        self.assert_highlighted_chr_multi_line(
            "choices = 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT K NK NK NK NK NK TTTTTTTTT",
            "repeat _ _ print _ _ _",
            "KKKKKK I I KKKKK I I I",
            level="level7", lang='en')


    def test_7_10(self):
        self.assert_highlighted_chr(
            "print 'What will the die indicate this time?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7", lang='en')


    def test_7_11(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome to Hedys restaurant!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "people = ask 'How many people are joining us today?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "repeat people times food = ask 'What would you like to eat?'",
            "KKKKKK TTTTTT KKKKK TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Thanks for your order! Its coming right up!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7", lang='en')


    def test_7_12(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level7", lang='en')


    def test_7_13(self):
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
            level="level7", lang='en')


    def test_7_14(self):
        self.assert_highlighted_chr(
            "repeat 5 times print 'In the next level you can repeat multiple lines of code at once!'",
            "KKKKKK N KKKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7", lang='en')


    def test_7_15(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level7", lang='en')


    def test_8_1(self):
        self.assert_highlighted_chr_multi_line(
            "repeat 5 times",
            "KKKKKK N KKKKK",
            "print 'Hello folks'",
            "KKKKK SSSSSSSSSSSSS",
            "print 'This will be printed 5 times'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8", lang='en')


    def test_8_2(self):
        self.assert_highlighted_chr_multi_line(
            "repeat 5 times",
            "KKKKKK N KKKKK",
            "print 'Hello everyone'",
            "KKKKK SSSSSSSSSSSSSSSS",
            "print 'This is all repeated 5 times'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8", lang='en')


    def test_8_3(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level8", lang='en')


    def test_8_4(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level8", lang='en')


    def test_8_5(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level8", lang='en')


    def test_8_6(self):
        self.assert_highlighted_chr_multi_line(
            "angle = 90",
            "TTTTT K NN",
            "repeat 10 times",
            "KKKKKK NN KKKKK",
            "turn angle",
            "KKKK TTTTT",
            "forward 50",
            "KKKKKKK NN",
            level="level8", lang='en')


    def test_8_7(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level8", lang='en')


    def test_8_8(self):
        self.assert_highlighted_chr(
            "hoeken = ask 'How many angles should I draw?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8", lang='en')


    def test_8_9(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level8", lang='en')


    def test_8_10(self):
        self.assert_highlighted_chr_multi_line(
            "print 'I am Hedy the fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You can ask me 3 questions.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "answers = yes, no, maybe",
            "TTTTTTT K TTTK TTK TTTTT",
            "repeat 3 times",
            "KKKKKK N KKKKK",
            "question = ask 'What do you want to know?'",
            "TTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print question",
            "KKKKK TTTTTTTT",
            "sleep",
            "KKKKK",
            "print 'My crystal ball says...' answers at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTT KK KKKKKK",
            level="level8", lang='en')


    def test_8_11(self):
        self.assert_highlighted_chr_multi_line(
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
            level="level8", lang='en')


    def test_8_12(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level8", lang='en')



    def test_9_1(self):
        self.assert_highlighted_chr_multi_line(
            "repeat 3 times",
            "KKKKKK N KKKKK",
            "food = ask 'What do you want?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSS",
            "if food is pizza",
            "KK TTTT KK TTTTT",
            "print 'nice!'",
            "KKKKK SSSSSSS",
            "else",
            "KKKK",
            "print 'pizza is better'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_2(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Robin is walking downtown'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "location = ask 'Is Robin going into a shop, or does she go home?'",
            "TTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if location is shop",
            "KK TTTTTTTT KK TTTT",
            "print 'She enters the shop.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            "print 'Robin sees an interesting looking book'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "book = ask 'Does Robin buy the book?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if book is yes",
            "KK TTTT KK TTT",
            "print 'Robin buys the book and goes home'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Robin leaves the shop and goes home'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Robin goes home'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_3(self):
        self.assert_highlighted_chr_multi_line(
            "sword = lost",
            "TTTTT K TTTT",
            "game = on",
            "TTTT K TT",
            "print 'Our hero is walking through the forest'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'The path splits two ways'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "repeat 2 times",
            "KKKKKK N KKKKK",
            "if game is on",
            "KK TTTT KK TT",
            "path = ask 'Which path should she choose?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if path is left",
            "KK TTTT KK TTTT",
            "if sword is found",
            "KK TTTTT KK TTTTT",
            "print 'Our hero comes across a dragon!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Luckily our hero has a sword to defeat the beast!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "game = over",
            "TTTT K TTTT",
            "else",
            "KKKK",
            "print 'Our hero finds a dragon, but she doesnt have any weapons!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Our hero is beaten by the dragon...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Try again'",
            "KKKKK SSSSSSSSSSS",
            "game = over",
            "TTTT K TTTT",
            "if path is right",
            "KK TTTT KK TTTTT",
            "if sword is lost",
            "KK TTTTT KK TTTT",
            "print 'Our hero finds a sword'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'This could come in very handy'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "sword = found",
            "TTTTT K TTTTT",
            "else",
            "KKKK",
            "print 'You have already found the sword. There is nothing left here.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'She walks back'",
            "KKKKK SSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_4(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level9", lang='en')


    def test_9_5(self):
        self.assert_highlighted_chr_multi_line(
            "choices is rock, paper, scissors",
            "TTTTTTT KK TTTTK TTTTTK TTTTTTTT",
            "your_choice is ask 'What do you choose?'",
            "TTTTTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSS",
            "print 'You choose ' your_choice",
            "KKKKK SSSSSSSSSSSSS TTTTTTTTTTT",
            "computer_choice is choices at random",
            "TTTTTTTTTTTTTTT KK TTTTTTT KK KKKKKK",
            "print 'The computer chooses ' computer_choice",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS TTTTTTTTTTTTTTT",
            "if computer_choice is your_choice",
            "KK TTTTTTTTTTTTTTT KK TTTTTTTTTTT",
            "print 'Tie'",
            "KKKKK SSSSS",
            "if computer_choice is rock",
            "KK TTTTTTTTTTTTTTT KK TTTT",
            "if your_choice is paper",
            "KK TTTTTTTTTTT KK TTTTT",
            "print 'You win!'",
            "KKKKK SSSSSSSSSS",
            "if your_choice is scissors",
            "KK TTTTTTTTTTT KK TTTTTTTT",
            "print 'You lose!'",
            "KKKKK SSSSSSSSSSS",
            "# finish this code",
            "CCCCCCCCCCCCCCCCCC",
            level="level9", lang='en')


    def test_9_6(self):
        self.assert_highlighted_chr_multi_line(
            "score = 0",
            "TTTTT K N",
            "repeat 10 times",
            "KKKKKK NN KKKKK",
            "numbers = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
            "TTTTTTT K NK NK NK NK NK NK NK NK NK NN",
            "number1 = numbers at random",
            "TTTTTTT K TTTTTTT KK KKKKKK",
            "number2 = numbers at random",
            "TTTTTTT K TTTTTTT KK KKKKKK",
            "correct_answer = number1 * number2",
            "TTTTTTTTTTTTTT K TTTTTTT K TTTTTTT",
            "print 'What is ' number1 ' times ' number2 '?'",
            "KKKKK SSSSSSSSSS TTTTTTT SSSSSSSSS TTTTTTT SSS",
            "answer = ask 'Type your answer here...'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Your answer is' answer",
            "KKKKK SSSSSSSSSSSSSSSS TTTTTT",
            "if answer is correct_answer",
            "KK TTTTTT KK TTTTTTTTTTTTTT",
            "score = score + 1",
            "TTTTT K TTTTT K N",
            "print 'Great job! Your score is... ' score ' out of 10!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTT SSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_7(self):
        self.assert_highlighted_chr(
            "print 'Welcome to this calculator!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_8(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome to Hedys restaurant!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "people = ask 'How many people will be joining us today?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Great!'",
            "KKKKK SSSSSSSS",
            "price = 0",
            "TTTTT K N",
            "repeat people times",
            "KKKKKK TTTTTT KKKKK",
            "food = ask 'What would you like to order?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print food",
            "KKKKK TTTT",
            "if food is fries",
            "KK TTTT KK TTTTT",
            "price = price + 3",
            "TTTTT K TTTTT K N",
            "sauce = ask 'What kind of sauce would you like with your fries?'",
            "TTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if sauce is no",
            "KK TTTTT KK TT",
            "print 'no sauce'",
            "KKKKK SSSSSSSSSS",
            "else",
            "KKKK",
            "price = price + 1",
            "TTTTT K TTTTT K N",
            "print 'with ' sauce",
            "KKKKK SSSSSSS TTTTT",
            "if food is pizza",
            "KK TTTT KK TTTTT",
            "price = price + 4",
            "TTTTT K TTTTT K N",
            "print 'That will be ' price ' dollar'",
            "KKKKK SSSSSSSSSSSSSSS TTTTT SSSSSSSSS",
            "print 'Enjoy your meal!'",
            "KKKKK SSSSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_9(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Escape from the Haunted House!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "player = alive",
            "TTTTTT K TTTTT",
            "doors = 1, 2, 3",
            "TTTTT K NK NK N",
            "monsters = zombie, vampire, giant spider",
            "TTTTTTTT K TTTTTTK TTTTTTTK TTTTTTTTTTTT",
            "repeat 3 times",
            "KKKKKK N KKKKK",
            "if player is alive",
            "KK TTTTTT KK TTTTT",
            "correct_door is doors at random",
            "TTTTTTTTTTTT KK TTTTT KK KKKKKK",
            "print 'There are 3 doors in front of you...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "chosen_door = ask 'Which door do you choose?'",
            "TTTTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if chosen_door is correct_door",
            "KK TTTTTTTTTTT KK TTTTTTTTTTTT",
            "print 'No monsters here!'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'You are eaten by a ' monsters at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSS TTTTTTTT KK KKKKKK",
            "player = dead",
            "TTTTTT K TTTT",
            "else",
            "KKKK",
            "print 'GAME OVER'",
            "KKKKK SSSSSSSSSSS",
            "if player is alive",
            "KK TTTTTT KK TTTTT",
            "print 'Great! You survived!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_10(self):
        self.assert_highlighted_chr(
            "print 'Escape from the haunted house!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_11(self):
        self.assert_highlighted_chr_multi_line(
            "repeat 2 times",
            "KKKKKK N KKKKK",
            "print 'if youre happy and you know it clap your hands'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'if youre happy and you know it and you really want to show it'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'if youre happy and you know it clap your hands'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_9_12(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level9", lang='en')


    def test_10_1(self):
        self.assert_highlighted_chr_multi_line(
            "animals is dog, cat, blobfish",
            "TTTTTTT KK TTTK TTTK TTTTTTTT",
            "for animal in animals",
            "KKK TTTTTT KK TTTTTTT",
            "print 'I love ' animal",
            "KKKKK SSSSSSSSS TTTTTT",
            level="level10", lang='en')


    def test_10_2(self):
        self.assert_highlighted_chr_multi_line(
            "animals = red bird, black sheep, green frog, yellow duck, little child",
            "TTTTTTT K TTTTTTTTK TTTTTTTTTTTK TTTTTTTTTTK TTTTTTTTTTTK TTTTTTTTTTTT",
            "print 'brown bear'",
            "KKKKK SSSSSSSSSSSS",
            "print 'brown bear'",
            "KKKKK SSSSSSSSSSSS",
            "print 'What do you see?'",
            "KKKKK SSSSSSSSSSSSSSSSSS",
            "for animal in animals",
            "KKK TTTTTT KK TTTTTTT",
            "print 'I see a ' animal ' looking at me'",
            "KKKKK SSSSSSSSSS TTTTTT SSSSSSSSSSSSSSSS",
            "print animal",
            "KKKKK TTTTTT",
            "print animal",
            "KKKKK TTTTTT",
            "print 'What do you see?'",
            "KKKKK SSSSSSSSSSSSSSSSSS",
            "print 'I see all the animals looking at me!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level10", lang='en')


    def test_10_3(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level10", lang='en')


    def test_10_4(self):
        self.assert_highlighted_chr_multi_line(
            "monkeys = 5, 4, 3, 2",
            "TTTTTTT K NK NK NK N",
            "for monkey in monkeys",
            "KKK TTTTTT KK TTTTTTT",
            "print monkey ' little monkeys jumping on the bed'",
            "KKKKK TTTTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'One fell off and bumped his head'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Mama called the doctor and the doctor said'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'NO MORE MONKEYS JUMPING ON THE BED!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "sharks = baby, mommy, daddy, grandma, grandpa",
            "TTTTTT K TTTTK TTTTTK TTTTTK TTTTTTTK TTTTTTT",
            "for shark in sharks",
            "KKK TTTTT KK TTTTTT",
            "print shark 'tututututudu'",
            "KKKKK TTTTT SSSSSSSSSSSSSS",
            "print shark 'tututututudu'",
            "KKKKK TTTTT SSSSSSSSSSSSSS",
            "print shark 'tututututudu'",
            "KKKKK TTTTT SSSSSSSSSSSSSS",
            "print shark",
            "KKKKK TTTTT",
            "animals = pig, dog, cow",
            "TTTTTTT K TTTK TTTK TTT",
            "for animal in animals",
            "KKK TTTTTT KK TTTTTTT",
            "if animal is pig",
            "KK TTTTTT KK TTT",
            "sound = oink",
            "TTTTT K TTTT",
            "if animal is dog",
            "KK TTTTTT KK TTT",
            "sound = woof",
            "TTTTT K TTTT",
            "if animal is cow",
            "KK TTTTTT KK TTT",
            "sound = moo",
            "TTTTT K TTT",
            "print 'Old McDonald had a farm'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'E I E I O!'",
            "KKKKK SSSSSSSSSSSS",
            "print 'and on that farm he had a ' animal",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTT",
            "print 'E I E I O!'",
            "KKKKK SSSSSSSSSSSS",
            "print 'with a ' sound sound ' here'",
            "KKKKK SSSSSSSSS TTTTT TTTTT SSSSSSS",
            "print 'and a ' sound sound ' there'",
            "KKKKK SSSSSSSS TTTTT TTTTT SSSSSSSS",
            "print 'here a ' sound",
            "KKKKK SSSSSSSSS TTTTT",
            "print 'there a ' sound",
            "KKKKK SSSSSSSSSS TTTTT",
            "print 'everywhere a ' sound sound",
            "KKKKK SSSSSSSSSSSSSSS TTTTT TTTTT",
            level="level10", lang='en')


    def test_10_5(self):
        self.assert_highlighted_chr_multi_line(
            "days = Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday",
            "TTTT K TTTTTTK TTTTTTTK TTTTTTTTTK TTTTTTTTK TTTTTTK TTTTTTTTK TTTTTT",
            "names = mom, dad, Emma, Sophie",
            "TTTTT K TTTK TTTK TTTTK TTTTTT",
            "for day in days",
            "KKK TTT KK TTTT",
            "print names at random ' does the dishes on ' day",
            "KKKKK TTTTT KK KKKKKK SSSSSSSSSSSSSSSSSSSSSS TTT",
            level="level10", lang='en')


    def test_10_6(self):
        self.assert_highlighted_chr_multi_line(
            "players = Ann, John, Jesse",
            "TTTTTTT K TTTK TTTTK TTTTT",
            "choices = 1, 2, 3, 4, 5, 6",
            "TTTTTTT K NK NK NK NK NK N",
            "for player in players",
            "KKK TTTTTT KK TTTTTTT",
            "print player ' throws ' choices at random",
            "KKKKK TTTTTT SSSSSSSSSS TTTTTTT KK KKKKKK",
            "sleep",
            "KKKKK",
            level="level10", lang='en')


    def test_10_7(self):
        self.assert_highlighted_chr_multi_line(
            "choices = rock, paper, scissors",
            "TTTTTTT K TTTTK TTTTTK TTTTTTTT",
            "players = Marleen, Michael",
            "TTTTTTT K TTTTTTTK TTTTTTT",
            "for player in players",
            "KKK TTTTTT KK TTTTTTT",
            "print player ' chooses ' choices at random",
            "KKKKK TTTTTT SSSSSSSSSSS TTTTTTT KK KKKKKK",
            level="level10", lang='en')


    def test_10_8(self):
        self.assert_highlighted_chr_multi_line(
            "numbers = 1, 2, 3",
            "TTTTTTT K NK NK N",
            "for number1 in numbers",
            "KKK TTTTTTT KK TTTTTTT",
            "for number2 in numbers",
            "KKK TTTTTTT KK TTTTTTT",
            "answer = ask 'How much is ' number2 ' times ' number1 '?'",
            "TTTTTT K KKK SSSSSSSSSSSSSS TTTTTTT SSSSSSSSS TTTTTTT SSS",
            "correct = number1 * number2",
            "TTTTTTT K TTTTTTT K TTTTTTT",
            "if answer is correct",
            "KK TTTTTT KK TTTTTTT",
            "print 'Great job!'",
            "KKKKK SSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Thats wrong. The right answer is ' correct",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTT",
            level="level10", lang='en')


    def test_10_9(self):
        self.assert_highlighted_chr_multi_line(
            "courses = appetizer, main course, dessert",
            "TTTTTTT K TTTTTTTTTK TTTTTTTTTTTK TTTTTTT",
            "for course in courses",
            "KKK TTTTTT KK TTTTTTT",
            "food = ask 'What would you like to eat as your ' course '?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTT SSS",
            "print food ' will be your ' course",
            "KKKKK TTTT SSSSSSSSSSSSSSSS TTTTTT",
            level="level10", lang='en')


    def test_10_10(self):
        self.assert_highlighted_chr_multi_line(
            "courses = appetizer, main course, dessert",
            "TTTTTTT K TTTTTTTTTK TTTTTTTTTTTK TTTTTTT",
            "names = Timon, Onno",
            "TTTTT K TTTTTK TTTT",
            "for name in names",
            "KKK TTTT KK TTTTT",
            "for course in courses",
            "KKK TTTTTT KK TTTTTTT",
            "food = ask name ', what would you like to eat as your ' course '?'",
            "TTTT K KKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTT SSS",
            "print name ' orders ' food ' as their ' course",
            "KKKKK TTTT SSSSSSSSSS TTTT SSSSSSSSSSSS TTTTTT",
            level="level10", lang='en')


    def test_10_11(self):
        self.assert_highlighted_chr(
            "courses = appetizer, main course, dessert",
            "TTTTTTT K TTTTTTTTTK TTTTTTTTTTTK TTTTTTT",
            level="level10", lang='en')


    def test_10_12(self):
        self.assert_highlighted_chr_multi_line(
            "houses = mansion, apartment, shack, house",
            "TTTTTT K TTTTTTTK TTTTTTTTTK TTTTTK TTTTT",
            "loves = nobody, a royal, their neighbour, their true love",
            "TTTTT K TTTTTTK TTTTTTTK TTTTTTTTTTTTTTTK TTTTTTTTTTTTTTT",
            "pets = dog, cat, elephant",
            "TTTT K TTTK TTTK TTTTTTTT",
            "names = Jenna, Ryan, Jim",
            "TTTTT K TTTTTK TTTTK TTT",
            "for name in names",
            "KKK TTTT KK TTTTT",
            "print name ' lives in a ' houses at random",
            "KKKKK TTTT SSSSSSSSSSSSSS TTTTTT KK KKKKKK",
            "print name ' will marry ' loves at random",
            "KKKKK TTTT SSSSSSSSSSSSSS TTTTT KK KKKKKK",
            "print name ' will get a ' pets at random ' as their pet.'",
            "KKKKK TTTT SSSSSSSSSSSSSS TTTT KK KKKKKK SSSSSSSSSSSSSSSS",
            "sleep",
            "KKKKK",
            level="level10", lang='en')


    def test_10_13(self):
        self.assert_highlighted_chr_multi_line(
            "houses = Gryffindor, Slytherin, Hufflepuff, Ravenclaw",
            "TTTTTT K TTTTTTTTTTK TTTTTTTTTK TTTTTTTTTTK TTTTTTTTT",
            "subjects = potions, defence against the dark arts, charms, transfiguration",
            "TTTTTTTT K TTTTTTTK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTK TTTTTTK TTTTTTTTTTTTTTT",
            "fears = Voldemort, spiders, failing your OWL test",
            "TTTTT K TTTTTTTTTK TTTTTTTK TTTTTTTTTTTTTTTTTTTTT",
            "names = Harry, Ron, Hermione",
            "TTTTT K TTTTTK TTTK TTTTTTTT",
            "for name in names",
            "KKK TTTT KK TTTTT",
            "print name ' is placed in ' houses at random",
            "KKKKK TTTT SSSSSSSSSSSSSSSS TTTTTT KK KKKKKK",
            "print name ' is great at ' subjects at random",
            "KKKKK TTTT SSSSSSSSSSSSSSS TTTTTTTT KK KKKKKK",
            "print name 's greatest fear is ' fears at random",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSS TTTTT KK KKKKKK",
            level="level10", lang='en')


    def test_10_14(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level10", lang='en')


    
    def test_11_1(self):
        self.assert_highlighted_chr_multi_line(
            "for counter in range 1 to 5",
            "KKK TTTTTTT KK KKKKK N KK N",
            "print counter",
            "KKKKK TTTTTTT",
            level="level11", lang='en')


    def test_11_2(self):
        self.assert_highlighted_chr_multi_line(
            "for i in range 5 to 1",
            "KKK T KK KKKKK N KK N",
            "print i ' little monkeys jumping on the bed'",
            "KKKKK T SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'One fell off and bumped his head'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Mama called the doctor and the doctor said'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if i is 1",
            "KK T KK N",
            "print 'PUT THOSE MONKEYS RIGHT TO BED!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'NO MORE MONKEYS JUMPING ON THE BED!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level11", lang='en')


    def test_11_3(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level11", lang='en')


    def test_11_4(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome to Restaurant Hedy!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "people = ask 'For how many people would you like to order?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "for i in range 1 to people",
            "KKK T KK KKKKK N KK TTTTTT",
            "print 'Order number ' i",
            "KKKKK SSSSSSSSSSSSSSS T",
            "food = ask 'What would you like to eat?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print food",
            "KKKKK TTTT",
            "if food is fries",
            "KK TTTT KK TTTTT",
            "sauce = ask 'What kind of sauce would you like with that?'",
            "TTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print sauce",
            "KKKKK TTTTT",
            "drinks = ask 'What would you like to drink?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print drinks",
            "KKKKK TTTTTT",
            "price = 4 * people",
            "TTTTT K N K TTTTTT",
            "print 'That will be ' price ' dollars, please!'",
            "KKKKK SSSSSSSSSSSSSSS TTTTT SSSSSSSSSSSSSSSSSSS",
            level="level11", lang='en')


    def test_11_5(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Escape from the Haunted House!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "player is alive",
            "TTTTTT KK TTTTT",
            "doors = 1, 2, 3",
            "TTTTT K NK NK N",
            "monsters = zombie, vampire, giant spider",
            "TTTTTTTT K TTTTTTK TTTTTTTK TTTTTTTTTTTT",
            "for i in range 1 to 3",
            "KKK T KK KKKKK N KK N",
            "if player is alive",
            "KK TTTTTT KK TTTTT",
            "correct_door = doors at random",
            "TTTTTTTTTTTT K TTTTT KK KKKKKK",
            "print 'Room ' i",
            "KKKKK SSSSSSS T",
            "print 'There are 3 doors in front of you...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "chosendoor = ask 'Which door do you choose?'",
            "TTTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if chosendoor is correct_door",
            "KK TTTTTTTTTT KK TTTTTTTTTTTT",
            "print 'No monsters here!'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'You are eaten by a ' monsters at random",
            "KKKKK SSSSSSSSSSSSSSSSSSSSS TTTTTTTT KK KKKKKK",
            "player = dead",
            "TTTTTT K TTTT",
            "else",
            "KKKK",
            "print 'GAME OVER'",
            "KKKKK SSSSSSSSSSS",
            "if player is alive",
            "KK TTTTTT KK TTTTT",
            "print 'Great! You survived!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level11", lang='en')


    def test_11_6(self):
        self.assert_highlighted_chr(
            "print 'Escape from the haunted house!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level11", lang='en')


    def test_11_7(self):
        self.assert_highlighted_chr_multi_line(
            "name = ask 'Who is your favorite cartoon character?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I love watching ' name",
            "KKKKK SSSSSSSSSSSSSSSSSS TTTT",
            "show = SpongeBob SquarePants",
            "TTTT K TTTTTTTTTTTTTTTTTTTTT",
            "print show 'is my favorite show!'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSS",
            level="level11", lang='en')


    def test_11_8(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level11", lang='en')

    
    def test_12_1(self):
        self.assert_highlighted_chr_multi_line(
            "print 'decimal numbers now need to use a dot'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 2.5 + 2.5",
            "KKKKK NNN K NNN",
            level="level12", lang='en')


    def test_12_2(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Two and a half plus two and a half is...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 2.5 + 2.5",
            "KKKKK NNN K NNN",
            level="level12", lang='en')


    def test_12_3(self):
        self.assert_highlighted_chr_multi_line(
            "name = 'Hedy the Robot'",
            "TTTT K SSSSSSSSSSSSSSSS",
            "print 'Hello ' name",
            "KKKKK SSSSSSSS TTTT",
            level="level12", lang='en')


    def test_12_4(self):
        self.assert_highlighted_chr_multi_line(
            "superheroes = 'Spiderman', 'Batman', 'Iron Man'",
            "TTTTTTTTTTT K SSSSSSSSSSSK SSSSSSSSK SSSSSSSSSS",
            "print superheroes at random",
            "KKKKK TTTTTTTTTTT KK KKKKKK",
            level="level12", lang='en')


    def test_12_5(self):
        self.assert_highlighted_chr_multi_line(
            "name = ask 'What is your name?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "if name = 'Hedy the Robot'",
            "KK TTTT K SSSSSSSSSSSSSSSS",
            "print 'Hi there!'",
            "KKKKK SSSSSSSSSSS",
            level="level12", lang='en')


    def test_12_6(self):
        self.assert_highlighted_chr_multi_line(
            "score = 25",
            "TTTTT K NN",
            "print 'You got ' score",
            "KKKKK SSSSSSSSSS TTTTT",
            level="level12", lang='en')


    def test_12_7(self):
        self.assert_highlighted_chr_multi_line(
            "a = 'Hello '",
            "T K SSSSSSSS",
            "b = 'world!'",
            "T K SSSSSSSS",
            "print a + b",
            "KKKKK T K T",
            level="level12", lang='en')


    def test_12_8(self):
        self.assert_highlighted_chr_multi_line(
            "name = 'The Queen of England'",
            "TTTT K SSSSSSSSSSSSSSSSSSSSSS",
            "print name ' was eating a piece of cake, when suddenly...'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level12", lang='en')


    def test_12_9(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level12", lang='en')


    def test_12_10(self):
        self.assert_highlighted_chr_multi_line(
            "actions = 'clap your hands', 'stomp your feet', 'shout Hurray!'",
            "TTTTTTT K SSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSS",
            "for action in actions",
            "KKK TTTTTT KK TTTTTTT",
            "for i in range 1 to 2",
            "KKK T KK KKKKK N KK N",
            "print 'if youre happy and you know it'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print action",
            "KKKKK TTTTTT",
            "print 'if youre happy and you know it and you really want to show it'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'if youre happy and you know it'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print action",
            "KKKKK TTTTTT",
            level="level12", lang='en')


    def test_12_11(self):
        self.assert_highlighted_chr_multi_line(
            "number1 = ask 'What is the first number?'",
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "number2 = ask 'What is the second number?'",
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "answer = number1 + number2",
            "TTTTTT K TTTTTTT K TTTTTTT",
            "print number1 ' plus ' number2 ' is ' answer",
            "KKKKK TTTTTTT SSSSSSSS TTTTTTT SSSSSS TTTTTT",
            level="level12", lang='en')


    def test_12_12(self):
        self.assert_highlighted_chr_multi_line(
            "price = 0",
            "TTTTT K N",
            "food = ask 'What would you like to order?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "drinks = ask 'What would you like to drink?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if food is 'hamburger'",
            "KK TTTT KK SSSSSSSSSSS",
            "price = price + 6.50",
            "TTTTT K TTTTT K NNNN",
            "if food is 'pizza'",
            "KK TTTT KK SSSSSSS",
            "price = price + 5.75",
            "TTTTT K TTTTT K NNNN",
            "if drinks is 'water'",
            "KK TTTTTT KK SSSSSSS",
            "price = price + 1.20",
            "TTTTT K TTTTT K NNNN",
            "if drink is 'soda'",
            "KK TTTTT KK SSSSSS",
            "price = price + 2.35",
            "TTTTT K TTTTT K NNNN",
            "print 'That will be ' price ' dollar, please'",
            "KKKKK SSSSSSSSSSSSSSS TTTTT SSSSSSSSSSSSSSSSS",
            level="level12", lang='en')


    def test_12_13(self):
        self.assert_highlighted_chr_multi_line(
            "fortunes = 'you will be rich', 'you will fall in love', 'you will slip on a banana peel'",
            "TTTTTTTT K SSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I will take a look in my crystall ball for your future.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I see... I see...'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            "sleep",
            "KKKKK",
            "print fortunes at random",
            "KKKKK TTTTTTTT KK KKKKKK",
            level="level12", lang='en')


    def test_12_14(self):
        self.assert_highlighted_chr_multi_line(
            "print 'The digital piggy bank'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            "wish = ask 'What would you like to buy?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "price = ask 'How much does that cost?'",
            "TTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "saved = ask 'How much money have you saved already?'",
            "TTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "allowance = ask 'How much pocket money do you get per week?'",
            "TTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "to_save = price - saved",
            "TTTTTTT K TTTTT K TTTTT",
            "weeks = to_save / allowance",
            "TTTTT K TTTTTTT K TTTTTTTTT",
            "print 'You can buy a ' wish ' in ' weeks ' weeks.'",
            "KKKKK SSSSSSSSSSSSSSSS TTTT SSSSSS TTTTT SSSSSSSSS",
            level="level12", lang='en')


    def test_12_15(self):
        self.assert_highlighted_chr_multi_line(
            "name is ask 'What is your name?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
            "if name is 'Agent007'",
            "KK TTTT KK SSSSSSSSSS",
            "a is 'Go to the airport '",
            "T KK SSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "a is 'Go to the trainstation '",
            "T KK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "password is ask 'What is the password?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSS",
            "if password is 'TOPSECRET'",
            "KK TTTTTTTT KK SSSSSSSSSSS",
            "b is 'tomorrow at 02.00'",
            "T KK SSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "b is 'today at 10.00'",
            "T KK SSSSSSSSSSSSSSSS",
            "print a + b",
            "KKKKK T K T",
            level="level12", lang='en')


    def test_12_16(self):
        self.assert_highlighted_chr(
            "## place your code here",
            "CCCCCCCCCCCCCCCCCCCCCCC",
            level="level12", lang='en')


    def test_12_17(self):
        self.assert_highlighted_chr_multi_line(
            "username is ask 'What is your username?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSS",
            "password is ask 'What is your password?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSS",
            "if username is 'Hedy'",
            "KK TTTTTTTT KK SSSSSS",
            "if password is 'secret'",
            "KK TTTTTTTT KK SSSSSSSS",
            "print 'Welcome Hedy!'",
            "KKKKK SSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Access denied'",
            "KKKKK SSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Access denied!'",
            "KKKKK SSSSSSSSSSSSSSSS",
            level="level12", lang='en')


    def test_12_18(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level12", lang='en')


    def test_13_1(self):
        self.assert_highlighted_chr_multi_line(
            "name = ask 'what is your name?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "age = ask 'what is your age?'",
            "TTT K KKK SSSSSSSSSSSSSSSSSSS",
            "if name is 'Hedy' and age is 2",
            "KK TTTT KK SSSSSS KKK TTT KK N",
            "print 'You are the real Hedy!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            level="level13", lang='en')


    def test_13_2(self):
        self.assert_highlighted_chr_multi_line(
            "sword = 'lost'",
            "TTTTT K SSSSSS",
            "game = 'on'",
            "TTTT K SSSS",
            "print 'Our hero is walking through the forest'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'The path splits two ways'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "for i in range 0 to 2",
            "KKK T KK KKKKK N KK N",
            "if game is 'on'",
            "KK TTTT KK SSSS",
            "path = ask 'Which path should she choose?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if path is 'left' and sword is 'found'",
            "KK TTTT KK SSSSSS KKK TTTTT KK SSSSSSS",
            "print 'Our hero comes across a dragon!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Luckily our hero has a sword to defeat the beast!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "game = 'over'",
            "TTTT K SSSSSS",
            "if path is 'left' and sword is 'lost'",
            "KK TTTT KK SSSSSS KKK TTTTT KK SSSSSS",
            "print 'Our hero finds a dragon, but she doesnt have any weapons!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Our hero is beaten by the dragon...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Try again'",
            "KKKKK SSSSSSSSSSS",
            "game = 'over'",
            "TTTT K SSSSSS",
            "if path is 'right' and sword is 'found'",
            "KK TTTT KK SSSSSSS KKK TTTTT KK SSSSSSS",
            "print 'You have already found the sword. There is nothing left here.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'She walks back'",
            "KKKKK SSSSSSSSSSSSSSSS",
            "if path is 'right' and sword is 'lost'",
            "KK TTTT KK SSSSSSS KKK TTTTT KK SSSSSS",
            "print 'Our hero finds a sword'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'This could come in very handy'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "sword = 'found'",
            "TTTTT K SSSSSSS",
            level="level13", lang='en')


    def test_13_3(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level13", lang='en')


    def test_13_4(self):
        self.assert_highlighted_chr_multi_line(
            "options = 'rock', 'paper', 'scissors'",
            "TTTTTTT K SSSSSSK SSSSSSSK SSSSSSSSSS",
            "your_choice = ask 'What do you choose?'",
            "TTTTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSS",
            "computer_choice = options at random",
            "TTTTTTTTTTTTTTT K TTTTTTT KK KKKKKK",
            "print 'You choose ' your_choice",
            "KKKKK SSSSSSSSSSSSS TTTTTTTTTTT",
            "print 'The computer chooses ' computer_choice",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS TTTTTTTTTTTTTTT",
            "if computer_choice is your_choice",
            "KK TTTTTTTTTTTTTTT KK TTTTTTTTTTT",
            "print 'Tie'",
            "KKKKK SSSSS",
            "if computer_choice is 'rock' and your_choice is 'paper'",
            "KK TTTTTTTTTTTTTTT KK SSSSSS KKK TTTTTTTTTTT KK SSSSSSS",
            "print 'You win!'",
            "KKKKK SSSSSSSSSS",
            "if computer_choice is 'rock' and your_choice is 'scissors'",
            "KK TTTTTTTTTTTTTTT KK SSSSSS KKK TTTTTTTTTTT KK SSSSSSSSSS",
            "print 'The computer wins!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSS",
            level="level13", lang='en')


    def test_13_5(self):
        self.assert_highlighted_chr_multi_line(
            "price = 10",
            "TTTTT K NN",
            "food = ask 'What would you like to eat?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "drinks = ask 'What would you like to drink?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if food is 'sandwich' and drinks is 'juice'",
            "KK TTTT KK SSSSSSSSSS KKK TTTTTT KK SSSSSSS",
            "print 'Thats our discount menu'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "price = price - 3",
            "TTTTT K TTTTT K N",
            "print 'That will be ' price ' dollars'",
            "KKKKK SSSSSSSSSSSSSSS TTTTT SSSSSSSSSS",
            level="level13", lang='en')


    def test_13_6(self):
        self.assert_highlighted_chr_multi_line(
            "drinks = ask 'What would you like to drink?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if drinks is 'water' or drinks is 'juice'",
            "KK TTTTTT KK SSSSSSS KK TTTTTT KK SSSSSSS",
            "print 'Thats a healthy choice'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            level="level13", lang='en')


    def test_13_7(self):
        self.assert_highlighted_chr_multi_line(
            "name is ask 'What is your name?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
            "password is ask 'What is your password?'",
            "TTTTTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSS",
            "if name is 'Agent007' and password is 'TOPSECRET'",
            "KK TTTT KK SSSSSSSSSS KKK TTTTTTTT KK SSSSSSSSSSS",
            "print 'Go to the airport at 02.00'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Go to the trainstation at 10.00'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level13", lang='en')


    def test_13_8(self):
        self.assert_highlighted_chr(
            "## place your code here",
            "CCCCCCCCCCCCCCCCCCCCCCC",
            level="level13", lang='en')


    def test_13_9(self):
        self.assert_highlighted_chr_multi_line(
            "first_grade = ask 'What score did you get on your first test?'",
            "TTTTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "second_grade = ask 'What score did you get on your second test?'",
            "TTTTTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "added is first_grade + second_grade",
            "TTTTT KK TTTTTTTTTTT K TTTTTTTTTTTT",
            "mean_grade is added / 2",
            "TTTTTTTTTT KK TTTTT K N",
            "if mean_grade = 1 or mean_grade = 2 or mean_grade = 3 or mean_grade = 4 or mean_grade = 5",
            "KK TTTTTTTTTT K N KK TTTTTTTTTT K N KK TTTTTTTTTT K N KK TTTTTTTTTT K N KK TTTTTTTTTT K N",
            "print 'Oh no! You have failed the subject...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Great! You have passed the subject!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level13", lang='en')


    def test_13_10(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level13", lang='en')


    def test_14_1(self):
        self.assert_highlighted_chr_multi_line(
            "age = ask 'How old are you?'",
            "TTT K KKK SSSSSSSSSSSSSSSSSS",
            "if age < 13",
            "KK TTT K NN",
            "print 'You are younger than me!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'You are older than me!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            level="level14", lang='en')


    def test_14_2(self):
        self.assert_highlighted_chr_multi_line(
            "age = ask 'How old are you?'",
            "TTT K KKK SSSSSSSSSSSSSSSSSS",
            "if age > 12",
            "KK TTT K NN",
            "print 'You are older than I am!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level14", lang='en')


    def test_14_3(self):
        self.assert_highlighted_chr_multi_line(
            "name = ask 'What is your name?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "if name == 'Hedy'",
            "KK TTTT KK SSSSSS",
            "print 'You are coo!'",
            "KKKKK SSSSSSSSSSSSSS",
            level="level14", lang='en')


    def test_14_4(self):
        self.assert_highlighted_chr_multi_line(
            "name = ask 'What is your name?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "if name != 'Hedy'",
            "KK TTTT KK SSSSSS",
            "print 'You are not Hedy'",
            "KKKKK SSSSSSSSSSSSSSSSSS",
            level="level14", lang='en')


    def test_14_5(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Guess which number'",
            "KKKKK SSSSSSSSSSSSSSSSSSSS",
            "numbers = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
            "TTTTTTT K NK NK NK NK NK NK NK NK NK NN",
            "number = numbers at random",
            "TTTTTT K TTTTTTT KK KKKKKK",
            "game = 'on'",
            "TTTT K SSSS",
            "for i in range 1 to 10",
            "KKK T KK KKKKK N KK NN",
            "if game == 'on'",
            "KK TTTT KK SSSS",
            "guess = ask 'Which number do you think it is?'",
            "TTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if guess > number",
            "KK TTTTT K TTTTTT",
            "print 'Lower!'",
            "KKKKK SSSSSSSS",
            "if guess < number",
            "KK TTTTT K TTTTTT",
            "print 'Higher!'",
            "KKKKK SSSSSSSSS",
            "if guess == number",
            "KK TTTTT KK TTTTTT",
            "print 'You win!'",
            "KKKKK SSSSSSSSSS",
            "game = 'over'",
            "TTTT K SSSSSS",
            level="level14", lang='en')


    def test_14_6(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level14", lang='en')


    def test_14_7(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Escape from the haunted house'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "lives = 3",
            "TTTTT K N",
            "doors = 1, 2, 3",
            "TTTTT K NK NK N",
            "monsters = 'the wicked witch', 'a zombie', 'a sleeping 3 headed dog'",
            "TTTTTTTT K SSSSSSSSSSSSSSSSSSK SSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "for i in range 1 to 10",
            "KKK T KK KKKKK N KK NN",
            "if lives > 0",
            "KK TTTTT K N",
            "good_door = doors at random",
            "TTTTTTTTT K TTTTT KK KKKKKK",
            "monster = monsters at random",
            "TTTTTTT K TTTTTTTT KK KKKKKK",
            "chosen_door = ask 'Which door do you choose?'",
            "TTTTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if good_door == chosen_door",
            "KK TTTTTTTTT KK TTTTTTTTTTT",
            "print 'You have chosen the correct door'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'You see...' monster",
            "KKKKK SSSSSSSSSSSS TTTTTTT",
            "if monster == 'a sleeping 3 headed dog'",
            "KK TTTTTTT KK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Pffieuw.... Its asleep'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'You lose one life'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            "lives = lives -1",
            "TTTTT K TTTTT KN",
            "else",
            "KKKK",
            "print 'GAME OVER'",
            "KKKKK SSSSSSSSSSS",
            level="level14", lang='en')


    def test_14_8(self):
        self.assert_highlighted_chr_multi_line(
            "money = ask 'How much money have you saved?'",
            "TTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "wish = ask 'How much money do you need?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "allowance = ask 'How much pocket money do you get each week?'",
            "TTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "to_save = wish - money",
            "TTTTTTT K TTTT K TTTTT",
            "weeks = to_save / allowance",
            "TTTTT K TTTTTTT K TTTTTTTTT",
            "if wish > money",
            "KK TTTT K TTTTT",
            "print 'You need to save up some more!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Youll need ' weeks ' more weeks.'",
            "KKKKK SSSSSSSSSSSSS TTTTT SSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Great! You have enough'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Lets go shopping!'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            level="level14", lang='en')


    def test_14_9(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Make your own quiz'",
            "KKKKK SSSSSSSSSSSSSSSSSSSS",
            "points_a = 0",
            "TTTTTTTT K N",
            "points_b = 0",
            "TTTTTTTT K N",
            "print 'Question'",
            "KKKKK SSSSSSSSSS",
            "print 'Answer option A'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "print 'Answer option B'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "answer = ask 'Which answer?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSS",
            "if answer == 'A'",
            "KK TTTTTT KK SSS",
            "points_a = points_a + 1",
            "TTTTTTTT K TTTTTTTT K N",
            "if answer == 'B'",
            "KK TTTTTT KK SSS",
            "points_b = points_b + 1",
            "TTTTTTTT K TTTTTTTT K N",
            "print 'End of the quiz!'",
            "KKKKK SSSSSSSSSSSSSSSSSS",
            "print 'Lets see the results!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            "if points_a > points_b",
            "KK TTTTTTTT K TTTTTTTT",
            "print 'You belong to the A club'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if points_b > points_a",
            "KK TTTTTTTT K TTTTTTTT",
            "print 'You belong to the B club'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level14", lang='en')


    def test_14_10(self):
        self.assert_highlighted_chr_multi_line(
            "game is 'on'",
            "TTTT KK SSSS",
            "for i in range 1 to 100",
            "KKK T KK KKKKK N KK NNN",
            "if game is 'on'",
            "KK TTTT KK SSSS",
            "answer = ask 'Do you want to continue?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if answer is 'no'",
            "KK TTTTTT KK SSSS",
            "game is 'over'",
            "TTTT KK SSSSSS",
            "if answer is 'yes'",
            "KK TTTTTT KK SSSSS",
            "print 'Ok we will continue'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSS",
            level="level14", lang='en')


    def test_14_11(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level14", lang='en')


    def test_15_1(self):
        self.assert_highlighted_chr_multi_line(
            "answer = 0",
            "TTTTTT K N",
            "while answer != 25",
            "KKKKK TTTTTT KK NN",
            "answer = ask 'What is 5 times 5?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "print 'A correct answer has been given'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level15", lang='en')


    def test_15_2(self):
        self.assert_highlighted_chr_multi_line(
            "keys = 'lost'",
            "TTTT K SSSSSS",
            "print 'You are standing in your garden and you have lost your keys.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Where do you want to look for them?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You can choose: tree, flowerbed, rock, postbox'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "while keys == 'lost'",
            "KKKKK TTTT KK SSSSSS",
            "location = ask 'Where do you want to look?'",
            "TTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if location == 'flowerbed'",
            "KK TTTTTTTT KK SSSSSSSSSSS",
            "print 'Here they are!'",
            "KKKKK SSSSSSSSSSSSSSSS",
            "keys = 'found'",
            "TTTT K SSSSSSS",
            "else",
            "KKKK",
            "print 'Nope they are not at the ' location",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTTTT",
            "print 'Now you can enter the house!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level15", lang='en')


    def test_15_3(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level15", lang='en')


    def test_15_4(self):
        self.assert_highlighted_chr_multi_line(
            "options = 1, 2, 3, 4, 5, 6",
            "TTTTTTT K NK NK NK NK NK N",
            "print 'Throw 6 as fast as you can!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "thrown = 0",
            "TTTTTT K N",
            "tries = 0",
            "TTTTT K N",
            "while thrown != 6",
            "KKKKK TTTTTT KK N",
            "thrown = options at random",
            "TTTTTT K TTTTTTT KK KKKKKK",
            "print 'You threw ' thrown",
            "KKKKK SSSSSSSSSSSS TTTTTT",
            "tries = tries + 1",
            "TTTTT K TTTTT K N",
            "print 'Yes! You have thrown 6 in ' tries ' tries.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTT SSSSSSSSS",
            level="level15", lang='en')


    def test_15_5(self):
        self.assert_highlighted_chr_multi_line(
            "won = 'no'",
            "TTT K SSSS",
            "options = 'rock', 'paper', 'scissors'",
            "TTTTTTT K SSSSSSK SSSSSSSK SSSSSSSSSS",
            "while won == 'no'",
            "KKKKK TTT KK SSSS",
            "your_choice = ask 'What do you choose?'",
            "TTTTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSS",
            "computer_choice = options at random",
            "TTTTTTTTTTTTTTT K TTTTTTT KK KKKKKK",
            "print 'you chose ' your_choice",
            "KKKKK SSSSSSSSSSSS TTTTTTTTTTT",
            "print 'the computer chose ' computer_choice",
            "KKKKK SSSSSSSSSSSSSSSSSSSSS TTTTTTTTTTTTTTT",
            "if computer_choice == your_choice",
            "KK TTTTTTTTTTTTTTT KK TTTTTTTTTTT",
            "print 'Tie!'",
            "KKKKK SSSSSS",
            "if computer_choice == 'rock' and your_choice == 'scissors'",
            "KK TTTTTTTTTTTTTTT KK SSSSSS KKK TTTTTTTTTTT KK SSSSSSSSSS",
            "print 'You lose!'",
            "KKKKK SSSSSSSSSSS",
            "if computer_choice == 'rock' and your_choice == 'paper'",
            "KK TTTTTTTTTTTTTTT KK SSSSSS KKK TTTTTTTTTTT KK SSSSSSS",
            "print 'You win!'",
            "KKKKK SSSSSSSSSS",
            "won = 'yes'",
            "TTT K SSSSS",
            level="level15", lang='en')


    def test_15_6(self):
        self.assert_highlighted_chr_multi_line(
            "score = 0",
            "TTTTT K N",
            "for i in range 0 to 9",
            "KKK T KK KKKKK N KK N",
            "numbers = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
            "TTTTTTT K NK NK NK NK NK NK NK NK NK NN",
            "number1 = numbers at random",
            "TTTTTTT K TTTTTTT KK KKKKKK",
            "number2 = numbers at random",
            "TTTTTTT K TTTTTTT KK KKKKKK",
            "correct = number1 * number2",
            "TTTTTTT K TTTTTTT K TTTTTTT",
            "answer = 0",
            "TTTTTT K N",
            "while answer != correct",
            "KKKKK TTTTTT KK TTTTTTT",
            "print 'How much is ' number1 ' times ' number2 '?'",
            "KKKKK SSSSSSSSSSSSSS TTTTTTT SSSSSSSSS TTTTTTT SSS",
            "answer = ask 'Fill in your answer:'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSS",
            "print 'Your answer is ' answer",
            "KKKKK SSSSSSSSSSSSSSSSS TTTTTT",
            "print 'Good job!'",
            "KKKKK SSSSSSSSSSS",
            "print 'You win!'",
            "KKKKK SSSSSSSSSS",
            level="level15", lang='en')


    def test_15_7(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Welcome at McHedy'",
            "KKKKK SSSSSSSSSSSSSSSSSSS",
            "more = 'yes'",
            "TTTT K SSSSS",
            "while more == 'yes'",
            "KKKKK TTTT KK SSSSS",
            "order = ask 'What would you like to order?'",
            "TTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print order",
            "KKKKK TTTTT",
            "more = ask 'Would you like to order anything else?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Thank you!'",
            "KKKKK SSSSSSSSSSSS",
            level="level15", lang='en')


    def test_15_8(self):
        self.assert_highlighted_chr_multi_line(
            "animals = 'chicken', 'horse', 'cow'",
            "TTTTTTT K SSSSSSSSSK SSSSSSSK SSSSS",
            "sounds = 'cluck', 'neigh', 'moo'",
            "TTTTTT K SSSSSSSK SSSSSSSK SSSSS",
            "for animal in animals",
            "KKK TTTTTT KK TTTTTTT",
            "print 'A ' animal ' says ' sounds at random",
            "KKKKK SSSS TTTTTT SSSSSSSS TTTTTT KK KKKKKK",
            "animals = 'chicken', 'horse', 'cow'",
            "TTTTTTT K SSSSSSSSSK SSSSSSSK SSSSS",
            "sounds = 'cluck', 'neigh', 'moo'",
            "TTTTTT K SSSSSSSK SSSSSSSK SSSSS",
            "for animal in animals",
            "KKK TTTTTT KK TTTTTTT",
            "for sound in sounds",
            "KKK TTTTT KK TTTTTT",
            "print 'A ' animal ' says ' sound",
            "KKKKK SSSS TTTTTT SSSSSSSS TTTTT",
            level="level15", lang='en')


    def test_15_9(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level15", lang='en')


    def test_16_1(self):
        self.assert_highlighted_chr_multi_line(
            "fruit = ['apple', 'banana', 'cherry']",
            "TTTTT K KSSSSSSSK SSSSSSSSK SSSSSSSSK",
            "print fruit",
            "KKKKK TTTTT",
            level="level16", lang='en')


    def test_16_2(self):
        self.assert_highlighted_chr_multi_line(
            "friends = ['Ahmed', 'Ben', 'Cayden']",
            "TTTTTTT K KSSSSSSSK SSSSSK SSSSSSSSK",
            "lucky_numbers = [15, 18, 6]",
            "TTTTTTTTTTTTT K KNNK NNK NK",
            "for i in range 1 to 3",
            "KKK T KK KKKKK N KK N",
            "print 'the lucky number of ' friends[i]",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS TTTTTTTKTK",
            "print 'is ' lucky_numbers[i]",
            "KKKKK SSSSS TTTTTTTTTTTTTKTK",
            level="level16", lang='en')


    def test_16_3(self):
        self.assert_highlighted_chr_multi_line(
            "animals = ['pig', 'dog', 'cow']",
            "TTTTTTT K KSSSSSK SSSSSK SSSSSK",
            "sounds = ['oink', 'woof', 'moo']",
            "TTTTTT K KSSSSSSK SSSSSSK SSSSSK",
            "for i in range 1 to 3",
            "KKK T KK KKKKK N KK N",
            "animal = animals[i]",
            "TTTTTT K TTTTTTTKTK",
            "sound = sounds[i]",
            "TTTTT K TTTTTTKTK",
            "print 'Old McDonald had a farm'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'E I E I O!'",
            "KKKKK SSSSSSSSSSSS",
            "print 'and on that farm he had a ' animal",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTT",
            "print 'E I E I O!'",
            "KKKKK SSSSSSSSSSSS",
            "print 'with a ' sound sound ' here'",
            "KKKKK SSSSSSSSS TTTTT TTTTT SSSSSSS",
            "print 'and a ' sound sound ' there'",
            "KKKKK SSSSSSSS TTTTT TTTTT SSSSSSSS",
            "print 'here a ' sound",
            "KKKKK SSSSSSSSS TTTTT",
            "print 'there a ' sound",
            "KKKKK SSSSSSSSSS TTTTT",
            "print 'everywhere a ' sound sound",
            "KKKKK SSSSSSSSSSSSSSS TTTTT TTTTT",
            "lines = ['what shall we do with the drunken sailor', 'shave his belly with a rusty razor', 'put him in a long boat till hes sober']",
            "TTTTT K KSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSK",
            "for line in lines",
            "KKK TTTT KK TTTTT",
            "for i in range 1 to 3",
            "KKK T KK KKKKK N KK N",
            "print line",
            "KKKKK TTTT",
            "print 'early in the morning'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            "for i in range 1 to 3",
            "KKK T KK KKKKK N KK N",
            "print 'way hay and up she rises'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'early in the morning'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level16", lang='en')


    def test_16_4(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level16", lang='en')


    def test_16_5(self):
        self.assert_highlighted_chr_multi_line(
            "numbers = [1, 2, 3]",
            "TTTTTTT K KNK NK NK",
            "i = numbers[random]",
            "T K TTTTTTTKTTTTTTK",
            "hint = ['growling', 'a cackling laugh', 'fluttering batwings']",
            "TTTT K KSSSSSSSSSSK SSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSK",
            "monsters = ['zombie', 'witch', 'vampire']",
            "TTTTTTTT K KSSSSSSSSK SSSSSSSK SSSSSSSSSK",
            "bad_fate = ['Your brain is eaten', 'You are forever cursed', 'You are bitten']",
            "TTTTTTTT K KSSSSSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSK",
            "good_fate = ['You throw the ham. The zombie is distracted and starts etaing it.', 'You set the curtains on fire. The witch flees out of fear for the fire', 'The vampire hates garlic and flees']",
            "TTTTTTTTT K KSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSK",
            "weapons = ['ham', 'lighter', 'garlic']",
            "TTTTTTT K KSSSSSK SSSSSSSSSK SSSSSSSSK",
            "print 'You are standing in front of an old mension'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'Something is not right here'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You hear ' hint[i]",
            "KKKKK SSSSSSSSSSS TTTTKTK",
            "print 'You are going to explore it'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'You enter the kitchen en see a lighter, a raw ham and a garlic.'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "your_weapon = ask 'What do you bring with you?'",
            "TTTTTTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'With your ' your_weapon ' you enter the living room'",
            "KKKKK SSSSSSSSSSSS TTTTTTTTTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'There you find a ' monsters[i]",
            "KKKKK SSSSSSSSSSSSSSSSSSS TTTTTTTTKTK",
            "needed_weapon = weapons[i]",
            "TTTTTTTTTTTTT K TTTTTTTKTK",
            "if your_weapon == needed_weapon",
            "KK TTTTTTTTTTT KK TTTTTTTTTTTTT",
            "print 'You use your ' your_weapon",
            "KKKKK SSSSSSSSSSSSSSS TTTTTTTTTTT",
            "print good_fate[i]",
            "KKKKK TTTTTTTTTKTK",
            "print 'YOU WIN!'",
            "KKKKK SSSSSSSSSS",
            "else",
            "KKKK",
            "print 'You have chosen the wrong weapon...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print bad_fate[i]",
            "KKKKK TTTTTTTTKTK",
            "print 'GAME OVER'",
            "KKKKK SSSSSSSSSSS",
            level="level16", lang='en')


    def test_16_6(self):
        self.assert_highlighted_chr_multi_line(
            "french_words = ['bonjour', 'ordinateur', 'pomme de terre']",
            "TTTTTTTTTTTT K KSSSSSSSSSK SSSSSSSSSSSSK SSSSSSSSSSSSSSSSK",
            "translation = ['hello', 'computer', 'potato']",
            "TTTTTTTTTTT K KSSSSSSSK SSSSSSSSSSK SSSSSSSSK",
            "score = 0",
            "TTTTT K N",
            "for i in range 1 to 3",
            "KKK T KK KKKKK N KK N",
            "answer = ask 'What does ' french_words[i] ' mean?'",
            "TTTTTT K KKK SSSSSSSSSSSS TTTTTTTTTTTTKTK SSSSSSSS",
            "correct = translation[i]",
            "TTTTTTT K TTTTTTTTTTTKTK",
            "if answer == correct",
            "KK TTTTTT KK TTTTTTT",
            "print 'Correct!'",
            "KKKKK SSSSSSSSSS",
            "score = score + 1",
            "TTTTT K TTTTT K N",
            "else",
            "KKKK",
            "print 'Wrong, ' french_words[i] ' means ' translation[i]",
            "KKKKK SSSSSSSSS TTTTTTTTTTTTKTK SSSSSSSSS TTTTTTTTTTTKTK",
            "print 'You gave ' score ' correct answers.'",
            "KKKKK SSSSSSSSSSS TTTTT SSSSSSSSSSSSSSSSSSS",
            level="level16", lang='en')


    def test_16_7(self):
        self.assert_highlighted_chr_multi_line(
            "print 'What is for dinner tonight?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "options = ['pizza', 'broccoli', 'green beans']",
            "TTTTTTT K KSSSSSSSK SSSSSSSSSSK SSSSSSSSSSSSSK",
            "chosen = options at random",
            "TTTTTT K TTTTTTT KK KKKKKK",
            "if chosen = 'pizza'",
            "KK TTTTTT K SSSSSSS",
            "print 'Yummy! Pizza!'",
            "KKKKK SSSSSSSSSSSSSSS",
            "else",
            "KKKK",
            "print 'Yikes...'",
            "KKKKK SSSSSSSSSS",
            level="level16", lang='en')


    def test_16_8(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level16", lang='en')


    def test_17_1(self):
        self.assert_highlighted_chr_multi_line(
            "for i in range 1 to 10:",
            "KKK T KK KKKKK N KK NNK",
            "print i",
            "KKKKK T",
            "print 'Ready or not, here I come!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level17", lang='en')


    def test_17_2(self):
        self.assert_highlighted_chr_multi_line(
            "prices = ['1 million dollars', 'an apple pie', 'nothing']",
            "TTTTTT K KSSSSSSSSSSSSSSSSSSSK SSSSSSSSSSSSSSK SSSSSSSSSK",
            "your_price = prices[random]",
            "TTTTTTTTTT K TTTTTTKTTTTTTK",
            "print 'You win ' your_price",
            "KKKKK SSSSSSSSSS TTTTTTTTTT",
            "if your_price == '1 million dollars' :",
            "KK TTTTTTTTTT KK SSSSSSSSSSSSSSSSSSS K",
            "print 'Yeah! You are rich!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSS",
            "elif your_price == 'an apple pie' :",
            "KKKK TTTTTTTTTT KK SSSSSSSSSSSSSS K",
            "print 'Lovely, an apple pie!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            "else:",
            "KKKKK",
            "print 'Better luck next time..'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level17", lang='en')


    def test_17_3(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level17", lang='en')

    def test_18_1(self):
        self.assert_highlighted_chr_multi_line(
            "naam = 'Hedy'",
            "TTTT K SSSSSS",
            "print('My name is ', naam)",
            "KKKKKKSSSSSSSSSSSSSK TTTTK",
            level="level18", lang='en')


    def test_18_2(self):
        self.assert_highlighted_chr_multi_line(
            "print('my name is Hedy!')",
            "KKKKKKSSSSSSSSSSSSSSSSSSK",
            "name = 'Hedy'",
            "TTTT K SSSSSS",
            "print('my name is ', name)",
            "KKKKKKSSSSSSSSSSSSSK TTTTK",
            level="level18", lang='en')


    def test_18_3(self):
        self.assert_highlighted_chr(
            "print ('Great job!!!')",
            "KKKKK KSSSSSSSSSSSSSSK",
            level="level18", lang='en')


