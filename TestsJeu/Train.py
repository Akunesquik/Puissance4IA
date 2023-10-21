from Game.Game_Puissance4 import   Puissance4
from IA.recompense import calculer_recompense
from IA.agent import DQNAgent
import sys

def RememberAgent(game,agent,colonne,ia_prev_state,jeu_termine,ia_recompense):
    ia_done = jeu_termine
    ia_action = colonne
    ia_next_state = game.grid
    ia_recompense += calculer_recompense(ia_prev_state,ia_action)
    agent.remember(ia_prev_state,ia_action,ia_recompense,ia_next_state,ia_done)

game = Puissance4()
agent = DQNAgent(game.nb_colonnes,game.nb_colonnes)         
# Fonction pour lancer le jeu
def main():
    

    fenetre = game.creation_fenetre()
    jeu_termine = False
    game.reset()
    while jeu_termine == False:

        # Afficher la Fenetre
        game.render(fenetre)

        # Gere les choix joueurs
        if(game.get_current_player() == 1):
            ia_prev_state = game.grid
            colonne = agent.act(ia_prev_state)
        else:
            colonne = game.jouer_coup_aleatoire()


        # Si pion valide
        if game.is_valid_move(colonne):
            game.make_move(colonne)
            # Setup la récompense
            ia_recompense = 0

            winner = game.is_winner()
            if winner:
                print(f"Le joueur {winner} a gagné !")
                if(winner == 1):
                    ia_recompense = 10000
                else:
                    ia_recompense = -1000
                jeu_termine = True
            elif winner == 0:
                print("Match nul !")
                jeu_termine = True
            else:
                game.switch_player()

            if(game.get_current_player() == 1):
                RememberAgent(game,agent,colonne,ia_prev_state,jeu_termine,ia_recompense)
        else:
            print("Coup invalide. Réessayez.")
        
nb_episodes = int(sys.argv[1])
if __name__ == "__main__":
    for i in range(nb_episodes):
        main()
