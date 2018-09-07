# Labb L2

Detta är en mer omfattande labb i logikprogrammering i
Prolog.  Se labb-peket för uppgifts-instruktioner.

## Testning

Man kan testa sin kod på de givna exempeldatabaserna på följande sätt.

Starta SWI-Prolog:
```
austrin@tcs59:~/progp16/git/repositories/austrin-L2$ swipl
Welcome to SWI-Prolog (Multi-threaded, 64 bits, Version 7.2.3)
Copyright (c) 1990-2015 University of Amsterdam, VU Amsterdam
SWI-Prolog comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to redistribute it under certain conditions.
Please visit http://www.swi-prolog.org for details.

For help, use ?- help(Topic). or ?- apropos(Word).
```
Ladda in en av exempel-databaserna:
```
?- ['examples/example1.pl'].
true.
```
Ladda in er lösning (om ni valt att kalla er fil `l2.pl`, annars byter ni det mot rätt filnamn):
```
?- ['L2/l2.pl'].
true.
```
Sök efter spindeln:
```
?- spider(X).
X = spider ;
```

För att felsöka sin kod och hänga med i exekveringen använder man trace:
Innan anropet `spider(X).` kör man:
```
?- trace.
true.
```
När man nu kör `spider(X).` kommer man få stega igenom exekveringen:
```
[trace]  ?- spider(X).
   Call: (7) spider(_G1893) ?
```
Man kan stega framåt genom att trycka Enter.  Man kan även hoppa
över steg och undersöka i mer detalj vad som pågår, tryck `h` för
att få hjälp om vilka alternativ som finns.

Det finns även ett trevligt GUI till trace som man kan använda.
För att använda det anropar man predikatet `guitracer` (helst
*innan* man aktiverar trace så man slipper trace:a igenom anropet
till guitracer).

## Inlämning

Lösningen ska läggas i en katalog `L2/` (stort L) i repot och skickas
in som hämtbegäran.  Du kan ge din hämtbegäran vilken titel du vill,
t.ex. "Labb-inlämning".

Beskrivningen av din hämtbegäran ska innehålla följande:

* `Fixes #1` för att ange att denna inläming "fixar" issue #1 som vi
  öppnat åt dig.

* `Kattis: <id>`

  där `<id>` är Submission-ID på Kattis för din godkända lösning.

* `Students: @<username> @<username>`

  där `<username>` ger ditt och din labbkompis användarnamn
  (KTH-användarnamnet, samma användarnamn som du har på ditt KTH
  Git-konto).  Om du labbat själv anger du bara ditt eget
  användarnamn.

  Observera: för att ditt Git-konto ska kunna matchas mot ditt
  Kattis-konto krävs att antingen:
  - Du har knutit ditt Kattis-konto till ditt kth.se-konto (detta borde
    vara fallet för de allra flesta), eller
  - Du har lagt till (och verifierat) din kth.se-epost-adress till
    ditt Kattis-konto
