from IA.recompenseAttaquant import calculer_recompense_attaquant, trouver_dernier_pion
from IA.recompenseDefenseur import calculer_recompense_defenseur
from IA.recompenseAvancee import ajout_recompense_avancee
import numpy as np
import random

def trouver_meilleure_colonne(grille):
    meilleures_colonnes = []  # Liste pour stocker les colonnes avec les récompenses maximales
    meilleure_recompense = float('-inf')  # Initialisation de la meilleure récompense avec une valeur minimale

    # Parcours de chaque colonne de la grille
    for colonne in range(len(grille[0])):
        # Vérification si la colonne est jouable (il y a de la place pour un nouveau pion)
        if grille[0][colonne] == 0:
            grille = jouer_coup(grille,1,colonne)
            # Calcul de la récompense pour cette colonne
            recompense = calculer_recompense_attaquant(grille, colonne)
            # Vérification si la récompense est meilleure que la meilleure récompense actuelle
            if recompense > meilleure_recompense:
                meilleures_colonnes = [colonne]  # Remplacer les meilleures colonnes précédentes
                meilleure_recompense = recompense
            elif recompense == meilleure_recompense:
                meilleures_colonnes.append(colonne)  # Ajouter cette colonne aux meilleures colonnes
            ligne = trouver_dernier_pion(grille,colonne)
            grille[ligne][colonne] = 0
    # Sélection aléatoire parmi les meilleures colonnes
    colonne_choisie = random.choice(meilleures_colonnes)
    return colonne_choisie

def jouer_coup(grille, joueur, colonne):
    for ligne in range(len(grille)-1, -1, -1):
        if grille[ligne][colonne] == 0:
            grille[ligne][colonne] = joueur
            return grille

def creer_situation_partie(num_episodes):
    situations = []
    for _ in range(num_episodes):  # Générer 100 états de jeu aléatoires avec les réponses calculées
        grille_temp = creer_Fausses_Grilles()
        reponse = trouver_meilleure_colonne_array(grille_temp)
        if reponse :  # Vérifie si une réponse valide a été trouvée
            situations.append((grille_temp, reponse))
    return situations


def creer_Fausses_Grilles():
    grille = np.zeros((6, 7), dtype=int)
    joueur = 1  # Le joueur qui commence

    for _ in range(random.randint(3, 20)):  # Générer un nombre aléatoire de coups entre 5 et 30
        colonne = random.randint(0, 6)
        while grille[0][colonne] != 0:  # Assurez-vous qu'il y a de la place dans la colonne choisie
            colonne = random.randint(0, 6)
        grille = jouer_coup(grille, joueur, colonne)
        joueur = 3 - joueur  # Changer de joueur

    return grille

def TrouveMeilleureActionAvecReward(next_state):
    meilleure_action = trouver_meilleure_colonne(next_state)
    next_state = jouer_coup(next_state,1,meilleure_action)
    reward = calculer_recompense_attaquant(next_state, meilleure_action)
    ligne = trouver_dernier_pion(next_state,meilleure_action)
    next_state[ligne][meilleure_action] = 0

    return meilleure_action,reward
# Exemple d'utilisation :
# situations = creer_situation_partie(100)
# for i, (grille, reponse) in enumerate(situations):
#     print(f"Situation {i+1}:")
#     print("Grille:")
#     print(grille)
#     print("Réponse (meilleure colonne à jouer) :", reponse)
#     print()


def trouver_meilleure_colonne_array(grille,joueur,typeBestMove):
    meilleures_colonnes = []  # Liste pour stocker les colonnes avec les récompenses maximales
    meilleure_recompense = -100  # Initialisation de la meilleure récompense avec une valeur minimale

    # Parcours de chaque colonne de la grille
    for colonne in range(len(grille[0])):
        recompense = 0
        # Vérification si la colonne est jouable (il y a de la place pour un nouveau pion)
        if grille[0][colonne] == 0:
            grille = jouer_coup(grille,joueur,colonne)
            # Calcul de la récompense pour cette colonne
            if(typeBestMove == "atk"):
                recompense = calculer_recompense_attaquant(grille, colonne)               
            elif(typeBestMove == "def"):
                recompense = calculer_recompense_defenseur(grille, colonne)
            elif(typeBestMove == "avc"):
                recompense = ajout_recompense_avancee(grille, colonne)
            elif(typeBestMove == "atkavc"):
                recompense += calculer_recompense_attaquant(grille, colonne)
                recompense += ajout_recompense_avancee(grille, colonne)
            elif(typeBestMove == "defavc"):
                recompense += calculer_recompense_defenseur(grille, colonne)
                recompense += ajout_recompense_avancee(grille, colonne)
            elif(typeBestMove == "all"):
                recompense += calculer_recompense_attaquant(grille, colonne)
                recompense += calculer_recompense_defenseur(grille, colonne)
                recompense += ajout_recompense_avancee(grille, colonne)

            #print(f"colonne {colonne} : {recompense}")
            # Vérification si la récompense est meilleure que la meilleure récompense actuelle
            if recompense > meilleure_recompense:
                meilleures_colonnes = [colonne]  # Remplacer les meilleures colonnes précédentes
                meilleure_recompense = recompense
            elif recompense == meilleure_recompense:
                meilleures_colonnes.append(colonne)  # Ajouter cette colonne aux meilleures colonnes
            ligne = trouver_dernier_pion(grille,colonne)
            grille[ligne][colonne] = 0
            
    return meilleures_colonnes


# import json
# # Utilisez la fonction creer_situation_partie pour générer les données
# situations = creer_situation_partie(100)
# 
# # Convertissez les tableaux NumPy en listes Python
# situations_converted = [(grille.tolist(), reponse) for grille, reponse in situations]
# 
# # Enregistrez les données dans un fichier JSON
# with open('meilleures_colonnes.json', 'w') as f:
#     json.dump(situations_converted, f)