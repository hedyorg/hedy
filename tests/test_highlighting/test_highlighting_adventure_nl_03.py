from tests.Highlighter import HighlightTester

class HighlighterTestLeveL3nl(HighlightTester):


    def test_2(self):
        self.assertHighlightedChrMultiLine(
            "dieren is hond, kat, kangoeroe",
            "TTTTTT KK TTTT  TTT  TTTTTTTTT",
            "print dieren op willekeurig",
            "KKKKK TTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_3(self):
        self.assertHighlightedChrMultiLine(
            "taarten is aardbei, chocolade",
            "TTTTTTT KK TTTTTTT  TTTTTTTTT",
            "voeg appel toe aan taarten",
            "KKKK TTTTT KKK KKK TTTTTTT",
            "verwijder chocolade uit taarten",
            "KKKKKKKKK TTTTTTTTT KKK TTTTTTT",
            "print taarten op willekeurig",
            "KKKKK TTTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_4(self):
        self.assertHighlightedChr(
            "print hallo wereld!",
            "KKKKK TTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_5(self):
        self.assertHighlightedChr(
            "print Hier komt straks jouw verhaal!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_6(self):
        self.assertHighlightedChrMultiLine(
            "dieren is 🦇, 🐿, 🦉, 🦔",
            "TTTTTT KK T  T  T  T",
            "print Hij hoort nu het geluid van een dieren op willekeurig",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_7(self):
        self.assertHighlightedChrMultiLine(
            "print Hij hoort een geluid...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTT",
            "dieren is 🐿, 🦔, 🦇, 🦉",
            "TTTTTT KK T  T  T  T",
            "dier is vraag Wat denk jij dat het is?",
            "TTTT KK KKKKK TTTTTTTTTTTTTTTTTTTTTTTT",
            "voeg dier toe aan dieren",
            "KKKK TTTT KKK KKK TTTTTT",
            "print het was een dieren op willekeurig",
            "KKKKK TTTTTTTTTTT TTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_8(self):
        self.assertHighlightedChrMultiLine(
            "print Zijn rugzak is veel te zwaar...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print In de rugzak zitten een fles water, een zaklamp en een baksteen.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "tas is water, zaklamp, baksteen",
            "TTT KK TTTTT  TTTTTTT  TTTTTTTT",
            "weggooien is vraag Welk ding zal onze held weggooien?",
            "TTTTTTTTT KK KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "verwijder weggooien uit tas",
            "KKKKKKKKK TTTTTTTTT KKK TTT",
            level="level3",lang='nl')


    def test_9(self):
        self.assertHighlightedChrMultiLine(
            "woorden is lorre, Hedy",
            "TTTTTTT KK TTTTT  TTTT",
            "print Train je papegaai!",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "nieuw_woord is vraag Welk woord moet je papegaai leren?",
            "TTTTTTTTTTT KK KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "voeg nieuw_woord toe aan woorden",
            "KKKK TTTTTTTTTTT KKK KKK TTTTTTT",
            "print 🧒: Zeg nieuw_woord , Hedy!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print 🦜: woorden op willekeurig",
            "KKKKK TTTTTTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_10(self):
        self.assertHighlightedChr(
            "# Schrijf jouw code hier",
            "CCCCCCCCCCCCCCCCCCCCCCCC",
            level="level3",lang='nl')


    def test_11(self):
        self.assertHighlightedChrMultiLine(
            "hoeken is 10, 50, 90, 150, 250",
            "TTTTTT KK TT  TT  TT  TTT  TTT",
            "draai hoeken op willekeurig",
            "KKKKK TTTTTT KK KKKKKKKKKKK",
            "vooruit 25",
            "KKKKKKK TT",
            level="level3",lang='nl')


    def test_12(self):
        self.assertHighlightedChrMultiLine(
            "print Schildpaddenrace!",
            "KKKKK TTTTTTTTTTTTTTTTT",
            "hoek is 90",
            "TTTT KK TT",
            "draai hoek",
            "KKKKK TTTT",
            "vooruit 25",
            "KKKKKKK TT",
            level="level3",lang='nl')


    def test_13(self):
        self.assertHighlightedChrMultiLine(
            "mensen is mama, papa, Emma, Sophie",
            "TTTTTT KK TTTT  TTTT  TTTT  TTTTTT",
            "print mensen op willekeurig",
            "KKKKK TTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_14(self):
        self.assertHighlightedChrMultiLine(
            "mensen is mama, papa, Emma, Sophie",
            "TTTTTT KK TTTT  TTTT  TTTT  TTTTTT",
            "jouw_naam is vraag Wie ben jij?",
            "TTTTTTTTT KK KKKKK TTTTTTTTTTTT",
            "verwijder jouw_naam uit mensen",
            "KKKKKKKKK TTTTTTTTT KKK TTTTTT",
            "print mensen op willekeurig doet de afwas vanavond!",
            "KKKKK TTTTTT KK KKKKKKKKKKK TTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_15(self):
        self.assertHighlightedChr(
            "print Wie doet de afwas?",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_16(self):
        self.assertHighlightedChrMultiLine(
            "keuzes is 1, 2, 3, 4, 5, regenworm",
            "TTTTTT KK T  T  T  T  T  TTTTTTTTT",
            "print keuzes op willekeurig",
            "KKKKK TTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_17(self):
        self.assertHighlightedChr(
            "print Wat zal de dobbelsteen deze keer aangeven?",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_18(self):
        self.assertHighlightedChrMultiLine(
            "keuzes is steen, papier, schaar",
            "TTTTTT KK TTTTT  TTTTTT  TTTTTT",
            "print keuzes op willekeurig",
            "KKKKK TTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_19(self):
        self.assertHighlightedChr(
            "print Welkom bij jouw eigen steen papier schaar!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_20(self):
        self.assertHighlightedChrMultiLine(
            "print Hoi Ik ben Hedy de Waarzegger",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "vraag is vraag Wat wil je weten?",
            "TTTTT KK KKKKK TTTTTTTTTTTTTTTTT",
            "print vraag",
            "KKKKK TTTTT",
            "antwoorden is ja, nee, misschien",
            "TTTTTTTTTT KK TT  TTT  TTTTTTTTT",
            "print Mijn glazen bol zegt...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTT",
            "slaap 2",
            "KKKKK T",
            "print antwoorden op willekeurig",
            "KKKKK TTTTTTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_21(self):
        self.assertHighlightedChrMultiLine(
            "gerechten is patat, pizza, spruitjes",
            "TTTTTTTTT KK TTTTT  TTTTT  TTTTTTTTT",
            "toetjes is een ijsje, appeltaart, franse stinkkaas",
            "TTTTTTT KK TTTTTTTTT  TTTTTTTTTT  TTTTTTTTTTTTTTTT",
            "drinken is cola, water, bier",
            "TTTTTTT KK TTTT  TTTTT  TTTT",
            "prijzen is 1 euro, 10 euro, 100 euro",
            "TTTTTTT KK TTTTTT  TTTTTTT  TTTTTTTT",
            "print Welkom bij het willekeurig restaurant",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Vandaag eet u gerechten op willekeurig",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTT KK KKKKKKKKKKK",
            "print Daarbij drinkt u drinken op willekeurig",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTT KK KKKKKKKKKKK",
            "print En u krijgt toetjes op willekeurig achteraf",
            "KKKKK TTTTTTTTTTTTTTTTTTT KK KKKKKKKKKKK TTTTTTTT",
            "print Dat wordt dan prijzen op willekeurig",
            "KKKKK TTTTTTTTTTTTTTTTTTTTT KK KKKKKKKKKKK",
            "print Eet smakelijk!",
            "KKKKK TTTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_22(self):
        self.assertHighlightedChrMultiLine(
            "print Mysterie Milkshake",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "smaken is aardbei, banaan, chocolade",
            "TTTTTT KK TTTTTTT  TTTTTT  TTTTTTTTT",
            "allergie is vraag Ben je allergisch voor een smaak?",
            "TTTTTTTT KK KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "verwijder allergie uit smaken",
            "KKKKKKKKK TTTTTTTT KKK TTTTTT",
            "print Jij krijgt een milkshake  smaken op willekeurig",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_23(self):
        self.assertHighlightedChrMultiLine(
            "print Ontsnap uit het spookhuis!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Voor je staan drie deuren...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "keuze is vraag Welke deur kies je?",
            "TTTTT KK KKKKK TTTTTTTTTTTTTTTTTTT",
            "print Je koos deur keuze",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "monsters is een zombie, een vampier, NIKS JE ONTSNAPT",
            "TTTTTTTT KK TTTTTTTTTT  TTTTTTTTTTT  TTTTTTTTTTTTTTTT",
            "print Jij ziet...",
            "KKKKK TTTTTTTTTTT",
            "slaap",
            "KKKKK",
            "print monsters op willekeurig",
            "KKKKK TTTTTTTT KK KKKKKKKKKKK",
            level="level3",lang='nl')


    def test_24(self):
        self.assertHighlightedChr(
            "print Ontsnap uit het spookhuis!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_25(self):
        self.assertHighlightedChrMultiLine(
            "naam is Sophie",
            "TTTT KK TTTTTT",
            "print Mijn naam is naam",
            "KKKKK TTTTTTTTTTTTTTTTT",
            level="level3",lang='nl')


    def test_26(self):
        self.assertHighlightedChr(
            "print Op naar het volgende level!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level3",lang='nl')