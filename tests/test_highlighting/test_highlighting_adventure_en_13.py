from tests.Highlighter import HighlightTester

class HighlighterTestLeveL13(HighlightTester):


    def test_1(self):
        self.assertHighlightedChrMultiLine(
            "name = ask 'what is your name?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "age = ask 'what is your age?'",
            "TTT K KKK SSSSSSSSSSSSSSSSSSS",
            "if name is 'Hedy' and age is 2",
            "KK TTTT KK SSSSSS KKK TTT KK N",
            "print 'You are the real Hedy!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            level="level13",lang='en')


    def test_2(self):
        self.assertHighlightedChrMultiLine(
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
            level="level13",lang='en')


    def test_3(self):
        self.assertHighlightedChr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level13",lang='en')


    def test_4(self):
        self.assertHighlightedChrMultiLine(
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
            level="level13",lang='en')


    def test_5(self):
        self.assertHighlightedChrMultiLine(
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
            level="level13",lang='en')


    def test_6(self):
        self.assertHighlightedChrMultiLine(
            "drinks = ask 'What would you like to drink?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "if drinks is 'water' or drinks is 'juice'",
            "KK TTTTTT KK SSSSSSS KK TTTTTT KK SSSSSSS",
            "print 'Thats a healthy choice'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSS",
            level="level13",lang='en')


    def test_7(self):
        self.assertHighlightedChrMultiLine(
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
            level="level13",lang='en')


    def test_8(self):
        self.assertHighlightedChr(
            "## place your code here",
            "CCCCCCCCCCCCCCCCCCCCCCC",
            level="level13",lang='en')


    def test_9(self):
        self.assertHighlightedChrMultiLine(
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
            level="level13",lang='en')


    def test_10(self):
        self.assertHighlightedChr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level13",lang='en')