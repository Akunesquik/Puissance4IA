import json

from CreationJeuDeDonneePourEvaluate import creer_situation_partie, trouver_meilleure_colonne
from datetime import datetime

# Génération des données d'évaluation
situations = creer_situation_partie(100)

# Liste pour stocker les grilles avec les meilleures réponses
data = []

# Collecte des données d'évaluation
for grille, reponse in situations:
    meilleure_colonne = trouver_meilleure_colonne(grille)
    data.append((grille.tolist(), meilleure_colonne))

# Enregistrement des données dans un fichier JSON
with open('evaluation_data.json', 'w') as f:
    json.dump(data, f)