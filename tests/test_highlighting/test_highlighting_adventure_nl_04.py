from tests.Highlighter import HighlightTester

class HighlighterTestLeveL3nl(HighlightTester):


    def test_1(self):
        self.assertHighlightedChr(
            "print 'hallo wereld'",
            "KKKKK SSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_3(self):
        self.assertHighlightedChrMultiLine(
            "print 'Vanaf nu gebruiken we aanhalingstekens!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "antwoord is vraag 'Wat gebruiken we vanaf nu?'",
            "TTTTTTTT KK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print 'We gebruiken ' antwoord",
            "KKKKK SSSSSSSSSSSSSSS TTTTTTTT",
            level="level4",lang='nl')


    def test_4(self):
        self.assertHighlightedChrMultiLine(
            "naam is Hans",
            "TTTT KK TTTT",
            "print 'De naam van de hoofdpersoon is' naam",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS     ",
            "print naam 'gaat nu in het bos lopen'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print naam 'is wel een beetje bang'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSS",
            "dieren is 🦔, 🦉, 🐿, 🦇",
            "TTTTTT KK TK TK TK T",
            "print 'Hij hoort het geluid van een ' dieren op willekeurig",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS TTTTTT KK KKKKKKKKKKK",
            "print naam ' is bang dat dit een spookbos is'",
            "KKKKK TTTT SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_5(self):
        self.assertHighlightedChr(
            "print 'Hier komt straks jouw verhaal!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_6(self):
        self.assertHighlightedChrMultiLine(
            "print 'Figuren tekenen'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "hoek is 90",
            "TTTT KK TT",
            "draai hoek",
            "KKKKK TTTT",
            "vooruit 25",
            "KKKKKKK TT",
            "draai hoek",
            "KKKKK TTTT",
            "vooruit 25",
            "KKKKKKK TT",
            level="level4",lang='nl')


    def test_7(self):
        self.assertHighlightedChrMultiLine(
            "print 'Figuren tekenen'",
            "KKKKK SSSSSSSSSSSSSSSSS",
            "hoek is 90",
            "TTTT KK TT",
            "draai hoek",
            "KKKKK TTTT",
            "vooruit 25",
            "KKKKKKK TT",
            level="level4",lang='nl')


    def test_8(self):
        self.assertHighlightedChrMultiLine(
            "mensen is mama, papa, Emma, Sophie",
            "TTTTTT KK TTTTK TTTTK TTTTK TTTTTT",
            "print ' de afwas wordt gedaan door '",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "print mensen op _",
            "KKKKK TTTTTT KK I",
            level="level4",lang='nl')


    def test_9(self):
        self.assertHighlightedChr(
            "print 'Wie doet de afwas?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_10(self):
        self.assertHighlightedChrMultiLine(
            "keuzes is 1, 2, 3, 4, 5, regenworm",
            "TTTTTT KK TK TK TK TK TK TTTTTTTTT",
            "print ' jij gooide '",
            "KKKKK SSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_11(self):
        self.assertHighlightedChr(
            "print 'Wat zal de dobbelsteen deze keer aangeven?'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_12(self):
        self.assertHighlightedChrMultiLine(
            "keuzes is steen, papier, schaar",
            "TTTTTT KK TTTTTK TTTTTTK TTTTTT",
            "print ' De computer koos: ' _ op _",
            "KKKKK SSSSSSSSSSSSSSSSSSSSS I KK I",
            level="level4",lang='nl')


    def test_13(self):
        self.assertHighlightedChr(
            "print 'Welkom bij jouw eigen steen papier schaar!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_14(self):
        self.assertHighlightedChrMultiLine(
            "print 'Hoi ik ben Hedy de Waarzegger!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            "voorspelling is vraag 'Wat wil je weten?'",
            "TTTTTTTTTTTT KK KKKKK SSSSSSSSSSSSSSSSSSS",
            "print 'Dit is je vraag: ' voorspelling",
            "KKKKK SSSSSSSSSSSSSSSSSSS TTTTTTTTTTTT",
            "antwoorden is ja, nee, misschien",
            "TTTTTTTTTT KK TTK TTTK TTTTTTTTT",
            "print 'Mijn glazen bol zegt...'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSS",
            "slaap 2",
            "KKKKK T",
            "print antwoorden op willekeurig",
            "KKKKK TTTTTTTTTT KK KKKKKKKKKKK",
            level="level4",lang='nl')


    def test_15(self):
        self.assertHighlightedChr(
            "# Schrijf jouw code hier",
            "CCCCCCCCCCCCCCCCCCCCCCCC",
            level="level4",lang='nl')


    def test_16(self):
        self.assertHighlightedChrMultiLine(
            "print 'Welkom bij Restaurant Hedy'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_17(self):
        self.assertHighlightedChr(
            "print 'Ontsnap uit het spookhuis!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_18(self):
        self.assertHighlightedChrMultiLine(
            "print 'Ontsnap uit het spookhuis!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_19(self):
        self.assertHighlightedChrMultiLine(
            "wachtwoord is vraag 'Wat is het goede wachtwoord?'",
            "TTTTTTTTTT KK KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')


    def test_20(self):
        self.assertHighlightedChr(
            "print 'Op naar het volgende level!'",
            "KKKKK SSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            level="level4",lang='nl')
