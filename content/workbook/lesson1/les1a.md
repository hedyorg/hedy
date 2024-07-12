# Hedy - Les 1a

[Teacher] Het doel van deze les is om de eerste codes uit level 1 van Hedy te leren kennen: `print` en `echo` [/Teacher]

## Printen en invoer

Aan het einde van de les kun jij:

* Code schrijven die tekst print
* Een verhaal met invoer maken

### Opdrachten
Een computer doet niet zomaar zelf iets, je moet een computer altijd een opdracht geven. Om code uit te printen, gebruiken we de code `print`.

### Tekst printen

Je hebt net op het bord de `print` opdracht gezien. 
Een `print` opdracht print een woord uit, als het tussen aanhalingstekens staat. Bijvoorbeeld zo:

```hedy
print Hallo allemaal
```

### Opdracht 1: Voorspel de uitvoer

[Assignment:Output
Code:print Hallo allemaal
Icon:>
Lines:1
Answer:Hallo allemaal] 

[Assignment:Output
Code:print goedemorgen!
Icon:>
Lines:1
Answer:goedemorgen!] 

### Opdracht 2: Foutje?
Soms sluipt er een foutje in je code. Dat is niet erg, maar Hedy kan je code dan niet goed lezen.
Welke van deze code zijn fout, denk jij?

[Assignment:MC
Options: Goed,Fout
Code:prnt Hallo allemaal!
Icon:A/B
Answer:Goed] 

[Assignment:MC
Options: Goed,Fout
Code:print print
Icon:A/B
Answer:Goed] 

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


### Opdracht 3: Voorspel de uitvoer

Voorspel wat de uitvoer van deze codes is. Vul steeds je eigen naam in, of een ander kloppend antwoord.

[Assignment:Output
Code:ask Hoe heet jij?
echo dus jij heet:
Icon:>
Lines:2
Answer:dus jij heet: **naam**] 

[Assignment:Output
Code:ask Hoe heet jij?
echo Leuk om je te ontmoeten, 
Icon:>
Lines:2
Answer:Leuk om je te ontmoeten, **naam**] 
