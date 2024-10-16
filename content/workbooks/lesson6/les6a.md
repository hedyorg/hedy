# Hedy - Toets Les 1 tot 5

{
    "teacher_note": "Dit is een toets voor leerlingen over level 1 t/m 5. We gebruiken wel overal de syntax van level 5, dus aanhalingstekens, en geen `echo` meer, anders wordt het verwarrend."
}

## SO

We maken vandaag een SO op papier. Lees dit goed voor je begint:

* De toets telt voor 1/6e mee voor je cijfer 
* We beginnen vandaag ook aan een huiswerk-opdracht. Die telt ook 1/6e mee.
* Lees goed wat je moet doen! Soms moet je twee dingen doen, vergeet dat dan niet!

#### Codes herkennen

Voor deze vragen moet jij stukjes code zoeken bij de juiste programmeerwoorden.
Kijk goed **wat** je moet vinden, en omcirkel dat.

{
    "assignment": "element selection",
    "question"  : "Omcirkel alle **variabelen** in deze code.",
    "icon"      : "◯",
    "code"      : "naam is Michael\n
                    print 'Hallo ' naam\n
                    leeftijd is 17\n
                    print 'Jij bent ' leeftijd ' jaar oud'",
    "answer"    : "Op alle regels"
}

{
    "assignment": "element selection",
    "question"  : "Omcirkel alle **variabelen** in deze code.",
    "icon"      : "◯",
    "code"      : "print 'welkom bij dit avontuur' naam
                   naam is Harry",
    "answer"    : "Op regel 2, maar niet op regel 1! Naam is namelijk nog niet ingesteld"
}

{
    "assignment": "element selection",
    "question"  : "Omcirkel nu de stukken code waarin de waarde van een variabele **wordt gebruikt.**",
    "icon"      : "◯",
    "code"      : "weer is zonnig\n
                    print 'het wordt vandaag ' weer",
    "answer"    : "Op regel 2"
}


{
    "assignment": "element selection",
    "question"  : "Omcirkel nu de stukken code waarin de waarde van een variabele **wordt gebruikt.**",
    "icon"      : "◯",
    "code"      : "naam is Ben\n
                    print 'Hallo ik ben Ben'",
    "answer"    : "Op geen regel"
}

{
    "assignment": "element selection",
    "question"  : "Op welke plek in de code wordt **er tekst uit een lijst geprint**?",
    "icon"      : "◯",
    "code"      : "winst is 10 euro, 5 euro, niks\n
                    print 'Jij wint ' winst at random",
    "answer"    : "Op het einde van regel 2"
}

{
    "assignment": "element selection",
    "question"  : "Op welke plek in de code wordt **er tekst uit een lijst geprint**?",
    "icon"      : "◯",
    "code"      : "vrienden is Mo, Layla, Sem\n
                    print vrienden at random ' gaat ook mee,'",
    "answer"    : "Op het begin van regel 2"
}


{
    "assignment": "element selection",
    "question"  : "Op welke plek in de code staat er een **conditie**?",
    "note"      : "Bij een conditie kijkt de computer of iets waar is of niet waar",
    "icon"      : "◯",
    "code"      :  "leeftijd is ask 'Hoe oud ben jij?'\n
                    if leeftijd is 18 print 'Jij mag nu een biertje' else print 'Jij bent te jong!'",
    "answer"    : "leeftijd is 18"
}

{
    "assignment": "element selection",
    "question"  : "Op welke plek in de code staat er een **conditie**?",
    "icon"      : "◯",
    "code"      :  "naam is Bert\n
                    if naam is Ernie print 'Jij bent oranje' else print 'Jij bent geel!'",
    "answer"    : "naam is Ernie"
}

### Goed of fout?

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "concierge is Michael\n
                    print Vandaag is concierge at random bij de receptie",
    "answer"    : "Fout, concierge is geen lijst"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "klassen is 1, 2, 5, 8, 12, 24\n
                    print De prijs valt op nummer .... klassen at random",
    "answer"    : "Goed, de naam hoeft niet te kloppen voor de computer."
}



