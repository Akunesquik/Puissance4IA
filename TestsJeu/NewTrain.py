from Game.Game_Puissance4 import   Puissance4
from FonctionsUtiles import *
import time

# Fonction pour lancer le jeu
def main():

    nb_episodes = getNbEpisode()
    # Setup de la game
    game = Puissance4()
    ## Setup de l'agent en focntion de ce que demande l'utilisateur
    typeAgent1 = choisir_agent() 
    typeAgent2 = choisir_agent()  
    agent1=typeAgent1
    agent2=typeAgent2

    if typeAgent1.startswith('agent'):
        agent1=charger_agent(game,typeAgent1)
    if typeAgent2.startswith('agent'):
        agent2=charger_agent(game,typeAgent2)

    win,lose,draw = 0,0,0

      
    for i in range(nb_episodes):
        ## Setup des variables necessaire au focntionnement du training
        # fenetre = game.creation_fenetre()
        jeu_termine = False
        game.reset()

        #Commencement de l'entrainement
        while jeu_termine == False:

            # Afficher la Fenetre
            # game.render(fenetre)

            # Gere les choix joueurs
            ia_prev_state = game.grid
            if(game.get_current_player() == 1):
                colonne = getColonneByPlayer(game,typeAgent1,agent1)
            else:
                colonne = getColonneByPlayer(game,typeAgent2,agent2)


            # Si pion valide
            if game.is_valid_move(colonne):
                game.make_move(colonne)
                # Setup la récompense
                ia_recompense = 0

                #Check de si y'a un winner dans la partie
                winner = game.is_winner()
                if winner:
                    # print(f"Le joueur {winner} a gagné !")
                    if(winner == 1):
                        lose += 1
                    else:
                        win += 1

                    jeu_termine = True
                elif winner == 0:
                    # print("Match nul !")
                    jeu_termine = True
                    draw +=1
                
                #apprentissage de(s) IA(s)
                if(game.get_current_player() == 1):
                    if typeAgent1.startswith('agent'):
                        RememberAgent(game,agent1,colonne,ia_prev_state,jeu_termine,ia_recompense)
                else:
                    if typeAgent2.startswith('agent'):
                        RememberAgent(game,agent2,colonne,ia_prev_state,jeu_termine,ia_recompense)
                
                game.switch_player()

            # else:
            #     print("Coup invalide. Réessayez.")
    
    EcrireResultat(typeAgent1,typeAgent2,win,lose,draw)
    ### saveAgent en fonction de leur type, de si ce sont des agents quoi
    SaveAgentSiIA(agent1,typeAgent1)
    SaveAgentSiIA(agent2,typeAgent2)        



if __name__ == "__main__":
    main()
