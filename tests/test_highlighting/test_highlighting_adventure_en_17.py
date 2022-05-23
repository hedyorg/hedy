from tests.Highlighter import HighlightTester

class HighlighterTestLeveL17(HighlightTester):

    def test_1(self):
        self.assert_highlighted_chr_multi_line(
            "for i in range 1 to 10:",
            "KKK T KK KKKKK N KK NNK",
            "print i",
            "KKKKK T",
            "print 'Ready or not, here I come!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level17", lang='en')


    def test_2(self):
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


    def test_3(self):
        self.assert_highlighted_chr(
            "print 'Lets go to the next level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level17", lang='en')