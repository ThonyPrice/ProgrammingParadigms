% KTH - DD3161 Programmeringsparadigm
% Laboration 2 Prolog - Konspirationsdetektion
% Thony Price, Ousainou Manneh

spider(S)     :-  person(S), isSpider(S).

isSpider(S)   :-  setof(X, person(X), All),           % Get list of all persons
                  gtFriends(S, Sfriends),             % Possible spider friends
                  allConnected(All, [S|Sfriends]),    % All persons must know spider/possible con
                  cases(Sfriends, [], _), !.          % Generate lists of possible cons

knows2(X, Y)   :- knows(X, Y); knows(Y, X).           % Check if two people knows each other 
gtFriends(P,C) :- setof(X, knows2(P, X), C).          % Get all friends of a person 
knowsSome1(X, List) :- member(Y, List),knows2(X, Y),!.% Check if X knows anyone in List

allConnected([], _) :- !.
allConnected([H|T], List) :-                          % True if everyone in first list knows 
                  knowsSome1(H, List), !,             % at least someone in other list
                  allConnected(T, List).

cases([], Res, Res).
cases([P|Tail], K, Res) :-                            % Case1: Set first element as conspirator 
                  not(knowsSome1(P, K)),              % Person, can't know any cons in K
                  gtFriends(P, Friends),              % Get friends of P
                  subtract(Tail, Friends, T1),        % Remove from possible cons (Tail)
                  check(T1, [P|K]),                   % Check all not in P and K knows someone in P or K
                  cases(T1, [P|K], Res).
cases([_|T], P, Res) :-                               % Case2: Set first element as person   
                  check(T, P),  
                  cases(T, P, Res). 

check(P, K) :-    setof(X, person(X), All),
                  append(P, K, PnK),
                  subtract(All, PnK, Others),
                  allConnected(Others, PnK).