# Comment gérer les maps dans Worms ?

Worms est jeu de destruction de terrain (du moins, on peut facilement résumer ce jeu comme ça). De fait, on peut se 
demander comment peut-on alors afficher des maps qui ont du sens, qui peuvent être manipulé en permettant d'ajouter
simplement des cratères d'explosion (qui n'ont rien d'être des formes simples). Pour ce faire, on va procéder par des
triangles ! 

Méthode de construction des maps.

* En effet, tout polygone peut être décomposé en triangle. Ainsi, on va dessiner des maps sous forme vectorielle (une suite
de points) en définissant en plus un intérieur et un extérieur. 
* Au chargement des maps, l'objet Map découpera la Map en triangle relativement uniforme (des combos de triangles 
rectangles au centre) et des triangles (encore rectangles) mais irrégulié sur les bords.
* Maitenant, on se retrouve avec une grille de "pixels" avec chacun comme position d'affichage de l'angle rectangle. On 
notera cependant que pour les calculs, on se positionnera au centre du triangle.
* Maintenant une modification du terrain (destruction du terrain) revient à définir un rayon d'action dans lequel, les 
triangles compris dedans se désintégerons. Modifiant ansi la structure du terrain.