In level 4 blijven de regels hetzelfde voor ask en print. Je moet dus nog steeds aanhalingstekens gebruiken als je iets wilt printen.
Er komt nu wel een nieuwe code bij, de if. If is Engels voor als.

Hier vind je weer een aantal opdrachten om mee aan de slag te gaan.

# Niet voor je kleine zusje of broertje!
Toen ik zelf leerde programmeren, was het eerste programma dat ik maakte een programma om te kijken of mijn zusje niet stiekem op de computer zat.
Dat kun jij nu ook maken, het gaat zo:

* `naam is ask Hoe heet jij?`
* `if naam is Felienne print 'ok jij mag computeren' else print 'verboden toegang voor jou'`

Deze code bekijkt of de naam die wordt ingetypt precies "Felienne" is. Is dat zo, dan print Hedy de eerste code, anders de tweede.
Let op! Hedy kijkt letterlijk naar de naam, dus het moet precies kloppen, ook met hoofdletter.

# Steen, schaar, papier
In Level 4 kunnen we ook weer steen schaar papier programmeren, maar nu kun je ook echt tegen de computer spelen, en bekijken wie de winnaar is.
Hier is het begin van het programma, maak jij de regels zelf af?

* `jouwkeuze is ask wat kies jij?`
* `keuzes is steen, schaar, papier`
* `computerkeuze is keuzes at random`
* `if computerkeuze is schaar and jouwkeuze is papier print 'de computer wint'`
* `if computerkeuze is schaar and jouwkeuze is steen print 'jij wint'`

Herinnering: random (je zegt ren-dom) is het Engelse woord voor willekeurig; and is het Engelse woord voor en.

# Maak dobbelsteen na
Je kunt ook in Level 4 weer een dobbelsteen maken en daarbij een if gebruiken. Bijv zo:

* `keuzes is 1, 2, 3, 4, 5, regenworm`
* `worp is keuzes at random`
* `print 'je hebt ' worp ' gegooid'`
* `if worp is regenworm print 'Je mag stoppen met gooien.' else print 'Je moet nog een keer hoor!`

Maar misschien wil jij wel een dobbelsteen uit een heel ander spel namaken.

# Wie doet de afwas?
Ook je afwasprogramma kun je nu leuker maken met een if. Bijvoorbeeld zo:

Dat doe je zo:

* `mensen is mama, papa, Emma, Sophie`
* `afwasser is mensen at random`
* `if afwasser is Sophie print 'chips ik moet de afwas doen' else print 'gelukkig geen afwas want ' afwasser ' doet het'`

# Een beter verhaal
Wat je ook kunt doet is je verhaal weer leuker maken, want nu kun je verschillende eindes programmeren.

###Voorbeeld
Maak een verhaal met twee eindes, bijvoorbeeld zo:

* De prinses loopt door het bos
* Ze komt een monster tegen

Goed einde:

* Ze pakt haar zwaard en het monster rent snel weg

Slecht einde

* Het monster eet de prinses op

### Opdracht

Nu jij! 

1. Schrijf een verhaal met twee eindes

### Voorbeeld Hedy code
* `print 'De prinses loopt door het bos'`
* `print 'Ze komt een monster tegen'`
* `einde is ask Wil je een goed of slecht einde?`
* `if einde is goed print 'Ze pakt haar zwaard en het monster rent snel weg' else print 'Het monster eet de prinses op'`

### Een interactief verhaal
Je kunt ook zorgen dat er weer een naam ingevoerd kan worden. Dat werkt net zoals in level 3. Dat kun je dus combineren met een if, en dan heb je al een heel programma gemaakt!

### Herhaling in je verhaal of spel
Helaas kun je nu steeds maar 1 dobbelsteen gooien, of 1 keer bepalen wie de afwas doet. Regenwormen moet eigenlijk met 8 dobbelstenen, en misschien wil jij wel een afwasrooster maken voor de hele week! Soms is het handig als je codes een paar keer kan herhalen.
Dat kan je leren in Level 5.
