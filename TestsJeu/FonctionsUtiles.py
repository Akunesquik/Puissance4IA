from IA.recompenseAttaquant import calculer_recompense_attaquant
from IA.agent import DQNAgent
from keras.models import save_model, load_model
import sys, os
import time
import json
import tensorflow as tf
import numpy as np

def RememberAgent(game,agent,colonne,ia_prev_state,jeu_termine,ia_recompense):
    ia_done = jeu_termine
    ia_action = colonne
    ia_next_state = game.grid
    ia_recompense = calculer_recompense_attaquant(ia_prev_state,ia_action)
    agent.learn(ia_prev_state,ia_action,ia_recompense,ia_next_state,ia_done)

    return ia_recompense

def choisir_agent():
    while 1==1 :
        agent_type = input("Choisissez le type d'agent (humain/alea/agent1/agent2) : ").lower()
        if agent_type == 'humain':
            return 'humain'  # Retourne None pour un joueur humain
        elif agent_type == 'alea':
            return 'aleatoire'  # Remplacez 'aleatoire' par le nom de votre classe d'agent aléatoire
        elif agent_type.startswith('agent'):
            return agent_type  # Ajoutez des paramètres au besoin
        
def charger_agent(agent_name):
    
    path='TestsJeu/Save_Agent/' 
    pathModel = path + f'models/{agent_name}/{agent_name}.keras'
    pathHyperpara = path + f'hyperparametres/{agent_name}.json'
    # Construire le nom de fichier basé sur le nom de l'agent
    # Charger le réseau neuronal à partir du fichier
    try:
        agent = load_agent(pathModel,pathHyperpara)
        print(f"Model chargé pour l'agent {agent_name}")
        
    except (FileNotFoundError, OSError):
       print(f"Aucun fichier trouvé pour l'agent {agent_name}")
       agent = DQNAgent()
       print(f"Nouvel agent créé : {agent_name}")
    agent.name= agent_name
    return agent  

def SaveAgentSiIA(agent,type):
    if type.startswith('agent'):
        
        path='TestsJeu/Save_Agent/' 
        pathModel = path + f'models/{agent.name}/{agent.name}.keras'
        pathHyperpara = path + f'hyperparametres/{agent.name}.json'
        save_agent(agent,pathModel,pathHyperpara)

        print(f"Model sauvegardé pour l'agent {type}")


def getColonneByPlayer(game,typeJoueur,agent):
    colonne = -1
    if typeJoueur == 'humain':
        colonne = game.obtenir_colonne_cliquee()
    elif typeJoueur == 'aleatoire':
        colonne = game.jouer_coup_aleatoire()
    elif typeJoueur.startswith('agent'):
        ia_prev_state = game.get_grid()
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


def EcrireResultat(typeAgent, typeAgent2, win, lose, draw,recompenseTotale):
    # Définir le chemin d'accès au fichier
    fichier_resultats = f"TestsJeu/Resultats/{typeAgent}_VS_{typeAgent2}.txt"

    # Vérifier si le fichier existe
    if not os.path.exists(fichier_resultats):
        # Créer le fichier s'il n'existe pas
        with open(fichier_resultats, "w"):
            pass

    # Ouvrir le fichier en mode append ("a") et ajouter la ligne
    with open(fichier_resultats, "a") as fichier:
        ligne = typeAgent +" vs " + typeAgent2 + " V : " + str(win) + " // D : " + str(lose) + " // Nul : " + str(draw) + " // Win Rate : " + (str(win/(win+lose+draw)) +" // Recompense moyenne : " + str(recompenseTotale/float(win+lose+draw)) )
        # Écrire la ligne dans le fichier
        fichier.write(ligne + "\n")

def save_agent(agent, model_path, hyperparameters_path):
    """
    Sauvegarde le modèle et les hyperparamètres d'un agent DQN.

    Args:
        agent: L'agent DQN à sauvegarder.
        model_path: Le chemin d'accès au fichier où le modèle sera sauvegardé.
        hyperparameters_path: Le chemin d'accès au fichier où les hyperparamètres seront sauvegardés.
    """

    # Sauvegarde du modèle
    agent.model.save(model_path)

    # Sauvegarde des hyperparamètres
    with open(hyperparameters_path, "w") as f:
        json.dump({"learning_rate": agent.learning_rate, "gamma": agent.gamma, "epsilon": agent.epsilon}, f)

def load_agent(model_path, hyperparameters_path):
    """
    Charge un agent DQN à partir d'un fichier de sauvegarde.

    Args:
        model_path: Le chemin d'accès au fichier où le modèle est sauvegardé.
        hyperparameters_path: Le chemin d'accès au fichier où les hyperparamètres sont sauvegardés.

    Returns:
        Un agent DQN avec les paramètres chargés.
    """

    # Chargement des hyperparamètres
    with open(hyperparameters_path, "r") as f:
        hyperparameters = json.load(f)

    # Création d'un nouvel agent avec les hyperparamètres chargés
    agent = DQNAgent(**hyperparameters)

    # Chargement du modèle
    agent.model = tf.keras.models.load_model(model_path)


    return agent
