from tests.Highlighter import HighlightTester

class HighlighterTestLeveL2nl(HighlightTester):



    def test_2(self):
        self.assertHighlightedChrMultiLine(
            "naam is Hedy",
            "TTTT KK TTTT",
            "leeftijd is 15",
            "TTTTTTTT KK TT",
            "print naam is leeftijd jaar oud",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_3(self):
        self.assertHighlightedChrMultiLine(
            "antwoord is vraag Hoe heet jij?",
            "TTTTTTTT KK KKKKK TTTTTTTTTTTTT",
            "print Hoi antwoord",
            "KKKKK TTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_4(self):
        self.assertHighlightedChrMultiLine(
            "print Mijn favoriete kleur is...",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "slaap 2",
            "KKKKK T",
            "print groen!",
            "KKKKK TTTTTT",
            level="level2",lang='nl')


    def test_5(self):
        self.assertHighlightedChr(
            "print hallo wereld!",
            "KKKKK TTTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_6(self):
        self.assertHighlightedChrMultiLine(
            "naam is vraag Hoe heet de hoofdpersoon?",
            "TTTT KK KKKKK TTTTTTTTTTTTTTTTTTTTTTTTT",
            "print naam gaat nu in het bos lopen",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print naam is wel een beetje bang",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print ineens hoort hij een vreemd geluid",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "slaap 2",
            "KKKKK T",
            "print naam is bang dat dit een spookbos is",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_7(self):
        self.assertHighlightedChr(
            "print Hier komt straks jouw verhaal!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_8(self):
        self.assertHighlightedChrMultiLine(
            "print Ik ben papegaai Hedy",
            "KKKKK TTTTTTTTTTTTTTTTTTTT",
            "naam is vraag Wie ben jij?",
            "TTTT KK KKKKK TTTTTTTTTTTT",
            "print naam",
            "KKKKK TTTT",
            "slaap",
            "KKKKK",
            "print koppie krauw",
            "KKKKK TTTTTTTTTTTT",
            "slaap",
            "KKKKK",
            "print naam",
            "KKKKK TTTT",
            level="level2",lang='nl')


    def test_9(self):
        self.assertHighlightedChr(
            "print Ik ben Hedy de papegaai!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_10(self):
        self.assertHighlightedChrMultiLine(
            "print Figuren tekenen",
            "KKKKK TTTTTTTTTTTTTTT",
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
            level="level2",lang='nl')


    def test_11(self):
        self.assertHighlightedChrMultiLine(
            "print Schildpaddenrace!",
            "KKKKK TTTTTTTTTTTTTTTTT",
            "hoek is 90",
            "TTTT KK TT",
            "draai hoek",
            "KKKKK TTTT",
            "vooruit 25",
            "KKKKKKK TT",
            level="level2",lang='nl')


    def test_12(self):
        self.assertHighlightedChrMultiLine(
            "keuze is _",
            "TTTTT KK  ",
            "print ik kies keuze",
            "KKKKK TTTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_13(self):
        self.assertHighlightedChr(
            "# Schrijf jouw code hier",
            "CCCCCCCCCCCCCCCCCCCCCCCC",
            level="level2",lang='nl')


    def test_14(self):
        self.assertHighlightedChrMultiLine(
            "print Welkom bij McHedy!",
            "KKKKK TTTTTTTTTTTTTTTTTT",
            "eten is vraag Wat wilt u eten?",
            "TTTT KK KKKKK TTTTTTTTTTTTTTTT",
            "saus is vraag Welke saus wilt u daarbij?",
            "TTTT KK KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTT",
            "drinken is vraag Wat wilt u drinken?",
            "TTTTTTT KK KKKKK TTTTTTTTTTTTTTTTTTT",
            "print U heeft eten met saus en drinken besteld.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Bedankt voor uw bestelling!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_15(self):
        self.assertHighlightedChrMultiLine(
            "monster1 is 👻",
            "TTTTTTTT KK T",
            "monster2 is 🤡",
            "TTTTTTTT KK T",
            "monster3 is 👶",
            "TTTTTTTT KK T",
            "print Je stapt het oude verlaten spookhuis binnen",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Meteen hoor je het geluid van een monster1",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Dus snel ren je naar de volgende kamer.",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print Maar daar wordt je opgewacht door een monster2",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "print HELP!",
            "KKKKK TTTTT",
            "print Je rent naar de keuken, maar wordt daar aangevallen door een monster3",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2",lang='nl')


    def test_16(self):
        self.assertHighlightedChr(
            "monster1 is _",
            "TTTTTTTT KK  ",
            level="level2",lang='nl')


    def test_17(self):
        self.assertHighlightedChr(
            "print Op naar het volgende level!",
            "KKKKK TTTTTTTTTTTTTTTTTTTTTTTTTTT",
            level="level2",lang='nl')
