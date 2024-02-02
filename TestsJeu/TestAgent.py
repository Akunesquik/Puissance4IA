from Game.Game_Puissance4 import   Puissance4
from FonctionsUtiles import *
import os

# Fonction pour lancer le jeu
def main():

    compteur_win_agent = 0
    compteur_lose_agent = 0
    match_nul = 0
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
        agent1.epsilon = 0
    if typeAgent2.startswith('agent'):
        agent2=charger_agent(game,typeAgent2)
        agent2.epsilon = 0

      
    for i in range(nb_episodes):
        ## Setup des variables necessaire au focntionnement du training
        fenetre = game.creation_fenetre()
        jeu_termine = False
        game.reset()

        #Commencement de l'entrainement
        while jeu_termine == False:

            # Afficher la Fenetre
            game.render(fenetre)

            # Gere les choix joueurs
            if(game.get_current_player() == 1):
                colonne = getColonneByPlayer(game,typeAgent1,agent1)
            else:
                colonne = getColonneByPlayer(game,typeAgent2,agent2)


            # Si pion valide
            if game.is_valid_move(colonne):
                game.make_move(colonne)

                #Check de si y'a un winner dans la partie
                winner = game.is_winner()
                ## Win agent
                if winner == 1 :
                    compteur_win_agent = compteur_win_agent+1
                    jeu_termine = True
                ## Lose Agent
                elif winner == 2:
                    compteur_lose_agent = compteur_lose_agent+1
                    jeu_termine = True
                ## Match nul
                elif winner == 0:
                    match_nul = match_nul+1
                    jeu_termine = True
                
                game.switch_player()

            #else:
                # print("Coup invalide. Réessayez.")      

    
    EcrireResultat(typeAgent1,typeAgent2,compteur_win_agent,compteur_lose_agent,match_nul)


if __name__ == "__main__":
    main()
