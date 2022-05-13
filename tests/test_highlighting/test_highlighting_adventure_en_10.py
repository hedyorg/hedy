from tests.Highlighter import HighlightTester

class HighlighterTestLeveL10(HighlightTester):


    def test_1(self):
        self.assert_highlighted_chr_multi_line(
            "animals is dog, cat, blobfish",
            "TTTTTTT KK TTTK TTTK TTTTTTTT",
            "for animal in animals",
            "KKK TTTTTT KK TTTTTTT",
            "print 'I love ' animal",
            "KKKKK SSSSSSSSS TTTTTT",
            level="level10",lang='en')


    def test_2(self):
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
            level="level10",lang='en')


    def test_3(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level10",lang='en')


    def test_4(self):
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
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS       ",
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
            level="level10",lang='en')


    def test_5(self):
        self.assert_highlighted_chr_multi_line(
            "days = Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday",
            "TTTT K TTTTTTK TTTTTTTK TTTTTTTTTK TTTTTTTTK TTTTTTK TTTTTTTTK TTTTTT",
            "names = mom, dad, Emma, Sophie",
            "TTTTT K TTTK TTTK TTTTK TTTTTT",
            "for day in days",
            "KKK TTT KK TTTT",
            "print names at random ' does the dishes on ' day",
            "KKKKK TTTTT KK KKKKKK SSSSSSSSSSSSSSSSSSSSSS TTT",
            level="level10",lang='en')


    def test_6(self):
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
            level="level10",lang='en')


    def test_7(self):
        self.assert_highlighted_chr_multi_line(
            "choices = rock, paper, scissors",
            "TTTTTTT K TTTTK TTTTTK TTTTTTTT",
            "players = Marleen, Michael",
            "TTTTTTT K TTTTTTTK TTTTTTT",
            "for player in players",
            "KKK TTTTTT KK TTTTTTT",
            "print player ' chooses ' choices at random",
            "KKKKK TTTTTT SSSSSSSSSSS TTTTTTT KK KKKKKK",
            level="level10",lang='en')


    def test_8(self):
        self.assert_highlighted_chr_multi_line(
            "numbers = 1, 2, 3",
            "TTTTTTT K NK NK N",
            "for number1 in numbers",
            "KKK TTTTTTT KK TTTTTTT",
            "for number2 in numbers",
            "KK  TTTTTTT KK TTTTTTT",
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
            level="level10",lang='en')


    def test_9(self):
        self.assert_highlighted_chr_multi_line(
            "courses = appetizer, main course, dessert",
            "TTTTTTT K TTTTTTTTTK TTTTTTTTTTTK TTTTTTT",
            "for course in courses",
            "KKK TTTTTT KK TTTTTTT",
            "food = ask 'What would you like to eat as your ' course '?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTT SSS",
            "print food ' will be your ' course",
            "KKKKK TTTT SSSSSSSSSSSSSSSS TTTTTT",
            level="level10",lang='en')


    def test_10(self):
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
            level="level10",lang='en')


    def test_11(self):
        self.assert_highlighted_chr(
            "courses = appetizer, main course, dessert",
            "TTTTTTT K TTTTTTTTTK TTTTTTTTTTTK TTTTTTT",
            level="level10",lang='en')


    def test_12(self):
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
            level="level10",lang='en')


    def test_13(self):
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
            level="level10",lang='en')


    def test_14(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level10",lang='en')