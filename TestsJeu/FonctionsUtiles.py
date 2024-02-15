from IA.recompenseAttaquant import calculer_recompense_attaquant
from IA.agent import DQNAgent

import sys, os
import tensorflow as tf
import numpy as np


def RememberAgent(game,agent,colonne,ia_prev_state,jeu_termine,ia_recompense):
    ia_done = jeu_termine
    ia_action = colonne
    ia_next_state = game.get_grid()
    ia_recompense = calculer_recompense_attaquant(ia_next_state,ia_action)
    agent.remember(ia_prev_state,ia_action,ia_recompense,ia_next_state,ia_done)

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
        elif agent_type == 'minmax':
            return agent_type
        
def charger_agent(agent_name):
    
    path='TestsJeu/Save_Agent/' 
    pathModel = path + f'models/{agent_name}'
    # Construire le nom de fichier basé sur le nom de l'agent
    # Charger le réseau neuronal à partir du fichier
    agent = DQNAgent()
    agent.name= agent_name
    if os.path.isfile(pathModel +"/saved_model.pb"):
        agent.load_model_agent()
    
    else:
        print(f"Aucun fichier trouvé pour l'agent {agent.name}")
        agent.build_model()
        print(f"Nouvel agent créé : {agent.name}")

    return agent  


def getColonneByPlayer(game,typeJoueur,agent):
    colonne = -1
    if typeJoueur == 'humain':
        colonne = game.obtenir_colonne_cliquee()
    elif typeJoueur == 'aleatoire':
        colonne = game.jouer_coup_aleatoire()
    elif typeJoueur.startswith('agent'):
        ia_prev_state = game.get_grid()
        colonne = agent.act(ia_prev_state)
    elif typeJoueur == 'minmax':
        depth = 4
        prev_state = game.get_grid()
        colonne , _ = game.minimax(prev_state,depth,True,2)

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


def EcrireResultat(agent, typeAgent, typeAgent2, win, lose, draw,recompenseTotale,i,mod,nb_episodesTotal):
    # Définir le chemin d'accès au fichier
    fichier_resultats = f"TestsJeu/Resultats/{typeAgent}_VS_{typeAgent2}.txt"

    # Vérifier si le fichier existe
    if not os.path.exists(fichier_resultats):
        # Créer le fichier s'il n'existe pas
        with open(fichier_resultats, "w"):
            pass

    # Ouvrir le fichier en mode append ("a") et ajouter la ligne
    with open(fichier_resultats, "a") as fichier:
        ligne = typeAgent +" vs " + typeAgent2 +" Iterations de "+ str(i-mod+1) + " a " + str(i)+ " sur "+ str(nb_episodesTotal) + " // V : " + str(win) + " // D : " + str(lose) + " // Nul : " + str(draw) + " // Win Rate : " + str(win/mod) +" // Recompense moyenne : " + str(recompenseTotale/mod) + " // Epsilon " + str(agent.epsilon) 
        # Écrire la ligne dans le fichier
        fichier.write(ligne + "\n")

def is_winner(board):
    # Vérification des lignes
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] != 0 and \
               board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                return board[row][col]

    # Vérification des colonnes
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] != 0 and \
               board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                return board[row][col]

    # Vérification des diagonales (vers le bas à droite)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] != 0 and \
               board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return board[row][col]

    # Vérification des diagonales (vers le haut à droite)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] != 0 and \
               board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                return board[row][col]

    return 0  # Aucun gagnant





