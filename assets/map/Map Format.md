# Format de la map

On remplacera les expressions entre `{`accolade`}` et exclura les commentaire en `//` 

Description de la map : `{numéro de la map}.map`
```
DIMENSIONS
{longueur} {largeur}
STARTSTOP // figure 1
{point.x} {point.y}
{point.x} {point.y}
{point.x} {point.y}
{point.x} {point.y}
{point.x} {point.y}
{point.x} {point.y}
STARTSTOP // figure 2
{point.x} {point.y}
{point.x} {point.y}
{point.x} {point.y}
...
{point.x} {point.y}
{point.x} {point.y}
{point.x} {point.y}

...

STARTSTOP // figure n
{point.x} {point.y}
{point.x} {point.y}
{point.x} {point.y}
...
{point.x} {point.y}
{point.x} {point.y}
{point.x} {point.y}
TEXTUREPATH
{path depuis la root du projet pour la texture}
```
**NB:**
* Pas de retour à la ligne en fin de fichier.
* Les descripteurs ne peuvent ne pas être ordonnés de la même manière
* Il peut y avoir plusieurs STARTSTOP mais qu'un seul exemplaire de
  * DIMENSIONS
  * TEXTUREPATH
* Il n'y a pas de TEXTUREPATH vide (sans coordonnée) ou avec moins de 3 coordonnées
* On peut également palcer un `notprovided` dans TEXTUREPATH pour afficher la couleur uni de debug
* On doit initialiser les dimensions avant de poser des coordonnées
* La map ne doit pas avoir deux points qui sont distants de seulement un espace 1 à 5 pixels