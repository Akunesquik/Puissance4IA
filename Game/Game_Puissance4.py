import numpy as np
import pygame


# Couleurs
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)

class Puissance4:
    def __init__(self, nb_lignes=6, nb_colonnes=7):
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.grid = np.zeros((nb_lignes, nb_colonnes), dtype=int)
        self.current_player = 1  # Joueur 1 commence
        self.moves = 0
        self.taillecase = 100
        self.rayon_jetons =  self.taillecase // 2 - 5

    def creation_fenetre(self):
        pygame.init()
        largeur_fenetre = self.nb_colonnes * self.taillecase
        hauteur_fenetre = (self.nb_lignes + 1) * self.taillecase
        # Création de la fenêtre
        fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        pygame.display.set_caption("Puissance 4")

        return fenetre
    
    def reset(self):
        self.grid = np.zeros((self.nb_lignes, self.nb_colonnes), dtype=int)
        self.current_player = 1
        self.moves = 0

    def make_move(self, colonne):
        for ligne in range(self.nb_lignes - 1, -1, -1):
            if self.grid[ligne][colonne] == 0:
                self.grid[ligne][colonne] = self.current_player
                self.moves += 1
                return True
        return False  # La colonne est pleine, le coup n'est pas valide

    def switch_player(self):
        self.current_player = 3 - self.current_player  # Alterner entre les joueurs 1 et 2

    def is_winner(self):
        for joueur in [1, 2]:
            for ligne in range(self.nb_lignes):
                for colonne in range(self.nb_colonnes - 3):
                    if np.all(self.grid[ligne, colonne:colonne+4] == joueur):
                        return joueur  # Le joueur a gagné horizontalement

            for colonne in range(self.nb_colonnes):
                for ligne in range(self.nb_lignes - 3):
                    if np.all(self.grid[ligne:ligne+4, colonne] == joueur):
                        return joueur  # Le joueur a gagné verticalement

            for colonne in range(self.nb_colonnes - 3):
                for ligne in range(3, self.nb_lignes):
                    if np.all(self.grid[ligne-3:ligne+1, colonne:colonne+4].diagonal() == joueur):
                        return joueur  # Le joueur a gagné en diagonale ascendante

            for colonne in range(self.nb_colonnes - 3):
                for ligne in range(self.nb_lignes - 3):
                    if np.all(np.fliplr(self.grid[ligne:ligne+4, colonne:colonne+4]).diagonal() == joueur):
                        return joueur  # Le joueur a gagné en diagonale descendante

        if self.moves == self.nb_lignes * self.nb_colonnes:
            return 0  # Match nul

        return None  # La partie n'est pas terminée

    def is_valid_move(self, colonne):
        return self.grid[0][colonne] == 0

    def get_current_player(self):
        return self.current_player

    def get_grid(self):
        return self.grid.copy()
    
    def render(self,fenetre):
        for colonne in range(self.nb_colonnes):
            for ligne in range(self.nb_lignes):
                pygame.draw.rect(fenetre, BLEU, (colonne * self.taillecase, (ligne + 1) * self.taillecase, self.taillecase, self.taillecase))
                pygame.draw.circle(fenetre, NOIR, (int(colonne*self.taillecase+self.taillecase/2), int(ligne*self.taillecase+self.taillecase+self.taillecase/2)), self.rayon_jetons)
                if self.grid[ligne][colonne] == 1:
                    pygame.draw.circle(fenetre, ROUGE, (colonne * self.taillecase + self.taillecase // 2, (ligne + 1) * self.taillecase + self.taillecase // 2), self.rayon_jetons)
                elif self.grid[ligne][colonne] == 2:
                    pygame.draw.circle(fenetre, JAUNE, (colonne * self.taillecase + self.taillecase // 2, (ligne + 1) * self.taillecase + self.taillecase // 2), self.rayon_jetons)
        pygame.display.update()

