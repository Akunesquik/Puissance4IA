from Game.Game_Puissance4 import   Puissance4
from FonctionsUtiles import *
from CreationJeuDeDonneePourEvaluate import trouver_meilleure_colonne_array, jouer_coup
import time

# Fonction pour lancer le jeu
def main():

    typeBestMove = "all"
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

      
    for i in range(nb_episodes):
        ## Setup des variables necessaire au focntionnement du training
        fenetre = game.creation_fenetre()
        jeu_termine = False
        game.reset()
        
        #Commencement de l'entrainement
        while jeu_termine == False:

            # Afficher la Fenetre
            game.render(fenetre,game.grid)

            # Gere les choix joueurs
            if(game.get_current_player() == 1):
                colonne = getColonneByPlayer(game,typeAgent1,agent1)
            else:
                colonne = getColonneByPlayer(game,typeAgent2,agent2)


            # Si pion valide
            if game.is_valid_move(colonne):
                
                
                if typeAgent1.startswith('agent') and game.get_current_player() == 1:
                    afficherBestMoves(game,fenetre,colonne,typeBestMove)
                if typeAgent2.startswith('agent') and game.get_current_player() == 2:
                    afficherBestMoves(game,fenetre,colonne,typeBestMove)

                game.make_move(colonne)
                
                #Check de si y'a un winner dans la partie
                winner = game.is_winner()
                if winner:
                    print(f"Le joueur {winner} a gagné !")
                    jeu_termine = True
                elif winner == 0:
                    print("Match nul !")
                    jeu_termine = True
                
                game.switch_player()
                
            else:
                print("Coup invalide. Réessayez.")      



if __name__ == "__main__":
    main()
