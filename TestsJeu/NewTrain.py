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

def choisir_agent(game):
    while 1==1 :
        agent_type = input("Choisissez le type d'agent (humain/alea/agent1/agent2) : ").lower()
        if agent_type == 'humain':
            return 'humain'  # Retourne None pour un joueur humain
        elif agent_type == 'alea':
            return 'aleatoire'  # Remplacez 'aleatoire' par le nom de votre classe d'agent aléatoire
        elif agent_type.startswith('agent'):
            return agent_type  # Ajoutez des paramètres au besoin
        
def charger_agent(game,agent_name, agent=None):
    agent = DQNAgent(game.nb_colonnes, game.nb_colonnes)
    agent.name= agent_name
    # Construire le nom de fichier basé sur le nom de l'agent
    filename = f"{agent_name}Neurone.h5"

    # Charger le réseau neuronal à partir du fichier
    try:
        agent = DQNAgent.load_model(filename)
        print(f"Réseau neuronal chargé pour l'agent {agent_name}")
        
    except FileNotFoundError:
        print(f"Aucun fichier trouvé pour l'agent {agent_name}")
        if agent is None:
              # Assurez-vous de définir input_size et output_size
            print(f"Nouvel agent créé : {agent_name}")
    return agent  

def getColonneByPlayer(game,typeJoueur,agent):
    colonne = -1
    if typeJoueur == 'humain':
        colonne = game.obtenir_colonne_cliquee()
    elif typeJoueur == 'aleatoire':
        colonne = game.jouer_coup_aleatoire()
    elif typeJoueur.startswith('agent'):
        ia_prev_state = game.grid
        colonne = agent.act(ia_prev_state)

    if colonne == -1:
        return "Erreur de choix de colonne .. Fct getColonneByPlayer"
    
    return colonne  
# Fonction pour lancer le jeu
def main():

    # Setup de la game
    game = Puissance4()
    ## Setup de l'agent en focntion de ce que demande l'utilisateur
    typeAgent1 = choisir_agent(game=game) 
    typeAgent2 = choisir_agent(game=game)  
    agent1=typeAgent1
    agent2=typeAgent2

    if typeAgent1.startswith('agent'):
        agent1=charger_agent(game,typeAgent1,agent1)
    if typeAgent2.startswith('agent'):
        agent2=charger_agent(game,typeAgent1,agent2)

    nb_episodes = int(sys.argv[1])    
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
                    print(f"Le joueur {winner} a gagné !")
                    if(winner == 1):
                        ia_recompense = 10000
                    else:
                        ia_recompense = -1000
                    jeu_termine = True
                elif winner == 0:
                    print("Match nul !")
                    jeu_termine = True
                
                #apprentissage de(s) IA(s)
                if(game.get_current_player() == 1):
                    if typeAgent1.startswith('agent'):
                        RememberAgent(game,agent1,colonne,ia_prev_state,jeu_termine,ia_recompense)
                else:
                    if typeAgent2.startswith('agent'):
                        RememberAgent(game,agent2,colonne,ia_prev_state,jeu_termine,ia_recompense)
                
                game.switch_player()

            else:
                print("Coup invalide. Réessayez.")
        



if __name__ == "__main__":
    main()
