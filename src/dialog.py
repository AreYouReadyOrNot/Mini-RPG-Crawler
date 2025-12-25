import pygame
import os

# Définir le répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DialogBox:
    """
    Classe DialogBox qui gère l'arrière-plan de la boîte de dialogue.

    :return: None

    >>> dialog_box = DialogBox()
    """

    X_POSITION = 60
    Y_POSITION = 470

    def __init__(self):
        """
        Initialise la boîte de dialogue.

        :return: None

        >>> dialog_box = DialogBox()  # Ceci initialisera la boîte de dialogue
        """
        dialog_box_path = os.path.join(BASE_DIR, 'dialogs', 'dialog_box.png')
        self.box = pygame.image.load(dialog_box_path)
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        font_path = os.path.join(BASE_DIR, 'dialogs', 'dialog_font.ttf')
        self.font = pygame.font.Font(font_path, 18)
        self.reading = False

    def execute(self, dialogs=[], npcs=[]):
        """
        Exécute une série de dialogues.

        :param dialogs: (list) La liste des dialogues à exécuter.
        :param npcs: (list) La liste des NPCs associés aux dialogues.
        :return: None
        :CU: type(dialogs) == list and type(npcs) == list

        >>> dialog_box.execute(["Bonjour", "Comment ça va ?"], [npc1, npc2])  # Ceci exécutera une série de dialogues avec les NPCs donnés
        """
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.dialogs = dialogs
            self.npcs = npcs
            self.current_dialog = 0
            self.texts = self.dialogs[self.current_dialog]
            self.npc = self.npcs[self.current_dialog]

    def render(self, screen):
        """
        Dessine la boîte de dialogue sur l'écran.

        :param screen: (pygame.Surface) L'écran sur lequel dessiner la boîte de dialogue.
        :return: None
        :CU: isinstance(screen, pygame.Surface)

        >>> dialog_box.render(screen)  # Ceci dessinera la boîte de dialogue sur l'écran
        """
        # Vérification : si pas de dialogues en cours, ne rien faire
        if not self.reading or not self.texts:
            return
        
        self.letter_index += 1

        # Récupérer le texte actuel (une chaîne)
        current_text = self.texts[self.text_index]

        # Si on a affiché toutes les lettres du texte actuel
        if self.letter_index >= len(current_text):
            self.letter_index = 0
            self.text_index += 1

            # Si on a affiché tous les textes du dialogue actuel
            if self.text_index >= len(self.texts):
                self.text_index = 0
                self.current_dialog += 1

                # Si on a affiché tous les dialogues
                if self.current_dialog >= len(self.dialogs):
                    self.reading = False
                    return  # Sortir si les dialogues sont terminés
                else:
                    self.texts = self.dialogs[self.current_dialog]
                    self.npc = self.npcs[self.current_dialog]

        # Dessiner la boîte et le texte
        screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
        current_text = self.texts[self.text_index]
        text = self.font.render(current_text[0:self.letter_index], False, (0, 0, 0))
        screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 30))

    def next_text(self):
        """
        Passe au texte suivant dans la boîte de dialogue.

        :return: None

        >>> dialog_box.next_text()  # Ceci passera au texte suivant dans la boîte de dialogue
        """
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            # Pour fermer le dialogue
            self.reading = False

if __name__ == "__main__":
    import doctest
    doctest.testmod()


