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
        agent1=charger_agent(typeAgent1)
    if typeAgent2.startswith('agent'):
        agent2=charger_agent(typeAgent2)

    mod = 50
    win,lose,draw = 0,0,0
    ia_recompense_totale = 0
      
    for i in range(nb_episodes):
        ## Setup des variables necessaire au focntionnement du training
        # fenetre = game.creation_fenetre()
        jeu_termine = False
        game.reset()
        compteur_loupe = 0
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
            
            if compteur_loupe == 3:
                     compteur_loupe = 0
                     colonne = (colonne +1) % 7

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
                        win += 1
                    else:
                        lose += 1

                    jeu_termine = True
                elif winner == 0:
                    # print("Match nul !")
                    jeu_termine = True
                    draw +=1
                
                #apprentissage de(s) IA(s)
                if(game.get_current_player() == 1):
                    if typeAgent1.startswith('agent'):
                        ia_recompense_totale += RememberAgent(game,agent1,colonne,ia_prev_state,jeu_termine,ia_recompense)
                else:
                    if typeAgent2.startswith('agent'):
                        ia_recompense_totale += RememberAgent(game,agent2,colonne,ia_prev_state,jeu_termine,ia_recompense)
                
                
                game.switch_player()

            else:
                 compteur_loupe += 1

        if i % (mod) == 0 and i != 0:
            EcrireResultat(typeAgent1,typeAgent2,win,lose,draw,ia_recompense_totale,i,mod,nb_episodes)  
            ### saveAgent en fonction de leur type, de si ce sont des agents quoi
            SaveAgentSiIA(agent1,typeAgent1)
            SaveAgentSiIA(agent2,typeAgent2)  
            win,lose,draw = 0,0,0
            ia_recompense_totale = 0
            
    EcrireResultat(typeAgent1,typeAgent2,win,lose,draw,ia_recompense_totale,nb_episodes,mod,nb_episodes)
    ### saveAgent en fonction de leur type, de si ce sont des agents quoi
    SaveAgentSiIA(agent1,typeAgent1)
    SaveAgentSiIA(agent2,typeAgent2) 
    
          



if __name__ == "__main__":
    main()
