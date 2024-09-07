# Hedy - Les 1a

[Teacher] Het doel van deze les is om de eerste drie codes uit level 1 van Hedy te leren kennen: `print`, `echo` en `ask`. [/Teacher]

## Printen en invoer

Aan het einde van de les kun jij:

* Code schrijven die tekst print
* Een verhaal met invoer maken

### Opdrachten
Een     "assignment": "output" doet niet zomaar zelf iets, je moet een computer altijd een opdracht geven. Zo'n opdracht heet commando. Om code uit te printen, gebruiken we de code `print`.

### Tekst printen

Je hebt net op het bord de `print` opdracht gezien. 
Een `print` opdracht print een woord uit, als het tussen aanhalingstekens staat. Bijvoorbeeld zo:

```hedy
print Hallo allemaal
```

#### Opdracht 1: Voorspel de uitvoer

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "print Hallo allemaal",
    "answer"    : "Hallo allemaal",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "print goedemorgen",
    "answer"    : "goedemorgen",
    "lines"     : 1
}



#### Opdracht 2: Foutje?
Soms sluipt er een foutje in je code. Dat is niet erg, maar Hedy kan je code dan niet goed lezen.
Welke van deze code zijn fout, denk jij?

{
    "assignment": "MC"
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "A/B",
    "code"      : "prnt Hallo allemaal!",
    "answer"    : "Fout"
}

{
    "assignment": "MC"
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "A/B",
    "code"      : "print print",
    "answer"    : "Goed"
}



### Invoer vragen

Alleen tekst is een beetje saai. Je kan in Hedy ook om _invoer_ vragen. Invoer is tekst die je aan de computer geeft.
De computer onthoudt die tekst en kan die later weer aan jou laten zien.
Deze code toont de vraag 'Hoe heet jij?'

```hedy
ask Hoe heet jij?
```

### Invoer laten zien

Alleen een ask slaat het antwoord op, maar laat het niet zien. Daarvoor heb je de opdracht `echo` nodig. Die laat het antwoord zien op het einde van de zin.
Bijvoorbeeld zo:

```hedy
ask Hoe heet jij?
echo dus jij heet: 
```

Als iemand die Maan heet deze code zou gebruiken, dan wordt de uitvoer:

```
dus jij heet: Maan
```

Let op, het komt precies zo in beeld als het er staat, dus met hetzelfde hoofdlettergebruik en de dubbele punt erbij!


#### Opdracht 3: Voorspel de uitvoer

Voorspel wat de uitvoer van deze codes is. Doe alsof je je eigen naam hebt ingevuld.

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "ask Hoe heet jij?\necho dus jij heet:",
    "answer"    : "dus jij heet: **naam**",
    "lines"     : 2
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "ask Hoe heet jij?\necho Leuk om je te ontmoeten,",
    "answer"    : "Leuk om je te ontmoeten, **naam**",
    "lines"     : 2
}


#### Opdracht 4: Programmeer-woorden 

Iedere les gaan we nieuwe woorden leren, deze les ook. Weet jij wat deze termen betekenen? Leg het uit je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent commando?",
    "lines"     : 1,
    "answer"    : "Een opdracht die je aan de computer geeft, bijv print."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent invoer?",
    "lines"     : 1,
    "answer"    : "Wat je intikt, als Hedy een ask venster laat zien."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent uitvoer?",
    "lines"     : 1,
    "answer"    : "Wat Hedy op het scherm zet als je op Uitvoeren drukt, in het rechterscherm."
}

#### Opdracht 5: Codes

We hebben tot nu toe 3 codes geleerd: `print`, `ask` en `echo`. Wat doen die? Leg het uit in je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `print`?",
    "lines"     : 1,
    "answer"    : "Zet tekst op het scherm."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `ask`?",
    "lines"     : 1,
    "answer"    : "Vraag om invoer van de gebruiker."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `echo`?",
    "lines"     : 1,
    "answer"    : "Herhaalt de invoer van de gebruiker."
}


## Op de computer!

Ga nu naar Les1b - Deel 1

## Tekenen

Aan het einde van de les kun jij:

* Tekeningen maken met de tekenturtle.


#### Opdracht 6: Programmeer-woorden 

Weet jij wat deze termen betekenen? Leg het uit je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent tabblad?",
    "lines"     : 1,
    "answer"    : "Een digitaal mapje waar een opdracht in zit."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent turtle (bij programmeren)?",
    "lines"     : 1,
    "answer"    : "De optie om te tekenen met code."
}

#### Opdracht 7: Codes

We hebben weer 2 nieuwe codes geleerd. Wat doen die? Leg het uit in je eigen woorden. 

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `forward`?",
    "lines"     : 1,
    "answer"    : "Beweegt de tekenschildpad vooruit"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `turn`?",
    "lines"     : 1,
    "answer"    : "Draait de tekenschildpad links of rechts"
}


#### Opdracht 8: Voorspel de uitvoer

Voorspel wat de uitvoer van deze codes is. Dat is bij de turtle of tekenschildpad natuurlijk een tekening.

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "forward 100\nturn left\nforward 100\nturn left\nforward 100\nturn left\nforward 100\nturn left\n",
    "answer"    : "een vierkant",
    "lines"     : 5
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "forward 100\nturn left\nforward 100\nturn right\nforward 100\nturn left\nforward 100\nturn right\n",
    "answer"    : "een trapje (zonder onderkant)",
    "lines"     : 5
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "forward 100\nturn right\nforward 5\nturn right\nforward 100\nturn right\nforward 5\nturn right\n",
    "answer"    : "een hele smalle vierkant",
    "lines"     : 6
}


#### Opdracht 9: Schrijf de code

We draaien het nu om! Je krijg een uitvoer en jij moet de code erbij schrijven.


{
    "assignment": {"type": "input"}
    "icon"      : "🧑‍💻",
    "output"    : "
```
----------
|        |
|        |
|        |
|        |
|        |
---------
```
"
    "answer"    : "forward 50\nturn left\nforward 50\nturn left\nforward 50\nturn left\n",
    "lines"     : 8
}



{
    "assignment": {"type": "input"}
    "icon"      : "🧑‍💻",
    "output"    : "
```
  _
   |
   _________
```
"
    "answer"    : "forward 5\nturn right\nforward 10\nturn left\nforward 50\n",
    "lines"     : 5
}
