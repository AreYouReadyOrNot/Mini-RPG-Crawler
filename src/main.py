
##################### installer modules : pygame, pytmx et pyscroll ######################
import subprocess
import sys

def install(package):
    """
    Installe un package Python en utilisant pip.

    :param package: (str) Le nom du package à installer.
    :CU: type(package) == str

    >>> install('numpy')  # Ceci installera le package numpy
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Installer les packages nécessaires
install('pygame')
install('pyscroll')
install('pytmx')

import pygame
from game import Game


if __name__ == '__main__':
    """
    Point d'entrée principal du programme. Initialise pygame et lance le jeu.
    """
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
























