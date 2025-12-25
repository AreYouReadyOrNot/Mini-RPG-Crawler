# RPG Crawler

Un petit jeu RPG en Python utilisant Pygame avec dialogues, combats, et déplacement sur une carte.

## 🎮 Fonctionnalités

- **Déplacement** : Utilisez les touches directionnelles pour vous déplacer
- **Dialogues** : Interagissez avec les NPCs en appuyant sur ESPACE
- **Combats** : Affrontez les ennemis dans des combats au tour par tour
- **Musique** : Ambiance sonore avec "Lost Woods"
- **Multiple Cartes** : Explorez différents mondes (world, dungeon, dungeon_2)

## 📋 Prérequis

- Python 3.7+
- pygame
- pytmx
- pyscroll

## 🚀 Installation

1. Clone le dépôt :
git clone https://github.com/AreYouReadyOrNot/Mini-RPG-Crawler.git
cd RPG-Crawler
2. Installe les dépendances :
pip install pygame pytmx pyscroll
3. Lance le jeu :
cd src
python main.py
## 🎮 Commandes

- **Flèches directionnelles** : Déplacer le joueur
- **ESPACE** : Interagir avec les NPCs

## 📁 Structure du projet
RPG-Crawler/
├── src/
│ ├── main.py # Point d'entrée du jeu
│ ├── game.py # Classe principale du jeu
│ ├── map.py # Gestion des cartes
│ ├── player.py # Classes Entity, Player, NPC
│ ├── combat.py # Système de combat
│ ├── dialog.py # Gestion des dialogues
│ └── animation.py # Gestion des animations
├── sprites/ # Images des personnages
├── map/ # Fichiers TMX des cartes
├── dialogs/ # Images et polices des dialogues
├── lost_woods.mp3 # Musique de fond
└── README.md # Ce fichier

## 🤝 Auteur

Walid Bouknia - AreYouReadyOrNot