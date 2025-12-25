# Créé par ENT, le 02/10/2023 en Python 3.7

import pygame
from player import Player
from dialog import DialogBox
from map import MapManager

import os

# Définir le répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Game:
    def __init__(self):
        """
        Initialise le jeu en créant la fenêtre, le joueur, le gestionnaire de carte et la boîte de dialogue.

        :return: None
        """
        self.reset_game()

    def reset_game(self):
        """
        Réinitialise le jeu en recréant la fenêtre, le joueur, le gestionnaire de carte et la boîte de dialogue.

        :return: None
        """
        # Pour créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 600)) # taille de la fenêtre
        pygame.display.set_caption("Dungeon et Donjon")


        # Générer un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self, self.player)
        self.dialog_box = DialogBox()

        # Créer une police et un texte de bienvenue
        font_path = os.path.join(BASE_DIR, 'dialogs', 'dialog_font.ttf')
        self.font = pygame.font.Font(font_path, 12)
        self.texte_bienvenue = self.font.render(
            "Bienvenue dans Dungeon et Donjon ! Appuyez sur {espace} pour déclencher un dialogue.", True,
            (255, 255, 255))
        self.texte_bienvenue2 = self.font.render(
            "Utilisez les touches directionnelles pour vous déplacer", True, (255, 255, 255))

        # Charger la musique
        music_path = os.path.join(BASE_DIR, 'lost_woods.mp3')
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            # Jouer la musique
            pygame.mixer.music.play(-1)
            # Régler le volume
            pygame.mixer.music.set_volume(0.05)
        else:
            print(f"Avertissement : fichier musique non trouvé : {music_path}")


    def handle_input(self):
        """
        Gère les entrées du joueur en vérifiant les touches enfoncées et en déplaçant le joueur en conséquence.

        :return: None
        """
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self):
        """
        Met à jour le gestionnaire de carte.

        :return: None
        """
        self.map_manager.update()


    def run(self):
        """
        Exécute le jeu en affichant un message de bienvenue, en gérant les entrées du joueur, en mettant à jour le jeu et en dessinant la carte.

        :return: None

        >>> game = Game()
        >>> game.run()  # Ceci exécutera le jeu
        """

        clock = pygame.time.Clock() # Fixe le nombre de fps à chaque boucle

        # Afficher un message de bienvenue
        self.screen.blit(self.texte_bienvenue, (40, 300))  # Positionner le texte au centre de l'écran
        self.screen.blit(self.texte_bienvenue2, (175, 350))  # Positionner le deuxième texte juste en dessous du premier
        pygame.display.flip()  # Actualiser l'écran
        pygame.time.wait(5000)  # Attendre 5 secondes

        # Boucle du jeu, pour pas que la fenêtre se ferme instantanément
        jouer = True

        while jouer:

            self.player.save_location()
            self.handle_input()
            self.update() # Actualisation du groupe
            self.map_manager.draw() # Centrer caméra sur joueur + Dessiner les calques sur l'écran
            self.dialog_box.render(self.screen)
            pygame.display.flip() # Actualiser en temps réel

            for event in pygame.event.get(): #Liste tous les événements qui peuvent survenir avec pygame
                if event.type == pygame.QUIT: # Si le joueur a tenté de fermer la fenêtre
                    jouer = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)

            clock.tick(60) # Définir 60 images par seconde


        pygame.quit()
        # Arrêter la musique lorsque le jeu est terminé
        pygame.mixer.music.stop()

if __name__ == "__main__":
    import doctest
    doctest.testmod()



