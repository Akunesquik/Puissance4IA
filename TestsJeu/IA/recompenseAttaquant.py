def longueur_chaine_horizontale(grille, ligne, colonne):
    pion_joueur = grille[ligne][colonne]
    longueur = 1  # Initialise la longueur à 1 (comprend le pion actuel)

    # Recherche de l'alignement à gauche
    for i in range(colonne - 1, -1, -1):
        if i >= 0 and grille[ligne][i] == pion_joueur:  # Vérification de la limite de la grille
            longueur += 1
        else:
            break

    # Recherche de l'alignement à droite
    for i in range(colonne + 1, len(grille[0])):
        if i < len(grille[0]) and grille[ligne][i] == pion_joueur:  # Vérification de la limite de la grille
            longueur += 1
        else:
            break

    return recompense_longueur(longueur)

def longueur_chaine_verticale(grille, ligne, colonne):
    pion_joueur = grille[ligne][colonne]
    longueur = 1  # Initialise la longueur à 1 (comprend le pion actuel)

    # Recherche de l'alignement vers le bas
    for i in range(ligne + 1, len(grille)):
        if grille[i][colonne] == pion_joueur:
            longueur += 1
        else:
            break

    # Recherche de l'alignement vers le haut
    for i in range(ligne - 1, -1, -1):
        if grille[i][colonne] == pion_joueur:
            longueur += 1
        else:
            break

    return recompense_longueur(longueur)

def longueur_chaine_diagonale_droite(grille, ligne, colonne):
    pion_joueur = grille[ligne][colonne]
    longueur = 1  # Initialise la longueur à 1 (comprend le pion actuel)

    # Recherche de l'alignement en diagonale droite (en bas à droite)
    i, j = ligne + 1, colonne + 1
    while i < len(grille) and j < len(grille[0]) and grille[i][j] == pion_joueur:
        longueur += 1
        i += 1
        j += 1

    # Recherche de l'alignement en diagonale droite (en haut à gauche)
    i, j = ligne - 1, colonne - 1
    while i >= 0 and j >= 0 and grille[i][j] == pion_joueur:
        longueur += 1
        i -= 1
        j -= 1

    return recompense_longueur(longueur)

def longueur_chaine_diagonale_gauche(grille, ligne, colonne):
    pion_joueur = grille[ligne][colonne]
    longueur = 1  # Initialise la longueur à 1 (comprend le pion actuel)

    # Recherche de l'alignement en diagonale gauche (en bas à gauche)
    i, j = ligne + 1, colonne - 1
    while i < len(grille) and j >= 0 and grille[i][j] == pion_joueur:
        longueur += 1
        i += 1
        j -= 1

    # Recherche de l'alignement en diagonale gauche (en haut à droite)
    i, j = ligne - 1, colonne + 1
    while i >= 0 and j < len(grille[0]) and grille[i][j] == pion_joueur:
        longueur += 1
        i -= 1
        j += 1

    return recompense_longueur(longueur)

def recompense_longueur(longueur):
    recompense = 0
    if longueur == 1:
        recompense = 0
    elif longueur == 2:
        recompense = 3
    elif longueur == 3:
        recompense = 7
    else:
        recompense = 500
    return recompense

def trouver_dernier_pion(grille, colonne):
    for ligne in range(len(grille)):
        if grille[ligne][colonne] != 0:
            return ligne
    return None  # Aucun pion dans la colonne

def calculer_recompense_attaquant(grille, colonne):

    recompense=0
    ligne = trouver_dernier_pion(grille, colonne)
    recompense += longueur_chaine_diagonale_droite(grille,ligne,colonne)
    recompense += longueur_chaine_diagonale_gauche(grille,ligne,colonne)
    recompense += longueur_chaine_horizontale(grille,ligne,colonne)
    recompense += longueur_chaine_verticale(grille,ligne,colonne)

    return recompense