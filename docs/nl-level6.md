In level 6 komen er weer een nieuwe codes bij, je kunt nu namelijk gaan rekenen in je code.

De plus is makkelijk, die schrijf je zoals bij rekenen: 5 + 5 bijvoorbeeld. De keer is een beetje anders, want er zit namelijk geen keer op je toetsenbord. Zoek maar eens, die is er echt niet!
Daarom doen we de keer met het sterretje boven de 8: 5 * 5. Lees dat maar als 5 keer 5 dan onthoud je het het makkeljkst.

Hier vind je weer een aantal opdrachten om mee aan de slag te gaan.

# Meer regenwormen!
Je kunt ook in Level 6 weer een regenwormendobbelsteen maken, maar nu kun je ook uitrekenen hoeveel punten er gegooid zijn.
Je weet misschien dat de worm bij regenworm telt voor 5 punten. Nu kun je een worp gooien, en dan meteen uitrekenen hoeveel punten je dan hebt gegooid.
Zo doe je dat voor 1 dobbelsteen:

1 `keuzes is 1, 2, 3, 4, 5, regenworm`

2 `punten is 0`

3 `worp is keuzes at random`

4 `print 'je gooide ' worp`

5 `if worp is regenworm punten is punten + 5 else punten is punten + worp`

6 `print 'dat zijn dan ' punten`
Kun jij de code nu zo maken dat je de totaalscore krijgt voor 8 dobbelstenen?
Lukt het niet, bekijk dan de uitlegvideo om te zien hoe je de code afmaakt voor meer dobbelstenen.

# Tafeloefenprogramma

Nu je kunt rekenen, kun je ook een programma maken om sommetjes te oefenen.
Je kunt de sommen zelf verzinnen, bijv zo:

* `goedeantwoord is 11 * 27`
* `print 'Hoeveel is 11 keer 27?'`
* `antwoord is ask Weet jij het antwoord?`
* `if antwoord is goedeantwoord print 'goedzo' else print 'Foutje! Het was ' goedeantwoord`

Maar je kunt ook de computer zelf willekeurige sommen laten maken met random.

Zo kies je een aantal tafels om uit te oefenen, en pak je daaruit steeds een andere som:

* `tafels is 4, 5, 6, 8`
* `keer is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`

* `tafel is tafels at random`
* `keergetal is keer at random`
* `goedeantwoord is tafel * keergetal`

* `print 'hoeveel is ' tafel ' keer ' keergetal`

* `antwoord is ask Weet jij het antwoord?`
* `if antwoord is goedeantwoord print 'goedzo' else print 'foutje! het was ' goedeantwoord`


# Wie doet de afwas, en is dat wel eerlijk?
Hoe vaak gaat iedereen eigenlijk afwassen? Is dat wel eerlijk? Dat kun je nu tellen.

1 `mensen is mama, papa, Emma, Sophie`

2 `emmawastaf is 0`

3 `afwasser is mensen at random`

4 `print 'De afwasser is ' afwasser`

5 `if afwasser is Emma emmawastaf is emmawastaf + 1`

6 `print 'Emma gaat deze week ' emmawastaf ' keer afwassen'`

Nu kun je regels 3 t/m 5 een paar keer (bijv 7 keer voor een hele week) kopiëren om weer voor een hele week vooruit te rekenen.


# Zing een liedje met getallen erin

In liedjes zit vaak veel herhaling, en soms zitten er dan ook getallen in. Bijv het bekende Potje met vet!

1 `couplet is 1`

2 `print 'Ik heb het potje met vet'`

3 `print 'al op de tafel gezet'`

4 `print 'Ik heb het'`

5 `repeat 4 times print 'potje'`

6 `print 'veeeeeet'`

7 `print 'al op de tafel gezet'`

8 `couplet is couplet + 1`

9 `print 'Door naar het ' couplet 'e couplet'`

Regels 2 t/m 9 kun je nu zo vaak herhalen als je maar wilt door de regels te kopiëren.

# Wel een hoop knippen en plakken zeg!
In Level 5 hebben we geleerd 1 regel te herhalen met repeat, zo:

* `repeat 3 times print 'Baby Shark Tutududududu'`
 
 Maar zoals je in deze les ziet, wil je soms meerdere regels samen herhalen. Dat kan met knippen en plakken, maar dat is wel veel werk. In level 7 leer je hoe je dat makkelijker kan doen.
