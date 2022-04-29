from tests.Highlighter import HighlightTester

class HighlighterTestLeveL15(HighlightTester):


    def test_1(self):
        self.assertHighlightedChrMultiLine(
            "answer = 0",
            "TTTTTT K N",
            "while answer != 25",
            "KKKKK TTTTTT KK NN",
            "answer = ask 'What is 5 times 5?'",
            "TTTTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "print 'A correct answer has been given'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level15",lang='en')


    def test_2(self):
        self.assertHighlightedChrMultiLine(
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
            level="level15",lang='en')


    def test_3(self):
        self.assertHighlightedChr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level15",lang='en')


    def test_4(self):
        self.assertHighlightedChrMultiLine(
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
            level="level15",lang='en')


    def test_5(self):
        self.assertHighlightedChrMultiLine(
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
            level="level15",lang='en')


    def test_6(self):
        self.assertHighlightedChrMultiLine(
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
            level="level15",lang='en')


    def test_7(self):
        self.assertHighlightedChrMultiLine(
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
            level="level15",lang='en')


    def test_8(self):
        self.assertHighlightedChrMultiLine(
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
            level="level15",lang='en')


    def test_9(self):
        self.assertHighlightedChr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level15",lang='en')