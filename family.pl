% Base facts (initially empty for dynamic updates)
:- dynamic parent/2.
:- dynamic male/1.
:- dynamic female/1.

% Rules for relationships
father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandfather(X, Y) :- grandparent(X, Y), male(X).
grandmother(X, Y) :- grandparent(X, Y), female(X).
child(X, Y) :- parent(Y, X).
daughter(X, Y) :- child(X, Y), female(X).
son(X, Y) :- child(X, Y), male(X).
uncle(X, Y) :- sibling(X, P), parent(P, Y), male(X).
aunt(X, Y) :- sibling(X, P), parent(P, Y), female(X).
relatives(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

% Constraints to enforce real-world logic
:- parent(X, X).  % A person cannot be their own parent.
:- father(X, Y), female(X).  % A father must be male.
:- mother(X, Y), male(X).  % A mother must be female.
:- parent(X, Y), parent(Y, X).  % Parent-child relationships cannot form a loop.
:- male(X), female(X).  % A person cannot be both male and female.

% Intelligent inferences
% If A is the parent of B and B is the parent of C, then A is the grandparent of C.
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% If X is the father of Y, then X is male (automatic inference).
male(X) :- father(X, _).

% If X is the mother of Y, then X is female (automatic inference).
female(X) :- mother(X, _).

% If A is the parent of B, and B is a parent of C, infer A is a grandparent of C.
grandparent(A, C) :- parent(A, B), parent(B, C).
