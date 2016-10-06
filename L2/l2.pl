% KTH - DD3161 Programmeringsparadigm
% Laboration 2 Prolog - Konspirationsdetektion
% Thony Price, Ousainou Manneh

% Check if two people knows each other 
knows2(X, Y) :- not(X =@= Y), knows(X, Y).
knows2(X, Y) :- not(X =@= Y), knows(Y, X).

% Reduce all persons to a list with people "in the web" 
inWeb(Web) :-
  bagof(X, person(X), All),
  webFilter(All, [], Web).

% Generate list of people who knows at least someone
webFilter([], Z, Z). :- !.  
webFilter([H|T], Tmp, Z) :-
  knows2(H, _), !,
  webFilter(T, [H|Tmp], Z).
webFilter([_|T], Tmp, Z) :-
  webFilter(T, Tmp, Z).

% Pick a person in the Web to be a spider
pickOne(List, S) :-
  member(S, List).

% Get all persons except one (spider)  
spiderKnows(S, C) :-
  bagof(X, knows2(S, X), C).

% Generate all subsets of a list, code from:
% http://stackoverflow.com/questions/4912869/subsets-in-prolog
subSet([], []).
subSet([E|Tail], [E|NTail]):-
  subSet(Tail, NTail).
subSet([_|Tail], NTail):-
  subSet(Tail, NTail).

% Check if someone from one list knows someone in another list
listKnows(List1, List2) :- 
  member(X, List1), 
  member(Y, List2),
  knows2(X, Y), !.  

% Given a list, return which persons not included  
notInList([], Return, Return) :- !.  
notInList([H|T], Out, Return) :-
  delete(Out, H, Out1), 
  notInList(T, Out1, Return).

% Check if anyone in a list is not known by anyone in another list
notKnows([], _) :- !.
notKnows([H|T], Others) :- 
  member(P, Others),
  knows2(H, P), !,  
  notKnows(T, Others).  

notKnows([H|T], Others) :- 
  member(P, Others),
  member(H1, [H|T]),
  knows2(H, H1), !, 
  knows2(H1, P), !, 
  notKnows(T, Others).  

% From a list, get a list of all people that's known 
allKnown([], Out, Out) :- !.
allKnown([H|T], Tmp, Out) :-
  spiderKnows(H, X),
  append(X, Tmp, Tmp1),
  allKnown(T, Tmp1, Out).

% Comment
notKnown([], _) :- !.  
notKnown([H|T], List) :-
  member(H, List), !,
  notKnown(T, List).  


% Generate-and-test...
spider(S) :-
  inWeb(All),                         % List of all people in web
  pickOne(All, Sx),                   % Choose a spider 
  spiderKnows(Sx, Cons),              % Get a list of all who knows spider
  subSet(Cons, Conset),               % Generate all conspirator-subsets of them
  
  Conset \= [],                       % There has to be some conspirators
  not(listKnows(Conset, Conset)),     % No cons can know each other    
  
  notInList([Sx|Conset], All , Not),  % Who is not in list?
  %notKnows([Sx|Conset], Not),        % Is there anyone not known by spider/con
  allKnown([Sx|Conset], [], AllKnown),% Get all known by spider and cons
  notKnown(Not, AllKnown),            % All not in list must be knows by spider or conspirators  
  
  S = Sx.                             % If all tests above succeds, Sx must be spider


  
% --*-- Written code that is currently unused --*-- %
  
% Binds spider to Z if Z knows all conspirators
knowsAll(_, []) :- !.
knowsAll(Z, [H|T]) :- 
  knows2(Z, H), !,      
  knowsAll(Z, T).

