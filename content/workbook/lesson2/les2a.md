# Hedy - Les 2a

[Teacher] In level 2 leren leerlingen de codes `is` en `is ask` [/Teacher]

## Variabelen

Aan het einde van de les kun jij:

* Iets opslaan in een variabele
* Een verhaal en tekening maken waarin je een variabele gebruikt

### Variabelen

Je hebt net op het bord de `is` opdracht gezien. 
Een `is` opdracht slaat iets op in de computer, en geeft het een naam. We noemen dat een variabelen.
Wat in de variabele is opgeslagen noemen we de waarde van de variabele.

```hedy
naam is Mo
print naam
```

#### Opdracht 1: Omcirkel het juiste stukje code

{
    "assignment": "element selection",
    "question"  : "Omcirkel alle variabelen in deze code.",
    "icon"      : "◯",
    "code"      : "naam is Hedy\nprint Hallo naam\nleeftijd is 17\nprint Jij bent leeftijd jaar oud",
    "answer"    : "Op alle regels"
}

{
    "assignment": "element selection",
    "question"  : "Omcirkel nu de stukken code waarin een variabele **wordt ingesteld.**",
    "icon"      : "◯",
    "code"      : "naam is Hedy\nprint Hallo naam\nleeftijd is 17\nprint Jij bent leeftijd jaar oud",
    "answer"    : "Op regel 1 en 3"
}

{
    "assignment": "element selection",
    "question"  : "Omcirkel nu de stukken code waarin de waarde van een variabele **wordt gebruikt.**",
    "icon"      : "◯",
    "code"      : "naam is Hedy\nprint Hallo naam\nleeftijd is 17\nprint Jij bent leeftijd jaar oud",
    "answer"    : "Op regel 2 en 4"
}



#### Opdracht 2: Voorspel de uitvoer

Tip: Vind je het lastig om de uitvoer te voorspellen? Gebruik dan dit stappenplan:

1. Omcirkel de plek waar een variabele wordt ingesteld
2. Omcirkel de plek waar de variabele wordt gebruikt
3. Trek een lijn tussen deze plekken
4. Zet de waarde (aan de rechterkant van de `is` op de plek van het gebruik).

Voorbeeld:

{TODO

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "naam is Mo\nprint Goed bezig naam!",
    "answer"    : "Goed bezig Mo!",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "naam is Mo\nprint Goed bezig Mo!",
    "answer"    : "Goed bezig Mo!",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "voornaam is Layla\nprint Goedemorgen naam!",
    "answer"    : "Goedemorgen naam!",
    "lines"     : 1
}


#### Opdracht 3: Foutje?
Lees de codes goed! Welke zijn er goed of fout.

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "A/B",
    "code"      : "achternaam is Jansen\nprint Goedemorgen naam!",
    "answer"    : "Goed"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "A/B",
    "code"      : "naam is\nprint Goedemorgen naam!",
    "answer"    : "Fout"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "A/B",
    "code"      : "naam is Jansen\nprint Goedemorgen meneer naam!\nprint Hallo meneer naam!",
    "answer"    : "Goed"
}


### Invoer vragen

Alleen tekst opslaan is nog niet krachtig. In level 1 hebben we de code `ask` gezien.
Die code mag je nu combineren met een `is`. Dat gaat zo:

```hedy
naam is ask Hoe heet jij?
```

### Invoer laten zien

Je kan nu gewoon met een `print` het antwoord laten zien, zonder `echo`.

```hedy
naam is ask Hoe heet jij?
print dus jij heet: naam 
```

Als iemand die Maan heet deze code zou gebruiken, dan wordt de uitvoer:

```
dus jij heet: Maan
```

#### Opdracht 4: Voorspel de uitvoer

Voorspel wat de uitvoer van deze codes is. Doe alsof je je eigen naam hebt ingevuld.

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "naam is ask Hoe heet jij?\nprint dus jij heet: naam",
    "answer"    : "dus jij heet: **naam**",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "toestand is ask Hoe gaat het met jou?\nprint Dus het gaat toestand met jou",
    "answer"    : " Dus het gaat **goed** met jou",
    "lines"     : 1
}


#### Opdracht 5: Programmeer-woorden 

We hebben deze les weer nieuwe woorden geleerd! Leg ze uit je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent variabele?",
    "lines"     : 1,
    "answer"    : "Een naam die je geeft aan iets, bijv voornaam of leeftijd."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent waarde?",
    "lines"     : 1,
    "answer"    : "Wat je opslaat in een variabele, bijv Henk of 12."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent instellen?",
    "lines"     : 1,
    "answer"    : "Een programma waarbij een gebruiker invoer kan geven."
}


#### Opdracht 6: Codes

We hebben nieuwe codes geleerd: `is`, `is ask` samen. Wat doen die? Leg het uit in je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `is`?",
    "lines"     : 1,
    "answer"    : "Waarde (rechts van de is) opslaan in een variabele (links van de is)"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `is ask`?",
    "lines"     : 1,
    "answer"    : "Vraag om invoer van de gebruiker en die opslaan in de variabele links van de is."
}

