% Programmeringsparadigm (DD1361) HT16 - L1
% Thony Price & Ousainou Manneh, CDATE2

% 1.  Fibonacci-talen
%     Skriv ett predikat fib(+N, ?F) som är sant om och endast om F är det 
%     N’te Fibonacci-talet. Målet fib(30, F) ska alltså ha exakt en lösning,
%     nämligen att F är det trettionde Fibonacci-talet.

% Base predicate for F = 0
fib(0, 0).
% Base predicate for F = 1
fib(1, 1).

% Recursive function
fib(+N, ?F) :-
  N > 1,
  N2 is N-2, fib(N2, F2),
  N1 is N-1, fib(N1, F1),
  F  is F1 + F2.
  
% Fixes;
% 1.  Uppgiftsbeskrivningen använder metasymboler som +N 
%     och ?F - Vad betyder dem och hur ska de implementeras?
% 2.  Funktionen klarar inte av fib(30, F) - Hur optimera?