import numpy as np
import pygame
import random
import sys
from FonctionsUtiles import is_winner

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
    
    # Reset la grille et les joueurs
    def reset(self):
        self.grid = np.zeros((self.nb_lignes, self.nb_colonnes), dtype=int)
        self.current_player = 1
        self.moves = 0

    # Met le pion dans dans la colonne
    def make_move(self, colonne):
        for ligne in range(self.nb_lignes - 1, -1, -1):
            if self.grid[ligne][colonne] == 0:
                self.grid[ligne][colonne] = self.current_player
                self.moves += 1
                return True
        return False  # La colonne est pleine, le coup n'est pas valide

    # Change entre player 1 et 2
    def switch_player(self):
        self.current_player = 3 - self.current_player  # Alterner entre les joueurs 1 et 2

    # Check si il y a un winner dans la game
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

    # Check si le move est valide
    def is_valid_move(self, colonne):
        return self.grid[0][colonne] == 0

    def get_current_player(self):
        return self.current_player

    def get_grid(self):
        return self.grid.copy()
    
    # Fonction pour afficher la fenetre de jeu
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


    # Fonction pour jouer un coup aléatoire
    def jouer_coup_aleatoire(self):
        coups_valides = [col for col in range(self.nb_colonnes) if self.grid[0][col] == 0]
        return random.choice(coups_valides)
    
    # Fonction pour jouer à la souris
    def obtenir_colonne_cliquee(game):
        colonne = None
        while colonne is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_souris = pygame.mouse.get_pos()
                    colonne = pos_souris[0] // game.taillecase  # Convertir la position X en colonne
                    if colonne < 0 or colonne >= game.nb_colonnes or game.grid[0][colonne] != 0:
                        colonne = None  # Le clic n'est pas valide
        return colonne

    def minimax(self, board, depth, maximizing_player, player):
        if depth == 0 or is_winner(board):
            return None, 0

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_possible_moves(board):
                new_board = self.get_next_state(board, move, player)
                _, eval = self.minimax(new_board, depth - 1, False, player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_possible_moves(board):
                new_board = self.get_next_state(board, move, 3 - player)  # Autre joueur
                _, eval = self.minimax(new_board, depth - 1, True, player)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move, min_eval

    def get_possible_moves(self,board):
        possible_moves = []
        for col in range(len(board[0])):
            # Vérifiez si la colonne est pleine
            if board[0][col] == 0:
                possible_moves.append(col)
        return possible_moves
    
    def get_next_state(self, board, move, player):
        new_board = [row[:] for row in board]  # Crée une copie du plateau
        for row in range(len(new_board)-1, -1, -1):
            if new_board[row][move] == 0:
                new_board[row][move] = player
                break
        return new_board
    

