from tests.Highlighter import HighlightTester

class HighlighterTestLeveL16(HighlightTester):


    def test_1(self):
        self.assert_highlighted_chr_multi_line(
            "fruit = ['apple', 'banana', 'cherry']",
            "TTTTT K KSSSSSSSK SSSSSSSSK SSSSSSSSK",
            "print fruit",
            "KKKKK TTTTT",
            level="level16",lang='en')


    def test_2(self):
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
            level="level16",lang='en')


    def test_3(self):
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
            level="level16",lang='en')


    def test_4(self):
        self.assert_highlighted_chr(
            "# place your code here",
            "CCCCCCCCCCCCCCCCCCCCCC",
            level="level16",lang='en')


    def test_5(self):
        self.assert_highlighted_chr_multi_line(
            "numbers = [1, 2, 3]",
            "TTTTTTT K KNK NK NK",
            "i = numbers[random]",
            "T K TTTTTTTK      K",
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
            level="level16",lang='en')


    def test_6(self):
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
            level="level16",lang='en')


    def test_7(self):
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
            level="level16",lang='en')


    def test_8(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level16",lang='en')