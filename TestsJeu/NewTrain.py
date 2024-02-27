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
        agent2.epsilon = 0.1

    mod = 50
    modEvaluation = 5*mod
    win,lose,draw = 0,0,0
    ia_recompense_totale = 0
      
    for i in range(1,nb_episodes+1):
        ## Setup des variables necessaire au focntionnement du training
        #fenetre = game.creation_fenetre()
        jeu_termine = False
        game.reset()
        compteur_loupe = 0
        #Commencement de l'entrainement
        while jeu_termine == False:

            # Afficher la Fenetre
            #game.render(fenetre,game.get_grid())
            
            # Gere les choix joueurs
            ia_prev_state = game.grid
            if(game.get_current_player() == 1):
                colonne = getColonneByPlayer(game,typeAgent1,agent1)
            else:
                colonne = getColonneByPlayer(game,typeAgent2,agent2)
            
            if compteur_loupe == 3:
                while(not(game.is_valid_move(colonne))):
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
                
                #game.render(fenetre,game.get_grid())
                game.switch_player()

            else:
                compteur_loupe += 1
                ia_recompense = -5000
                 #apprentissage de(s) IA(s)
                if(game.get_current_player() == 1):
                    if typeAgent1.startswith('agent'):
                       RememberAgent(game,agent1,colonne,ia_prev_state,jeu_termine,ia_recompense)
                       agent1.replay2()         
                else:
                    if typeAgent2.startswith('agent'):
                        RememberAgent(game,agent2,colonne,ia_prev_state,jeu_termine,ia_recompense)

        if typeAgent1.startswith('agent'):
            agent1.replay2()
        if typeAgent2.startswith('agent'):
            agent2.replay2()
        if i % (mod) == 0 and i != 0 :
            epsilon1 = 0
            epsilon2 = 0
            if typeAgent1.startswith('agent'):
                agent1.save_model_agent()
                epsilon1 = agent1.epsilon
                if i % (modEvaluation) == 0:
                    agent1.evaluate_model()
            if typeAgent1.startswith('agent'):
                agent2.save_model_agent()
                epsilon2 = agent2.epsilon
                if i % (modEvaluation) == 0:
                    agent2.evaluate_model()

            EcrireResultat(epsilon1,epsilon2,typeAgent1,typeAgent2,win,lose,draw,ia_recompense_totale,i,mod,nb_episodes)  
            win,lose,draw = 0,0,0
            ia_recompense_totale = 0
        
        

                 
if __name__ == "__main__":
    main()
