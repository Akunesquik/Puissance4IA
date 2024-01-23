from IA.recompenseAttaquant import calculer_recompense_attaquant
from IA.agent import DQNAgent
from keras.models import save_model, load_model
import sys, os

def RememberAgent(game,agent,colonne,ia_prev_state,jeu_termine,ia_recompense):
    ia_done = jeu_termine
    ia_action = colonne
    ia_next_state = game.grid
    ia_recompense += calculer_recompense_attaquant(ia_prev_state,ia_action)
    agent.remember(ia_prev_state,ia_action,ia_recompense,ia_next_state,ia_done)

def choisir_agent():
    while 1==1 :
        agent_type = input("Choisissez le type d'agent (humain/alea/agent1/agent2) : ").lower()
        if agent_type == 'humain':
            return 'humain'  # Retourne None pour un joueur humain
        elif agent_type == 'alea':
            return 'aleatoire'  # Remplacez 'aleatoire' par le nom de votre classe d'agent aléatoire
        elif agent_type.startswith('agent'):
            return agent_type  # Ajoutez des paramètres au besoin
        
def charger_agent(game,agent_name):
    agent = DQNAgent(game.nb_colonnes, game.nb_colonnes)
    agent.name= agent_name
    # Construire le nom de fichier basé sur le nom de l'agent
    path = 'TestsJeu/Save_Agent/'
    filename = f"{agent_name}.keras"

    fichier = path+filename
    # Charger le réseau neuronal à partir du fichier
    try:
        ##agent.load_weights(fichier)
        loaded_model = load_model(fichier)
        agent.model = loaded_model
        print(f"Réseau neuronal chargé pour l'agent {fichier}")
        
    except (FileNotFoundError, OSError):
        print(f"Aucun fichier trouvé pour l'agent {fichier}")
        if agent is None:
              # Assurez-vous de définir input_size et output_size
            print(f"Nouvel agent créé : {fichier}")
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

def getNbEpisode():

    try:
        nombre = int(input("Nombre de parties: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        sys.exit(1)

    return nombre

def SaveAgentSiIA(agent,type):
    if type.startswith('agent'):
        # Suppose que votre DQNAgent s'appelle agent
        path = 'TestsJeu/Save_Agent/'
        filename = f"{agent.name}.keras"
        fichier = path+filename
        #agent.save_weights(path+filename, overwrite=True)
        agent.model.save(fichier)
        print(f"Réseau neuronal sauvegardé pour l'agent {fichier}")



def EcrireResultat(typeAgent, typeAgent2, win, lose, draw):
    # Définir le chemin d'accès au fichier
    fichier_resultats = f"TestsJeu/Resultats/{typeAgent}_VS_{typeAgent2}.txt"

    # Vérifier si le fichier existe
    if not os.path.exists(fichier_resultats):
        # Créer le fichier s'il n'existe pas
        with open(fichier_resultats, "w"):
            pass

    # Ouvrir le fichier en mode append ("a") et ajouter la ligne
    with open(fichier_resultats, "a") as fichier:
        ligne = typeAgent +" vs " + typeAgent2 + " V : " + str(win) + " // D : " + str(lose) + " // Nul : " + str(draw) + " // Win Rate : " + (str(win/(win+lose+draw)))
        # Écrire la ligne dans le fichier
        fichier.write(ligne + "\n")