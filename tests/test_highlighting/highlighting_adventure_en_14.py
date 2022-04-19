from tests.Highlighter import HighlightTester

class HighlighterTestLeveL14(HighlightTester):


    def test_1(self):
        self.assertHighlightedMultiLine(
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
            level="level14",lang='en')


    def test_2(self):
        self.assertHighlightedMultiLine(
            "age = ask 'How old are you?'",
            "TTT K KKK SSSSSSSSSSSSSSSSSS",
            "if age > 12",
            "KK TTT K NN",
            "print 'You are older than I am!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level14",lang='en')


    def test_3(self):
        self.assertHighlightedMultiLine(
            "name = ask 'What is your name?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "if name == 'Hedy'",
            "KK TTTT KK SSSSSS",
            "print 'You are coo!'",
            "KKKKK SSSSSSSSSSSSSS",
            level="level14",lang='en')


    def test_4(self):
        self.assertHighlightedMultiLine(
            "name = ask 'What is your name?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "if name != 'Hedy'",
            "KK TTTT KK SSSSSS",
            "print 'You are not Hedy'",
            "KKKKK SSSSSSSSSSSSSSSSSS",
            level="level14",lang='en')


    def test_5(self):
        self.assertHighlightedMultiLine(
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
            level="level14",lang='en')


    def test_6(self):
        self.assertHighlighted(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level14",lang='en')


    def test_7(self):
        self.assertHighlightedMultiLine(
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
            level="level14",lang='en')


    def test_8(self):
        self.assertHighlightedMultiLine(
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
            level="level14",lang='en')


    def test_9(self):
        self.assertHighlightedMultiLine(
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
            level="level14",lang='en')


    def test_10(self):
        self.assertHighlightedMultiLine(
            "game is 'on'",
            "TTTT KK SSSS",
            "for i in range 1 to 100",
            "KKK T KKKKKKKK N KK NNN",
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
            level="level14",lang='en')


    def test_11(self):
        self.assertHighlighted(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level14",lang='en')
