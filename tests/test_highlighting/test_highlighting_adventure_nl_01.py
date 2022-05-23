from tests.Highlighter import HighlightTester

class HighlighterTestLeveL1nl(HighlightTester):
    def test_1(self):
        self.assert_highlighted_chr(
            "print hallo wereld!",
            "KKKKK TTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_2(self):
        self.assert_highlighted_chr_multi_line(
            "print Hallo!",
            "KKKKK TTTTTT",
            "print Welkom bij Hedy!",
            "KKKKK TTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_3(self):
        self.assert_highlighted_chr_multi_line(
            "vraag Hoe heet je?",
            "KKKKK TTTTTTTTTTTT",
            "echo hallo",
            "KKKK TTTTT",
            level="level1", lang='nl')


    def test_4(self):
        self.assert_highlighted_chr(
            "vraag wie is de hoofdpersoon van jouw verhaal",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_5(self):
        self.assert_highlighted_chr_multi_line(
            "vraag De hoofdpersoon van dit verhaal is",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print De hoofdpersoon gaat nu in het bos lopen",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo Hij is wel een beetje bang, die",
            "KKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Overal hoort hij gekke geluiden",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Hij is bang dat dit een spookbos is",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_6(self):
        self.assert_highlighted_chr(
            "print Hier begint jouw verhaal",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_7(self):
        self.assert_highlighted_chr_multi_line(
            "print Ik ben papegaai Hedy",
            "KKKKK TTTTTTTTTTTTTTTTTTTT",
            "vraag Wie ben jij?",
            "KKKKK TTTTTTTTTTTT",
            "echo",
            "KKKK",
            "echo",
            "KKKK",
            level="level1", lang='nl')


    def test_8(self):
        self.assert_highlighted_chr(
            "print Ik ben Hedy de papegaai!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_9(self):
        self.assert_highlighted_chr_multi_line(
            "draai rechts",
            "KKKKK KKKKKK",
            "vooruit 50",
            "KKKKKKK   ",
            "draai links",
            "KKKKK KKKKK",
            "vooruit 50",
            "KKKKKKK   ",
            level="level1", lang='nl')


    def test_10(self):
        self.assert_highlighted_chr_multi_line(
            "vooruit 50",
            "KKKKKKK   ",
            "draai rechts",
            "KKKKK KKKKKK",
            level="level1", lang='nl')


    def test_11(self):
        self.assert_highlighted_chr_multi_line(
            "print wat kies jij?",
            "KKKKK TTTTTTTTTTTTT",
            "vraag kies uit steen, papier of schaar",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo dus jouw keuze was:",
            "KKKK TTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_12(self):
        self.assert_highlighted_chr(
            "print Welkom bij jouw eigen steen papier schaar!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_13(self):
        self.assert_highlighted_chr_multi_line(
            "print Hoi, ik ben Hedy de waarzegger!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "vraag Wie ben jij?",
            "KKKKK TTTTTTTTTTTT",
            "print Ik voorspel... Ik voorspel...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "echo Jouw naam is",
            "KKKK TTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_14(self):
        self.assert_highlighted_chr(
            "# Maak jouw eigen code hier",
            "CCCCCCCCCCCCCCCCCCCCCCCCCCC",
            level="level1", lang='nl')


    def test_15(self):
        self.assert_highlighted_chr_multi_line(
            "print Welkom bij McHedy! 🍟",
            "KKKKK TTTTTTTTTTTTTTTTTTTT",
            "vraag Wat wilt u bestellen?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTT",
            "echo Dus u wilt graag",
            "KKKK TTTTTTTTTTTTTTTT",
            "print Bedankt voor uw bestelling!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Het komt eraan!",
            "KKKKK TTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_16(self):
        self.assert_highlighted_chr(
            "print Welkom bij McHedy!",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_17(self):
        self.assert_highlighted_chr_multi_line(
            "print Hoe ben ik hier terechtgekomen?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Ik herinner me dat ik mijn vrienden vertelde over die verlaten villa..",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print en toen werd ineens alles zwart.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Maar waarom lig ik hier nu op de grond...?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print ik heb knallende hoofdpijn, alsof ik een harde klap heb gehad.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Huh? Wat is dat geluid?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTT",
            "print Oh nee! Volgens mij ben ik niet alleen in dit huis!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Ik moet maken dat ik wegkom!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Er staan drie deuren voor me, maar welke moet ik kiezen?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "vraag Welke deur kies ik?",
            "KKKKK TTTTTTTTTTTTTTTTTTT",
            "echo Ik kies deur",
            "KKKK TTTTTTTTTTTT",
            "print ...?",
            "KKKKK TTTT",
            level="level1", lang='nl')


    def test_18(self):
        self.assert_highlighted_chr(
            "print Hoe ben ik hier terechtgekomen?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_19(self):
        self.assert_highlighted_chr(
            "print Op naar het volgende level!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')


    def test_20(self):
        self.assert_highlighted_chr_multi_line(
            "print Welkom bij restaurant Hedy",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "vraag Wat wilt u eten?",
            "KKKKK TTTTTTTTTTTTTTTT",
            "echo Dus dit wilt u eten",
            "KKKK TTTTTTTTTTTTTTTTTTT",
            "vraag Wat wilt u drinken",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "echo Dus dit wilt u drinken",
            "KKKK TTTTTTTTTTTTTTTTTTTTTT",
            level="level1", lang='nl')
