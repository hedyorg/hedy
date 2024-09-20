# Hedy - Les 4a

[Teacher] In level 4 leren leerlingen aanhalingstekens gebruiken in code. Dat is niet altijd de meest leuke les maar goed oefenen is wel nodig om latere frustratie te voorkomen.
Om het leuker te maken kan je in deze les andere features aanbieden, zoals `clear` of een muziekopdracht.[/Teacher]

## Aanhalingstekens

Aan het einde van de les:

* snap jij waarom aanhalingstekens nodig zijn in programmeren.
* kan jij aanhalingstekens op de goede plek in code zetten.
* kan jij foutmeldingen over aanhalingstekens goed lezen.

### Aanhalingstekens

We hebben geleerd om aanhalingstekens te gebruiken, als iets letterlijk zo in beeld moet komen.
We gebruiken aanhalingstekens bij `print` en bij `ask`.

```hedy
vriend is ask 'Hoe heet jij?'
print 'Leuk! Ik ga naar de stad met ' vriend
```

#### Opdracht 1: Maak de code af.

Deze opdrachten doe je in twee stappen:
1. Zet op de juiste plekken aanhalingstekens in de code.
2. Staat alles goed? Voorspel dan wat de uitvoer van de code is.

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : 
                    "print Hallo allemaal!n
                    print Welkom bij Hedy\n",
    "answer"    : 
                    "Hallo allemaal\n
                    Welkom bij Hedy",
    "lines"     : 2
}


{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : 
                    "naam is Hermans\n
                    lokaal is 305\n
                    print Vandaag hebben we les van naam in lokaal!",
    "answer"    : "print Vandaag hebben we les van Hermans in 305!",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : 
                    "docenten is Hermans, Merbis, Bagci, Senkal\n
                    print De docent vandaag is docenten at random.",
    "answer"    :   "De docent vandaag is Hermans",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : 
                    "weer is zonnig, regen, wolken, onweer\n
                    print Wat is het lekker weer vandaag!",
    "answer"    :   "Wat is het lekker weer vandaag!",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : 
                    "print Wat is het lekker weer vandaag!\n
                    naam is Bassie",
    "answer"    :   "Wat is het lekker weer vandaag!",
    "lines"     : 1
}

#### Opdracht 2: Foutje?
Lees de codes goed! Welke zijn er goed of fout.

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "weer is zonnig, regen, wolken, onweer\nprint Bah! De computer loopt weer vast.",
    "answer"    : "Fout. Je kan een lijst niet printen"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "docenten is Hermans\nprint Vandaag alweer docenten at random",
    "answer"    : "Fout, docenten is geen lijst"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "docenten is onweer, regen, ijzel\nprint Vandaag alweer docenten at random!",
    "answer"    : "Goed, de naam hoeft niet te kloppen voor de computer."
}

### Avonturen

[Teacher] Dit zijn alle avonturen zonder `add to` en `remove from`.[/Teacher]
Dit is een goed moment voor deze avonturen:
Introductie
willekeurig
Dobbelsteen
Steen, papier, schaar
Muziek
Waarzegger
Restaurant
Spookhuis
Afwas?

### Lijsten aanpassen

Tot nu toe hebben we lijsten steeds aan het begin van het programma ingesteld.

```hedy
antwoorden is ja, nee, misschien
print Het antwoord is antwoorden at random
```

Maar soms wil je dat de gebruiker van een programma ook opties kan toevoegen.
Dat doe je met een `add` en een `to` commando.

```
dieren is 🐿, 🦔, 🦇, 🦉
dier is ask Wat zou het kunnen zijn?
add dier to dieren
print het was een dieren op willekeurig
```

Je kan ook iets uit een lijst verwijderen, met `remove` en `from`.

#### Opdracht 4: Goed of fout?

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "letters is a,b,c,d\nremove a to letters",
    "answer"    : "Fout. Bij remove hoort from, niet to."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "eten is pizza, friet, kapsalon\nremove kroket from eten",
    "answer"    : "Goed, je mag iets verwijderen dat niet in de lijst zit."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "eten is pizza, friet, kapsalon\nadd pizza to eten",
    "answer"    : "Goed, je mag iets toevoegen dat al in de lijst zit."
}


#### Opdracht 5: Schrijf de code

Kijk goed naar de uitvoer, en schrijf er een passende code bij. 
**Zorg ervoor dat er steeds minstens een willekeurige keuze in je programma zit, dus niet alleen een print!**

{
    "assignment": "input",
    "icon"      : "🧑‍💻",
    "output"    : "Welkom bij de bingoavond\nDe drie geluksnummers zijn:\n5 en 3 en 10",
    "answer"    : "getallen is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10\nprint Welkom bij de bingoavond\nprint De drie geluksnummers zijn:\nprint nummers at random en print nummers at random en print nummers at random",
    "lines"     : 4
}


{
    "assignment": "input",
    "icon"      : "🧑‍💻",
    "output"    : "We gaan vanavond naar de film.\nWe kiezen: Inside Out",
    "answer"    : "films is Avengers, Barbie, Inside Out\nprint We gaan vanavond naar de film.\nWe kiezen: films at random",
    "lines"     : 2
}


#### Opdracht 6: Programmeerwoorden 

We hebben deze les weer nieuwe programmeerwoorden geleerd! Leg ze uit je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent lijst?",
    "lines"     : 1,
    "answer"    : "Een variabele waarin meerdere waardes kunnen worden opgeslagen"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent willekeurig?",
    "lines"     : 1,
    "answer"    : "Iets dat door de computer wordt uitgekozen."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent toevoegen?",
    "lines"     : 1,
    "answer"    : "Iets in een lijst erbij zetten"
}


#### Opdracht 7: Codes

De code `is` is in dit leven veranderd, en we hebben ook nieuwe codes geleerd. 
Wat doen die? Leg het uit in je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `is`? (Let op: `is` kan dus meerdere dingen doen!)",
    "lines"     : 1,
    "answer"    : "Waarde (rechts van de is) opslaan in een variabele of lijst (links van de is)"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `add to`?",
    "lines"     : 1,
    "answer"    : "Voeg iets aan een lijst toe. Het element om toe te voegen staat tussen `add` en `to`, en de lijst staat erachter."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `remove from`?",
    "lines"     : 1,
    "answer"    : "Verwijdert iets uit een lijst. Het element om te verwijderen staat tussen `add` en `to`, en de lijst staat erachter."
}


{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `at random`?",
    "lines"     : 1,
    "answer"    : "Kiest een willekeurig element uit de lijst."
}


### Wat vond jij?

{
    "assignment": "text",
    "icon"      : "✍️",
    "question"  : "Wat was de leukste opdracht van dit level?",
    "lines"     : 1
}

{
    "assignment": "text",
    "icon"      : "✍️",
    "question"  : "Waarom vond je juist die opdracht leuk?",
    "lines"     : 5
}

{
    "assignment": "text",
    "icon"      : "✍️",
    "question"  : "Welke opdracht was het minst leuk?",
    "lines"     : 1
}

{
    "assignment": "text",
    "icon"      : "✍️",
    "question"  : "Waarom vond je juist die opdracht niet leuk?",
    "lines"     : 5
}


``
