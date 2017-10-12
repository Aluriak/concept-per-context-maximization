
% Number of object and attribute
#const nobj=4.
#const natt=4.

% Objects and attributes themselves.
obj(1..nobj).
att(1..natt).

% Choose a subset of edges, minimize it.
1 {edge(X,Y): obj(X), att(Y) } nobj*natt.
nb_edge(E):- E={edge(_,_)}.
#maximize{E@2: nb_edge(E)}.

% Register each edge in python side.
% do(@accumulate(X,Y)):- edge(X,Y).

% Compute the score in python side, and maximize it.
% nb_concept(@compute_concept_number()).
% #maximize{S@S,1: nb_concept(S)}.


#show.
#show nb_concept/1.
#show nb_edge/1.


#script (python)
from main import main
#end.
