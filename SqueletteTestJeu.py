from Game.Game_Puissance4 import Puissance4


# Fonction pour lancer le jeu
def main():
    game = Puissance4()

    fenetre = game.creation_fenetre()

    while True:

        # Afficher la Fenetre
        game.render(fenetre)

        #Gere la gestion des joueurs
        if(game.get_current_player() == 1):
            colonne = game.obtenir_colonne_cliquee()
        else:
            colonne = game.jouer_coup_aleatoire()

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
