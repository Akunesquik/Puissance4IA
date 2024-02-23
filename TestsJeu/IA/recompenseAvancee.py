from IA.recompenseAttaquant import trouver_dernier_pion
def create_future_alignment_opportunities_reward(grille, ligne, colonne):
    pion_joueur = grille[ligne][colonne]
    reward = 0
    
    # Vérifier les alignements potentiels futurs dans les quatre directions
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        future_alignment_count = 0
        # Parcourir dans les deux directions à partir de la position actuelle
        for direction in [-1, 1]:
            x, y = ligne, colonne
            for _ in range(1, 4):  # Rechercher trois cases dans chaque direction
                x += dx * direction
                y += dy * direction
                # Vérifier si la case est à l'intérieur de la grille et si elle appartient au joueur actuel
                if 0 <= x < len(grille) and 0 <= y < len(grille[0]) and grille[x][y] == pion_joueur:
                    future_alignment_count += 1
                else:
                    break
        # Ajouter la récompense en fonction du nombre d'alignements futurs possibles dans cette direction
        if future_alignment_count >= 2:  # Au moins 2 pions du joueur dans une direction donnée
            reward += 1
    
    return reward

def maintain_center_dominance_reward(grille, ligne, colonne):
    reward = 0
    center_col = len(grille[0]) // 2  # Colonne centrale
    if colonne == center_col:
        reward += 1
    return reward

def prevent_potential_enemy_combinations_reward(grille, ligne, colonne):
    pion_joueur = grille[ligne][colonne]
    reward = 0
    
    # Vérifier les alignements potentiels adverses dans les quatre directions
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        future_alignment_count = 0
        # Parcourir dans les deux directions à partir de la position actuelle
        for direction in [-1, 1]:  
            x, y = ligne, colonne
            for _ in range(1, 4):  # Rechercher trois cases dans chaque direction
                x += dx * direction
                y += dy * direction
                # Vérifier si la case est à l'intérieur de la grille et si elle appartient à l'adversaire
                if 0 <= x < len(grille) and 0 <= y < len(grille[0]) and grille[x][y] != pion_joueur and grille[x][y] != 0:
                    future_alignment_count += 1
                else:
                    break
        # Si l'adversaire a au moins deux pions alignés dans une direction, ajoutez une récompense pour bloquer cela
        if future_alignment_count >= 2:
            reward += 1
    
    return reward

def ajout_recompense_avancee(grille,colonne):
    reward_totale = 0
    ligne = trouver_dernier_pion(grille,colonne)
    reward_totale += prevent_potential_enemy_combinations_reward(grille,ligne,colonne)
    reward_totale += maintain_center_dominance_reward(grille,ligne,colonne)
    reward_totale += create_future_alignment_opportunities_reward(grille,ligne,colonne)

    return reward_totale