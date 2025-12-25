from dataclasses import dataclass
import pygame, pytmx, pyscroll

from player import NPC
from combat import Combat

import os

# Définir le répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class Portal:
    """
    Classe Portal qui gère les portails pour déplacer le joueur d'une carte à l'autre.

    :param from_world: (str) Le nom du monde d'origine du portail.
    :param origin_point: (str) Le point d'origine du portail.
    :param target_world: (str) Le nom du monde cible du portail.
    :param teleport_point: (str) Le point de téléportation du portail.
    :return: None
    :CU: type(from_world) == str and type(origin_point) == str and type(target_world) == str and type(teleport_point) == str

    >>> portal = Portal(from_world="world", origin_point="enter_dungeon", target_world="dungeon", teleport_point="spawn_dungeon")  # Ceci créera un nouveau portail de "world" à "dungeon"
    """
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass # Pour initialiser la classe automatiquement
class Map:
    """
    Classe Map qui représente une carte du jeu.

    :param name: (str) Le nom de la carte.
    :param walls: (list) La liste des murs de la carte.
    :param group: (pyscroll.PyscrollGroup) Le groupe de la carte.
    :param tmx_data: (pytmx.TiledMap) Les données tmx de la carte.
    :param portals: (list) La liste des portails de la carte.
    :param npcs: (list) La liste des NPCs de la carte.
    :return: None
    :CU: type(name) == str and type(walls) == list and isinstance(group, pyscroll.PyscrollGroup) and isinstance(tmx_data, pytmx.TiledMap) and type(portals) == list and type(npcs) == list

    >>> map = Map(name="world", walls=[], group=pyscroll.PyscrollGroup(), tmx_data=pytmx.TiledMap(), portals=[], npcs=[])  # Ceci créera une nouvelle carte nommée "world" sans murs, portails ou NPCs
    """
    name: str # type du nom de la map
    walls: list[pygame.Rect] # collisions avec le joueur
    group: pyscroll.PyscrollGroup # Assembler toutes les tuiles de notre jeu
    tmx_data: pytmx.TiledMap    # Recuperer objets depuis la carte
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:
    """
    Classe MapManager qui gère les cartes du jeu.

    :param screen: (pygame.Surface) L'écran sur lequel dessiner les cartes.
    :param game: (Game) Le jeu auquel appartient le gestionnaire de cartes.
    :param player: (Player) Le joueur du jeu.
    :return: None
    :CU: isinstance(screen, pygame.Surface) and isinstance(game, Game) and isinstance(player, Player)

    >>> map_manager = MapManager(screen, game, player)  # Ceci créera un nouveau gestionnaire de cartes pour l'écran, le jeu et le joueur donnés
    """

    def __init__(self, screen, game,  player):
        """
        Initialise le gestionnaire de cartes en enregistrant les cartes et en téléportant le joueur et les NPCs.

        :param screen: (pygame.Surface) L'écran sur lequel dessiner les cartes.
        :param game: (Game) Le jeu auquel appartient le gestionnaire de cartes.
        :param player: (Player) Le joueur du jeu.
        :return: None
        :CU: isinstance(screen, pygame.Surface) and isinstance(game, Game) and isinstance(player, Player)

        >>> map_manager = MapManager(screen, game, player)  # Ceci initialisera le gestionnaire de cartes, enregistrera les cartes et téléportera le joueur et les NPCs
        """
        self.maps = dict() # "dungeon" -> Map("dungeon", walls, group) -> directement accéder aux données d'une map
        self.screen = screen
        self.game = game
        self.player = player
        self.current_map = "world"

        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_dungeon", target_world="dungeon", teleport_point="spawn_dungeon")
        ], npcs=[
            NPC("mushroom", nb_points=4, dialog=["Je te souhaite une excellente aventure   ", "Les cours de NSI sont les meilleurs !!!   ", "Dédicace au meilleur graphiste : Karl   ", " Bye !   "]),
        ])
        self.register_map("dungeon", portals=[
            Portal(from_world="dungeon", origin_point="exit_dungeon", target_world="world", teleport_point="enter_dungeon_exit"),
            Portal(from_world="dungeon", origin_point="enter_dungeon_2", target_world="dungeon_2", teleport_point="spawn_dungeon_2")
        ], npcs=[
            NPC("bandit", nb_points=1, dialog=["hihihi   ", "Je vais te saccager de la tête aux pieds   "]),
            NPC("wizard", nb_points=1, dialog=["ZAAAaaAAAP   ","Je suis le côté obscur du magicien d'Oz   "]),
            NPC("knight", nb_points=1, dialog=["Mwahahah je suis le plus fort du moonde !!   ", "Nonobstant les cours de NSI sont les meilleurs   ", "Maintenant c'est l'heure du combat !!!   "])
        ])
        self.register_map("dungeon_2", portals=[
            Portal(from_world="dungeon_2", origin_point="exit_dungeon_2", target_world="dungeon", teleport_point="enter_dungeon_2_exit")
        ])

        self.teleport_player("player")
        self.teleport_npcs()


    def check_npc_collisions(self, dialog_box):
        """
        Vérifie les collisions entre le joueur et les NPCs et déclenche un combat si nécessaire.

        :param dialog_box: (DialogBox) La boîte de dialogue à utiliser pour afficher les dialogues.
        :return: None
        :CU: isinstance(dialog_box, DialogBox)

        >>> map_manager.check_npc_collisions(dialog_box)  # Ceci vérifiera les collisions entre le joueur et les NPCs et déclenchera un combat si nécessaire
        """
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                # Lancer les dialogues
                dialog_box.execute([sprite.dialog], [sprite])

                # Attendre que tous les dialogues soient affichés
                while dialog_box.reading:
                    dialog_box.render(self.screen)
                    pygame.display.flip()  # Mettre à jour l'affichage
                    pygame.time.delay(40)  # Petit délai pour ne pas surcharger le CPU

                # UNE FOIS les dialogues terminés, lancer le combat
                combat = Combat(self.player, sprite, self.screen, self.game)
                combat.run()


    def check_collisions(self):
        """
        Vérifie les collisions entre le joueur et les NPCs et déclenche un combat si nécessaire.

        :return: None

        >>> map_manager.check_collisions()  # Ceci vérifiera les collisions entre le joueur et les NPCs et déclenchera un combat si nécessaire
        """
        # portails et leurs déclenchements
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect): #si les pieds du joueurs rentrent en collision avec ce ractangle
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)



        # collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        """
        Téléporte le joueur à un point spécifique.

        :param name: (str) Le nom de l'objet à partir duquel obtenir les coordonnées de téléportation.
        :return: None
        :CU: type(name) == str

        >>> map_manager.teleport_player("player")  # Ceci téléportera le joueur à l'objet nommé "player"
        """
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()  # Eviter problematique de tp avec colllision


    def register_map(self, name, portals=[], npcs=[]):
        """
        Enregistre une carte dans le gestionnaire de cartes.

        :param name: (str) Le nom de la carte à enregistrer.
        :param portals: (list) La liste des portails de la carte.
        :param npcs: (list) La liste des NPCs de la carte.
        :return: None
        :CU: type(name) == str and type(portals) == list and type(npcs) == list

        >>> map_manager.register_map("world", portals=[Portal(from_world="world", origin_point="enter_dungeon", target_world="dungeon", teleport_point="spawn_dungeon")], npcs=[NPC("mushroom", 4, ["Je te souhaite une excellente aventure", "Les cours de NSI sont les meilleurs", "Dédicace au meilleur graphiste : Karl", " Bye !"])])  # Ceci enregistrera une carte nommée "world" avec un portail et un NPC
        """
        # Charger la carte sous format tmx
        map_path = os.path.join(BASE_DIR, 'map', f'{name}.tmx')
        tmx_data = pytmx.util_pygame.load_pygame(map_path)  # Pour spécifier le bon fichier tmx contenant notre carte
        map_data = pyscroll.data.TiledMapData(tmx_data)  # Extraire la carte
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())  # Va contenir tous les calques de la map regroupés
                                                                                            # + parametre self.ecran permettent de choisir sur quelle surface dessiner la map
        map_layer.zoom = 3  # zoomer en X fois plus gros

        # définir une liste qui va stocker les rectangles de collision
        walls = []

        for object in tmx_data.objects:
            if object.type == "collision":
                walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        # Dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)  # default_layer permet de donner la position du calque par défaut
        group.add(self.player)

        # recuperer tous les npc pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # Enregistrer la nouvelle carte chargée
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        """
        Récupère la carte actuelle.

        :return: (Map) La carte actuelle.

        >>> current_map = map_manager.get_map()  # Ceci récupérera la carte actuelle
        """
        return self.maps[self.current_map]

    def get_group(self):
        """
        Récupère les murs de la carte actuelle.

        :return: (list) Les murs de la carte actuelle.

        >>> walls = map_manager.get_walls()  # Ceci récupérera les murs de la carte actuelle
        """
        return self.get_map().group

    def get_walls(self):
        """
        Récupère les murs de la carte actuelle.

        :return: (list) Les murs de la carte actuelle.

        >>> walls = map_manager.get_walls()  # Ceci récupérera les murs de la carte actuelle
        """
        return self.get_map().walls

    def get_object(self, name):
        """
        Récupère un objet de la carte actuelle par son nom.

        :param name: (str) Le nom de l'objet à récupérer.
        :return: (pytmx.TiledObject) L'objet récupéré.
        :CU: type(name) == str

        >>> object = map_manager.get_object("player")  # Ceci récupérera l'objet nommé "player" de la carte actuelle
        """
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        """
        Téléporte tous les NPCs à leurs points de spawn respectifs.

        :return: None

        >>> map_manager.teleport_npcs()  # Ceci téléportera tous les NPCs à leurs points de spawn respectifs
        """
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data) # Charger les points du npc par rapport à son monde
                npc.teleport_spawn()

    def draw(self):
        """
        Dessine la carte actuelle.

        :return: None

        >>> map_manager.draw()  # Ceci dessinera la carte actuelle
        """
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center) # Centrer sur le joueur

    def update(self):
        """
        Met à jour le groupe de la carte actuelle et vérifie les collisions.

        :return: None

        >>> map_manager.update()  # Ceci mettra à jour le groupe de la carte actuelle et vérifiera les collisions
        """
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()

if __name__ == "__main__":
    import doctest
    doctest.testmod()


