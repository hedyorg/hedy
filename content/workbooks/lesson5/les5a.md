# Hedy - Les 5a

[Teacher] In level 5 leren leerlingen de `if` en `else` codes, die zijn vrij lastig omdat nu niet meer alles regels altijd worden uitgevoerd. [/Teacher]

## Aanhalingstekens

Aan het einde van de les:

* hoe je de computer kan laten reageren op invoer.

### Keuzes maken

Tot nu toe voerde Hedy altijd alle regels code uit. Vanaf nu kan je met een `if` bepaalde regels uitvoeren, alleen in bepaalde gevallen.
De code die je na `if` schrijft, noem je een conditie.
In dit voorbeeld is de conditie `vriend is Jasmijn.`

```hedy
vriend is ask 'Hoe heet jij?'
if vriend is Jasmijn print 'Hallo!' else print 'Nee, jij niet!'
```

#### Opdracht 1a: Onderstreep de condities

Wat is een conditie? Onderstreep in deze codes steeds de conditie.

{
    "assignment": "element selection",
    "question"  : "Omcircel alle lijsten in deze code",
    "icon"      : "◯",
    "code"      :  "vandaag is ask 'Welke dag is het?'\n
                    if vandaag is vrijdag print 'Ja' else print 'Nee'",
    "answer"    : "print 'Ja'"
}

{
    "assignment": "element selection",
    "question"  : "Omcircel alle lijsten in deze code",
    "icon"      : "◯",
    "code"      :  "vandaag is ask 'Welke dag is het?'\n
                    if vandaag is zaterdag print 'Geen school vandaag' else print 'Helaas wel'",
    "answer"    : "print 'Helaas wel'"
}

{
    "assignment": "element selection",
    "question"  : "Omcircel alle lijsten in deze code",
    "icon"      : "◯",
    "code"      :  "leeftijd is ask 'Hoe oud ben jij?'\n
                    if leeftijd is 16 print 'Perfecto' else print 'Jij bent te jong!'",
    "answer"    : "print 'Jij bent te jong!'"
}

#### Opdracht 1b: Omcirkel de juiste regels

Welke code wordt uitgevoerd? Omcirkel alleen die stukken.
Doe alsof het vandaag vrijdag is, en jij 12 jaar bent.

{
    "assignment": "element selection",
    "question"  : "Omcircel alle lijsten in deze code",
    "icon"      : "◯",
    "code"      :  "vandaag is ask 'Welke dag is het?'\n
                    if vandaag is vrijdag print 'Ja' else print 'Nee'",
    "answer"    : "print 'Ja'"
}

{
    "assignment": "element selection",
    "question"  : "Omcircel alle lijsten in deze code",
    "icon"      : "◯",
    "code"      :  "vandaag is ask 'Welke dag is het?'\n
                    if vandaag is zaterdag print 'Geen school vandaag' else print 'Helaas wel'",
    "answer"    : "print 'Helaas wel'"
}

{
    "assignment": "element selection",
    "question"  : "Omcircel alle lijsten in deze code",
    "icon"      : "◯",
    "code"      :  "leeftijd is ask 'Hoe oud ben jij?'\n
                    if leeftijd is 16 print 'Perfecto' else print 'Jij bent te jong!'",
    "answer"    : "print 'Jij bent te jong!'"
}


#### Opdracht 2: Foutje?
Lees de codes goed! Welke zijn er goed of fout.

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      :  "leeftijd is ask 'Hoe oud ben jij?'\n
                    if leeftijd is 16 print 'Perfecto' else 'Jij bent te jong!'",
    "answer"    : "Fout. Er staat geen print achter else"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      :  "dier is ask 'Wat voor dier is dat?'\n
                    if dier is Lama print 'Beeeee'",
    "answer"    : "Goed! Er hoeft geen else code te staan"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "print \"Daar lopen twee oma's\"",
    "answer"    : "Goed! Als je twee aanhalingstekens gebruikt dan kan je wel oma's schrijven."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "if naam Hedy 
                    print 'Programmeren is leuk!'",
    "answer"    : "Fout, de is mist."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "ask 'Hoe heet deze school?'
                    if school is LK print 'Ja!' ",
    "answer"    : "Fout. Er staat geen variabele bij ask."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "aantal is ask \"Hoeveel capibara's lopen daar?\"
                   if aantal is 5 print 'Dat zijn er dan aantal'",
    "answer"    : "Fout. Het woord aantal wordt geprint en niet de variabele"
}


#### Opdracht 3: Voorspel de uitvoer

Wat is de uitvoer van deze programma's? 
Let op! Soms staat er random in een programma. Dan moet je zelf kiezen wat Hedy zou kiezen.
Er kunnen dan dus meerdere antwoorden goed zijn!

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "docenten is Hermans, Merbis, Bagci, Senkal\n
                    docent is docenten at random
                    if docent is Hermans print 'Hoera!'",
    "answer"    : "Hoera! of niks",
    "lines"     : 1
}


#### Opdracht 5: Programmeerwoorden 

We hebben deze les weer nieuwe programmeerwoorden geleerd! Leg ze uit je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat is een conditie?",
    "lines"     : 1,
    "answer"    : "Iets dat waar of niet waar is"
}



#### Opdracht 6: Codes

We hebben ook nieuwe codes geleerd in level 5.

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `if`? ",
    "lines"     : 1,
    "answer"    : "Bepalen welke regel wordt uigevoerd."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `else`?",
    "lines"     : 1,
    "answer"    : "Wordt uitgevoerd als de conditie niet waar is."
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
