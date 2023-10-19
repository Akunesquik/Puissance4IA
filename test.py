from Game.Game_Puissance4 import Puissance4
import pygame
import sys
import random

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

# Fonction pour jouer un coup aléatoire
def jouer_coup_aleatoire(game):
    coups_valides = [col for col in range(game.nb_colonnes) if game.grid[0][col] == 0]
    return random.choice(coups_valides)

def main():
    game = Puissance4()
    # Initialisation de Pygame
    pygame.init()

    fenetre = game.creation_fenetre()

    while True:

        # Afficher la Fenetre
        game.render(fenetre)


        #Gere la gestion des joueurs
        if(game.get_current_player() == 1):
            colonne = obtenir_colonne_cliquee(game)
        else:
            colonne = jouer_coup_aleatoire(game)




        # Si pion valide
        if game.is_valid_move(colonne):
            game.make_move(colonne)

            winner = game.is_winner()
            if winner:
                print(f"Le joueur {winner} a gagné !")
                break
            elif winner == 0:
                print("Match nul !")
                break
            else:
                game.switch_player()
        else:
            print("Coup invalide. Réessayez.")
        

if __name__ == "__main__":
    main()