{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "naam is Gea\n
                    print 'Goedemorgen ' voornaam!",
    "answer"    : "Fout (geen variabele gebruikt)"
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "print 'Daar staat een auto, fout geparkeerd!",
    "answer"    : "Fout. De aanhalingstekens moeten altijd in paren gebruikt worden."
}

{
    "assignment": "MC-code",
    "options"   : ["Goed" , "Fout"],
    "question"  : "Is deze code goed of fout?",
    "icon"      : "🤔",
    "code"      : "print \"De auto's staan op straat\"\n
                    print 'Dat mag niet!!'",
    "answer"    : "Goed. Je mag aanhalingstekens door elkaar gebruiken, als ze per regel maar hetzelfde zijn. Op de eerste regel moeten de dubbele door het woord auto's."
}

### Voorspel de uitvoer

Bij deze opdracht moet je voorspellen wat de computer gaat doen. 
Denk eraan dat computers heel precies zijn, iedere spatie of punt of komma telt!

* Zit er een `ask` in de code? Kies dan zelf een antwoord.
* Zit er een `random` in de code?  Kies dan een mogelijke keus van de computer.

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      :  "weer is zonnig, regen, wolken, onweer\n
                    print 'Vandaag wordt het... ' weer at random!",
    "answer"    : "Wat is het **keuze uit zonnig, regen, wolken, onweer**!",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "docenten is Hermans, Merbis, Bagci, Senkal\n
                    docent is docenten at random\n
                    if docent is Hermans print 'Jammer!'",
    "answer"    : "Jammer! of niks",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "toestand is ask Hoe gaat het met jou?\n
                    print 'Dus het gaat ' toestand ' met jou.'",
    "answer"    : " Dus het gaat **goed(bijv)** met jou",
    "lines"     : 1
}

{
    "assignment": "output",
    "icon"      : "💻",
    "code"      : "getallen is 1, 2, 3\n
                    print 'Welkom bij de bingoavond'\n
                    getal is getallen at random\n
                    if getal is 10 print 'Gewonnen!' else print 'Helaas'\n",
    "answer"    : "Welkom bij de bingoavond\n**'Helaas'** (want het kan nooit 10 worden)",
    "lines"     : 2
}

### Commando's en programmeerwoorden

We hebben deze lessen veel nieuwe commando's en woorden geleerd. 
In deze opdracht mag je er twee commando's uitleggen (is en if). Kies er daarna drie die je nog weet, en leg die uit.

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `is`?",
    "lines"     : 1,
    "answer"    : "Stelt een variabele of lijst in"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `if`?",
    "lines"     : 1,
    "answer"    : "Maakt een keuze op basis van een conditie"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `______`?",
    "lines"     : 1,
    "answer"    : ""
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `______`?",
    "lines"     : 1,
    "answer"    : "Maakt een keuze op basis van een conditie"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat doet het commando `______`?",
    "lines"     : 1,
    "answer"    : "Maakt een keuze op basis van een conditie"
}

Hetzelfde voor woorden. Eerst leg je twee woorden uit (variabele en lijst), dan kies je er zelf nog drie die je kan uitleggen.

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent het woord variabele?",
    "lines"     : 1,
    "answer"    : "Een waarde die een naam krijgt"
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent het woord lijst?",
    "lines"     : 1,
    "answer"    : "Een groepje waardes die samen een naam krijgt."
}

{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent het woord __________?",
    "lines"     : 1,
    "answer"    : ""
}


{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent het woord __________?",
    "lines"     : 1,
    "answer"    : ""
}


{
    "assignment": "define",
    "icon"      : "📖",
    "question"  : "Wat betekent het woord __________?",
    "lines"     : 1,
    "answer"    : ""
}

### De laatste vragen!



{
    "assignment": "text",
    "icon"      : "✍️",
    "question"  : "Weet jij nog meer over programmeren met Hedy dan er in deze toets staat?\n
                   Noem iets dat jij weet, maar niet in deze toets stond. Als het klopt, krijg je bonus.",
    "lines"     : 2
}

{
    "assignment": "text",
    "icon"      : "✍️",
    "question"  : "Verzin een goede toetsvraag\n
                  Wat had jij een goede vraag gevonden voor deze toets? Zet er ook het antwoord bij! ",
    "lines"     : 6
}


