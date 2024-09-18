# Hedy - Les 3a

[Teacher] In level 3 leren leerlingen werken met lijsten. Die worden ingesteld zoals een variabele, met `is`, en kan je uitlezen met `at random`. [/Teacher]

## Lijsten en willekeurigheid

Aan het einde van de les kun jij:

* Meerdere dingen opslaan in een variabele, zo'n variabele heet een lijst.
* Een verhaal maken waarin willekeurige dingen gebeuren.
* Een tekening maken waarin willekeurige dingen verschijnen.

### Variabelen

Je hebt net op het bord de `is` opdracht gezien met een lijst. 
Met als bij een gewone variabele, slaan we iets op in een lijst met `is`.

```hedy
vrienden is Mo, Layla, Denny
print Ik ga vandaag naar vrienden at random
```

#### Opdracht 1: Omcirkel het juiste stukje code

{
    "assignment": "element selection",
    "question"  : "Omcircel alle lijsten in deze code",
    "icon"      : "◯",
    "code"      : "vandaag is maandag\nklassen is 1HC, 1HB, 1HA\nlokalen is 011, 304, 305, OLC",
    "answer"    : "klassen en lokalen"
}

{
    "assignment": "element selection",
    "question"  : "Op welke plek in de code wordt er tekst uit een lijst gebruikt?",
    "icon"      : "◯",
    "code"      : "klassen is 1HC, 1HB, 1HA\nprint vandaag heeft klassen at random vrij!",
    "answer"    : "Op het einde van regel 2"
}

#### Opdracht 2: Voorspel de uitvoer

Vind je het lastig? Gebruik dan weer het stappenplan om variabele-uitvoer te voorspellen.

1. Omcirkel de plek waar de lijst wordt ingesteld
2. Omcirkel de plek waar de lijst wordt gebruikt
3. Trek een lijn tussen deze plekken
4. Bij een `at` `random` mag je zelf willekeurig iets uit de lijst kiezen.

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "docenten is Hermans, Merbis, Bagci, Senkal\nprint Vandaag les van docenten at random!",
    "answer"    : "Vandaag les van **keuze uit docenten**",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "docenten is Hermans, Merbis, Bagci, Senkal\nprint De docent vandaag is Hermans.",
    "answer"    : "De docent vandaag is Hermans",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "weer is zonnig, regen, wolken, onweer\nprint Wat is het lekker weer vandaag!",
    "answer"    : "Fout! Je kan een lijst niet printen",
    "lines"     : 1
}

{TODO A/B Icon!

#### Opdracht 3: Foutje?
Lees de codes goed! Welke zijn er goed of fout.

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "A/B",
    "code"      : "weer is zonnig, regen, wolken, onweer\nprint Bah! De computer loopt weer vast.",
    "answer"    : "Fout. Je kan een lijst niet printen"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "A/B",
    "code"      : "docenten is Hermans\nprint Vandaag alweer docenten at random",
    "answer"    : "Fout, docenten is geen lijst"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "A/B",
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

#### Opdracht 4: Schrijf de code

Kijk goed naar de uitvoer, en schrijf er een passende code bij. 
**Zorg ervoor dat er steeds minstens een willekeurige keuze in je programma zit, dus niet alleen een print!**

{
    "assignment": "input",
    "icon"      : "🧑‍💻",
    "output"    : "Welkom bij de bingoavond\nDe drie geluksnummers zijn\n: 5 en 3 en 10",
    "answer"    : "getallen is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10\nprint Welkom bij de bingoavond\nprint De drie geluksnummers zijn:\nprint nummers at random en print nummers at random en print nummers at random",
    "lines"     : 4
}


{
    "assignment": "input",
    "icon"      : "🧑‍💻",
    "output"    : "We gaan vanavond naar de film.\nWe kiezen: Inside Out",
    "answer"    : "films is Avengers, Barbie, Inside Out\nprint e gaan vanavond naar de film.\nWe kiezen: films at random",
    "lines"     : 2
}


#### Opdracht 5: Programmeerwoorden 

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


#### Opdracht 6: Codes

De code `is` is in dit leven veranderd. En we hebben ook nieuwe codes geleerd. 
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

{TODO: goed of fout, 


------

#### Opdracht 8: Voorspel de uitvoer

Voorspel wat de uitvoer van deze codes is. Dat is bij de turtle of tekenschildpad natuurlijk een tekening.

{
    "assignment": "output",
    "icon"      : "💻",
    "type"      : "turtle",
    "code"      : "forward 100\nturn left\nforward 100\nturn left\nforward 100\nturn left\nforward 100\nturn left\n",
    "answer"    : "een vierkant",
    "lines"     : 5
}

{
    "assignment": "output",
    "icon"      : "💻",
    "type"      : "turtle",
    "code"      : "forward 100\nturn left\nforward 100\nturn right\nforward 100\nturn left\nforward 100\nturn right\n",
    "answer"    : "een trapje (zonder onderkant)",
    "lines"     : 5
}

{
    "assignment": "output",
    "icon"      : "💻",
    "type"      : "turtle",
    "code"      : "forward 100\nturn right\nforward 5\nturn right\nforward 100\nturn right\nforward 5\nturn right\n",
    "answer"    : "een hele smalle vierkant",
    "lines"     : 6
}






### Wat vond jij?

{
    "assignment": "text",
    "icon"      : "✍️",
    "question"  : "Wat was de leukste opdracht van level 1?",
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
