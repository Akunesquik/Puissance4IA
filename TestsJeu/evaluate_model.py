import os
from FonctionsUtiles import charger_agent

plop = 100
# Chemin vers le répertoire contenant les agents sauvegardés
chemin_repertoire_agents = "TestsJeu/Save_Agent/models/"

# Obtenez la liste de tous les dossiers (noms d'agents) dans le répertoire
noms_agents = [fichier for fichier in os.listdir(chemin_repertoire_agents) if os.path.isfile(os.path.join(chemin_repertoire_agents, fichier))]

# Parcours de chaque agent
for nom_agent in noms_agents:
        try:
                
                print(f"Évaluation de l'agent {nom_agent}...")
                nom_agent, _ = os.path.splitext(nom_agent)
                # Chargez l'agent
                agent = charger_agent(nom_agent)
                bonneRepTotale = 1.0
                # Évaluez l'agent
                for i in range(plop):
                        bonneRepTotale += agent.evaluate_model(verbose=0)

                print(f"Moy de l'agent {agent.name} : " + str(bonneRepTotale/plop))
                # Vous pouvez enregistrer les résultats dans un fichier ou les afficher à l'écran
                # Par exemple, pour les afficher à l'écran :
                print("\n")  # Saut de ligne pour séparer les résultats des différents agents

        except OSError:
                print(f"Erreur de parsing avec l'agent {nom_agent}")