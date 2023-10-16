import pickle

# Sauvegarde du réseau neuronal
def sauvegarder_reseau(agent, nom_fichier):
    with open(nom_fichier, 'wb') as fichier:
        pickle.dump(agent.model, fichier)

# Chargement du réseau neuronal
def charger_reseau(nom_fichier):
    with open(nom_fichier, 'rb') as fichier:
        model = pickle.load(fichier)
    return model