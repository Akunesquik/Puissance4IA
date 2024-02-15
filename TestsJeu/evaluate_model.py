import os
from FonctionsUtiles import charger_agent

# Chemin vers le répertoire contenant les agents sauvegardés
chemin_repertoire_agents = "TestsJeu/Save_Agent/models/"

# Obtenez la liste de tous les dossiers (noms d'agents) dans le répertoire
noms_agents = os.listdir(chemin_repertoire_agents)

# Parcours de chaque agent
for nom_agent in noms_agents:
        try:

                print(f"Évaluation de l'agent {nom_agent}...")

                # Chargez l'agent
                agent = charger_agent(nom_agent)

                # Évaluez l'agent
                agent.evaluate_model()

                # Vous pouvez enregistrer les résultats dans un fichier ou les afficher à l'écran
                # Par exemple, pour les afficher à l'écran :
                print("\n")  # Saut de ligne pour séparer les résultats des différents agents

        except OSError:
                print(f"Erreur de parsing avec l'agent {nom_agent}")