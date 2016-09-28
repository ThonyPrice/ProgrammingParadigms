% Programmeringsparadigm (DD1361) HT16 - L1
% Thony Price & Ousainou Manneh, CDATE2

% -*-    1. Fibonacci-talen    -*- %

% Beräkna det N:e fibonaccitalet 
fib(N, F) :-
  N > 0,
  fib_help(N,0,1,F).
  
% När rekursionen i fib_help nått fib-talet 1, 
% unifiera det ackumulerade fibtalet med F
fib_help(1,_,F,F).

% För varje iteration minskar N med ett samtidigt som vi beräknar
% nästa fib-tal i Ack. Detta återanvänder vi för att vid nästa
% iteration beräkna nästa fib-tal osv.
fib_help(N,A1,A2,F) :-
  N1 is N-1,
  Ack is A1+A2,
  fib_help(N1,A2,Ack,F).
  
% -*-    2. Rovarsprak    -*- %

% Funktion för att se om en bokstav är en vokal
vokal(X) :- member(X, [101, 105, 111, 117, 125, 131]).

% Basfall för tom lista (när alla bokstäverna gåtts igenom)
rovarsprak([], []).

% Rekursiv funktion som fångar fall med vokal som head
rovarsprak(Text, RovarText) :-
  write("Hej"),
  Text \= [],
  [H|T] = Text,
  vokal(H),
  write(H),
  append([H], rovarsprak(T, RovarText), X),
  RovarText is X.


% -*-    3. Medellangd    -*- %

% Om teckenkod är bokstav
enbokstav(Decimal) :-
  char_code(X, Decimal),
  is_alpha(X).

% Unifiera ackumulerade summan med Result när listan gåtts igenom
sum_bokstaver([], Ack, Ack).

% Summera all bokstäver genom att öka ackumulator vid funnen bokstav
sum_bokstaver([H|T], Ack, Result) :-
  enbokstav(H),
  NyAck is Ack + 1,
  sum_bokstaver(T, NyAck, Result);
  not(enbokstav(H)),
  sum_bokstaver(T, Ack, Result).
  
% Basfall som binder ackumulerade summan till Result
sum_ord([], Ack, Ack).

% Om en bokstav upptäcks -> Ord påbörjat -> Öka ackumulatorn
% och skicka till tills_ejord som loopar tills nytt ord påbörjas.
sum_ord([H|T], Ack, Result) :-
  enbokstav(H),
  NyAck is Ack + 1,
  tills_ejord(T, NyAck, Result);
  not(enbokstav(H)),
  sum_ord(T, Ack, Result).

% Se kommentar över sum_ord.
tills_ejord([], Ack, Ack).
tills_ejord([H|T], Ack, Result) :-
  enbokstav(H),
  tills_ejord(T, Ack, Result);
  not(enbokstav(H)),
  sum_ord(T, Ack, Result).
  
% Huvudfunktion: dividerar antal bokstäver med antal ord och
% unifierar svaret med AvgLen
medellangd(Text, AvgLen) :-
   sum_bokstaver(Text, 0, X),
   sum_ord(Text, 0, Y),
   AvgLen is (X/Y).
  
% Givet kodskelett;
% fib(N, F) :- F = N.
% rovarsprak(Text, RovarText) :- RovarText = Text.
% medellangd(Text, AvgLen) :- AvgLen = 1.0.
% skyffla(Lista, Skyfflad) :- Skyfflad = Lista.