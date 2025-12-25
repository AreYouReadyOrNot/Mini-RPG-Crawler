import pygame
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class AnimateSprite(pygame.sprite.Sprite):
    """
    Classe AnimateSprite qui gère l'animation des sprites.

    :param name: (str) Le nom du sprite à animer.
    :return: None
    :CU: type(name) == str

    >>> animate_sprite = AnimateSprite("player")  # Ceci créera un nouveau sprite animé avec le nom "player"
    """
    def __init__(self, name):
        """
        Initialise le sprite animé.

        :param name: (str) Le nom du sprite à animer.
        :return: None
        :CU: type(name) == str

        >>> animate_sprite = AnimateSprite("player")  # Ceci initialisera le sprite animé avec le nom "player"
        """
        super().__init__() # Pour l'héritage
        self.sprite_sheet = pygame.image.load(os.path.join(SCRIPT_DIR, f'../sprites/{name}.png'))
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(97)
        }
        self.speed = 2

    def change_animation(self, name):
        """
        Change l'animation du sprite.

        :param name: (str) Le nom de l'animation à utiliser.
        :return: None
        :CU: type(name) == str

        >>> animate_sprite.change_animation("right")  # Ceci changera l'animation du sprite à "right"
        """
        self.image = self.images[name][self.animation_index]
        self.image.set_alpha(255) # Opacité maximale
        self.clock += self.speed * 8

        if self.clock >= 100:

            self.animation_index += 1 # passer à l'image suivante

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0
    def get_images(self, y):
        """
        Récupère les images pour l'animation du sprite.

        :param y: (int) La position y de l'image à récupérer.
        :return: (list) La liste des images récupérées.
        :CU: type(y) == int

        >>> images = animate_sprite.get_images(0)  # Ceci récupérera les images pour l'animation du sprite à la position y 0
        """
        images = []

        for i in range(0, 3):
            x = i*23
            image = self.get_image(x, y)
            images.append(image)

        return images

    def get_image(self, x, y):
        """
        Récupère une image pour l'animation du sprite.

        :param x: (int) La position x de l'image à récupérer.
        :param y: (int) La position y de l'image à récupérer.
        :return: (pygame.Surface) L'image récupérée.
        :CU: type(x) == int and type(y) == int

        >>> image = animate_sprite.get_image(0, 0)  # Ceci récupérera l'image pour l'animation du sprite à la position (0, 0)
        """
        image = pygame.Surface([23, 32], pygame.SRCALPHA)  # Taille en largeur et hauteur
        image.blit(self.sprite_sheet, (0, 0), (x, y, 23, 32))  # Extraire un morceau de sprite
                                                               # (0,0) -> distance par défaut
                                                               # (x, y, 22, 33) coordonnées + hauteur et largeur de l'image
        return image  # renvoie l'image qui a été découpée

if __name__ == "__main__":
    import doctest
    doctest.testmod()
