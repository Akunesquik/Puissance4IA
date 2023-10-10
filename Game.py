import pygame
import sys
import numpy as np
import random
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la grille
nb_colonnes = 7
nb_lignes = 6
taille_case = 100
rayon_jetons = taille_case // 2 - 5
largeur_fenetre = nb_colonnes * taille_case
hauteur_fenetre = (nb_lignes + 1) * taille_case

# Couleurs
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)
NOIR = (0, 0, 0)

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Puissance 4")

# Création de la grille
grille = np.zeros((nb_lignes, nb_colonnes), dtype=int)

# Fonction pour dessiner la grille
def dessiner_grille():
    for colonne in range(nb_colonnes):
        for ligne in range(nb_lignes):
            pygame.draw.rect(fenetre, BLEU, (colonne * taille_case, (ligne + 1) * taille_case, taille_case, taille_case))
            pygame.draw.circle(fenetre, NOIR, (int(colonne*taille_case+taille_case/2), int(ligne*taille_case+taille_case+taille_case/2)), rayon_jetons)
            if grille[ligne][colonne] == 1:
                pygame.draw.circle(fenetre, ROUGE, (colonne * taille_case + taille_case // 2, (ligne + 1) * taille_case + taille_case // 2), rayon_jetons)
            elif grille[ligne][colonne] == 2:
                pygame.draw.circle(fenetre, JAUNE, (colonne * taille_case + taille_case // 2, (ligne + 1) * taille_case + taille_case // 2), rayon_jetons)
    pygame.display.update()

# Fonction pour placer un jeton dans la colonne choisie
def placer_jeton(colonne, joueur):
    for ligne in range(nb_lignes - 1, -1, -1):
        if grille[ligne][colonne] == 0:
            grille[ligne][colonne] = joueur
            return True
    return False

# Fonction pour vérifier s'il y a une victoire
def victoire(joueur):
    # Vérification horizontale
    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes - 3):
            if np.all(grille[ligne, colonne:colonne+4] == joueur):
                return True

    # Vérification verticale
    for colonne in range(nb_colonnes):
        for ligne in range(nb_lignes - 3):
            if np.all(grille[ligne:ligne+4, colonne] == joueur):
                return True

    # Vérification diagonale ascendante
    for colonne in range(nb_colonnes - 3):
        for ligne in range(3, nb_lignes):
            if np.all(grille[ligne-3:ligne+1, colonne:colonne+4].diagonal() == joueur):
                return True

    # Vérification diagonale descendante
    for colonne in range(nb_colonnes - 3):
        for ligne in range(nb_lignes - 3):
            if np.all(np.fliplr(grille[ligne:ligne+4, colonne:colonne+4]).diagonal() == joueur):
                return True

    return False

# Fonction pour jouer un coup aléatoire
def jouer_coup_aleatoire():
    coups_valides = [col for col in range(nb_colonnes) if grille[0][col] == 0]
    return random.choice(coups_valides)

def obtenir_etat_actuel():
    etat = np.copy(grille)  # Crée une copie de la grille actuelle

    # Remplacez les valeurs 1 (jeton rouge) par 1 et les valeurs 2 (jeton jaune) par -1
    etat[etat == 1] = 1
    etat[etat == 2] = -1

    return etat

# Fonction principale du jeu
def jouer(nb_episodes):
    for _ in range(nb_episodes):  # Boucle pour le nombre d'épisodes spécifié
        tour = 0
        jeu_termine = False
        grille[:] = 0  # Réinitialisation de la grille

        dessiner_grille()
        while not jeu_termine:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if tour % 2 == 0:
                colonne = jouer_coup_aleatoire()
                placer_jeton(colonne, 1)
            else:
                colonne = jouer_coup_aleatoire()
                placer_jeton(colonne, 2)

            dessiner_grille()

            if victoire(1):
                print("Joueur Rouge gagne !")
                jeu_termine = True
                time.sleep(3)
            elif victoire(2):
                print("Joueur Jaune gagne !")
                jeu_termine = True
                time.sleep(3)
            elif np.all(grille != 0):
                print("Match nul !")
                jeu_termine = True
                time.sleep(3)

            tour += 1
            time.sleep(0.5)  # Délai pour voir le résultat

        # Demande à l'utilisateur s'il souhaite relancer une partie
        replay = input("Voulez-vous jouer une autre partie ? (Oui/Non) ").strip().lower()
        if replay != "oui":
            pygame.quit()
            sys.exit()

# Lancement du jeu avec 5 parties
if __name__ == "__main__":
    jouer(nb_episodes=5)  # Spécifiez le nombre d'épisodes à jouer ici
