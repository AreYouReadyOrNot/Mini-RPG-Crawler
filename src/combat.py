import pygame
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Combat:
    """
    Classe Combat qui gère les combats entre le joueur et un NPC.

    :param player: (Player) Le joueur du jeu.
    :param npc: (NPC) Le NPC avec lequel le joueur combat.
    :param screen: (pygame.Surface) L'écran sur lequel dessiner le combat.
    :param game: (Game) Le jeu auquel appartient le combat.
    :return: None
    :CU: isinstance(player, Player) and isinstance(npc, NPC) and isinstance(screen, pygame.Surface) and isinstance(game, Game)

    >>> combat = Combat(player, npc, screen, game)  # Ceci créera un nouveau combat entre le joueur et le NPC donnés
    """
    def __init__(self, player, npc, screen, game):
        """
        Initialise le combat entre le joueur et le NPC.

        :param player: (Player) Le joueur du jeu.
        :param npc: (NPC) Le NPC avec lequel le joueur combat.
        :param screen: (pygame.Surface) L'écran sur lequel dessiner le combat.
        :param game: (Game) Le jeu auquel appartient le combat.
        :return: None
        :CU: isinstance(player, Player) and isinstance(npc, NPC) and isinstance(screen, pygame.Surface) and isinstance(game, Game)

        >>> combat = Combat(player, npc, screen, game)  # Ceci initialisera le combat entre le joueur et le NPC
        """
        self.player = player
        self.npc = npc
        self.screen = screen
        self.game = game
        self.turn = 0  # 0 pour le tour du joueur, 1 pour le tour du PNJ


    def player_attack(self):
        """
        Fait attaquer le joueur le NPC.

        :return: None

        >>> combat.player_attack()  # Ceci fera attaquer le joueur le NPC
        """

        damage = self.player.attack_strength
        self.npc.hp -= damage
        print(f"Vous avez infligé {damage} points de dégâts au {self.npc.name} !")
        if self.npc.hp <= 0:
                print(f"Vous avez vaincu le {self.npc.name} !")

    def npc_attack(self):
        """
        Fait attaquer le NPC le joueur.

        :return: None

        >>> combat.npc_attack()  # Ceci fera attaquer le NPC le joueur
        """
        damage = self.npc.attack_strength
        self.player.hp -= damage
        print(f"Le {self.npc.name} vous a infligé {damage} points de dégâts !")
        if self.player.hp <= 0:
            print(f"Vous avez été vaincu par le {self.npc.name} !")

    def run(self):
        """
        Exécute le combat en alternant les tours entre le joueur et le NPC.

        :return: None

        >>> combat.run()  # Ceci exécutera le combat
        """
        while self.player.hp > 0 and self.npc.hp > 0:
            if self.turn == 0:
                self.player_attack()
                self.turn = 1
            else:
                self.npc_attack()
                self.turn = 0

        if self.player.hp <= 0:
            # Créer un écran noir
            black_screen = pygame.Surface(self.screen.get_size())
            black_screen.fill((0, 0, 0))  # Remplir l'écran de noir

            # Créer le message "Vous êtes mort"
            font_path = os.path.join(BASE_DIR, 'dialogs', 'dialog_font.ttf')
            font = pygame.font.Font(font_path, 36)  # Choisir la police et la taille du texte
            text = font.render("Vous êtes mort", True, (255, 255, 255))  # Créer le texte

            # Positionner le texte au centre de l'écran
            text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

            # Dessiner l'écran noir et le texte
            self.screen.blit(black_screen, (0, 0))
            self.screen.blit(text, text_rect)

            # Mettre à jour l'affichage
            pygame.display.flip()

            # Attendre 3 secondes avant de réinitialiser la partie
            pygame.time.wait(3000)

            # Réinitialiser la partie
            self.game.reset_game()
        elif self.npc.hp <= 0:
            print(f"{self.npc.name} a perdu")
            # Supprimer le PNJ de la carte
            self.npc.kill()

if __name__ == "__main__":
    import doctest
    doctest.testmod()


