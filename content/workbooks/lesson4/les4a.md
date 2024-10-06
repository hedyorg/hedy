# Hedy - Les 4a

{
    "teacher_note": "In level 4 leren leerlingen aanhalingstekens gebruiken in code. Dat is niet altijd de meest leuke les maar goed oefenen is wel nodig om latere frustratie te voorkomen.  Om het leuker te maken kan je in deze les andere features aanbieden, zoals `clear` of een muziekopdracht."
}


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
                    "print Hallo allemaal!\n
                    print Welkom bij Hedy\n",
    "answer"    : 
                    "Hallo allemaal\n
                    Welkom bij Hedy",
    "lines"     : 2
}

Vergeet niet deze opdrachten in twe stappen te doen, eerst de aanhalingstekens links.
Dan de code rechts!


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
    "code"      : "print 'Daar lopen twee lama's'",
    "answer"    : "Fout. Er staat een aanhalingsteken tussen de enkele aanhalingstekens."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "print 'De lama wandelt op straat",
    "answer"    : "Fout. De aanhalingstekens moeten altijd in paren gebruikt worden."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "print "Daar lopen twee oma's",
    "answer"    : "Goed! Als je twee aanhalingstekens gebruikt dan kan je wel oma's schrijven."

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "print 'De lama wandelt op straat'\n
                    print \"Wat een avontuur\"",
    "answer"    : "Goed. Je mag aanhalingstekens door elkaar gebruiken, als ze per regel maar hetzelfde zijn!"
}

#### Ask

Vergeet niet dat je ook bij `ask` aanhalingstekens gebruikt!

#### Opdracht 3: Foutje?
Lees de codes goed! Welke zijn er goed of fout.

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "ask 'Daar lopen twee konijnen'",
    "answer"    : "Fout. Vergeet niet bij ask een variabele te gebruiken!"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "naam is ask 'Hoe heet jij?'",
    "answer"    : "Fout. Aanhalingstekens moeten altijd in paren gebruikt worden."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "aantal is ask \"Hoeveel capibara's lopen daar?\"",
    "answer"    : "Goed."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "aantal is ask \"Hoeveel capibara's lopen daar?\"
                   print 'Dat zijn er aantal'",
    "answer"    : "Fout. Het woord aantal wordt geprint en niet de variabele"
}

#### Opdracht 4: Schrijf de code

Kijk goed naar de uitvoer, en schrijf er een passende code bij. 

{
    "assignment": "input",
    "icon"      : "🧑‍💻",
    "output"    : "Welkom bij de bingoavond\n
                    Hier komt het eerste getal...!",
    "answer"    : "print 'Welkom bij de bingoavond'\n
                    print 'Hier komt het eerste getal!'",
    "lines"     : 2
}


{
    "assignment": "input",
    "icon"      : "🧑‍💻",
    "output"    : "We gaan vanavond naar de film.\n
                    Waar heb jij zin in?",
    "answer"    : "print 'We gaan vanavond naar de film.'\n
                    film is ask 'Waar heb jij zin in?'",
    "lines"     : 2
}


#### Opdracht 5: Programmeerwoorden 

We hebben deze les weer nieuwe programmeerwoorden geleerd! Leg ze uit je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat zijn aanhalingstekens?",
    "lines"     : 1,
    "answer"    : "Hoge komma's"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Waarvoor gebruiken we in Hedy aanhalingstekens?",
    "lines"     : 1,
    "answer"    : "Voor iets dat door de computer precies zo moet worden geprint."
}



#### Opdracht 6: Codes

We hebben ook nieuwe codes geleerd in level 4.

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `clear`?",
    "lines"     : 1,
    "answer"    : "Maakt het scherm leeg"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `color`?",
    "lines"     : 1,
    "answer"    : "Verandert de kleur van de turtle"
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

