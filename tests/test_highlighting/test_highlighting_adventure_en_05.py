from tests.Highlighter import HighlightTester

class HighlighterTestLeveL5(HighlightTester):


    def test_1(self):
        self.assertHighlightedChrMultiLine(
            "name is ask 'what is your name?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
            "if name is Hedy print 'cool!' else print 'meh'",
            "KK TTTT KK TTTT KKKKK SSSSSSS KKKK KKKKK SSSSS",
            level="level5",lang='en')


    def test_2(self):
        self.assertHighlightedChrMultiLine(
            "name is ask 'what is your name?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
            "if name is Hedy print 'nice' else print 'boo!'",
            "KK TTTT KK TTTT KKKKK SSSSSS KKKK KKKKK SSSSSS",
            level="level5",lang='en')


    def test_3(self):
        self.assertHighlightedChrMultiLine(
            "pretty_colors is green, yellow",
            "TTTTTTTTTTTTT KK TTTTTK TTTTTT",
            "color is ask 'What is your favorite color?'",
            "TTTTT KK KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if color in pretty_colors print 'pretty!'",
            "KK TTTTT KK TTTTTTTTTTTTT KKKKK SSSSSSSSS",
            "else print 'meh'",
            "KKKK KKKKK SSSSS",
            level="level5",lang='en')


    def test_4(self):
        self.assertHighlightedChrMultiLine(
            "name is ask 'what is your name?'",
            "TTTT KK KKK SSSSSSSSSSSSSSSSSSSS",
            "if name is Hedy print 'nice'",
            "KK TTTT KK TTTT KKKKK SSSSSS",
            "else print 'boo!'",
            "KKKK KKKKK SSSSSS",
            level="level5",lang='en')


    def test_5(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_6(self):
        self.assertHighlightedChr(
            "print 'Here your story will start!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')


    def test_7(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_8(self):
        self.assertHighlightedChr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level5",lang='en')


    def test_9(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_10(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_11(self):
        self.assertHighlightedChrMultiLine(
            "people is mom, dad, Emma, Sophie",
            "TTTTTT KK TTTK TTTK TTTTK TTTTTT",
            "dishwasher is people at random",
            "TTTTTTTTTT KK TTTTTT KK KKKKKK",
            "if dishwasher is Sophie print _ too bad I have to do the dishes _ else print 'luckily no dishes because' _ 'is already washing up'",
            "KK TTTTTTTTTT KK TTTTTT KKKKK I                                 I KKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS I SSSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')


    def test_12(self):
        self.assertHighlightedChr(
            "print 'Who does the dishes?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')


    def test_13(self):
        self.assertHighlightedChrMultiLine(
            "choices is 1, 2, 3, 4, 5, earthworm",
            "TTTTTTT KK TK TK TK TK TK TTTTTTTTT",
            "throw is _",
            "TTTTT KK I",
            "print 'you have' _ 'thrown'",
            "KKKKK SSSSSSSSSS I SSSSSSSS",
            "if _ is earthworm print 'You can stop throwing.' _ print 'You have to hear it again!'",
            "KK I KK TTTTTTTTT KKKKK SSSSSSSSSSSSSSSSSSSSSSSS I KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')


    def test_14(self):
        self.assertHighlightedChr(
            "print 'What will the die indicate this time?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')


    def test_15(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_16(self):
        self.assertHighlightedChr(
            "print 'Welcome to your own rock scissors paper!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')


    def test_17(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_18(self):
        self.assertHighlightedChrMultiLine(
            "print 'Im Hedy the fortune teller!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I can predict if youll win the lottery tomorrow!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "person is ask 'Who are you?'",
            "TTTTTT KK KKK SSSSSSSSSSSSSS",
            "if person is Hedy print 'You will definitely win!🤩' else print 'Bad luck! Someone else will win!😭'",
            "KK TTTTTT KK TTTT KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSS KKKK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')


    def test_19(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_20(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_21(self):
        self.assertHighlightedChrMultiLine(
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
            level="level5",lang='en')


    def test_22(self):
        self.assertHighlightedChrMultiLine(
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
            "KKKKK SSSSSSSSSSSSSSS TTTTT SSSSSSSSSSSSSSSSSSSS       SSSSSSSSS",
            "print 'The drinks are free in this level because Hedy cant calculate the price yet...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')


    def test_23(self):
        self.assertHighlightedChr(
            "print 'On to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSS",
            level="level5",lang='en')
