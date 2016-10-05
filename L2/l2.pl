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

% Get who's the spider when all conspirators is defined
spider(Z) :-
  bagof(X, isCon(X), L), 
  knowsAll(Z, L).

% Binds spider to Z if Z knows all conspirators
knowsAll(_, []) :- !.
knowsAll(Z, [H|T]) :-
  knows2(Z, H),
  knowsAll(Z, T).

isCon(conspirator1).
isCon(conspirator2).
persons(other1, other2).

% spider(X) :-
%   knows2()

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
  
% Make a list with as many lists as there are persons,
% each list should have a different head than the other ones.
sLists(L) :-
  inWeb(X),
  length(X, C),
  Tmp = [],
  append(X, Tmp, X1),
  rots(X1, Tmp, C, Res),
  L = Res.

% Ger en lista för lite, basfallet kan sänkas till noll för att ge alla 
% listor men då flir sista elementet i sista listan 'element'|...
rots(_, Res, 1, Res) :- !.  
rots(X, Tmp, C, Res) :-
  C1 is C-1,
  rotatelist(X, X1),
  append([X1], Tmp, Tmp1),
  rots(X1, Tmp1, C1, Res).

% Rotate list, putting last element first
rotatelist([H|T], R) :- append(T, [H], R).  

combinations(A) :-
  sLists(X),
  combos(X, [], Res),
  A = Res.

combos([], Res, Res) :- !.  
combos([H|T], Tmp, Res) :-
  [S|P] = H,  % S is spider, P is persons
  subset(P, C),
  append(S, C, Tmp),
  combos(T, Tmp, Res).
  

% Return permutations for all people inWeb
perm(A) :-
  inWeb(L),
  subset(L, A).

% Generate all subsets of a list, code from:
% http://stackoverflow.com/questions/4912869/subsets-in-prolog
subset([], []).
subset([E|Tail], [E|NTail]):-
  subset(Tail, NTail).
subset([_|Tail], NTail):-
  subset(Tail, NTail).



% --*-- Code that might be reused later --*-- %

% Make someone a conspirator
% makeCon(X) :- assert(isCon(X)).

% Make someone a spider
makeSpider(X) :- assert(isSpider(X)).

permutation([], []).
permutation([E | X], Y) :-
  permutation(X, Y1),
  append(Y2, Y3, Y1),
  append(Y2, [E | Y3], Y).
  
