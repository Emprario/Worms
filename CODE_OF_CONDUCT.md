# Code Of Conduct - Usages

Ce fichier contient plusieurs notes sur comment collaborer à beaucoup sur un prpjet.
Merci de prendre ces notes en compte et de les appliquer afin de pouvoir s'y retrouver.
Cela concerne essentiellement les typages en pythons et d'autres notes concernant l'environement IDE et python.

## Typages en pythons

Premièrement afin de faciliter la lisibilté d'un code, python introduit des moyens mettre des types sur des variables.
Bien que l'interpréteur n'introduiera pas d'erreur à l'execution d'un code qui ne suiverait pas ces indications,
l'IDE affichera bien des avertissements concernant le type de variable ce qui est très utile pour la relecture.
Cela permet de voire du premier coup d'oeil où il y a un problème (exemple un string d'un nombre est fourni et non un
int)

Exemple :

```python
VERSION: str = "alpha"
TFIDF: dict[str, dict[str, float]] = {"Nomination_chirac": {"bonjour": 0.2, "la": 0.2, "france": 0.6}}
```

*Ici `VERSION` est un string et `TFIDF` est une matrice TF-IDF composé d'un dictionnaire de string en clée avec pour
valeur un autre dictionnaire avec en clée un string et en valeur un nombre flottant.*

### Typages des types simples

Pour typer une variable il de procéder ainsi `nom_de_la_variable: type = valeur`.

Avec `type` un type de base (`int, float, str, bool, ...`) ou un type construit (`list, tuple, set, dict`).

Exemple :

```python
string: str = "Hello World!"
tab: list = [0, 1, 2]
resultat: int = None
VRAI: bool = True
```

**NB1: Il n'est en réalité uniquement conseillé d'annoter ainsi des variables uniquement pour les constantes. Ici
uniquement la constante `VRAI` (en majuscule les constantes) aurait du être typé simplement.**

*NB2: On peut également la valeur `None` (null) à une variable à sa déclaration si on ne veut pas confondre la variable
non initialisé avec celle juste vide. Ici par exemple résultat a été affecté à None afin de ne confondre avec un autre
nombre qui aurait pu être un résultat valide.*

### Typages des types construits linéaires (`list`, `tuple`, `set`)

Pour typer plus précisment des types linéaires avec par exemple le type qui va être contenu dans le type,
on peut utiliser deux syntaxes :

- `nom_de_variable:type_var[type_contenue] = valeur` avec la variable qui contient un certain nombre (inconnu) (au moins
  une) de valeur de ce type et toujours le même type
- `nom_de_variable:type_var[type_a|type_b|type_c] = [a,b,c]` avec le tableau qui contient toujours 3 valeurs de type
  `type_a` puis `type_b` puis `type_c`

Exemple :

```python
tab_triee: list[int] = [-21, -7, 0, 7, 14, 23, 137]
bools: tuple[bool, bool] = (True, False)
campus: set[list[str | int]] = {["La Factory", 3], ["La Maison", -1], ["New Republique", 10]} 
```

*NB: Comme il est possible de l'observer la syntaxe du typage du tuple est différente car ce dernier est censée être un
type construit immuable donc la place des éléments est "plus importantes" et "a le droit" d'être hétérogène et sa taille
est normalement fixe, d'où le fait de citer le type de tout ses éléments.*

### Typage des dictionnaires (`dict`)

La synatxe du dictionnaire est plutôt simple elle est la suivante : `nom_de_variable:dict[type_cle,type_valeur]`.

Exemple : cf la matrice TF-IDF au-dessus.

### Typages des fonctions

On peut également (**ET ON DOIT SYSTEMATIQUEMENT**) typer des fonctions afin de comprendres les entrées et les sorties.
On notera que les fonctions en elle-même n'ont pas de type (sûrement pas le type `function`).

Syntaxe :`def function(param1: type, param2: type) -> type:`

Exemple

```python
def somme(tab: list[int]) -> int:
    sum = 0
    for element in tab:
        sum += element
    return sum
```

## Description des fonctions (docstring)

Il n'y a pas de format de description générale en python, chacun y vas un peu de sa sauce, voici celui qui sera le
nôtre :

```python
def somme(tab: list[int]) -> int:
    """
    Fait une somme
    :param tab: Tableau d'élément à sommer
    :return: La somme
    """
    sum = 0
    for element in tab:
        sum += element
    return sum
```

*NB: On notera que l'on essayera (bien que cela n'est pas toujours possible) de ne pas répéter la signature de la
fonction.*

## Indications globales

* Ajouter un docstring précisant le contenu du module.
* Mettre des commentaires de temps en temps.
* Ne pas hésiter à mettre des fichiers de documentations à des emplacements critiques (par exemple pour expliquer
  comment fonctionne les .map).
* Utiliser si possible Pycharm pour avoir une mise en forme uniforme.
* Merci de mettre en forme régulièrement (au moins avant de commit) avec `Ctrl+Alt+L` (Pycharm) le fichier traité.
* Faire des commits isolés (un commit pour chaque fonction modifié) sinon vous risquez de vous retrouver avec un merge
conflict.
* Have fun!

## Références pour appronfondir

* Typing : https://docs.python.org/fr/3.12/library/typing.html
* PEP 585 - Type Hinting Generics In Standard Collections : https://peps.python.org/pep-0585/
* PEP 484 - Type Hints : https://peps.python.org/pep-0484/
* PEP 257 - Docstring Conventions : https://peps.python.org/pep-0257/
* Avec JetBrains : https://www.jetbrains.com/help/pycharm/type-hinting-in-product.html
* Pourquoi on met Union sur les listes et Virgule sur les tuples ? :
  https://stackoverflow.com/questions/53526516/why-cant-list-contain-multiple-types