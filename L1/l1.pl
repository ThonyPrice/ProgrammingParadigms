% Laboration 1 Prolog- uppvärmning
% Logikprogrammering
% Thony Price, Ousainou Manneh

% Uppgift 1

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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Rövarspråk Uppgift 2

rovarsprak([], []).

% Här mönstermatchas head för båda två
rovarsprak([H|T], [H|T2]) :-
% Här kollar vi ifall det är en vokal
member(H, [97, 101, 105, 111, 117, 121]),
% Rekursivt anrop
rovarsprak(T, T2).

% Här mönstermnatchas de båda headen igen, men lägger till ett o mellan de.
rovarsprak([H|T], [H,111,H|T2]) :-
rovarsprak(T, T2).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Medellängd Uppgift 3

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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Uppgift 4

%skyffla(lista, skyfflad)

% Här blir det sant med två listor
skyffla([], []).
skyffla([H|[]], [H|[]]).

% Här skyfflas listan med två hjälpfunktioner
% en som somskyfflar och den andra som förberedder nästa skyffel med resten av listan
skyffla([H,N | T], Skyfflad) :-
skyff([H, N |T], X),
rest([H, N|T], Rest1),
skyffla(Rest1, Y),
append(X, Y, Skyfflad).

%Här skyfflas det, returnerar varannat element
skyff([], []).
skyff([H| []], [H|[]]).

skyff([H, _|T], [H|T2]):-
skyff(T, T2).

% Tar varannat element för att förberedda nästa skyffling
rest([], []).
rest([_| []], []).
rest([_, N|T], [N|T2]):-
rest(T, T2).
