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

**💻 Vraag**: Wat is de uitvoer van deze code? <br>
Code:									                        Uitvoer:
```hedy
print Hallo allemaal!nprint Welkom bij Hedy       ________________________________________
                                                  ________________________________________

```


**💻 Vraag**: Wat is de uitvoer van deze code? <br>
Code:									                        Uitvoer:
```hedy
naam is Hermans                                   ________________________________________
lokaal is 305                                     
print Vandaag hebben we les van naam in lokaal!   

```

**💻 Vraag**: Wat is de uitvoer van deze code? <br>
Code:									                        Uitvoer:
```hedy
docenten is Hermans, Merbis, Bagci, Senkal        ________________________________________
print De docent vandaag is docenten at random.    

```

**💻 Vraag**: Wat is de uitvoer van deze code? <br>
Code:									                        Uitvoer:
```hedy
weer is lalala, regen, wolken, onweer             ________________________________________
print Wat is het lekker weer vandaag!             

```

**💻 Vraag**: Wat is de uitvoer van deze code? <br>
Code:									                        Uitvoer:
```hedy
print Wat is het lekker weer vandaag!             ________________________________________
naam is Bassie                                    

```


#### Opdracht 1: Omcirkel het juiste stukje code

**◯ Opdracht**: Omcircel alle lijsten in deze code
```hedy
vandaag is maandag
klassen is 1HC, 1HB, 1HA
lokalen is 011, 304, 305, OLC
```

**◯ Opdracht**: Op welke plek in de code wordt er tekst uit een lijst gebruikt?
```hedy
klassen is 1HC, 1HB, 1HA
print vandaag heeft klassen at random vrij!
```


#### Opdracht 3: Foutje?
Lees de codes goed! Welke zijn er goed of fout.

**🤔 Vraag**: Is deze code goed of fout?
```hedy
weer is zonnig, regen, wolken, onweer
print Bah! De computer loopt weer vast.
```
Antwoord: <br> 〇 Goed<br> 〇 Fout

**🤔 Vraag**: Is deze code goed of fout?
```hedy
docenten is Hermans
print Vandaag alweer docenten at random
```
Antwoord: <br> 〇 Goed<br> 〇 Fout

**🤔 Vraag**: Is deze code goed of fout?
```hedy
docenten is onweer, regen, ijzel
print Vandaag alweer docenten at random!
```
Antwoord: <br> 〇 Goed<br> 〇 Fout

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

**🤔 Vraag**: Is deze code goed of fout?
```hedy
letters is a,b,c,d
remove a to letters
```
Antwoord: <br> 〇 Goed<br> 〇 Fout

**🤔 Vraag**: Is deze code goed of fout?
```hedy
eten is pizza, friet, kapsalon
remove kroket from eten
```
Antwoord: <br> 〇 Goed<br> 〇 Fout

**🤔 Vraag**: Is deze code goed of fout?
```hedy
eten is pizza, friet, kapsalon
add pizza to eten
```
Antwoord: <br> 〇 Goed<br> 〇 Fout


#### Opdracht 5: Schrijf de code

Kijk goed naar de uitvoer, en schrijf er een passende code bij.
**Zorg ervoor dat er steeds minstens een willekeurige keuze in je programma zit, dus niet alleen een print!**

**🧑‍💻 Vraag**: Welke code hoort bij deze uitvoer? <br>
Code:									                        Uitvoer:
```hedy
________________________________________          Welkom bij de bingoavond
________________________________________          De drie geluksnummers zijn:
________________________________________          5 en 3 en 10
________________________________________

```


**🧑‍💻 Vraag**: Welke code hoort bij deze uitvoer? <br>
Code:									                        Uitvoer:
```hedy
________________________________________          We gaan vanavond naar de film.
________________________________________          We kiezen: Inside Out
________________________________________

```


#### Opdracht 6: Programmeerwoorden

We hebben deze les weer nieuwe programmeerwoorden geleerd! Leg ze uit je eigen woorden.

**📖 Vraag**: Wat betekent lijst?
Antwoord: ____________________________________________________________________________________________________<br>

**📖 Vraag**: Wat betekent willekeurig?
Antwoord: ____________________________________________________________________________________________________<br>

**📖 Vraag**: Wat betekent toevoegen?
Antwoord: ____________________________________________________________________________________________________<br>


#### Opdracht 7: Codes

De code `is` is in dit leven veranderd, en we hebben ook nieuwe codes geleerd.
Wat doen die? Leg het uit in je eigen woorden.

**📖 Vraag**: Wat doet het commando `is`? (Let op: `is` kan dus meerdere dingen doen!)
Antwoord: ____________________________________________________________________________________________________<br>

**📖 Vraag**: Wat doet het commando `add to`?
Antwoord: ____________________________________________________________________________________________________<br>

**📖 Vraag**: Wat doet het commando `remove from`?
Antwoord: ____________________________________________________________________________________________________<br>


**📖 Vraag**: Wat doet het commando `at random`?
Antwoord: ____________________________________________________________________________________________________<br>


### Wat vond jij?

**✍️ Vraag**: Wat was de leukste opdracht van dit level? <br>

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
 <br>

**✍️ Vraag**: Waarom vond je juist die opdracht leuk? <br>

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
 <br>

**✍️ Vraag**: Welke opdracht was het minst leuk? <br>

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
 <br>

**✍️ Vraag**: Waarom vond je juist die opdracht niet leuk? <br>

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br>
 <br>


``
