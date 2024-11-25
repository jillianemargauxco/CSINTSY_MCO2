:- dynamic parent/2.
:- dynamic male/1.
:- dynamic female/1.
:- dynamic father/2.
:- dynamic mother/2.
:- dynamic child/2.
:- dynamic sibling/2.
:- dynamic daughter/2.
:- dynamic son/2.
:- dynamic sister/2.
:- dynamic brother/2.
:- dynamic grandparent/2.
:- dynamic grandfather/2.
:- dynamic grandmother/2.
:- dynamic uncle/2.
:- dynamic aunt/2.
:- dynamic relatives/2.


father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).
child(X, Y) :- parent(Y, X).

sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.
sister(X, Y) :- sibling(X, Y), female(X).
brother(X, Y) :- sibling(X, Y), male(X).

daughter(X, Y) :- child(X, Y), female(X).
son(X, Y) :- child(X, Y), male(X).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandfather(X, Y) :- grandparent(X, Y), male(X).
grandmother(X, Y) :- grandparent(X, Y), female(X).

uncle(X, Y) :- sibling(X, P), parent(P, Y), male(X).
aunt(X, Y) :- sibling(X, P), parent(P, Y), female(X).

relatives(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

relatives(X, Y) :- parent(X, Y).         
relatives(X, Y) :- parent(Y, X).              
relatives(X, Y) :- sibling(X, Y).  

relatives(X, Y) :- grandparent(X, Y).          
relatives(X, Y) :- grandparent(Y, X).          
relatives(X, Y) :- uncle(X, Y).                
relatives(X, Y) :- aunt(X, Y).                
relatives(X, Y) :- uncle(Y, X).             
relatives(X, Y) :- aunt(Y, X).                 

relatives(X, Y) :- parent(X, Y).
relatives(X, Y) :- parent(Y, X).
relatives(X, Y) :- sibling(X, Y).

relatives(X, Y) :- daughter(X, Y).             
relatives(X, Y) :- son(X, Y).                   
relatives(X, Y) :- sister(X, Y).                
relatives(X, Y) :- brother(X, Y).               

relatives(X, Y) :- mother(X, Y).                
relatives(X, Y) :- father(X, Y).               

relatives(X, Y) :- grandfather(X, Y).          
relatives(X, Y) :- grandmother(X, Y).  

relatives(X, Y) :- parent(Z, X), relatives(Z, Y).
relatives(X, Y) :- parent(Z, Y), relatives(Z, X).

        


