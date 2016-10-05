% KTH - DD3161 Programmeringsparadigm
% Laboration 2 Prolog - Konspirationsdetektion
% Thony Price, Ousainou Manneh


% I den här databasen är det bara "spider" som kan vara spindeln i
% nätet i en konspiration (högst oväntat!)
person(spider).
person(conspirator1).
person(conspirator2).
person(other1).
person(other2).

knows(spider,conspirator1).
knows(spider,conspirator2).
knows(conspirator1,other1).
knows(conspirator2,other2).

% Check if two people knows eachother
knows2(X, Y) :- knows(Y, X).
knows2(X, Y) :- !, knows(X, Y).

% Generate a list of all persons
allPersons(L) :- bagof(X, person(X), L).

% Reduce all persons to a list with people "in the web"
inWeb(L) :-
  Tmp = [],
  allPersons(X),
  webFilter(X, Tmp, Z),
  L = Z.

% Generate list of people who knows at least someone
webFilter([], Z, Z). :- !.  
webFilter([H|T], Tmp, Z) :-
  knows2(H, _), !,
  webFilter(T, [H|Tmp], Z).

webFilter([H|T], Tmp, Z) :-
  not(knows2(H, _)),
  webFilter(T, Tmp, Z).

% Make someone a conspirator
makeCon(X) :- assert(isCon(X)).

% Make someone a spider
makeSpider(X) :- assert(isSpider(X)).

% Rotate list, putting first element last
rotatelist([H|T], R) :- append(T, [H], R).
  
% Return permutations for all people inWeb
perm(A) :-
  inWeb(L),
  permutation(L, A).

permutation([], []).
permutation([E | X], Y) :-
  permutation(X, Y1),
  append(Y2, Y3, Y1),
  append(Y2, [E | Y3], Y).
  
