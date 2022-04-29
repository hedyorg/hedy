from tests.Highlighter import HighlightTester

class HighlighterTestLeveL11(HighlightTester):

    
    def test_1(self):
        self.assertHighlightedChrMultiLine(
            "for counter in range 1 to 5",
            "KKK TTTTTTT KK KKKKK N KK N",
            "print counter",
            "KKKKK TTTTTTT",
            level="level11",lang='en')


    def test_2(self):
        self.assertHighlightedChrMultiLine(
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
            level="level11",lang='en')


    def test_3(self):
        self.assertHighlightedChr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level11",lang='en')


    def test_4(self):
        self.assertHighlightedChrMultiLine(
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
            level="level11",lang='en')


    def test_5(self):
        self.assertHighlightedChrMultiLine(
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
            level="level11",lang='en')


    def test_6(self):
        self.assertHighlightedChr(
            "print 'Escape from the haunted house!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level11",lang='en')


    def test_7(self):
        self.assertHighlightedChrMultiLine(
            "name = ask 'Who is your favorite cartoon character?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'I love watching ' name",
            "KKKKK SSSSSSSSSSSSSSSSSS TTTT",
            "show = SpongeBob SquarePants",
            "TTTT K TTTTTTTTTTTTTTTTTTTTT",
            "print show 'is my favorite show!'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSS",
            level="level11",lang='en')


    def test_8(self):
        self.assertHighlightedChr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level11",lang='en')