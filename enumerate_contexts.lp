% Number of object and attribute
#const nobj=4.
#const natt=4.

% Objects and attributes themselves.
obj(1..nobj).
att(1..natt).

% Choose a subset of edges, minimize it.
1 {rel(X,Y): obj(X), att(Y) } nobj*natt.

#show.
#show rel/2.
