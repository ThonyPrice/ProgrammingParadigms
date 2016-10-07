% KTH - DD3161 Programmeringsparadigm
% Laboration 2 Prolog - Konspirationsdetektion
% Thony Price, Ousainou Manneh

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

spider(S) :-
  person(Sx),
  gtFriends(Sx, Sfriends),
  inWeb(All),
  allConnected([Sx|Sfriends], All),
  cases(Sfriends, [], K),
  notInList(K, All, Persons),
  allConnected([Sx|Sfriends], Persons), 
  Sx = S.


% Check if two people knows each other 
knows2(X, Y) :- not(X =@= Y), knows(X, Y).
knows2(X, Y) :- not(X =@= Y), knows(Y, X).

% Get all friends of a person 
gtFriends(P, C) :-              
  setof(X, knows2(P, X), C).

% Get all persons  
inWeb(All) :-                       
  setof(X, person(X), All).

% True if everyone in first list knows someone in other list
allConnected(_, []) :- !.
allConnected(Cons, [H|T]) :-
  member(C, Cons),
  knows2(C, H), !,
  allConnected(Cons, T).

% Check if X knows anyone in List
listKnows(X, List) :-  
  member(Y, List),
  knows2(X, Y), !. 

% Bind Tmp to Res when list is empty (base case)
cases([], K, K).
% Case 1: Set first element as conspirator
cases([H|T], P, K) :-
  not(listKnows(H, P)),   % H (possible con) can't know any other cons
  cases(T, [P|H], K).
% Case2: Set first element as person   
cases([_|T], P, K) :-
  cases(T, P, K).  
  
% Given a list, return which persons not included  
notInList([], Return, Return) :- !.  
notInList([H|T], Out, Return) :-
  delete(Out, H, Out1), 
  notInList(T, Out1, Return).

