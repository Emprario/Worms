"""
Moteur de jeu - Gestion des interfaces pygame
Ce module devra s'occuper de plusieurs tâches :
    - Gestion de l'affichage graphique + Interface Utilisateur
    - Gestion de l'interface avec pygame (events I/O)
"""
from pygame.sprite import Sprite


class GameEngine:
    """Affichage Graphique / Interface Utilisateur / Interface PyGame"""

    def __init__(self):
        """Valeur de Base + Initialisation'"""
        pass

    def update_sprites(self, sprites: list[Sprite]):
        """
        Affichage des sprite (dans la boucle principale du jeu)
        Utilise la méthode interne des sprites pour l'affichage graphique : pg_blit
        :param sprites: liste des sprites à afficher
        """
        pass

    def display_menu(self):
        """Affichage du menu principal"""
        pass

    def game_over(self):
        """Affiche un menu à la fin de la partie"""
        pass

    def events(self):
        """Gestion des events pygame (ce n'est pas la boucle principale)"""
        pass


class MaitreDuJeu:
    """Se charge de la gestion du gameplay"""
    pass
