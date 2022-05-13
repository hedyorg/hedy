from tests.Highlighter import HighlightTester

class HighlighterTestLeveL12(HighlightTester):

    
    def test_1(self):
        self.assert_highlighted_chr_multi_line(
            "print 'decimal numbers now need to use a dot'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 2.5 + 2.5",
            "KKKKK NNN K NNN",
            level="level12",lang='en')


    def test_2(self):
        self.assert_highlighted_chr_multi_line(
            "print 'Two and a half plus two and a half is...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 2.5 + 2.5",
            "KKKKK NNN K NNN",
            level="level12",lang='en')


    def test_3(self):
        self.assert_highlighted_chr_multi_line(
            "name = 'Hedy the Robot'",
            "TTTT K SSSSSSSSSSSSSSSS",
            "print 'Hello ' name",
            "KKKKK SSSSSSSS TTTT",
            level="level12",lang='en')


    def test_4(self):
        self.assert_highlighted_chr_multi_line(
            "superheroes = 'Spiderman', 'Batman', 'Iron Man'",
            "TTTTTTTTTTT K SSSSSSSSSSSK SSSSSSSSK SSSSSSSSSS",
            "print superheroes at random",
            "KKKKK TTTTTTTTTTT KK KKKKKK",
            level="level12",lang='en')


    def test_5(self):
        self.assert_highlighted_chr_multi_line(
            "name = ask 'What is your name?'",
            "TTTT K KKK SSSSSSSSSSSSSSSSSSSS",
            "if name = 'Hedy the Robot'",
            "KK TTTT K SSSSSSSSSSSSSSSS",
            "print 'Hi there!'",
            "KKKKK SSSSSSSSSSS",
            level="level12",lang='en')


    def test_6(self):
        self.assert_highlighted_chr_multi_line(
            "score = 25",
            "TTTTT K NN",
            "print 'You got ' score",
            "KKKKK SSSSSSSSSS TTTTT",
            level="level12",lang='en')


    def test_7(self):
        self.assert_highlighted_chr_multi_line(
            "a = 'Hello '",
            "T K SSSSSSSS",
            "b = 'world!'",
            "T K SSSSSSSS",
            "print a + b",
            "KKKKK T K T",
            level="level12",lang='en')


    def test_8(self):
        self.assert_highlighted_chr_multi_line(
            "name = 'The Queen of England'",
            "TTTT K SSSSSSSSSSSSSSSSSSSSSS",
            "print name ' was eating a piece of cake, when suddenly...'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level12",lang='en')


    def test_9(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level12",lang='en')


    def test_10(self):
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
            level="level12",lang='en')


    def test_11(self):
        self.assert_highlighted_chr_multi_line(
            "number1 = ask 'What is the first number?'",
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "number2 = ask 'What is the second number?'",
            "TTTTTTT K KKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "answer = number1 + number2",
            "TTTTTT K TTTTTTT K TTTTTTT",
            "print number1 ' plus ' number2 ' is ' answer",
            "KKKKK TTTTTTT SSSSSSSS TTTTTTT SSSSSS TTTTTT",
            level="level12",lang='en')


    def test_12(self):
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
            level="level12",lang='en')


    def test_13(self):
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
            level="level12",lang='en')


    def test_14(self):
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
            level="level12",lang='en')


    def test_15(self):
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
            level="level12",lang='en')


    def test_16(self):
        self.assert_highlighted_chr(
            "## place your code here",
            "CCCCCCCCCCCCCCCCCCCCCCC",
            level="level12",lang='en')


    def test_17(self):
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
            level="level12",lang='en')


    def test_18(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level12",lang='en')