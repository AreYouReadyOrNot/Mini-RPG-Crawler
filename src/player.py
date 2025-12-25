

import pygame
from animation import AnimateSprite


class Entity(AnimateSprite):
    """
    Classe mère pour un élément non statique, hérite d'AnimateSprite.

    :param name: (str) Le nom de l'entité.
    :param x: (int) La position x initiale de l'entité.
    :param y: (int) La position y initiale de l'entité.
    :return: None
    :CU: type(name) == str and type(x) == int and type(y) == int

    >>> entity = Entity("player", 0, 0)  # Ceci créera une nouvelle entité avec le nom "player" et la position (0, 0)
    """

    def __init__(self, name, x, y):
        super().__init__(name) # On appelle la superclasse pour initialiser le sprite sans avoir à nommer la classe parente explicitement

        self.image = self.get_image(0, 0)
        self.image.set_alpha(255)
        self.rect = self.image.get_rect() # définir le rectangle qui est sa position
        self.position = [x, y]

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)
        self.old_position = self.position.copy()

    def save_location(self):
        """
        Enregistre la position actuelle de l'entité.

        :return: None

        >>> entity.save_location()  # Ceci enregistrera la position actuelle de l'entité
        """
        self.old_position = self.position.copy()


    def move_right(self):
        """
        Déplace l'entité vers la droite.

        :return: None

        >>> entity.move_right()  # Ceci déplacera l'entité vers la droite
        """
        self.change_animation("right")
        self.position[0] += self.speed # Se déplacer à droite


    def move_left(self):
        """
        Déplace l'entité vers la gauche.

        :return: None

        >>> entity.move_left()  # Ceci déplacera l'entité vers la gauche
        """
        self.change_animation("left")
        self.position[0] -= self.speed # Se déplacer à gauche

    def move_up(self):
        """
        Déplace l'entité vers le haut.

        :return: None

        >>> entity.move_up()  # Ceci déplacera l'entité vers le haut
        """
        self.change_animation("up")
        self.position[1] -= self.speed # Se déplacer en haut

    def move_down(self):
        """
        Déplace l'entité vers le bas.

        :return: None

        >>> entity.move_down()  # Ceci déplacera l'entité vers le bas
        """
        self.change_animation("down")
        self.position[1] += self.speed # Se déplacer en bas

    def update(self):
        """
        Met à jour la position de l'entité.

        :return: None

        >>> entity.update()  # Ceci mettra à jour la position de l'entité
        """
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """
        Déplace l'entité à sa position précédente.

        :return: None

        >>> entity.move_back()  # Ceci déplacera l'entité à sa position précédente
        """
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom




class Player(Entity):
    """
    Classe Player qui hérite de la classe Entity.

    :return: None

    >>> player = Player()  # Ceci créera un nouveau joueur
    """

    def __init__(self):
        super().__init__("player", 0, 0)
        self.attack_strength = 10
        self.hp = 100

class NPC(Entity):
    """
    Classe NPC qui hérite de la classe Entity.

    :param name: (str) Le nom du NPC.
    :param nb_points: (int) Le nombre de points du NPC.
    :param dialog: (list) La liste des dialogues du NPC.
    :return: None
    :CU: type(name) == str and type(nb_points) == int and type(dialog) == list

    >>> npc = NPC("mushroom", 4, ["Je te souhaite une excellente aventure", "Les cours de NSI sont les meilleurs", "Dédicace au meilleur graphiste : Karl", " Bye !"])  # Ceci créera un nouveau NPC avec le nom "mushroom", 4 points et une liste de dialogues
    """

    def __init__(self, name, nb_points, dialog):
            super().__init__(name, 0, 0)
            self.nb_points = nb_points
            self.dialog = dialog
            self.points = []   # points de notre chemin
            self.name = name # nom de notre entité
            self.speed = 1
            self.current_point = 0
            self.attack_strength = 7
            self.hp = 50



    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0


        current_rect = self.points[current_point] #rectangle surlequel se trouve les joueurs
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y  and abs(current_rect.x - target_rect.x) < 3: # pouvoir faire déplacement du pnj si rectangle est à peu près 3 pixels de différence
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3: # pouvoir faire déplacement du pnj si rectangle est à peu près 3 pixels de différence
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3: # pouvoir faire déplacement du pnj si rectangle est à peu près 3 pixels de différence
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3: # pouvoir faire déplacement du pnj si rectangle est à peu près 3 pixels de différence
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point # La position cible devient le nouveau point d'origine



    def teleport_spawn(self):
        """
        Téléporte le NPC à son point de spawn.

        :return: None

        >>> npc.teleport_spawn()  # Ceci téléportera le NPC à son point de spawn
        """
        location = self.points[self.current_point] # self.current_point équivaut a 0, cest le point actuel
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        """
        Charge les points du NPC à partir des données tmx.

        :param tmx_data: (pytmx.TiledMap) Les données tmx à partir desquelles charger les points.
        :return: None
        :CU: isinstance(tmx_data, pytmx.TiledMap)

        >>> npc.load_points(tmx_data)  # Ceci chargera les points du NPC à partir des données tmx
        """
        for numero in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{numero}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

if __name__ == "__main__":
    import doctest
    doctest.testmod()






