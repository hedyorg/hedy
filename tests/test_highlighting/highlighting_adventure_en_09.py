from tests.Highlighter import HighlightTester

class HighlighterTestLeveL9(HighlightTester):


    def test_1(self):
        self.assertHighlightedMultiLine(
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
            level="level9",lang='en')


    def test_2(self):
        self.assertHighlightedMultiLine(
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
            level="level9",lang='en')


    def test_3(self):
        self.assertHighlightedMultiLine(
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
            level="level9",lang='en')


    def test_4(self):
        self.assertHighlighted(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level9",lang='en')


    def test_5(self):
        self.assertHighlightedMultiLine(
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
            level="level9",lang='en')


    def test_6(self):
        self.assertHighlightedMultiLine(
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
            level="level9",lang='en')


    def test_7(self):
        self.assertHighlighted(
            "print 'Welcome to this calculator!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level9",lang='en')


    def test_8(self):
        self.assertHighlightedMultiLine(
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
            level="level9",lang='en')


    def test_9(self):
        self.assertHighlightedMultiLine(
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
            level="level9",lang='en')


    def test_10(self):
        self.assertHighlighted(
            "print 'Escape from the haunted house!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level9",lang='en')


    def test_11(self):
        self.assertHighlightedMultiLine(
            "repeat 2 times",
            "KKKKKK N KKKKK",
            "print 'if youre happy and you know it clap your hands'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'if youre happy and you know it and you really want to show it'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'if youre happy and you know it clap your hands'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level9",lang='en')


    def test_12(self):
        self.assertHighlighted(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level9",lang='en')